"""Offline head-screen at eight indexed pickup endpoints; NOT a full ATC proof."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cnc_ansichtsmodell as m
from atc_anschlusspruefung09 import world_body,overlaps


def run(cache=None):
    p=m.load_parameters(ROOT/'Parameter.json');defs=m.recipe();v=m.all_values(p)
    p['teller_feed']=1.
    p['head_down']=v['spindle_face_z']+p['head_down']-p['teller_gauge_z']
    names={'Spindelkopf_Guss_Detail','Kopf_Frontplatte_Detail','Pinole_Huelse_Detail'}
    heads={d['name']:world_body(d,p,cache) for d in defs if d['name'] in names}
    moving=[d for d in defs if d['group']=='20_ATC_Option' and not d['name'].startswith('Spannpaket_')]
    checks=[];hits=[]
    # Symmetric magazine: rotate all fork/holder positions, inspect every selected pocket.
    for i in range(8):
        p['teller_index_cos']=math.cos(-i*math.pi/4)
        p['teller_index_sin']=math.sin(-i*math.pi/4)
        for d in moving:
            if d['name']=='ATC_BT30_ER20_70_Raumhuelle_'+str(i+1):continue
            shape=world_body(d,p,cache)
            for name,head in heads.items():
                volume=head.intersect(shape).Volume() if overlaps(head,shape) else 0.
                checks.append(dict(pocket=i+1,head=name,part=d['name'],intersection_mm3=round(volume,6)))
                if volume>.01:hits.append(checks[-1])
    return dict(native_nx_executed=False,trajectory_verified=False,
        excluded_selected_stock_spindle_joint=True,
        scope='8 indexed pickup endpoints against stock casting/front plate/quill only. Selected holder/stock joint, guards, replacement spindle, workpieces, full motion, structural strength and clamping not validated.',
        checks=checks,collisions=hits)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    result=run();Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf8')
    print('Checks:',len(result['checks']),'collisions:',len(result['collisions']))
    if result['collisions']:raise SystemExit(1)
