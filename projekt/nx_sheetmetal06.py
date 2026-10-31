# -*- coding: utf-8 -*-
"""Native NX Sheet-Metal gate, patch 07.2; no silent solid fallback.

The reported NX2406 Python binding has no UF.Modl.AskFaceData. Resolve the
same named query on the available UF objects before invoking it. Do not
reinterpret a native read error as a missing namespace or try other queries.
07.2 corrects Preferences.Sheetmetal to the documented Preferences.PartSheetmetal.
Only that exact property is used, with read-only capability diagnostics before
changing preferences. This adapter has offline contract tests, NOT a local
Siemens NX runtime test. See Dokumentation/API_BLECH_FIX_07_2.md.
"""
import math

ADAPTER_VERSION = '07.2'
PREFERENCES_PATH = 'Preferences.PartSheetmetal'
PREFERENCE_METHODS = ('SetThickness', 'SetBendRadius', 'SetNeutralFactor', 'Commit')
FACE_QUERY_GROUPS = ('Modeling', 'Modl', 'ModlGeneral')


def validate_options(q):
    if not isinstance(q, dict) or q.get('mode') not in ('required', 'solid'):
        raise ValueError('Blech_Optionen: mode muss required oder solid sein; kein automatischer Rueckfall')
    if set(q) - {'mode', '_Hinweis'}:
        raise ValueError('Unbekannte Blechoption')
    return q['mode']


def resolve_face_query(uf, log=lambda x: None):
    """Discover available bindings; never call a method while selecting it.

    Modeling is preferred for Python. Modl/ModlGeneral are only accepted if
    their actual object exposes the exact callable AskFaceData. These are
    availability probes, not a claim that every NX version implements them.
    The method is resolved afresh for each conversion, not cached across parts.
    """
    found = []
    for group_name in FACE_QUERY_GROUPS:
        label = 'UF.%s.AskFaceData' % group_name
        try:
            group = getattr(uf, group_name, None)
            query = getattr(group, 'AskFaceData', None)
        except Exception as exc:
            log('Blech-Flaechen-API: %s nicht lesbar: %s: %s' %
                (label, type(exc).__name__, exc))
            continue
        log('Blech-Flaechen-API: %s callable=%s' % (label, callable(query)))
        if callable(query):
            found.append((query, label))
    if not found:
        raise RuntimeError('AskFaceData fehlt als aufrufbare Methode in UF.Modeling, '
                           'UF.Modl und UF.ModlGeneral. Keine Basisflaeche geraten; '
                           'Blech-Pflichtmodus bleibt aktiv.')
    query, label = found[0]
    log('Blech-Flaechenabfrage ausgewaehlt: ' + label)
    log('Blech-Flaechen-API-Dokumentation %s:\n%s' %
        (label, (getattr(query, '__doc__', None) or 'Keine eingebettete Dokumentation')[:6000]))
    return query, label


