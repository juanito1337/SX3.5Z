"""Exact solid intersection screening of added09 bodies against all model bodies.
Static view only, no threads/contact stress/safety proof. Touching faces not a collision.
"""
from pathlib import Path
import sys,json,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cnc_ansichtsmodell as m
from atc_anschlusspruefung09 import world_body,overlaps

def run(cache=None):
    p=m.load_parameters(ROOT/'Parameter.json');ds=m.recipe();bs={d['name']:world_body(d,p,cache) for d in ds}
    new={d['name'] for d in ds if d.get('revision_added')=='09'}
    checks=0;broad=0;hits=[]
    for i,a in enumerate(ds):
        for b in ds[i+1:]:
            if a['name'] not in new and b['name'] not in new:continue
            checks+=1
            ba,bb=bs[a['name']],bs[b['name']]
            if not overlaps(ba,bb):continue
            broad+=1;v=ba.intersect(bb).Volume()
            if v>.01:hits.append(dict(a=a['name'],b=b['name'],volume_mm3=round(v,6)))
    return dict(scope='Added09 bodies vs all bodies in default pose; no movement sweep, no strength or tolerance proof',native_nx_executed=False,pair_count=checks,solid_intersection_checks=broad,collisions=hits)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--cache');a=ap.parse_args();r=run(a.cache)
    (ROOT/'Pruefung_09/Normteile_Anschlusspruefung.json').write_text(json.dumps(r,indent=2))
    print({k:v for k,v in r.items() if k!='collisions'});print(json.dumps(r['collisions'],indent=2))
