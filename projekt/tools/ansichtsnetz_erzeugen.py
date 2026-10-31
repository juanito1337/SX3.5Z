"""Optional independent tessellation/check, NOT a replacement for the NX journal.
Requires CadQuery+Plotly in a separate normal Python environment. Not needed in NX.
No native .prt is generated here. The shared analytic recipe is unchanged.
"""
import sys,json,time,math,hashlib,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model

def fingerprint(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()

def make_tool(op,values):
    import cadquery as cq
    ev=lambda x:model.evaluate(x,values)
    o=cq.Vector(*[ev(x) for x in op['origin']])
    if op['kind']=='box':return cq.Solid.makeBox(*[ev(x) for x in op['size']],pnt=o)
    axis=cq.Vector(*op['direction']);h=ev(op['height'])
    if op['kind']=='cylinder':return cq.Solid.makeCylinder(ev(op['diameter'])/2,h,o,axis)
    if op['kind']=='cone':return cq.Solid.makeCone(ev(op['diameter'])/2,ev(op['top_diameter'])/2,h,o,axis)
    if op['kind']=='prism':
        pts=[cq.Vector(*[ev(x) for x in p]) for p in op['points']]
        return cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts+[pts[0]]),[],axis.multiply(h))
    raise ValueError('Unknown primitive: '+op['kind'])

def build(output,cache):
    import cadquery as cq
    output=Path(output);cache=Path(cache);output.mkdir(parents=True,exist_ok=True);cache.mkdir(parents=True,exist_ok=True)
    p=model.load_parameters(ROOT/'Parameter.json');v=model.check_recipe(p);defs=model.recipe()
    report=dict(schema='CNC_VIEW_INDEPENDENT_GEOMETRY_CHECK',native_nx_executed=False,
                parameter_sha256=fingerprint(p),recipe_sha256=fingerprint(defs),parts=[],failures=[])
    meshes=[];bodies={};start=time.monotonic()
    for raw in defs:
        d=model.local_definition(raw);sig=fingerprint([d,p]);cp=cache/(sig+'.brep');rp=cache/(sig+'.json');body=None;rows=[]
        if cp.exists() and rp.exists():
            body=cq.Shape.importBrep(str(cp));rows=json.loads(rp.read_text())
        else:
            for i,op in enumerate(d['ops'],1):
                tool=make_tool(op,v);before=body.Volume() if body else 0
                if body is None:body=tool
                elif op['op']=='add':body=body.fuse(tool).clean()
                else:body=body.cut(tool).clean()
                after=body.Volume();delta=after-before;valid=body.isValid();solids=len(body.Solids())
                row=dict(n=i,kind=op['kind'],operation=op['op'],label=op['label'],before=before,after=after,delta=delta,valid=valid,solids=solids)
                rows.append(row)
                if not valid or solids!=1 or abs(delta)<1e-6:
                    report['failures'].append(dict(id=d['id'],name=d['name'],row=row))
                    print('ERROR',d['name'],row,flush=True)
                    (output/'Geometriepruefung.json').write_text(json.dumps(report,indent=2),encoding='utf8')
                    raise RuntimeError('Invalid/no-op geometry in '+d['name']+' '+op['label'])
            body.exportBrep(str(cp));rp.write_text(json.dumps(rows),encoding='utf8')
        datum=[model.evaluate(x,v) for x in raw['datum']];world=body.translate(tuple(datum));bodies[d['name']]=world
        bb=world.BoundingBox()
        pts,tris=world.tessellate(0.35,0.27)
        vertices=[[round(t.x,4),round(t.y,4),round(t.z,4)] for t in pts]
        meshes.append(dict(id=d['id'],name=d['name'],group=d['group'],material=d['material'],status=d['status'],vertices=vertices,triangles=tris))
        report['parts'].append(dict(id=d['id'],name=d['name'],group=d['group'],rows=rows,volume_mm3=body.Volume(),bounds_world_mm=[bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax]))
        print('OK',d['id'],d['name'],len(rows),len(tris),flush=True)
        (output/'Geometriepruefung.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    checks=[]
    for axis,targets in [('X',['Arbeitstisch_Foto','Kreuzschlitten_Guss_Detail']),('Y',['Basis_Guss_Foto','Kreuzschlitten_Guss_Detail']),('Z',['Saeule_Guss_Foto','Spindelkopf_Guss_Detail','Blechsaeule_Stirnblech_oben'])]:
        for part in ['Mutteraufnahme_Entwurf','Anschlussplatte_Entwurf','Motor_Gehaeuse','Kugelspindel_Huelle']:
            name='CNC_'+axis+'_'+part
            for target in targets:
                a,b=bodies[name],bodies[target]
                aa,bb=a.BoundingBox(),b.BoundingBox()
                overlap=all(min(getattr(aa,k+'max'),getattr(bb,k+'max'))>max(getattr(aa,k+'min'),getattr(bb,k+'min'))+1e-5 for k in 'xyz')
                vol=a.intersect(b).Volume() if overlap else 0.0
                checks.append(dict(component=name,casting=target,intersection_mm3=round(vol,4),status='MODEL_INTERSECTION_REQUIRES_REDESIGN' if vol>0.01 else 'NO_STATIC_OVERLAP_IN_THIS_CHECK'))
    (output/'Statische_Anschlusskonflikte.json').write_text(json.dumps(dict(note='Statische Auswahlpruefung der Rekonstruktion, NICHT reale Maschine oder Verfahrweg. Keine Freigabe.',checks=checks),indent=2),encoding='utf8')
    report.update(part_count=len(defs),operation_count=sum(len(x['rows']) for x in report['parts']),elapsed_seconds=round(time.monotonic()-start,3),triangle_count=sum(len(x['triangles']) for x in meshes))
    (output/'Geometriepruefung.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    (output/'Ansichtsnetz.json').write_text(json.dumps(meshes,separators=(',',':')),encoding='utf8')
    (ROOT/'Geometrie_Referenz_Ansicht.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--cache',required=True);args=parser.parse_args()
    print(json.dumps({k:v for k,v in build(args.output,args.cache).items() if k not in ('parts','failures')},indent=2))
