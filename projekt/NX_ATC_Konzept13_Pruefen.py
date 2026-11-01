# -*- coding: utf-8 -*-
"""Fresh-session NX2406 reopen and AP214 export for concept 13.

SX35Z_VERIFY_RUN must name a completed run below this repository's cad/nx.
Reads PRT files without saving; writes a uniquely named report and STEP only.
NX APIs follow NX_Git_Lieferstand_Pruefen.py and the locally executed
ergebnisse/entwicklung/20261101_step12/export_step.py (NX2406).
"""
import hashlib
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

HERE = Path(__file__).resolve().parent
VERSION = 'CNC_KONZEPT_13_SEITENMAGAZIN'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(',', ':')).encode('utf8')).hexdigest()


def contained_file(root, relative):
    path = (root / relative).resolve()
    path.relative_to(root)
    if not path.is_file():
        raise ValueError('Lieferdatei fehlt: ' + str(path))
    return path


def validate_bundle(run, model):
    """File/recipe contract, independently testable without importing NXOpen."""
    if model.VERSION != VERSION:
        raise ValueError('Kein Konzept13-Modell: ' + model.VERSION)
    manifest = json.loads(contained_file(run, 'Erzeugte_Teile.json').read_text(encoding='utf8'))
    recipe = json.loads(contained_file(run, 'Rezept_beim_Aufbau.json').read_text(encoding='utf8'))
    parameters = json.loads(contained_file(run, 'Parameter_beim_Aufbau.json').read_text(encoding='utf8'))
    metadata = json.loads(contained_file(run, 'NX_Lieferstand13.json').read_text(encoding='utf8'))
    if metadata.get('version') != VERSION or not metadata.get('build_completed'):
        raise ValueError('Kein abgeschlossener Konzept13-Lauf.')
    # Canonical serialization preserves every numeric value; no tolerance/hash rounding.
    recipe_hash = fingerprint(recipe)
    if recipe_hash != fingerprint(model.recipe()) or recipe_hash != metadata['recipe_sha256']:
        raise ValueError('Lieferstandrezept stimmt nicht exakt mit Konzept13 ueberein.')
    if fingerprint(parameters) != metadata['parameter_sha256']:
        raise ValueError('Gespeicherte Parameter weichen vom Aufbau ab.')
    model.check_recipe(parameters)
    expected = {d['id']: d for d in recipe}
    if len(expected) != len(recipe) or len(manifest) != len(expected):
        raise ValueError('Teileanzahl oder doppelte Rezeptkennung.')
    if {m['id'] for m in manifest} != set(expected):
        raise ValueError('Manifest enthaelt nicht exakt die Rezeptteile.')
    expected_paths = {}
    values = model.all_values(parameters)
    for item in manifest:
        definition = expected[item['id']]
        path = contained_file(run, item['file'])
        if path in expected_paths or path.suffix.lower() != '.prt':
            raise ValueError('Doppelte oder ungueltige PRT-Datei: ' + str(path))
        if item['name'] != definition['name'] or item['group'] != definition['group']:
            raise ValueError('Manifestzuordnung weicht vom Rezept ab: ' + item['id'])
        datum = [model.evaluate(x, values) for x in definition['datum']]
        if item['datum'] != datum:
            raise ValueError('Manifestlage weicht vom Rezept ab: ' + item['id'])
        if 'sheetmetal' in definition:
            result = item.get('sheetmetal') or {}
            if not result.get('sheetmetal_verified'):
                raise ValueError('Native Blechkonvertierung nicht bestaetigt: ' + item['id'])
        expected_paths[path] = item
    if metadata['sheetmetal_mode'] != 'required':
        raise ValueError('Blech-Pflichtmodus fehlt.')
    for name, digest in metadata['source_sha256'].items():
        if sha256(contained_file(HERE, name)) != digest:
            raise ValueError('Quellstand nach Aufbau geaendert: ' + name)
    main_name = contained_file(run, 'HAUPTBAUGRUPPE.txt').read_text(encoding='utf8').strip()
    main_path = contained_file(run, main_name)
    if main_path.suffix.lower() != '.prt':
        raise ValueError('Hauptbaugruppe ist keine PRT-Datei.')
    return manifest, recipe, parameters, metadata, expected_paths, main_path


