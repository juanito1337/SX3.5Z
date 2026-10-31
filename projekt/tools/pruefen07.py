"""Independent BRep interference screening for changed K07 parts only.
No NX runtime or physical/continuous-motion validation.
"""
from pathlib import Path
import sys,json,itertools,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cadquery as cq
import cnc_ansichtsmodell as m
from ansichtsnetz_erzeugen import fingerprint,make_tool
from enclosure_checks03 import body_bounds
from laengen_und_huellraum import signature
CACHE=ROOT.parent/'brep_cache'
def overlap(a,b):return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-5 for k in range(3))
def run():
 p=m.load_parameters(ROOT/'Parameter.json');v=m.all_values(p);ds=m.recipe();by={d['name']:d for d in ds}
 bbs={d['name']:body_bounds(d,v,m.evaluate) for d in ds};bodies={};comparisons=0
 def body(name):
  if name not in bodies:
   d=by[name];local=m.local_definition(d);path=CACHE/(fingerprint([local,p])+'.brep')
   if path.exists():b=cq.Shape.importBrep(str(path)).translate(tuple(m.evaluate(x,v) for x in d['datum']))
   else:
    b=None
    for o in d['ops']:
     t=make_tool(o,v);b=t if b is None else (b.fuse(t).clean() if o['op']=='add' else b.cut(t).clean())
   bodies[name]=b
  return bodies[name]
 conflicts=[]
 wet=[d for d in ds if d['group']=='17_KSS'];other=[d for d in ds if d['group']!='17_KSS']
 pairs=[(a,b) for a in wet for b in other]+list(itertools.combinations(wet,2))
 for a,b in pairs:
  if not overlap(bbs[a['name']],bbs[b['name']]):continue
  comparisons+=1;vol=body(a['name']).intersect(body(b['name'])).Volume()
  if vol>.01:conflicts.append(dict(a=a['name'],b=b['name'],mm3=vol))
 # Cabinet/closed wall: designed touching faces not counted as interference.
 cabinet=[d for d in ds if d['group']=='16_Schaltschrank']
 for a in cabinet:
  for b in ds:
   if b['group'] not in ('14_Untergestell','15_Einhausung'):continue
   if not overlap(bbs[a['name']],bbs[b['name']]):continue
   comparisons+=1;vol=body(a['name']).intersect(body(b['name'])).Volume()
   if vol>.01:conflicts.append(dict(a=a['name'],b=b['name'],mm3=vol))
 pose_conflicts=[];not_tested=[];poses=list(itertools.product([-p['travel_x']/2,p['travel_x']/2],[-p['travel_y']/2,p['travel_y']/2],[0,p['z_travel_used']]))
 for pose in poses:
  vv=m.all_values(dict(p,pos_x=pose[0],pos_y=pose[1],head_down=pose[2]))
  for a in [d for d in ds if int(d['group'][:2])<=13]:
   if signature(a,vv)!=signature(a,v):
    if a['name'] not in not_tested:not_tested.append(a['name'])
    continue
   delta=[m.evaluate(x,vv)-m.evaluate(x,v) for x in a['datum']];aa=[x+delta[k%3] for k,x in enumerate(bbs[a['name']])]
   for b in wet:
    if not overlap(aa,bbs[b['name']]):continue
    comparisons+=1;vol=body(a['name']).translate(tuple(delta)).intersect(body(b['name'])).Volume()
    if vol>.01:pose_conflicts.append(dict(pose=pose,a=a['name'],b=b['name'],mm3=vol))
 # Removal envelope: rear cover removed, basket subassembly rigid +Y.
 movable=[d for d in wet if d.get('service_translation')];extracted={d['name'] for d in movable}|{'KSS_Serviceklappe_hinten'}
 service_conflicts=[]
 for stroke in (0,55,110,165,220):
  for a in movable:
   aa=[x+(stroke if k%3==1 else 0) for k,x in enumerate(bbs[a['name']])]
   for b in ds:
    if b['name'] in extracted or not overlap(aa,bbs[b['name']]):continue
    comparisons+=1;vol=body(a['name']).translate((0,stroke,0)).intersect(body(b['name'])).Volume()
    if vol>.01:service_conflicts.append(dict(stroke_mm=stroke,a=a['name'],b=b['name'],mm3=vol))
 r=dict(native_nx_executed=False,method='Independent OpenCascade solid intersection after analytic AABB screen',exact_comparisons=comparisons,
        static_conflicts=conflicts,axis_poses_checked=len(poses),axis_pose_conflicts=pose_conflicts,nonrigid_parts_not_swept=not_tested,
        basket_strokes_mm=[0,55,110,165,220],basket_conflicts=service_conflicts,
        limits='Changed KSS vs drawn parts and cabinet vs stand/enclosure. Known original machine conflicts unchanged. Weld/contact tolerances, continuous motion, chip/fluid transport, strength, seals and safety not proven.')
 (ROOT/'Dokumentation/K07_Kollisionen.json').write_text(json.dumps(r,indent=2,ensure_ascii=False))
 print(json.dumps(r,indent=2,ensure_ascii=False),flush=True)
 if conflicts or pose_conflicts or service_conflicts:raise RuntimeError('K07 changed-geometry conflicts; see report')
 return r
if __name__=='__main__':run()
