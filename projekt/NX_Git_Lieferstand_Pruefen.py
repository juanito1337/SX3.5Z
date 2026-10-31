# -*- coding: utf-8 -*-
"""Read-only native reopen check of a newly generated Stand09 delivery.

Set SX35Z_VERIFY_RUN to its directory below this repository's cad/nx/.
Use a fresh run_journal process. Writes only a new JSON report, never saves PRT.
NX API signatures checked against local NX 2406 UGOPEN/pythonStubs.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import NXOpen
import cnc_ansichtsmodell as model


def main():
    run = Path(os.environ['SX35Z_VERIFY_RUN']).resolve()
    run.relative_to((HERE.parent / 'cad' / 'nx').resolve())
    manifest = json.loads((run / 'Erzeugte_Teile.json').read_text(encoding='utf8'))
    main_name = (run / 'HAUPTBAUGRUPPE.txt').read_text(encoding='utf8').strip()
    main_path = (run / main_name).resolve()
    main_path.relative_to(run)
    expected = {d['id']: d for d in model.recipe()}
    assert len(manifest) == len(expected) == 560
    assert {d['id'] for d in manifest} == set(expected)
    expected_paths = {}
    for item in manifest:
        path = (run / item['file']).resolve()
        path.relative_to(run)
        assert path.is_file(), str(path)
        assert item['name'] == expected[item['id']]['name']
        assert path not in expected_paths, str(path)
        expected_paths[path] = item
    session = NXOpen.Session.GetSession()
    assert not list(session.Parts), 'Pruefung verlangt eine frische NX-Sitzung.'
    options = session.Parts.LoadOptions
    options.ComponentsToLoad = NXOpen.LoadOptions.LoadComponents.All
    options.UsePartialLoading = False
    options.UseLightweightRepresentations = False
    options.AllowSubstitution = False
    options.AbortOnFailure = True
    options.ComponentLoadMethod = NXOpen.LoadOptions.LoadMethod.SearchDirectories
    options.SetSearchDirectories([str(run), str(run / 'Teile'), str(run / 'Unterbaugruppen')],
                                 [False, False, False])
    result = dict(native_nx_executed=True, saved_parts_reopened=False,
                  manufacturing_released=False, purchase_released=False,
                  machine_operation_enabled=False, atc_operational=False,
                  directory=str(run), main_part=main_name, components=[], errors=[])
    try:
        part, status = session.Parts.OpenBaseDisplay(str(main_path))
        try:
            unloaded = [dict(part=status.GetPartName(i), error=status.GetStatusDescription(i))
                        for i in range(status.NumberUnloadedParts)]
            result['unloaded'] = unloaded
            assert not unloaded, repr(unloaded)
        finally:
            status.Dispose()
        assert Path(part.FullPath).resolve() == main_path
        root = part.ComponentAssembly.RootComponent
        groups = root.GetChildren()
        assert len(groups) == len(model.GROUPS) == 20
        found = set()
        metadata_checked = 0
        sheet_spec = next(s for s in model.SPECS if s['name'] == 'sheet_t')
        parameters = json.loads((run / 'Parameter_beim_Aufbau.json').read_text(encoding='utf8'))
        for group in groups:
            group_path = Path(group.Prototype.FullPath).resolve()
            group_path.relative_to(run)
            assert group.Prototype.IsFullyLoaded
            for component in group.GetChildren():
                prototype = component.Prototype
                path = Path(prototype.FullPath).resolve()
                path.relative_to(run)
                assert path in expected_paths, str(path)
                assert path not in found, str(path)
                found.add(path)
                assert prototype.IsFullyLoaded, str(path)
                assert len(list(prototype.Bodies)) == 1, str(path)
                assert not component.GetChildren(), str(path)
                expressions = {e.Name: e for e in prototype.Expressions}
                if 'sx_sheet_t' in expressions:
                    assert expressions['sx_sheet_t'].Value == parameters['sheet_t']
                    for suffix, value in [('STATUS', sheet_spec['status']),
                                          ('BESCHREIBUNG', sheet_spec['note']),
                                          ('QUELLE', sheet_spec['source']), ('EINHEIT', 'mm')]:
                        assert prototype.GetUserAttributeAsString(
                            'SX_EXPR_sheet_t_' + suffix, NXOpen.NXObject.AttributeType.String, -1) == value
                    metadata_checked += 1
                result['components'].append(dict(id=expected_paths[path]['id'],
                    file=str(path.relative_to(run)), fully_loaded=True, body_count=1))
        assert found == set(expected_paths)
        assert metadata_checked > 0, 'Keine gespeicherten Ausdrucksmetadaten geprueft.'
        for loaded in session.Parts:
            Path(loaded.FullPath).resolve().relative_to(run)
        result.update(saved_parts_reopened=True, part_count=len(found), group_count=len(groups),
                      metadata_parts_checked=metadata_checked)
        print('WIEDEROEFFNUNG_BESTANDEN: 560 Einzelteile, 20 Unterbaugruppen, Metadaten persistent.')
    except Exception as exc:
        result['errors'].append(type(exc).__name__ + ': ' + str(exc))
        raise
    finally:
        name = 'NX_Wiederoeffnung_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json'
        with (run / name).open('x', encoding='utf8') as stream:
            json.dump(result, stream, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
