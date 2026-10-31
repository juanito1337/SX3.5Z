"""Conservative analytic bounds of the shared recipe; NOT an NX collision test.
Cuts cannot enlarge a body: union of additive primitive AABBs is an upper bound.
Eight corners cover affine axis translations in this recipe. Flexible-body models
are included as drawn, not as real material deformation, cables or workpieces.
"""
import itertools
import math


def primitive_bounds(op, values, evaluate):
    ev=lambda q: float(evaluate(q, values))
    if op['kind']=='prism':
        pts=[[ev(q) for q in pt] for pt in op['points']]
        axis=[ev(q) for q in op['direction']];length=math.sqrt(sum(x*x for x in axis))
        if length<=0:raise ValueError('Nullrichtung')
        delta=[x/length*ev(op['height']) for x in axis]
        pts=pts+[[v[k]+delta[k] for k in range(3)] for v in pts]
        return [min(v[k] for v in pts) for k in range(3)]+[max(v[k] for v in pts) for k in range(3)]
    o=[ev(q) for q in op['origin']]
    if op['kind']=='box':return o+[o[k]+ev(op['size'][k]) for k in range(3)]
    if op['kind'] not in ('cylinder','cone'):raise ValueError('Unbekannte Geometrie '+op['kind'])
    axis=[ev(q) for q in op['direction']];length=math.sqrt(sum(x*x for x in axis))
    if length<=0:raise ValueError('Nullrichtung')
    axis=[x/length for x in axis];h=ev(op['height'])
    radius=ev(op['diameter'])/2
    if op['kind']=='cone':radius=max(radius,ev(op['top_diameter'])/2)
    r=[radius*math.sqrt(max(0,1-x*x)) for x in axis];end=[o[k]+axis[k]*h for k in range(3)]
    return [min(o[k],end[k])-r[k] for k in range(3)]+[max(o[k],end[k])+r[k] for k in range(3)]


def body_bounds(definition, values, evaluate):
    adds=[primitive_bounds(o,values,evaluate) for o in definition['ops'] if o['op']=='add']
    if not adds:raise ValueError('Kein Grundkoerper '+definition['name'])
    return [min(b[k] for b in adds) for k in range(3)]+[max(b[k] for b in adds) for k in range(3,6)]


def sweep_report(model, parameters, definitions):
    v=model.all_values(parameters)
    limits=[v['enc_left']+v['sheet_t']+v['window_t'],v['enc_front']+40,0,
            v['enc_right']-v['sheet_t']-v['window_t'],v['enc_back']-v['sheet_t'],v['enclosure_h']]
    poses=list(itertools.product([-v['travel_x']/2,v['travel_x']/2],[-v['travel_y']/2,v['travel_y']/2],[0,v['z_travel_used']]))
    parts=[d for d in definitions if int(d['group'][:2])<=13]
    union=[math.inf]*3+[-math.inf]*3;boundary=[None]*6;violations=[]
    for pose in poses:
        vv=model.all_values(dict(parameters,pos_x=pose[0],pos_y=pose[1],head_down=pose[2]))
        for d in parts:
            b=body_bounds(d,vv,model.evaluate)
            for k in range(3):
                if b[k]<union[k]:union[k]=b[k];boundary[k]=d['name']
                if b[k+3]>union[k+3]:union[k+3]=b[k+3];boundary[k+3]=d['name']
            margins=[b[k]-limits[k] for k in range(3)]+[limits[k+3]-b[k+3] for k in range(3)]
            if min(margins)<-1e-6:violations.append(dict(name=d['name'],pose=list(pose),margins_mm=margins))
    return dict(native_nx_executed=False,method='ADDITIVE_PRIMITIVE_AABB_AT_EIGHT_AXIS_RANGE_CORNERS',
                note='Konservative Modellhuellen. Kein Maschinen-Kollisionstest, keine reale Balg-/Kabel-/Werkstueckpruefung. Aufstellebene z=0 ist erlaubter Kontakt.',
                pose_count=len(poses),checked_part_count=len(parts),interior_limits_mm=limits,
                swept_bounds_mm=union,boundary_parts=boundary,
                margins_mm=[union[k]-limits[k] for k in range(3)]+[limits[k+3]-union[k+3] for k in range(3)],
                violations=violations)
