"""Finite offline samples only: feed at raised head, then head descent. No M6/IO."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
import cnc_ansichtsmodell as m
from enclosure_checks03 import body_bounds
from atc_anschlusspruefung09 import world_body


def run():
    p=m.load_parameters();defs=m.recipe();checks=[];hits=[];cache={}
    moving=[d for d in defs if d['group']=='20_ATC_Option' and
        d['name'].startswith(('ATC_Gabel_','ATC_BT30_','ATC_Teller_','ATC_Indexierantrieb_','ATC_Teleskop'))]
    fixed=[d for d in defs if d not in moving and not d['name'].startswith('Spannpaket_')]
    end=m.assembly_pose(p,'wechsel')
    poses=[dict(p,teller_feed=f,head_down=0.) for f in (0.,.25,.5,.75,1.)]
    poses += [dict(end,head_down=end['head_down']*f) for f in (.25,.5,.75,1.)]
    for i,q in enumerate(poses):
        v=m.all_values(q);bounds={d['name']:body_bounds(d,v,m.evaluate) for d in defs}
        def body(d):
            # Local definition + all parameters is conservative cache identity.
            key=(d['name'],i)
            if key not in cache:cache[key]=world_body(d,q)
            return cache[key]
        for a in moving:
            for b in fixed:
                # Selected holder entering the incompatible stock spindle is not a proof of fit.
                if a['name']=='ATC_BT30_ER20_70_Raumhuelle_1' and b['group']=='05_Spindelkopf':continue
                aa,bb=bounds[a['name']],bounds[b['name']]
                if not all(min(aa[k+3],bb[k+3])-max(aa[k],bb[k])>1e-5 for k in range(3)):continue
                vol=body(a).intersect(body(b)).Volume()
                row=dict(sample=i,feed=q['teller_feed'],head_down=q['head_down'],a=a['name'],b=b['name'],mm3=round(vol,6))
                checks.append(row)
                if vol>.01:hits.append(row)
    return dict(native_nx_executed=False,trajectory_verified=False,sampled_poses=len(poses),
        scope='Finite feed samples with head raised, then head descent; all drawn fixed bodies except clamping reserves and selected holder/stock head interface. No continuous proof, workpieces, tools beyond holder, real bearings or machine operation.',
        checks=checks,collisions=hits)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    result=run();Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf8')
    print('poses',result['sampled_poses'],'BRep comparisons',len(result['checks']),'collisions',len(result['collisions']))
    raise SystemExit(bool(result['collisions']))
