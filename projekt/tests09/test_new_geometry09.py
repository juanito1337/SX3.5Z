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

def test_magazine_does_not_intersect_retained_head_at_six_pick_endpoints():
    from atc_anschlusspruefung09 import run
    result=run(os.environ.get('SX35Z_GEOMETRY_CACHE'))
    assert not result['collisions'], result['collisions'][:3]
