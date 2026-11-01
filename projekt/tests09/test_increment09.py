import copy, json
from pathlib import Path
import pytest
import cnc_ansichtsmodell as model
ROOT=Path(__file__).resolve().parents[1]

def test_revision09_is_implemented():
    assert model.VERSION=='CNC_UMSETZUNG_10_TELLER'

def test_stock_castings_and_complete_moving_door_unchanged():
    import cnc_ansichtsmodell08 as old
    new={d['name']:d for d in model.recipe()}
    for d in old.recipe():
        if 'Guss' in d['name'] or 'door_leaf' in d or d['name'].startswith('Spindelnase_'):
            assert new[d['name']]['ops']==d['ops']
            assert new[d['name']]['datum']==d['datum']

def test_new_purchase_mapping_and_counts():
    cat=json.loads((ROOT/'Einkauf/Kaufteile_09.json').read_text())['items']
    new=[d for d in model.recipe() if d.get('revision_added')=='09']
    assert len(new)==48  # retained service/cabinet hardware; table magazine replaced
    for d in new:
        if d['supply_kind']=='BUY':
            assert d['item_id'] in cat
            assert cat[d['item_id']]['source_ids']
            assert d['purchase_instance']
    handles=[d for d in new if d.get('item_id')=='K09-GN425']
    assert len({d['purchase_instance'] for d in handles})==3
    assert sum(d.get('item_id')=='K09-GLAND20' for d in new)==2

def test_eight_pockets_not_a_claim_of_operational_atc():
    assert hasattr(model,'atc_report'), 'ATC interface/reach gate is missing'
    r=model.atc_report(model.load_parameters(ROOT/'Parameter.json'))
    assert len(r['pockets'])==8
    assert r['machine_operation_enabled'] is False
    assert r['original_spindle']=='SK30/M12 DIN2080'
    assert r['required_spindle_interface']=='BT30 automatic clamping'
    assert r['nominal_reach_ok'] is False  # no complete trajectory/spindle proof
    assert r['trajectory_verified'] is False

def test_atc_radius_too_small_rejected():
    assert hasattr(model,'atc_report'), 'ATC validation missing'
    p=model.load_parameters(ROOT/'Parameter.json');p['teller_radius']=40
    with pytest.raises(ValueError):model.atc_report(p)

def test_new_catalog_dimensions_cannot_be_silently_overridden():
    p=model.load_parameters(ROOT/'Parameter.json');p['n09_grip_pitch']=171
    with pytest.raises(ValueError):model.validate(p)

def test_original_machine_is_not_drilled_for_magazine():
    import cnc_ansichtsmodell08 as old
    t=next(d for d in old.recipe() if d['name']=='Arbeitstisch_Foto')
    n=next(d for d in model.recipe() if d['name']=='Arbeitstisch_Foto')
    assert t['ops']==n['ops']

def test_assembly_references_unique():
    ds=model.recipe()
    assert len(set(d['id'] for d in ds))==len(ds)
    assert len(set(d['name'] for d in ds))==len(ds)

def test_hardware_has_matching_mounting_cuts():
    ds={d['name']:d for d in model.recipe()}
    assert sum('09_Griffdurchgang' in o['label'] for o in ds['KSS_Serviceklappe_hinten']['ops'])==2
    for n in ['Staender_Blechschuerze_links','Staender_Blechschuerze_rechts']:
        assert sum('09_Griffdurchgang' in o['label'] for o in ds[n]['ops'])==2
    assert any('09_Kabeleinfuehrungsfenster' in o['label'] for o in ds['Schaltschrank_Hohlschale']['ops'])

def test_formula_validation():
    model.check_recipe(model.load_parameters(ROOT/'Parameter.json'))