def export_step(session, source, output, NXOpen):
    """Full assembly, synchronous export; never saves source PRT files."""
    if output.exists():
        raise FileExistsError(str(output))
    settings = Path('C:/Siemens/nx2406/STEP214UG/ugstep214.def')
    if not settings.is_file():
        raise FileNotFoundError(str(settings))
    builder = session.DexManager.CreateStepCreator()
    try:
        builder.SettingsFile = str(settings)
        builder.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
        builder.ExportFrom = NXOpen.StepCreator.ExportFromOption.DisplayPart
        builder.ExportSelectionBlock.SelectionScope = NXOpen.ObjectSelector.Scope.EntireAssembly
        builder.InputFile = str(source)
        builder.OutputFile = str(output)
        builder.ObjectTypes.Solids = True
        builder.ObjectTypes.Surfaces = False
        builder.ObjectTypes.Curves = False
        builder.ColorAndLayers = True
        builder.LayerMask = '1-256'
        builder.ExportExtRef = False
        builder.FileSaveFlag = False
        builder.ProcessHoldFlag = True
        builder.Commit()
    finally:
        builder.Destroy()
    if not output.is_file() or output.stat().st_size <= 1000:
        raise RuntimeError('STEP-Export fehlt oder ist leer: ' + str(output))
    return dict(file=str(output), bytes=output.stat().st_size, sha256=sha256(output),
                format='AP214', scope='EntireAssembly', source_prt_saved=False)


