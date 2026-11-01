"""Independent offline CAD geometry and swept-placement checks for concept13."""
import sys,math,itertools,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import atc13_modell as m
from ansichtsnetz_erzeugen import make_tool
from enclosure_checks03 import body_bounds

def world_body(d,p,trace=False):
    v=m.all_values(p);local=m.local_definition(d);b=None
    for op in local['ops']:
        tool=make_tool(op,v)
        b=tool if b is None else b.fuse(tool).clean() if op['op']=='add' else b.cut(tool).clean()
        if trace and (not b.isValid() or len(b.Solids())!=1):raise ValueError((d['name'],op['label'],len(b.Solids())))
    return b.translate(tuple(m.evaluate(x,v) for x in d['datum']))

def overlap(a,b):return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-5 for k in range(3))

def poses(p):
    radius=math.hypot(p['a13_pivot_x'],p['a13_pivot_y']);theta=math.atan2(-p['a13_pivot_y'],-p['a13_pivot_x'])
    for i in range(25):
        a=math.pi/2+(theta-math.pi/2)*i/24
        yield 'low_retracted_swing',dict(p,head_down=0.,a13_c=math.cos(a),a13_s=math.sin(a),a13_tool_carried=1.,a13_jaw_open=0.)
    for ext in (15.,30.,45.,60.):
        for a,label in ((math.pi/2,'magazine_feed'),(theta,'spindle_feed')):
            yield label,dict(p,head_down=0.,a13_c=math.cos(a),a13_s=math.sin(a),a13_extend=ext,a13_tool_carried=1.,a13_jaw_open=0.)
    for lift in (15.,30.,45.,60.,75.,90.):
        yield 'spindle_lift',dict(m.assembly_pose(p,'wechsel'),a13_lift=lift)
    for ext in (0.,15.,30.,45.,60.):
        yield 'empty_high_feed',dict(m.assembly_pose(p,'wechsel'),a13_extend=ext,a13_tool_carried=2.,a13_jaw_open=22.)
        yield 'empty_magazine_feed',dict(p,head_down=0.,a13_extend=ext,a13_tool_carried=0.,a13_jaw_open=22.)
    for jaw in (0.,5.5,11.,16.5,22.):
        yield 'spindle_grip',dict(m.assembly_pose(p,'wechsel'),a13_tool_carried=2.,a13_jaw_open=jaw)
    for x,y,z in itertools.product((-250.,250.),(-100.,100.),(0.,p['z_travel_used'])):
        yield 'park_axis_corner',dict(p,pos_x=x,pos_y=y,head_down=z)

def run():
    p=m.load_parameters();ds=m.recipe();cache={};geometry=[];hits=[];checks=0;park_hits=[]
    by={d['name']:d for d in ds}
    def body(d,q):
        v=m.all_values(q);key=(d['name'],tuple((k,v[k]) for k in sorted(m.used_parameters(d))))
        if key not in cache:cache[key]=world_body(d,q,True)
        return cache[key]
    for d in ds:
        b=body(d,p);geometry.append(dict(name=d['name'],valid=b.isValid(),solids=len(b.Solids())))
    print('Geometry',len(geometry),'parts valid',flush=True)
    new=[d for d in ds if d['name'].startswith('ATC13_') and d['group']=='20_ATC_Option']
    machine=[d for d in ds if d['group']!='20_ATC_Option' and not d['name'].startswith('Faltenbalg')]
    fixed=[d for d in new if d.get('atc_motion')=='fixed']
    moving=[d for d in new if d.get('atc_motion') in ('swing','feed','tool')]
    park=m.all_values(p);workbox=[-620.,-190.,180.,620.,190.,530.]
    for d in new:
        bb=body_bounds(d,park,m.evaluate)
        if overlap(bb,workbox):park_hits.append(d['name'])
    # New functional envelopes against machine, including pullstud and cutter.
    ps=list(poses(p))
    for j,(phase,q) in enumerate(ps):
        v=m.all_values(q);bounds={d['name']:body_bounds(d,v,m.evaluate) for d in ds}
        pairs=[(a,b) for a in (new if phase=='park_axis_corner' else moving) for b in machine]
        for an in ('Radialzylinder_Reserve','Radialkolbenstange_Reserve'):
            for bn in ('Radialschlitten','Radialfuehrung_-24','Radialfuehrung_24','Schwenkarm_Kasten80x40'):
                pairs.append((by['ATC13_'+an],by['ATC13_'+bn]))
        for side in (-1,1):
            for bn in ('BT30_Werkzeug_01','Magazingabel_01','Taschenriegel_01'):
                pairs.append((by['ATC13_Greiferbacke_'+str(side)],by['ATC13_'+bn]))
        for bn in ('Hubmast','Hubplatte','Lagertraeger_270','Lagertraeger_410'):
            pairs.append((by['ATC13_Schwenkarm_Kasten80x40'],by['ATC13_'+bn]))
        for an,bn in (('Magazin_Getriebemotor_Reserve','Magazinlagerplatte'),
                      ('Hubplatte','Hubmotor_Bremse_Reserve'),('Hubmast','Hubmotor_Bremse_Reserve'),
                      ('Greifergehaeuse','Radialfuehrung_-24'),('Greifergehaeuse','Radialfuehrung_24'),
                      ('Magazin_Indexverriegelung_Reserve','Magazinscheibe_12'),
                      ('Magazin_Indexverriegelung_Reserve','BT30_Werkzeug_04'),
                      ('Magazin_Tropfboden','Magazinstaender')):
            pairs.append((by['ATC13_'+an],by['ATC13_'+bn]))
        for a,b in pairs:
            if a.get('atc13_transfer_holder') and b['group']=='05_Spindelkopf' and (phase=='spindle_lift' or q['a13_tool_carried']==2):continue
            if not overlap(bounds[a['name']],bounds[b['name']]):continue
            checks+=1;vol=body(a,q).intersect(body(b,q)).Volume()
            if vol>.01:hits.append(dict(sample=j,phase=phase,a=a['name'],b=b['name'],mm3=vol))
        if j%10==0:print('Pose',j,'checks',checks,'hits',len(hits),flush=True)
    return dict(native_nx_executed=False,part_geometry=geometry,pose_count=len(ps),brep_checks=checks,
        collisions=hits,park_workbox_collisions=park_hits,park_workbox_mm=workbox,
        scope='Machine vs new functional envelopes; 25 retracted low swings,8 endpoint feeds,6 spindle lifts,8 full-axis corners. Pullstud28mm and cutter35mm included. Selected holder/spindle joint excluded only in lift. No continuous swept-volume proof; internal mechanism contacts, replacement spindle and arbitrary workpieces not released.',
        trajectory_verified=False,manufacturing_released=False,atc_operational=False)

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
    result=run();Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf8')
    print('RESULT',result['pose_count'],result['brep_checks'],len(result['collisions']),result['park_workbox_collisions'])
    raise SystemExit(bool(result['collisions'] or result['park_workbox_collisions']))
