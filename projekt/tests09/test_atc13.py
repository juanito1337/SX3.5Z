import math
import pytest
import atc13_modell as m

def test_twelve_tools_no_legacy_obstruction_and_original_travel():
    p=m.load_parameters();ds=m.recipe()
    assert len([d for d in ds if d['name'].startswith('ATC13_BT30_Werkzeug_')])==12
    assert not any(d['name'].startswith(('ATC_Saeulen','ATC_RATTM','ATC_Parkhaube')) for d in ds)
    assert (p['travel_x'],p['travel_y'],p['table_x'],p['table_y'])==(500,200,740,180)
    assert len([d for d in ds if d['name'].startswith('KSS_Fangblech_')])==4

def test_spindle_and_magazine_endpoints_and_empty_park_gripper():
    p=m.load_parameters()
    a=m.atc_report(m.assembly_pose(p,'wechsel'))
    assert a['transfer_holder_gauge_mm']==pytest.approx([0,0,530],abs=1e-7)
    assert a['nominal_spindle_axis_and_face_mm']==pytest.approx([0,0,530])
    a=m.atc_report(m.assembly_pose(p,'park'))
    assert not a['tool_carried']
    assert math.dist(a['gripper_axis_xy_mm'],a['transfer_holder_gauge_mm'][:2])==pytest.approx(60)

def test_no_false_release_and_named_workpiece_limit():
    r=m.atc_report(m.load_parameters())
    assert not r['atc_operational'] and not r['manufacturing_released']
    assert r['pocket_count']==12
    assert r['toolchange_workpiece_limit_mm']>0
    assert r['unrestricted_arbitrary_workpiece_change'] is False

@pytest.mark.parametrize('key,value',[('a13_extend',61),('a13_lift',91),('a13_c',float('nan')),('a13_tool_carried',3),('a13_jaw_open',23)])
def test_invalid_pose_rejected(key,value):
    p=m.load_parameters();p[key]=value
    with pytest.raises(ValueError):m.validate(p)

def test_full_recipe_is_parametric_and_unique():
    p=m.load_parameters();m.check_recipe(p)
    ds=m.recipe()
    assert len({d['id'] for d in ds})==len(ds)
    assert all(d['item_id'] for d in ds)
    assert 'a13_extend' in m.used_parameters(next(d for d in ds if d['name']=='ATC13_Radialschlitten'))

@pytest.mark.parametrize('pose',['park','wechsel'])
def test_lift_motor_and_radial_rails_do_not_block_motion(pose):
    from tools.atc13_pruefen import world_body
    p=m.assembly_pose(m.load_parameters(),pose);ds={d['name']:d for d in m.recipe()}
    pairs=[('Hubplatte','Hubmotor_Bremse_Reserve'),('Hubmast','Hubmotor_Bremse_Reserve')]
    pairs += [('Greifergehaeuse','Radialfuehrung_'+str(t)) for t in (-24,24)]
    for a,b in pairs:
        assert world_body(ds['ATC13_'+a],p).intersect(world_body(ds['ATC13_'+b],p)).Volume()<.01,(pose,a,b)
