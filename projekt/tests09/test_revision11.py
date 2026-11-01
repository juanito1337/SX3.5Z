import pytest
import cnc_ansichtsmodell as m
from enclosure_checks03 import body_bounds


def test_original_external_equipment_is_removed_but_core_retained():
    ds = {d['name']:d for d in m.recipe()}
    assert 'Bediengehaeuse_Hohlschale' not in ds
    assert 'Spindelschutz_oben' not in ds
    assert 'Riemenabdeckung_Blech' not in ds
    assert not any(d['group'] in {'07_Bedienpanel','08_Blechsaeule','09_Elektrik'} for d in ds.values())
    for name in ['Faltenbalg_Z','Faltenbalg_Y_hinten','Spindelkopf_Guss_Detail','W92_1000F_Gehaeuse_Rippen','Bedienpult_Aussen_Reserve']:
        assert name in ds


def test_right_magazine_and_actual_change_pose_reach_spindle():
    p=m.load_parameters(); assert m.all_values(p)['teller_park_x']>0
    q=m.assembly_pose(p,'wechsel');v=m.check_recipe(q)
    d=next(d for d in m.recipe() if d['name']=='ATC_BT30_ER20_70_Raumhuelle_1')
    xyz=[m.evaluate(x,v) for x in d['ops'][-1]['origin']]
    assert xyz==pytest.approx([0,0,v['spindle_face_z']],abs=1e-8)
    assert p['teller_feed']==0
    with pytest.raises(ValueError):m.assembly_pose(p,'typo')


def test_four_side_catch_sheets_slope_to_open_rear_outlet():
    p=m.load_parameters();v=m.all_values(p)
    sheets=[d for d in m.recipe() if d['name'].startswith('KSS_Fangblech_')]
    assert len(sheets)==4
    for d in sheets:
        bb=body_bounds(d,v,m.evaluate)
        assert bb[3]<0 if 'links' in d['name'] else bb[0]>0
        pts=[[m.evaluate(x,v) for x in pt] for pt in d['ops'][0]['points']]
        assert pts[0][2]>pts[3][2]
        assert d['supply_kind']=='MAKE'
        assert d['plate_normal_thickness']=='sheet_t'


def test_old_left_tray_has_no_false_support_cut():
    ds={d['name']:d for d in m.recipe()}
    for side,expected in [('links',False),('rechts',False)]:
        assert any(o.get('label')=='ATC_Stuetzendurchfuehrung' for o in ds['KSS_Leitblech_'+side+'_vorn']['ops']) is expected


def test_chip_catch_parameters_reject_missing_slope_and_too_high():
    p=m.load_parameters()
    for key,value in [('catch_slope',0),('catch_z',150)]:
        q=dict(p);q[key]=value
        with pytest.raises(ValueError):m.validate(q)


def test_park_forks_do_not_intersect_hood():
    from tools.atc_anschlusspruefung09 import world_body
    p=m.load_parameters();ds={d['name']:d for d in m.recipe()}
    fork=world_body(ds['ATC_Gabel_Raumreserve_5'],p)
    hood=world_body(ds['ATC_Parkhaube_Ruecken_Entwurf'],p)
    assert fork.intersect(hood).Volume()<.01
