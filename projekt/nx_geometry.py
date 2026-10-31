# -*- coding: utf-8 -*-
"""v4.6: measured native solids, explicit CSG and numerical recipe contracts.

Uses only Python's standard library and NXOpen inside NX. No geometry is moved,
no recipe operation is skipped and no CAD tolerance is relaxed on failure.
Reference data from OpenCascade is a cross-kernel check, NOT an NX validation.
"""
import itertools
import json
import math
import os
import hashlib

GEOMETRY_VERSION = '4.6'
BOUND_TOL_MM = 0.005
REL_VOLUME_TOL = 1e-5
ABS_VOLUME_TOL = 0.002


def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()


def unit_vector(vector):
    vector = [float(x) for x in vector]
    length = math.sqrt(sum(x*x for x in vector))
    if not math.isfinite(length) or length <= 1e-12:
        raise ValueError('Ungueltiger Richtungsvektor: '+repr(vector))
    return [x/length for x in vector]


def cross(a,b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def bounds_of_points(points):
    return [min(p[i] for p in points) for i in range(3)]+[max(p[i] for p in points) for i in range(3)]


def primitive_contract(op, values, evaluate):
    """Exact analytical raw-tool AABB and volume; lengths mm, volume mm^3."""
    ev=lambda s:float(evaluate(s,values))
    origin=[ev(x) for x in op['origin']]
    kind=op['kind']
    if kind=='box':
        size=[ev(x) for x in op['size']]
        bounds=origin+[origin[i]+size[i] for i in range(3)]
        volume=math.prod(size)
    else:
        h=ev(op['height']);direction=unit_vector(op['direction'])
        end=[origin[i]+h*direction[i] for i in range(3)]
        if kind in ('cylinder','cone'):
            r=ev(op['diameter'])/2
            r2=r if kind=='cylinder' else ev(op['top_diameter'])/2
            radial=[math.sqrt(max(0.0,1.0-d*d)) for d in direction]
            bounds=[min(origin[i]-r*radial[i],end[i]-r2*radial[i]) for i in range(3)]
            bounds += [max(origin[i]+r*radial[i],end[i]+r2*radial[i]) for i in range(3)]
            volume=math.pi*h*(r*r+r*r2+r2*r2)/3
        elif kind=='prism':
            pts=[[ev(x) for x in p] for p in op['points']]
            ends=[[p[i]+direction[i]*h for i in range(3)] for p in pts]
            bounds=bounds_of_points(pts+ends)
            area=[0.0,0.0,0.0]
            # Translate to the first vertex to reduce cancellation.
            for i in range(1,len(pts)-1):
                a=[pts[i][j]-pts[0][j] for j in range(3)]
                b=[pts[i+1][j]-pts[0][j] for j in range(3)]
                c=cross(a,b)
                area=[area[j]+c[j]/2 for j in range(3)]
            volume=abs(sum(area[i]*direction[i]*h for i in range(3)))
        else:
            raise ValueError('Kein Geometrievertrag fuer '+str(kind))
    if not all(math.isfinite(x) for x in bounds+[volume]) or volume<=0:
        raise ValueError('Ungueltige Sollgeometrie: '+repr(op))
    return dict(bounds_mm=bounds,volume_mm3=volume)


def assert_volume(actual,expected,label):
    tolerance=max(ABS_VOLUME_TOL,abs(expected)*REL_VOLUME_TOL)
    if not math.isfinite(actual) or abs(actual-expected)>tolerance:
        raise RuntimeError('%s: Volumen IST %.12g / SOLL %.12g mm^3 (Toleranz %.12g). '
                           'Keine Geometriekorrektur/kein Ueberspringen.'%(label,actual,expected,tolerance))


def assert_contract(actual,expected,label):
    bounds=actual['bounds_mm'];wanted=expected['bounds_mm']
    if len(bounds)!=6 or any(not math.isfinite(a) or abs(a-e)>BOUND_TOL_MM for a,e in zip(bounds,wanted)):
        raise RuntimeError('%s: Koerperlage/Abmessung falsch. IST %r / SOLL %r mm. '
                           'Abbruch VOR boolescher Operation.'%(label,bounds,wanted))
    assert_volume(actual['volume_mm3'],expected['volume_mm3'],label)


def assert_boolean_change(operation,before,after,tool_volume,label):
    change=after-before
    eps=max(1e-6,abs(before)*1e-11)
    if operation=='cut':
        if not change < -eps:
            raise RuntimeError(label+': Subtraktion entfernt kein messbares Material; nicht uebersprungen.')
        if -change>tool_volume+max(ABS_VOLUME_TOL,tool_volume*REL_VOLUME_TOL):
            raise RuntimeError(label+': Abtragsvolumen groesser als Werkzeugvolumen.')
    elif operation=='add':
        if not change > eps:
            raise RuntimeError(label+': Vereinigung fuegt kein messbares Material hinzu; nicht uebersprungen.')
        if change>tool_volume+max(ABS_VOLUME_TOL,tool_volume*REL_VOLUME_TOL):
            raise RuntimeError(label+': Zuwachs groesser als Werkzeugvolumen.')
    else:raise ValueError('Ungueltige boolesche Operation: '+str(operation))


class MeasurementValueError(RuntimeError):
    """A measurement was returned, but it cannot represent a solid volume."""


class BodyInspector:
    """Read actual NX geometry, never substitute recipe/reference values.

    v4.6: AskMassProps3d is OPTIONAL. Prefer the high-level MeasureManager
    with explicitly named units (including CubicMilliMeter), then use a UF
    volume method only if one is actually exposed by this Python binding.
    API selection happens on the first body; later failures are fatal, not
    silently retried with another measurement API. Every raw-tool result is
    checked against its analytical contract by NativeModelBuilder.primitive.
    """
    UNIT_NAMES = ('SquareMilliMeter', 'CubicMilliMeter', 'Kilogram',
                  'MilliMeter', 'Newton')
    MANAGER_MODES = ('manager_bodies_accuracy', 'manager_collector_accuracy',
                     'manager_bodies_tolerances', 'manager_collector_tolerances',
                     'manager_collector_accuracy_no_geometry',
                     'manager_collector_tolerances_no_geometry')

    def __init__(self, part, log):
        import NXOpen.UF
        self.part = part
        self.log = log
        self.uf = NXOpen.UF.UFSession.GetUFSession()
        self._groups = []
        self.mode = None
        self.last_api = None
        self.last_units = None
        self.attempts = []
        # Python UF grouping differs from the C#/C++ documentation.
        # Do not require a method just because another language lists it.
        for name in ('Modl', 'ModlGeneral', 'Modeling'):
            try:
                group = getattr(self.uf, name, None)
            except Exception as exc:
                self.log('NX-Mess-API Gruppe %s nicht lesbar: %s' % (name, exc))
                continue
            if group is not None:
                self._groups.append((name, group))
        self.box, self.box_name = self._method('AskBoundingBoxExact')
        self.mass, self.mass_name = self._method('AskMassProps3d')
        try:
            self.manager = getattr(part, 'MeasureManager', None)
            self.new_mass = getattr(self.manager, 'NewMassProperties', None)
        except Exception as exc:
            self.log('NX MeasureManager nicht lesbar: ' + str(exc))
            self.manager = self.new_mass = None
        self.log('NX-Mess-API: BoundingBox=%s; NewMassProperties=%s; UF-Masse=%s' %
                 (self.box_name, callable(self.new_mass), self.mass_name))
        if not callable(self.box):
            self.diagnostics()
            raise RuntimeError('NX-Messfunktion AskBoundingBoxExact fehlt. '
                               'Keine angenaeherten Grenzen als Ersatz.')
        if not callable(self.new_mass) and not callable(self.mass):
            self.diagnostics()
            raise RuntimeError('Keine ausfuehrbare NX-Volumenmessung gefunden: '
                               'MeasureManager.NewMassProperties und UF AskMassProps3d fehlen.')

    def _method(self, name):
        """Resolve known UF method names, with case-insensitive alias support."""
        for group_name, group in self._groups:
            names = [name]
            try:
                names += [n for n in dir(group)
                          if n != name and n.casefold() == name.casefold()]
            except Exception:
                pass
            for spelling in names:
                try:
                    function = getattr(group, spelling, None)
                except Exception:
                    continue
                if callable(function):
                    return function, 'UF.' + group_name + '.' + spelling
        return None, None

    @staticmethod
    def _positive(value):
        number = float(value)
        if not math.isfinite(number) or number <= 0.0:
            raise MeasurementValueError('NX liefert kein positives endliches '
                                        'Koerpervolumen: ' + repr(value))
        return number

    def _units(self):
        # Fetch fresh Unit objects on every call; no references across Undo.
        # The five entries are area, volume, mass, length and force (weight).
        units = []
        for name in self.UNIT_NAMES:
            try:
                unit = self.part.UnitCollection.FindObject(name)
            except Exception as exc:
                raise RuntimeError('NX-Messeinheit %s nicht gefunden: %s' %
                                   (name, exc)) from exc
            if unit is None:
                raise RuntimeError('NX-Messeinheit fehlt: ' + name)
            units.append(unit)
        self.last_units = list(self.UNIT_NAMES)
        return units

    @staticmethod
    def _release(obj, names):
        if obj is None:
            return
        for name in names:
            method = getattr(obj, name, None)
            if callable(method):
                method()
                return
        raise RuntimeError('Temporaeres NX-Messobjekt nicht freigebbar: ' +
                           type(obj).__name__)

    def _manager_volume(self, body, mode):
        units = self._units()
        measurement = None
        collector = None
        try:
            objects = [body]
            if 'collector' in mode:
                collector = self.part.ScCollectors.CreateCollector()
                rule = self.part.ScRuleFactory.CreateRuleBodyDumb([body])
                collector.ReplaceRules([rule], False)
                objects = collector
            accuracy = ([1e-7] * 11 if 'tolerances' in mode else 0.999999)
            if mode.endswith('_no_geometry'):
                measurement = self.new_mass(units, accuracy, False, objects)
            else:
                measurement = self.new_mass(units, accuracy, objects)
            if measurement is None:
                raise RuntimeError('NewMassProperties lieferte kein Messobjekt.')
            # Result is already mm^3 because units[1] is CubicMilliMeter.
            # No 1e9 multiplier on this path. No CreateFeature/CreateEmbedded.
            return self._positive(measurement.Volume)
        finally:
            try:
                self._release(measurement, ('Dispose', 'FreeResource'))
            finally:
                self._release(collector, ('Destroy',))

    def _uf_volume(self, body):
        # UF units=4: kg and m. Only THIS path converts m^3 to mm^3.
        props, statistics = self.mass([body.Tag], 1, 1, 4, 1.0, 1,
                                      [0.999999] + [0.0] * 10)
        if len(props) < 2:
            raise RuntimeError('UF-Massenmessung lieferte kein Volumenfeld.')
        return self._positive(float(props[1]) * 1e9)

    def _call_volume(self, body, mode):
        self.last_api = ('MeasureManager.NewMassProperties/' + mode
                         if mode.startswith('manager_') else self.mass_name)
        if mode.startswith('manager_'):
            return self._manager_volume(body, mode)
        if mode == 'uf_mass':
            return self._uf_volume(body)
        raise RuntimeError('Unbekannter NX-Messmodus: ' + str(mode))

    def _volume(self, body):
        if self.mode is not None:
            return self._call_volume(body, self.mode)
        candidates = list(self.MANAGER_MODES) if callable(self.new_mass) else []
        if callable(self.mass):
            candidates.append('uf_mass')
        for mode in candidates:
            try:
                volume = self._call_volume(body, mode)
            except MeasurementValueError:
                # A nonsensical result is not an overload-selection failure.
                raise
            except Exception as exc:
                self.attempts.append(dict(mode=mode, error=type(exc).__name__ + ': ' + str(exc)))
                self.log('NX-Messvariante nicht verwendbar: %s / %s: %s' %
                         (mode, type(exc).__name__, exc))
                continue
            self.mode = mode
            self.log('NX-Volumenmessung ausgewaehlt: %s; Ausgabe mm^3. '
                     'Soll-Ist-Kontrolle folgt am real erzeugten Koerper.' % mode)
            return volume
        self.diagnostics()
        raise RuntimeError('Alle vorhandenen NX-Volumenmessvarianten fehlgeschlagen. '
                           'Die Geometriepruefung wurde NICHT abgeschaltet.')

    def diagnostics(self):
        self.log('--- NX-Mess-API-Diagnose v4.6 ---')
        self.log('Messmodus: %r; letzter Aufruf: %r; Einheiten: %r' %
                 (self.mode, self.last_api, self.last_units))
        for name, group in self._groups:
            try:
                methods = [n for n in dir(group)
                           if any(s in n.casefold() for s in ('mass', 'volume', 'bounding'))]
                self.log('UF.%s relevante Methoden: %s' % (name, ', '.join(methods)))
            except Exception as exc:
                self.log('Methodenliste %s: %s' % (name, exc))
        for name, fn in ((self.box_name, self.box), (self.mass_name, self.mass),
                         ('MeasureManager.NewMassProperties', self.new_mass)):
            if callable(fn):
                self.log('NX-Mess-API %s: %s' % (name, str(getattr(fn, '__doc__', ''))[:9000]))

    def measure(self, body):
        try:
            tag = body.Tag
            corner, directions, distances = self.box(tag, self.part.WCS.CoordinateSystem.Tag)
            if len(directions) == 9 and not hasattr(directions[0], '__len__'):
                directions = [directions[i:i+3] for i in (0, 3, 6)]
            if (len(corner) != 3 or len(distances) != 3 or len(directions) != 3 or
                    any(len(row) != 3 for row in directions)):
                raise RuntimeError('Ungueltige Matrix/Laengen aus AskBoundingBoxExact')
            numbers = list(corner) + list(distances) + [v for row in directions for v in row]
            if not all(math.isfinite(float(x)) for x in numbers) or any(float(x) < 0 for x in distances):
                raise RuntimeError('Ungueltige/nicht endliche Begrenzungen aus AskBoundingBoxExact')
            corners = []
            for signs in itertools.product((0, 1), repeat=3):
                corners.append([float(corner[i]) + sum(signs[j] * float(directions[j][i]) *
                                float(distances[j]) for j in range(3)) for i in range(3)])
            volume = self._volume(body)
            return dict(tag=int(tag), bounds_mm=bounds_of_points(corners),
                        volume_mm3=volume, volume_backend=self.mode)
        except Exception:
            self.diagnostics()
            raise


class ReferenceCheck:
    """Only compare reference volumes for the EXACT audited parameter/recipe set."""
    def __init__(self,path,parameters,definitions,log):
        with open(path,encoding='utf8') as f:data=json.load(f)
        self.data={}
        parameter_hash = fingerprint(parameters)
        recipe_hash = fingerprint(definitions)
        log('Referenzfingerprints: Parameter passend=%s; Rezept passend=%s' %
            (parameter_hash == data['parameter_sha256'], recipe_hash == data['recipe_sha256']))
        match=(parameter_hash==data['parameter_sha256'] and
               recipe_hash==data['recipe_sha256'])
        if match:
            self.data={d['id']:d['rows'] for d in data['parts']}
            log('Referenzvergleich aktiv: Standardparameter; OpenCascade-Zwischenvolumina, kein NX-Pruefnachweis.')
        else:
            log('Referenzfingerprint nicht identisch (kein Nachweis einer bewussten Massaenderung): '
                'kein Standard-Referenzvergleich; Werkzeuglage, Werkzeugvolumen und boolesche Wirkung bleiben aktiv.')
            log('Referenzhash Parameter SOLL=%s IST=%s; Rezept SOLL=%s IST=%s' %
                (data['parameter_sha256'], parameter_hash, data['recipe_sha256'], recipe_hash))

    def check(self,part_id,index,measurement):
        rows=self.data.get(part_id)
        if rows is not None:
            row=rows[index-1]
            if row['n']!=index:raise RuntimeError('Beschaedigte Geometriereferenz')
            assert_volume(measurement['volume_mm3'],row['after'],part_id+' Feature '+str(index)+' Referenz')
