"""Self-contained Canvas 2D software viewer of the analytic NX recipe.
No WebGL/network/browser libraries required. This view is NOT an NX export.
"""
import sys,json,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model

def build(meshfile,output):
    meshes=json.loads(Path(meshfile).read_text(encoding='utf8'))
    params=model.load_parameters(ROOT/'Parameter.json');values=model.all_values(params)
    definitions={d['name']:d for d in model.recipe()}
    for m in meshes:
        m['rgb']=[int(255*x) for x in model.PALETTE[m['material']][:3]]
        leaf=definitions[m['name']].get('door_leaf')
        m['doorShiftZ']=model.evaluate(definitions[m['name']]['door_shift_z'],values) if leaf else 0

    template=Path(__file__).with_name('viewer_template.html').read_text(encoding='utf8')
    template=template.replace('__PART_COUNT__',str(len(meshes))).replace('__GROUP_COUNT__',str(len(set(m['group'] for m in meshes))))
    template=template.replace('/*DOOR_REFERENCE*/',str(params['door_open']))
    template=template.replace('/*MODEL_DATA*/',json.dumps(meshes,separators=(',',':')))
    template=template.replace('/*GROUP_NAMES*/',json.dumps(model.GROUPS,ensure_ascii=False))
    Path(output).write_text(template,encoding='utf8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mesh',required=True);p.add_argument('--output',required=True);a=p.parse_args();build(a.mesh,a.output)
