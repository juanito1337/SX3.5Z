"""Behavioral requirements for the table-independent carousel study."""
import copy
import math
import pytest
import cnc_ansichtsmodell as model


def test_magazine_is_independent_of_table_xy():
    parts = [d for d in model.recipe() if d['group'] == '20_ATC_Option']
    assert parts
    for d in parts:
        assert not ({'pos_x', 'pos_y'} & model.used_parameters(d)), d['name']
    assert not any(d['name'] == 'ATC_Grundplatte' for d in parts)


def test_all_indexed_pockets_reach_fixed_spindle_without_table_motion():
    p = model.load_parameters()
    r = model.atc_report(p)
    assert r.get('layout') == 'RADIAL_TELESCOPIC_CAROUSEL'
    assert r['reserved_table_strip_mm'] == [0, 0]
    assert len(r['pockets']) == 8
    for pocket in r['pockets']:
        assert pocket['pickup_axis_xy_mm'] == pytest.approx([0, 0], abs=1e-9)
    assert r['required_feed_mm'] == pytest.approx(419.33296255)
    assert not r['spindle_clamping_verified']
    assert not r['trajectory_verified']


def test_clamping_package_remains_explicit_unverified_geometry():
    ds = [d for d in model.recipe() if d['name'].startswith('Spannpaket_')]
    assert len(ds) >= 2
    assert all(d['supply_kind'] == 'RESERVE' for d in ds)
    r = model.atc_report(model.load_parameters())
    assert r['original_spindle'] == 'SK30/M12 DIN2080'
    assert r['clamping_package_required'] is True
    assert r['machine_operation_enabled'] is False


@pytest.mark.parametrize('key,value', [('teller_feed', 1.1), ('teller_radius', 50.),
                                      ('teller_gauge_z', 600.), ('teller_feed', True)])
def test_invalid_carousel_layout_is_rejected(key, value):
    p = model.load_parameters()
    p[key] = value
    with pytest.raises(ValueError):
        model.validate(p)


def test_support_penetration_has_real_cut_and_separate_collar():
    ds = {d['name']: d for d in model.recipe()}
    assert 'ATC_KSS_Dichtkragen_Entwurf' in ds
    assert any(o['op'] == 'cut' and o['label'] == 'ATC_Stuetzendurchfuehrung'
               for o in ds['KSS_Leitblech_links_vorn']['ops'])


def test_original_castings_and_stock_spindle_are_retained():
    import cnc_ansichtsmodell08 as old
    ds = {d['name']: d for d in model.recipe()}
    for d in old.recipe():
        if 'Guss' in d['name'] or d['name'].startswith('Spindelnase_') or 'door_leaf' in d:
            assert ds[d['name']]['ops'] == d['ops']


def test_actual_indexed_tool_geometry_reaches_spindle_axis():
    ds={d['name']:d for d in model.recipe()}
    for i in range(8):
        p=model.load_parameters()
        p.update(teller_feed=1.,teller_index_cos=math.cos(-i*math.pi/4),
                 teller_index_sin=math.sin(-i*math.pi/4))
        v=model.all_values(p)
        tool=ds['ATC_BT30_ER20_70_Raumhuelle_'+str(i+1)]
        xy=[model.evaluate(q,v) for q in tool['ops'][0]['origin'][:2]]
        assert xy==pytest.approx([0,0],abs=1e-8)


def test_current_export_preserves_historical_reports(tmp_path):
    import shutil,json
    from pathlib import Path
    import umbau_daten09 as data
    root=Path(__file__).resolve().parents[1]
    for relative in ('Parameter.json','CNC_Parameter.json','Ausbau_Parameter.json',
                     'Detail_Parameter_09.json','Teller_Parameter_10.json',
                     'Einkauf/Kaufteile_09.json','Aufmass/Messwerte_08.json',
                     'Aufmass/Messwerte_09_Zusatz.json','Pruefung_08/Freigaben.json'):
        dest=tmp_path/relative;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(root/relative,dest)
    for name in ('Pruefung_09','Werkzeugwechsler'):(tmp_path/name).mkdir(exist_ok=True)
    old=tmp_path/'Pruefung_09/Freigabestatus_09.json'
    old.write_text('HISTORISCH',encoding='utf8')
    data.export(tmp_path)
    assert old.read_bytes()==b'HISTORISCH'
    assert (tmp_path/'Einkauf/Modellzuordnung_10.csv').exists()
    assert (tmp_path/'Werkzeugwechsler/ATC_Schnittstellenstatus_10.json').exists()


def test_raised_gauge_keeps_park_roof_above_stored_tool_reserve():
    from enclosure_checks03 import body_bounds
    p=model.load_parameters();p['teller_gauge_z']=420.
    v=model.check_recipe(p)
    roof=next(d for d in model.recipe() if d['name']=='ATC_Parkhaube_Dach_Entwurf')
    lowest=body_bounds(roof,v,model.evaluate)[2]
    assert lowest>=420.+48.4+30.+10.


def test_collar_cannot_end_below_the_wet_tray():
    p=model.load_parameters();p['teller_collar_top']=65.
    with pytest.raises(ValueError,match='Kragen'):
        model.check_recipe(p)
