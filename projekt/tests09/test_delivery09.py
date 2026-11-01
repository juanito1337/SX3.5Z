import json
from pathlib import Path
import pytest
import cnc_ansichtsmodell as model
ROOT=Path(__file__).resolve().parents[1]

def test_new_native_entrypoint_reloads_and_checks_revision09():
    s=(ROOT/'NX_CNC_Gesamtansicht.py').read_text()
    assert "'CNC_UMSETZUNG_10_TELLER'" in s
    assert "'normteile09'" in s and "'cnc_ansichtsmodell08'" in s
    assert 'umbau_daten09' in s
    assert (ROOT/'NX_Normteile_ATC_Pruefen.py').exists()

def test_planned_new_catalog_quantities_match_physical_instances():
    cat=json.loads((ROOT/'Einkauf/Kaufteile_09.json').read_text())['items']
    ds=model.recipe()
    for key,item in cat.items():
        if not key.startswith(('K09','N09')):continue
        inst={d['purchase_instance'] for d in ds if d.get('item_id')==key and d.get('supply_kind')=='BUY'}
        assert item['planned_quantity']==len(inst),key

def test_magazine_no_longer_depends_on_old_table_slot_attachment():
    p=model.load_parameters(ROOT/'Parameter.json');p['atc_y']=-20
    assert model.validate(p)
    assert model.atc_report(p)['table_mounting'] is False

def test_export_module_and_full_mapping():
    assert (ROOT/'umbau_daten09.py').exists(),'09 single source export missing'
    import umbau_daten09 as data
    rows=data.bom_rows(model.recipe(),ROOT)
    assert len(rows)>61
    assert len(data.model_map(model.recipe()))==len(model.recipe())
    r=data.release_report(ROOT)
    assert r['atc_operational'] is False
    assert 'A09' in r['open_gates']

def test_magazine_sheet_thickness_in_manufacturing_matches_model():
    import umbau_daten09 as data
    p=model.load_parameters(ROOT/'Parameter.json')
    rows={r['name']:r for r in data.manufacturing_rows(model.recipe(),p,model)}
    assert 'ATC_Magazintraeger_Kantblech' not in rows
    assert '2mm' in rows['ATC_Parkhaube_Dach_Entwurf']['material']
