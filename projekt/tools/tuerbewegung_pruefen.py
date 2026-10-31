"""Independent sampled solid test of door motion, including stand, KSS and floor.
Not native NX, not a continuous-motion or safety validation.
"""
from pathlib import Path
import sys,json,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cnc_ansichtsmodell as m
from enclosure_checks03 import body_bounds
from ansichtsnetz_erzeugen import make_tool

def motion_delta(d,v,q):
 return (0.,0.,m.evaluate(d.get('door_shift_z','0'),v)*q)

def overlap(a,b):return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-6 for k in range(3))

def run():
 p=m.load_parameters(ROOT/'Parameter.json');p['door_open']=0.;v=m.all_values(p);ds=m.recipe()
 moving=[d for d in ds if d.get('door_leaf')];fixed=[d for d in ds if not d.get('door_leaf')]
 bounds={d['name']:body_bounds(d,v,m.evaluate) for d in ds};bodies={}
 def body(d):
  name=d['name']
  if name not in bodies:
   b=None
   for o in d['ops']:
    t=make_tool(o,v)
    b=t if b is None else (b.fuse(t).clean() if o['op']=='add' else b.cut(t).clean())
   bodies[name]=b
  return bodies[name]
 conflicts=[];count=0;exact=0;states=[i/8 for i in range(9)];floor_min=1e30
 pairs=[(d,e) for d in moving for e in fixed]+[(d,e) for d in moving for e in moving if d['door_leaf']=='LOWER' and e['door_leaf']=='UPPER']
 for q in states:
  shifts={d['name']:motion_delta(d,v,q) for d in moving}
  moved_bounds={d['name']:[x+shifts[d['name']][i%3] for i,x in enumerate(bounds[d['name']])] for d in moving}
  floor_min=min(floor_min,*(b[2]+p['stand_h'] for b in moved_bounds.values()))
  moved={}
  def at(d):
   if not d.get('door_leaf'):return body(d)
   if d['name'] not in moved:moved[d['name']]=body(d).translate(shifts[d['name']])
   return moved[d['name']]
  for d,e in pairs:
   count+=1
   aa=moved_bounds[d['name']];bb=moved_bounds[e['name']] if e.get('door_leaf') else bounds[e['name']]
   if not overlap(aa,bb):continue
   exact+=1;vol=at(d).intersect(at(e)).Volume()
   if vol>.01:conflicts.append(dict(door_open=q,a=d['name'],b=e['name'],intersection_mm3=vol))
 result=dict(native_nx_executed=False,method='OpenCascade solid intersections after conservative AABB screening',
  positions=states,pairs_checked=count,solid_comparisons=exact,conflicts=conflicts,
  minimum_moving_part_floor_clearance_mm=floor_min,
  limits='Nine samples. All drawn stationary model parts vs moving door; cross-segment pairs included. Intra-segment assembly/contact excluded. No continuous path, actual hardware, tolerances, deformation, seal, drainage or safety proof.')
 path=ROOT/'Dokumentation/Tuerbewegung_Stichproben.json';path.write_text(json.dumps(result,indent=2,ensure_ascii=False));print(json.dumps(result,indent=2))
 if conflicts or floor_min<0:raise RuntimeError('Tuerkonflikte oder Bodendurchtritt, siehe Bericht')
 return result
if __name__=='__main__':run()
