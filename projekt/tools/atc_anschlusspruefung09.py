"""Conservative subset checks for proposed table magazine against retained head.
Does NOT prove compatibility with a future replacement spindle or a toolchange trajectory.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cnc_ansichtsmodell as m
from ansichtsnetz_erzeugen import make_tool,fingerprint

def world_body(raw,p,cache=None):
    import cadquery as cq
    d=m.local_definition(raw);v=m.all_values(p)
    cp=Path(cache or '/nonexistent')/(fingerprint([d,p])+'.brep')
    if cp.exists():b=cq.Shape.importBrep(str(cp))
    else:
        b=None
        for op in d['ops']:
            t=make_tool(op,v);b=t if b is None else b.fuse(t).clean() if op['op']=='add' else b.cut(t).clean()
    return b.translate(tuple(m.evaluate(q,v) for q in raw['datum']))

def overlaps(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    return all(min(getattr(aa,k+'max'),getattr(bb,k+'max'))>max(getattr(aa,k+'min'),getattr(bb,k+'min'))+1e-5 for k in 'xyz')

def run(cache=None):
    p=m.load_parameters(ROOT/'Parameter.json');v=m.all_values(p);defs=m.recipe();reach=m.atc_report(p)
    names=['Spindelkopf_Guss_Detail','Kopf_Frontplatte_Detail','Pinole_Huelse_Detail']
    hs={d['name']:world_body(d,p,cache) for d in defs if d['name'] in names}
    ds=[d for d in defs if d['group']=='20_ATC_Option'];bs={d['name']:world_body(d,p,cache) for d in ds}
    checks=[];hits=[]
    for pose in reach['pockets']:
        dz=pose['required_gauge_z_mm']-v['spindle_face_z'];dx=pose['required_pos_x_mm']-p['pos_x'];dy=pose['required_pos_y_mm']-p['pos_y']
        for hn,h in hs.items():
            head=h.translate((0,0,dz))
            for d in ds:
                # Selected holder intentionally enters the original spindle envelope;
                # that incompatible joint is NOT tested or claimed here.
                if d['name']=='ATC_BT30_ER20_70_Raumhuelle_'+str(pose['pocket']):continue
                t=bs[d['name']].translate((dx,dy,0));vol=head.intersect(t).Volume() if overlaps(head,t) else 0
                if vol>.01:hits.append(dict(pocket=pose['pocket'],head=hn,part=d['name'],volume_mm3=vol))
                checks.append(dict(pocket=pose['pocket'],head=hn,part=d['name'],intersection_mm3=round(vol,6)))
    return dict(native_nx_executed=False,scope='6 pick-up endpoints; head casting/front plate/quill vs magazine except selected holder. NO full path, guards, workpiece, spindle-joint or replacement-head proof.',checks=checks,collisions=hits)
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--cache',default=None);args=ap.parse_args()
    out=run(args.cache)
    (ROOT/'Pruefung_09/ATC_Endpunktpruefung.json').write_text(json.dumps(out,indent=2))
    print('checks',len(out['checks']),'collisions',len(out['collisions']))
    print(json.dumps(out['collisions'][:8],indent=2))
