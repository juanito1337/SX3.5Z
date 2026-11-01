"""Selected BT30 layout: reach and mounting, not spindle fit certification."""
import math
import pytest
import cnc_ansichtsmodell as m


def test_selected_product_image_dimensions_and_short_feed():
    p=m.load_parameters(); r=m.atc_report(p)
    assert r['required_feed_mm']==pytest.approx(200.)
    assert r['selected_product']=='1005009887984460'
    assert r['selected_interface']=='BT30'
    assert p['atc12_disc_d']==280 and p['teller_plate_t']==16
    assert [p[k] for k in ('atc12_base_l','atc12_base_w','atc12_base_t')]==[330,175,22]
    assert not r['supplier_geometry_verified']
    assert not r['spindle_clamping_verified']


def test_stationary_column_console_and_closed_wet_tray():
    ds={d['name']:d for d in m.recipe()}
    assert 'ATC_Saeulenanschluss_Entwurf' in ds
    assert 'ATC_Standstuetze_Entwurf' not in ds
    assert 'ATC_KSS_Dichtkragen_Entwurf' not in ds
    for side in ('links','rechts'):
        assert not any(o['label']=='ATC_Stuetzendurchfuehrung' for o in ds['KSS_Leitblech_'+side+'_vorn']['ops'])
    for name in ('ATC_Saeulenanschluss_Entwurf','ATC_Saeulenkonsole_Entwurf'):
        assert not ({'head_down','pos_x','pos_y','teller_feed'} & m.used_parameters(ds[name]))
    assert len([d for d in ds.values() if d['name'].startswith('KSS_Fangblech_')])==4


def test_feed_moves_actual_tool_axis_two_hundred_mm_without_table():
    ds={d['name']:d for d in m.recipe()};tool=ds['ATC_BT30_ER20_70_Raumhuelle_1']
    p=m.load_parameters();q=m.assembly_pose(p,'wechsel')
    def axis(params):
        v=m.all_values(params)
        return [m.evaluate(x,v) for x in tool['ops'][-1]['origin']]
    a,b=axis(p),axis(q)
    assert math.dist(a[:2],b[:2])==pytest.approx(200.)
    assert b==pytest.approx([0,0,m.all_values(q)['spindle_face_z']],abs=1e-8)


@pytest.mark.parametrize('key,value',[('atc12_stroke',0),('atc12_base_l',300),('atc12_disc_d',310),('teller_plate_t',10)])
def test_unreviewed_product_dimensions_rejected(key,value):
    p=m.load_parameters();p[key]=value
    with pytest.raises(ValueError):m.validate(p)


def test_console_and_magazine_clear_sampled_machine_motion():
    from tools.wechselweg12_pruefen import run
    result=run()
    assert not result['collisions'],result['collisions'][:8]
    assert result['park_axis_samples']==8
    assert result['trajectory_verified'] is False
    assert result['supplier_internal_fit_verified'] is False


def test_console_contacts_actual_column_wall_not_only_foot_bounds():
    from tools.atc_anschlusspruefung09 import world_body
    ds={d['name']:d for d in m.recipe()}
    for width in (138.,148.):
        p=m.load_parameters();p['column_x']=width
        casting=world_body(ds['Saeule_Guss_Foto'],p)
        plate=world_body(ds['ATC_Saeulenanschluss_Entwurf'],p)
        arm=world_body(ds['ATC_Saeulenkonsole_Entwurf'],p)
        assert plate.distance(casting)<1e-6
        assert len(plate.fuse(casting).Solids())==1
        assert len(plate.fuse(arm).Solids())==1
        assert plate.intersect(casting).Volume()<.01


def test_fork_root_remains_attached_to_smaller_disc_envelope():
    from tools.atc_anschlusspruefung09 import world_body
    ds={d['name']:d for d in m.recipe()}
    for radius in (180.,185.):
        p=m.load_parameters();p['teller_radius']=radius
        fork=world_body(ds['ATC_Gabel_Raumreserve_1'],p)
        disc=world_body(ds['ATC_RATTM_Tellerscheibe_Bildmasse'],p)
        assert len(fork.fuse(disc).Solids())==1
        assert fork.intersect(disc).Volume()>1.
