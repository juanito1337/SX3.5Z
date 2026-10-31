"""Reproduce axial envelope arithmetic and translation-only cell AABB screening.
Not a collision proof for the casting, bearings, cables or moving bellows.
Reads independent geometry bounds. Does not create or test NX parts.
"""
from pathlib import Path
import json,sys,itertools,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model

def signature(d,v):
 out=[]
 for op in model.local_definition(d)['ops']:
  fields=[]
  for key in ('origin','size','direction','points','diameter','top_diameter','height'):
   if key not in op:continue
   def num(x):
    if isinstance(x,(list,tuple)):return tuple(num(i) for i in x)
    return round(model.evaluate(x,v),7)
   fields.append((key,num(op[key])))
  out.append(tuple(fields))
 return tuple(out)

def run():
 p=model.load_parameters(ROOT/'Parameter.json');v=model.all_values(p)
 q=dict(p);q.update(cnc_x_extra_l=0.,cnc_z_extra_l=0.)
 data=dict(note='Axiale Hüllrechnung; keine Bestelllängen oder Freigabe. Gegenstück, Führungsüberdeckung und Kontakt fehlen.',old=model.length_report(q),new=model.length_report(p))
 dest=ROOT/'Dokumentation';(dest/'Spindellaengen.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 geometry=json.loads((dest/'Geometrie/Geometriepruefung.json').read_text());bounds={p['name']:p['bounds_world_mm'] for p in geometry['parts']}
 limits=[v['enc_left']+v['sheet_t']+v['window_t'],v['enc_front']+40,0,v['enc_right']-v['sheet_t'],v['enc_back']-v['sheet_t'],v['enclosure_h']]
 poses=list(itertools.product([-p['travel_x']/2,p['travel_x']/2],[-p['travel_y']/2,p['travel_y']/2],[0,p['z_travel_used']]))
 checks=[];skipped=[]
 for d in model.recipe():
  if int(d['group'][:2])>13:continue
  sig=signature(d,v);origin=[model.evaluate(x,v) for x in d['datum']];bb=bounds[d['name']];worst=float('inf');bad=[];valid=True
  for px,py,h in poses:
   pp=dict(p,pos_x=px,pos_y=py,head_down=h);vv=model.all_values(pp)
   if signature(d,vv)!=sig:valid=False;break
   delta=[model.evaluate(x,vv)-origin[i] for i,x in enumerate(d['datum'])]
   moved=[bb[i]+delta[i%3] for i in range(6)]
   margins=[moved[k]-limits[k] for k in range(3)]+[limits[k+3]-moved[k+3] for k in range(3)]
   worst=min(worst,*margins)
   if min(margins)<-1e-5:bad.append(dict(pose=[px,py,h],margins_mm=margins))
  if not valid:skipped.append(dict(name=d['name'],reason='local_shape_changes_with_pose_not_translation_only'));continue
  checks.append(dict(name=d['name'],minimum_aabb_wall_margin_mm=round(worst,3),violations=bad))
 result=dict(native_nx_executed=False,note='Only rigid translations at eight parameter-range corners; no collision or containment proof for flexible/omitted/real components. Casting interferences remain.',interior_limits_mm=limits,target_ranges_mm=dict(X=poses[0][0],Xmax=p['travel_x']/2,Ymin=-p['travel_y']/2,Ymax=p['travel_y']/2,Zhead_down=[0,p['z_travel_used']]),checks=checks,not_checked=skipped)
 (dest/'Einhausung_Huellraumpruefung.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 print('checked',len(checks),'skipped',len(skipped),'with_violations',sum(bool(r['violations']) for r in checks))
 for x in checks:
  if x['violations']:print(x['name'],x['minimum_aabb_wall_margin_mm'])
 return result
if __name__=='__main__':run()
