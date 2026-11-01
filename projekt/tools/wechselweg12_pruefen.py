"""Discrete BRep placement checks. No continuous-motion or supplier-fit proof."""
import itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cnc_ansichtsmodell as m
from enclosure_checks03 import body_bounds
from atc_anschlusspruefung09 import world_body


def run():
    p=m.load_parameters();defs=m.recipe();checks=[];hits=[];cache={}
    atc=[d for d in defs if d['group']=='20_ATC_Option' and not d['name'].startswith('Spannpaket_')]
    excluded={'Faltenbalg_Z','Faltenbalg_Y_hinten'}
    machine=[d for d in defs if d['group']!='20_ATC_Option' and d['name'] not in excluded]
    end=m.assembly_pose(p,'wechsel')
    poses=[('feed',dict(p,teller_feed=f,head_down=0.)) for f in (0.,.25,.5,.75,1.)]
    poses += [('head_descent',dict(end,head_down=end['head_down']*f)) for f in (.25,.5,.75,1.)]
    poses += [('park_axis_corner',dict(p,pos_x=x,pos_y=y,head_down=z))
              for x,y,z in itertools.product((-p['travel_x']/2,p['travel_x']/2),
                  (-p['travel_y']/2,p['travel_y']/2),(0.,p['z_travel_used']))]
    pairs=[(a,b) for a in atc for b in machine]
    # Internal purchased-product details are deliberately unverified envelopes.
    # Own support/screen vs purchased product is still checked.
    pairs += [(a,b) for a,b in itertools.combinations(atc,2)
              if (a['supply_kind']=='MAKE') != (b['supply_kind']=='MAKE')]
    for i,(phase,q) in enumerate(poses):
        v=m.all_values(q);bounds={d['name']:body_bounds(d,v,m.evaluate) for d in defs}
        def body(d):
            key=(d['name'],tuple((n,v[n]) for n in sorted(m.used_parameters(d))))
            if key not in cache:cache[key]=world_body(d,q)
            return cache[key]
        for a,b in pairs:
            if a['name']=='ATC_BT30_ER20_70_Raumhuelle_1' and b['group']=='05_Spindelkopf':continue
            aa,bb=bounds[a['name']],bounds[b['name']]
            if not all(min(aa[k+3],bb[k+3])-max(aa[k],bb[k])>1e-5 for k in range(3)):continue
            vol=body(a).intersect(body(b)).Volume()
            row=dict(sample=i,phase=phase,feed=q['teller_feed'],head_down=q['head_down'],
                     pos_x=q['pos_x'],pos_y=q['pos_y'],a=a['name'],b=b['name'],mm3=round(vol,6))
            checks.append(row)
            if vol>.01:hits.append(row)
    return dict(native_nx_executed=False,trajectory_verified=False,supplier_internal_fit_verified=False,
        sampled_poses=len(poses),park_axis_samples=8,
        scope='5 feed +4 head-descent +8 park axis corners. All ATC except clamping reserves vs drawn machine; own support/screen vs product. Selected holder/stock head, deformable bellows, product-internal fits, continuous path, workpieces and additional cutters excluded.',
        checks=checks,collisions=hits)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    result=run();Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf8')
    print('poses',result['sampled_poses'],'BRep comparisons',len(result['checks']),'collisions',len(result['collisions']))
    raise SystemExit(bool(result['collisions']))