def _finite_vec3(value, label):
    try:
        if len(value) != 3 or any(isinstance(x, bool) for x in value):
            raise ValueError('genau drei Zahlen erwartet')
        result = tuple(float(x) for x in value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise RuntimeError('AskFaceData: ungueltiger %s: %r' % (label, value)) from exc
    if not all(math.isfinite(x) for x in result):
        raise RuntimeError('AskFaceData: nicht endlicher %s: %r' % (label, value))
    return result


def select_base_face(body, modl, axis, plane, tol=1e-5):
    """Select the single nominated prototype plane, never the first face.

    `modl` accepts the resolved callable or a legacy provider with AskFaceData.
    Normal sign is irrelevant. No global occurrence coordinate is substituted.
    """
    if type(axis) is not int or axis not in (0, 1, 2):
        raise ValueError('Blechbasisachse muss 0, 1 oder 2 sein')
    if (isinstance(plane, bool) or not isinstance(plane, (int, float)) or
            not math.isfinite(plane)):
        raise ValueError('Blechbasiskoordinate muss eine endliche Zahl sein')
    if (isinstance(tol, bool) or not isinstance(tol, (int, float)) or
            not math.isfinite(tol) or tol <= 0):
        raise ValueError('Blechbasis-Toleranz muss positiv und endlich sein')
    query = modl if callable(modl) else getattr(modl, 'AskFaceData', None)
    if not callable(query):
        raise RuntimeError('AskFaceData fehlt am gewaehlten Flaechenprovider')
    matches = []
    for face in body.GetFaces():
        # Query errors are fatal. Never retry another namespace on failure.
        result = query(face.Tag)
        if not isinstance(result, tuple) or len(result) != 7:
            raise RuntimeError('Unbekannte AskFaceData-Signatur: %s; '
                               '7er-Tupel erwartet; keine Flaeche geraten' % type(result).__name__)
        kind, point, direction, box, radius, rad_data, sense = result
        if kind != 22:
            continue
        point = _finite_vec3(point, 'Punkt')
        direction = _finite_vec3(direction, 'Normalenvektor')
        length = math.hypot(*direction)
        if not math.isfinite(length) or length <= 0:
            raise RuntimeError('AskFaceData: ungueltige Flaechennormale')
        if abs(abs(direction[axis] / length) - 1) > 1e-7:
            continue
        if abs(point[axis] - plane) < tol:
            matches.append(face)
    if len(matches) != 1:
        raise RuntimeError('Blechbasisflaeche nicht eindeutig: %d Treffer' % len(matches))
    return matches[0]


def _describe(label, owner, members, log):
    """Bounded, read-only diagnostics for a subsequent NX binding failure."""
    for name in members:
        try:
            value = getattr(owner, name)
        except Exception as exc:
            log('Blech-API %s.%s nicht lesbar: %s' % (label, name, exc))
            continue
        log('Blech-API %s.%s: Typ=%s; callable=%s' %
            (label, name, type(value).__name__, callable(value)))
        if callable(value):
            log((getattr(value, '__doc__', None) or 'Keine eingebettete Dokumentation')[:4000])


def _preference_inventory(owner, log):
    """List names without evaluating unrelated getters or changing settings."""
    try:
        names = [name for name in dir(owner) if 'sheet' in name.lower()]
        log('Blech-API: verfuegbare Sheet-Eigenschaften an Preferences: ' +
            (', '.join(names[:40]) or '(keine)'))
    except Exception as exc:
        log('Blech-API: Eigenschaftsliste nicht lesbar: %s' % exc)


def require_part_sheetmetal(part, log=lambda x: None):
    """Use the documented property, not a guessed/case-insensitive alias.

    No native call is retried after a getter, setter or license exception.
    Never cache a preference object across parts. All setters are checked before
    any preference mutation. Availability does not prove successful NX execution.
    """
    preferences = part.Preferences
    try:
        pref = preferences.PartSheetmetal
    except Exception:
        _preference_inventory(preferences, log)
        raise
    if pref is None:
        _preference_inventory(preferences, log)
        raise RuntimeError('Preferences.PartSheetmetal liefert kein Objekt; Pflichtmodus stoppt.')
    _describe(PREFERENCES_PATH, pref, PREFERENCE_METHODS, log)
    missing = [name for name in PREFERENCE_METHODS
               if not callable(getattr(pref, name, None))]
    if missing:
        raise RuntimeError('NX Blecheinstellung nicht verfuegbar: %s.%s' %
                           (PREFERENCES_PATH, ', '.join(missing)))
    log('Blechpraeferenzen ausgewaehlt: ' + PREFERENCES_PATH)
    return pref


def convert(part, body, metadata, evaluate, expr_text, mode, log=lambda x: None, nx=None):
    validate_options({'mode': mode})
    if mode == 'solid':
        return body, dict(status='SOLID_PRECURSOR_ONLY', sheetmetal_verified=False,
            adapter_version=ADAPTER_VERSION,
            note='Explizit gewaehlte Visualisierungs-Vorform; scharfkantige Biegungen, keine NX-Sheet-Metal-Freigabe')
    log('Blechadapter-Version: ' + ADAPTER_VERSION)
    stage = 'SheetmetalManager'
    try:
        manager = getattr(getattr(part, 'Features', None), 'SheetmetalManager', None)
        if manager is None or not callable(getattr(manager, 'CreateConvertToSheetmetalFeatureBuilder', None)):
            raise RuntimeError('NX SheetmetalManager/CreateConvertToSheetmetalFeatureBuilder fehlt. '
                               'Pflichtmodus stoppt; kein stiller Ersatz durch Vollmaterial.')
        if nx is None:
            import NXOpen as nx
            import NXOpen.UF
        stage = 'UFSession / AskFaceData-Aufloesung'
        uf = nx.UF.UFSession.GetUFSession()
        query, query_name = resolve_face_query(uf, log)
        stage = 'Basisflaeche / ' + query_name
        axis = metadata['plane_axis']
        plane = evaluate(metadata['plane_coordinate'])
        log('Blechbasis-Suche: lokale Achse=%s, Ebenenkoordinate=%s mm' % (axis, plane))
        face = select_base_face(body, query, axis, plane)
        log('Blechbasisflaeche eindeutig: Tag=%s; Abfrage=%s' % (face.Tag, query_name))
        stage = PREFERENCES_PATH
        pref = require_part_sheetmetal(part, log)
        stage = 'Preferences.PartSheetmetal.SetThickness'
        pref.SetThickness(False, expr_text(metadata['thickness']))
        stage = 'Preferences.PartSheetmetal.SetBendRadius'
        pref.SetBendRadius(False, expr_text(metadata['bend_radius']))
        stage = 'Preferences.PartSheetmetal.SetNeutralFactor'
        pref.SetNeutralFactor(False, expr_text(metadata['neutral_factor']))
        stage = 'Preferences.PartSheetmetal.Commit'
        pref.Commit()
        stage = 'CreateConvertToSheetmetalFeatureBuilder'
        _describe('SheetmetalManager', manager, ('CreateConvertToSheetmetalFeatureBuilder',), log)
        builder = manager.CreateConvertToSheetmetalFeatureBuilder(nx.Features.Feature.Null)
        try:
            stage = 'ConvertToSheetmetalBuilder.BaseFace'
            builder.BaseFace = face
            stage = 'ConvertToSheetmetalBuilder.MaintainZeroBendRadius'
            builder.MaintainZeroBendRadius = False
            stage = 'ConvertToSheetmetalBuilder.CommitFeature'
            feature = builder.CommitFeature()
        except Exception:
            _describe('ConvertToSheetmetalBuilder', builder,
                      ('BaseFace', 'MaintainZeroBendRadius', 'CommitFeature'), log)
            raise
        finally:
            builder.Destroy()
        stage = 'Konvertiertes Feature / Koerperzahl'
        feature.SetName('K06_Natives_Kantblech')
        bodies = list(feature.GetBodies())
        if len(bodies) != 1:
            raise RuntimeError('NX Blechkonvertierung liefert nicht genau einen Koerper')
        result = bodies[0]
        stage = 'SheetmetalManager.IsSheetmetalBody'
        if not manager.IsSheetmetalBody(result):
            raise RuntimeError('NX erkennt Ergebnis nicht als Blechkoerper')
        stage = 'SheetmetalManager.GetBodyThickness'
        thickness = float(manager.GetBodyThickness(result))
        expected = evaluate(metadata['thickness'])
        if not math.isfinite(thickness) or abs(thickness - expected) > 0.005:
            raise RuntimeError('Blechdicke stimmt nach Konvertierung nicht: %r statt %r' % (thickness, expected))
        record = dict(status='NATIVE_SHEETMETAL_CREATED', sheetmetal_verified=True,
            adapter_version=ADAPTER_VERSION, face_query=query_name,
            preferences_path=PREFERENCES_PATH,
            selected_face_tag=int(face.Tag),
            measured_thickness_mm=thickness, requested_inner_radius_mm=evaluate(metadata['bend_radius']),
            requested_neutral_factor=evaluate(metadata['neutral_factor']),
            flat_pattern_generated=False, manufacturing_released=False)
        log('Blechkonvertierung OK: NX-Blechkoerper, Dicke %.6g mm' % thickness)
        return result, record
    except Exception as exc:
        log('NX-Blech-Pflichtmodus fehlgeschlagen [%s]: %s: %s' %
            (stage, type(exc).__name__, exc))
        raise