def main():
    sys.path.insert(0, str(HERE))
    import NXOpen
    import atc13_modell as model
    run = Path(os.environ['SX35Z_VERIFY_RUN']).resolve()
    run.relative_to((HERE.parent / 'cad' / 'nx').resolve())
    if not run.is_dir():
        raise ValueError('NX-Laufordner fehlt: ' + str(run))
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '_' + uuid4().hex[:8]
    result = dict(version=VERSION, date=datetime.now().astimezone().isoformat(),
        command='C:/Siemens/nx2406/NXBIN/run_journal.exe ' + str(Path(__file__).resolve()),
        environment='NX2406 target / ' + sys.version,
        nxopen_module=str(getattr(NXOpen,'__file__','unknown')),native_nx_executed=True,
        saved_parts_reopened=False, source_prt_unchanged=False,
        build_ready=False, manufacturing_released=False, purchase_released=False,
        machine_operation_enabled=False, atc_operational=False,
        scope='Fresh reopen, membership, positions, expressions, metadata and AP214; no motion or fit proof',
        directory=str(run), components=[], errors=[])
    originals = {}
    try:
        manifest, recipe, parameters, metadata, expected_paths, main_path = validate_bundle(run, model)
        result.update(source_revision=metadata['source_revision'],
                      source_sha256=metadata['source_sha256'], recipe_sha256=metadata['recipe_sha256'])
        originals = {p: sha256(p) for p in run.rglob('*.prt')}
        session = NXOpen.Session.GetSession()
        if list(session.Parts):
            raise RuntimeError('Pruefung verlangt eine frische NX-Sitzung.')
        options = session.Parts.LoadOptions
        options.ComponentsToLoad = NXOpen.LoadOptions.LoadComponents.All
        options.UsePartialLoading = False
        options.UseLightweightRepresentations = False
        options.AllowSubstitution = False
        options.AbortOnFailure = True
        options.ComponentLoadMethod = NXOpen.LoadOptions.LoadMethod.SearchDirectories
        options.SetSearchDirectories([str(run), str(run / 'Teile'), str(run / 'Unterbaugruppen')], [False]*3)
        part, status = session.Parts.OpenBaseDisplay(str(main_path))
        try:
            result['unloaded'] = [dict(part=status.GetPartName(i), error=status.GetStatusDescription(i))
                                  for i in range(status.NumberUnloadedParts)]
            assert not result['unloaded'], repr(result['unloaded'])
        finally:
            status.Dispose()
        assert Path(part.FullPath).resolve() == main_path
        readattr = lambda obj, name: obj.GetUserAttributeAsString(name, NXOpen.NXObject.AttributeType.String, -1)
        assert readattr(part, 'SX_VERSION') == VERSION
        groups = part.ComponentAssembly.RootComponent.GetChildren()
        expected_groups = {m['group'] for m in manifest}
        assert len(groups) == len(expected_groups)
        found, seen_groups = set(), set()
        specs = {s['name']: s for s in model.SPECS}
        definitions = {d['id']: d for d in recipe}
        values = model.all_values(parameters)
        metadata_checked = 0
        expression_count = 0
        sheetmetal_count = 0
        for group in groups:
            group_path = Path(group.Prototype.FullPath).resolve()
            group_path.relative_to(run)
            assert group.Prototype.IsFullyLoaded
            assert readattr(group.Prototype, 'SX_VERSION') == VERSION
            origin, axes = group.GetPosition()
            assert max(abs(origin.X),abs(origin.Y),abs(origin.Z)) <= 1e-9
            assert all(abs(getattr(axes,n)-v) <= 1e-9 for n,v in
                       [('Xx',1),('Xy',0),('Xz',0),('Yx',0),('Yy',1),('Yz',0),('Zx',0),('Zy',0),('Zz',1)])
            children = group.GetChildren()
            assert children, 'Leere Unterbaugruppe'
            actual_group = None
            for component in children:
                prototype = component.Prototype
                path = Path(prototype.FullPath).resolve()
                path.relative_to(run)
                assert path in expected_paths and path not in found, str(path)
                item = expected_paths[path]
                actual_group = actual_group or item['group']
                assert item['group'] == actual_group
                found.add(path)
                assert prototype.IsFullyLoaded and len(list(prototype.Bodies)) == 1, str(path)
                assert not component.GetChildren()
                assert readattr(prototype, 'SX_VERSION') == VERSION
                assert readattr(prototype, 'SX_PART_ID') == item['id']
                assert readattr(component, 'SX_PART_ID') == item['id']
                definition = definitions[item['id']]
                needed = model.used_parameters(model.local_definition(definition))
                if 'sheetmetal' in definition:
                    needed.update({'sheet_t','bend_r','bend_k'})
                    manager = prototype.Features.SheetmetalManager
                    body = list(prototype.Bodies)[0]
                    assert manager.IsSheetmetalBody(body), item['id']
                    thickness = float(manager.GetBodyThickness(body))
                    assert abs(thickness-model.evaluate(definition['sheetmetal']['thickness'],values)) <= 0.005
                    sheetmetal_count += 1
                expression_names = {e.Name for e in prototype.Expressions}
                assert {'sx_'+n for n in needed}.issubset(expression_names), item['id']
                position, orientation = component.GetPosition()
                assert all(abs(a-b) <= 1e-6 for a,b in zip((position.X,position.Y,position.Z),item['datum']))
                assert all(abs(getattr(orientation,n)-v) <= 1e-9 for n,v in
                           [('Xx',1),('Xy',0),('Xz',0),('Yx',0),('Yy',1),('Yz',0),('Zx',0),('Zy',0),('Zz',1)])
                for expression in prototype.Expressions:
                    name = expression.Name
                    if not name.startswith('sx_') or name[3:] not in values:
                        continue
                    key = name[3:]
                    expected_value = values[key]
                    assert math.isclose(expression.Value, expected_value, rel_tol=1e-9, abs_tol=1e-7), name
                    expression_count += 1
                    if key in specs:
                        spec = specs[key]
                        for suffix, value in [('STATUS',spec['status']),('BESCHREIBUNG',spec['note']),('QUELLE',spec['source'])]:
                            assert readattr(prototype,'SX_EXPR_'+key+'_'+suffix) == value, name
                        unit = ('einheitenlos (Verhaeltnis)' if spec.get('unit') == 'unitless' else
                                ('Zahlenwert in mm; NX-Ausdruck einheitenlos' if item['expression_mode'] == 'Number_mm' else 'mm'))
                        assert readattr(prototype,'SX_EXPR_'+key+'_EINHEIT') == unit
                        metadata_checked += 1
                result['components'].append(dict(id=item['id'],file=item['file'],fully_loaded=True,body_count=1))
            assert actual_group not in seen_groups
            seen_groups.add(actual_group)
            assert len(children) == sum(m['group'] == actual_group for m in manifest)
            assert readattr(group.Prototype,'SX_BAUGRUPPE') == model.GROUPS[actual_group]
        assert seen_groups == expected_groups and found == set(expected_paths)
        assert metadata_checked > 0 and expression_count > 0
        for loaded in session.Parts:
            Path(loaded.FullPath).resolve().relative_to(run)
        result.update(saved_parts_reopened=True,part_count=len(found),group_count=len(groups),
                      metadata_expressions_checked=metadata_checked,expressions_checked=expression_count,
                      native_sheetmetal_parts_reopened=sheetmetal_count)
        output = run / ('SX35Z_KONZEPT13_' + metadata['pose'].upper() + '_' + stamp + '.step')
        result['step_export'] = export_step(session,main_path,output,NXOpen)
        assert all(sha256(p) == digest for p,digest in originals.items()), 'PRT-Dateien veraendert'
        result.update(source_prt_unchanged=True,journal_completed=True)
        print('KONZEPT13_WIEDEROEFFNUNG_UND_STEP_BESTANDEN: %d Teile, %d Gruppen' % (len(found),len(groups)))
    except Exception as exc:
        result['errors'].append(type(exc).__name__ + ': ' + str(exc))
        raise
    finally:
        if originals:
            result['source_prt_unchanged'] = all(p.is_file() and sha256(p) == h for p,h in originals.items())
        with (run / ('NX_Wiederoeffnung13_' + stamp + '.json')).open('x',encoding='utf8') as stream:
            json.dump(result,stream,indent=2,ensure_ascii=False)


if __name__ == '__main__':
    main()
