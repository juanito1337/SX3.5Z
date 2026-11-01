"""Independent kernel checks, NOT Siemens NX tests. Every operation must act on one solid."""
import sys,os
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cnc_ansichtsmodell as model
from ansichtsnetz_erzeugen import make_tool

def test_first_service_handle_is_connected_after_each_addition():
    v=model.all_values(model.load_parameters(ROOT/'Parameter.json'))
    raw=next(d for d in model.recipe() if d['name']=='Servicegriff_links')
    d=model.local_definition(raw);shape=None
    for op in d['ops']:
        tool=make_tool(op,v)
        shape=tool if shape is None else shape.fuse(tool).clean() if op['op']=='add' else shape.cut(tool).clean()
        assert len(shape.Solids())==1, op['label']
        assert shape.isValid()

def test_carousel_head_screen_reports_scope_and_exclusions():
    from teller_pruefung10 import run
    result=run(os.environ.get('SX35Z_GEOMETRY_CACHE'))
    assert not result['collisions'], result['collisions'][:3]
    assert result['trajectory_verified'] is False
    assert result['excluded_selected_stock_spindle_joint'] is True


@pytest.mark.parametrize('raw',[d for d in model.recipe() if d.get('revision_added') in ('10','11')],ids=lambda d:d['name'])
def test_new_study_parts_are_single_valid_solids(raw):
    v=model.all_values(model.load_parameters(ROOT/'Parameter.json'))
    shape=None
    for op in model.local_definition(raw)['ops']:
        tool=make_tool(op,v)
        before=shape.Volume() if shape is not None else 0
        shape=tool if shape is None else shape.fuse(tool).clean() if op['op']=='add' else shape.cut(tool).clean()
        assert shape.isValid() and len(shape.Solids())==1,op['label']
        assert abs(shape.Volume()-before)>1e-6,op['label']
