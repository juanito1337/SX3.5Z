"""Regression for real return-path gaps; offline evidence, never an NX claim."""
import pytest
import cnc_ansichtsmodell as model
from enclosure_checks03 import body_bounds


@pytest.mark.parametrize('changes', [
    {'stand_d': 1400., 'chip_outlet_y': 600.},
    {'tank_d': 300.},
])
def test_return_cannot_miss_basket_or_tank(changes):
    p = model.load_parameters()
    p.update(changes)
    with pytest.raises(ValueError):
        model.validate(p)


def test_standard_return_layout_remains_valid():
    assert model.validate(model.load_parameters())


@pytest.mark.parametrize('side,bound,wall', [
    ('links', 0, 'enc_left'), ('rechts', 3, 'enc_right'),
])
def test_front_drain_sheet_reaches_side_wall(side, bound, wall):
    v = model.all_values(model.load_parameters())
    d = next(d for d in model.recipe() if d['name'] == 'KSS_Leitblech_'+side+'_vorn')
    assert body_bounds(d, v, model.evaluate)[bound] == pytest.approx(v[wall])


def test_service_cover_removal_includes_its_handle_and_fasteners():
    ds = model.recipe()
    removed = {d['name'] for d in ds if d.get('service_removal_group') == 'KSS_RUECKKLAPPE'}
    assert removed == {'KSS_Serviceklappe_hinten', 'Servicegriff_KSS',
                       'Griff_Hinterlegung_KSS', 'Griffscheibe_KSS1',
                       'Griffscheibe_KSS2', 'Griffschraube_KSS1', 'Griffschraube_KSS2'}


def test_kss_sheet_manufacturing_is_not_default_milled_s355():
    import umbau_daten09 as data
    p = model.load_parameters()
    rows = {r['name']: r for r in data.manufacturing_rows(model.recipe(), p, model)}
    for name in ('KSS_Tank_Entwurf', 'KSS_Tankdeckel', 'KSS_Ruecklaufkasten_Stirnwand'):
        assert 'Blech' in rows[name]['process']
        assert 'S355' not in rows[name]['material']
