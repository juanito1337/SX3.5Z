"""Thin-wall manufacturing intent, without inventing Sheet-Metal API calls.
U sections have sharp precursor corners. NX conversion adds the nominated bends.
The recipe is explicitly not a developed blank or an independently certified design.
"""
import math
import modell_v4 as b

def u_profile(d, origin, width, depth, length, axes=((1,0,0),(0,1,0),(0,0,1)), thickness='sheet_t'):
    """Open U cross section; two parallel folds, constant nominal thickness.
    axes = web width, return direction, extrusion direction; all cardinal.
    Existing prism operator creates associative lines + extrusion in native NX.
    """
    w,dp,t=str(width),str(depth),str(thickness)
    pts=[('0','0'),(w,'0'),(w,dp),(f'({w})-({t})',dp),
         (f'({w})-({t})',t),(t,t),(t,dp),('0',dp)]
    def xyz(u,v):
        return [f'({origin[k]})+({u})*({axes[0][k]})+({v})*({axes[1][k]})' for k in range(3)]
    b.prism(d,[xyz(u,v) for u,v in pts],length,axes[2],label='Kantprofil_Zwei_Biegungen_Vorform')
    # Plane coordinate relative to d['datum']; never global occurrence coordinates.
    a=next(i for i in range(3) if axes[1][i])
    d['sheetmetal']={'thickness':thickness,'bend_radius':'bend_r','neutral_factor':'bend_k',
        'plane_axis':a,'plane_coordinate':f'({origin[a]})-({d["datum"][a]})',
        'bend_count':2,'web_width':width,'return_depth':depth,'extrusion_length':length,
        'precursor':'SHARP_CONSTANT_THICKNESS_SOLID', 'flat_pattern_released':False}
    d['note']+=' K06: Kantblech-Vorform; NXSM-Konvertierung im Pflichtmodus. Keine freigegebene Abwicklung.'
    return d

def spring_balance(mass_lower, mass_upper, stroke, fraction=.70, progression=1.30):
    """Virtual work for q_lower=s, q_upper=2s. Four push-type springs.
    Two fixed-to-lower plus two lower-to-upper. Their separate relative strokes
    are s each, NOT 2s. Assistance acts UPWARD, opposite downward opening.
    No force rating, mounting approval or fall protection is inferred.
    """
    nums=(mass_lower,mass_upper,stroke,fraction,progression)
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in nums):raise ValueError('Finite numerical spring inputs required')
    if min(mass_lower,mass_upper,stroke)<=0 or not 0<fraction<1 or progression<1 or fraction*progression>=1:raise ValueError('Invalid mass/stroke or overbalanced study')
    g=9.81; main=fraction*(mass_lower+mass_upper)*g/2; relative=fraction*mass_upper*g/2
    gravity=(mass_lower+2*mass_upper)*g
    # Hand at upper panel (twice lower travel). Negative holding force denotes
    # upward force required to stop the slightly underbalanced door descending.
    return dict(released=False,spring_count=4,stroke_each_mm=stroke,
        main_F1_N=main,relative_F1_N=relative,main_F2_N=main*progression,relative_F2_N=relative*progression,
        masses_kg={'LOWER':mass_lower,'UPPER':mass_upper},
        opening_hand_force_N=[(gravity-2*(main+relative)*(1+(progression-1)*q))/2 for q in (0,.25,.5,.75,1)],
        hand_force_meaning='UPWARD HOLDING FORCE AT UPPER LEAF; POSITIVE VALUE IS NOT A DOWNWARD PUSH',
        maximum_balance_fraction=fraction*progression,
        force_direction='UPWARD_OPPOSES_DOWNWARD_OPENING',
        note='Mass estimate, not NX material measurement. No friction, temperature, fatigue or fault-case analysis. Four unselected gas-spring envelopes, no safety release.')
