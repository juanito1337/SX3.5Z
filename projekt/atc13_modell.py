"""Separate native-NX concept13. Retains machine12; no operating release.
Twelve-pocket magazine, low/retracted single-arm transfer, enlarged side/rear bay.
All new mechanism dimensions are engineering drafts, not vendor dimensions.
"""
import copy, math, re
from collections import OrderedDict
import cnc_ansichtsmodell as old
import blech06

VERSION='CNC_KONZEPT_13_SEITENMAGAZIN'
ROOT=old.ROOT
base=old.base
evaluate=old.evaluate
local_definition=old.local_definition
PALETTE=old.PALETTE
DEFAULT_COLORS=old.DEFAULT_COLORS
GROUPS=OrderedDict(old.GROUPS)
GROUPS['20_ATC_Option']='13 - Zwoelfplatz-Seitenmagazin und Einzelgreifer; Konzept'
LAYERS=old.LAYERS
DEFAULTS=dict(a13_pivot_x=850.,a13_pivot_y=-350.,a13_pitch=220.,a13_extend=0.,
    a13_lift=0.,a13_c=0.,a13_s=1.,a13_tool_carried=0.,a13_jaw_open=22.,a13_transfer_gauge=440.,
    a13_outer_right=1187.,a13_outer_back=1100.,a13_bay_left=550.,
    a13_cutter_projection=35.,a13_stud_height=28.)
UNITLESS={'a13_c','a13_s','a13_tool_carried'}
SPECS=copy.deepcopy(old.SPECS)
for k,v in DEFAULTS.items():
    SPECS.append(dict(name=k,value=v,unit='unitless' if k in UNITLESS else 'mm',limits=None,
        status='ENTWURF_13_UNBESTAETIGT',source='E13 Konzept01.11.2026',
        note='Konstruktionsannahme, keine Herstellerpassung oder Betriebsfreigabe.'))
DERIVED=OrderedDict(old.DERIVED)
DERIVED.update(OrderedDict([
    ('a13_radius','sqrt(a13_pivot_x*a13_pivot_x+a13_pivot_y*a13_pivot_y)'),
    ('a13_reach','a13_radius-60+a13_extend'),
    ('a13_mag_x','a13_pivot_x'),('a13_mag_y','a13_pivot_y+a13_radius+a13_pitch'),
    ('a13_grip_x','a13_pivot_x+a13_reach*a13_c'),
    ('a13_grip_y','a13_pivot_y+a13_reach*a13_s'),
    ('a13_gauge','a13_transfer_gauge+a13_lift'),
    ('a13_tool_x','a13_tool_carried*(2-a13_tool_carried)*a13_grip_x+(1-a13_tool_carried)*(2-a13_tool_carried)/2*a13_mag_x'),
    ('a13_tool_y','a13_tool_carried*(2-a13_tool_carried)*a13_grip_y+(1-a13_tool_carried)*(2-a13_tool_carried)/2*(a13_mag_y-a13_pitch)'),
    ('a13_tool_gauge','a13_tool_carried*(2-a13_tool_carried)*a13_gauge+(1-a13_tool_carried)*(2-a13_tool_carried)/2*a13_transfer_gauge+a13_tool_carried*(a13_tool_carried-1)/2*spindle_face_z'),
]))
CAT=copy.deepcopy(old.CAT)

def __getattr__(name):return getattr(old,name)

def load_parameters(path=None):
    p=old.load_parameters(path);p.update(DEFAULTS);return p

def all_values(p):
    v=OrderedDict(p)
    for n,e in DERIVED.items():v[n]=evaluate(e,v)
    return v

def validate(p):
    old.validate(p)
    for k in DEFAULTS:
        if isinstance(p[k],bool) or not isinstance(p[k],(int,float)) or not math.isfinite(p[k]):raise ValueError(k)
    if not 0<=p['a13_extend']<=60 or not 0<=p['a13_lift']<=90:raise ValueError('ATC13 Hubgrenze')
    if p['a13_tool_carried'] not in (0,1,2):raise ValueError('ATC13 Werkzeugzustand')
    if not 0<=p['a13_jaw_open']<=22:raise ValueError('ATC13 Greiferhub')
    if abs(p['a13_c']**2+p['a13_s']**2-1)>1e-8:raise ValueError('ATC13 Winkelvektor')
    for k in set(DEFAULTS)-{'a13_extend','a13_lift','a13_c','a13_s','a13_tool_carried','a13_jaw_open'}:
        if p[k]!=DEFAULTS[k]:raise ValueError('ATC13 Rahmenmass erfordert neue Layoutpruefung: '+k)
    return True

def assembly_pose(p,name):
    q=dict(p);q.update(a13_extend=0.,a13_lift=0.,a13_c=0.,a13_s=1.,a13_tool_carried=0.,a13_jaw_open=22.)
    if name=='wechsel':
        r=math.hypot(q['a13_pivot_x'],q['a13_pivot_y'])
        q.update(head_down=0.,a13_extend=60.,a13_lift=90.,a13_c=-q['a13_pivot_x']/r,
            a13_s=-q['a13_pivot_y']/r,a13_tool_carried=1.,a13_jaw_open=0.)
    elif name=='magazin':q.update(head_down=0.,a13_extend=60.,a13_tool_carried=1.,a13_jaw_open=0.)
    elif name!='park':raise ValueError('Unbekannte Stellung13: '+name)
    validate(q);return q

def used_parameters(d):
    known={s['name'] for s in SPECS}|set(DERIVED);out=set()
    def scan(x):
        if isinstance(x,str):out.update(set(re.findall(r'\b[A-Za-z_]\w*\b',x))&known)
        elif isinstance(x,dict):
            for k,v in x.items():
                if k not in ('label','name','note','source'):scan(v)
        elif isinstance(x,(list,tuple)):
            for v in x:scan(v)
    scan(d['ops']);scan(d['datum']);scan(d.get('sheetmetal',{}))
    while True:
        before=set(out)
        for n in list(out):
            if n in DERIVED:scan(DERIVED[n])
        if out==before:return out

def atc_report(p):
    v=all_values(p)
    return dict(schema='ATC13_SINGLE_ARM_CONCEPT',pocket_count=12,tool_carried=p['a13_tool_carried']==1,
        gripper_axis_xy_mm=[v['a13_grip_x'],v['a13_grip_y']],
        transfer_holder_gauge_mm=[v['a13_tool_x'],v['a13_tool_y'],v['a13_tool_gauge']],
        nominal_spindle_axis_and_face_mm=[0.,0.,v['spindle_face_z']],
        magazine_center_xy_mm=[v['a13_mag_x'],v['a13_mag_y']],
        pocket_pitch_mm=2*p['a13_pitch']*math.sin(math.pi/12),
        toolchange_workpiece_limit_mm=p['a13_transfer_gauge']-p['n09_tool_projection']-p['a13_cutter_projection']-v['table_top_z']-15,
        unrestricted_arbitrary_workpiece_change=False,manufacturing_released=False,atc_operational=False,
        machine_operation_enabled=False,spindle_clamping_verified=False,trajectory_verified=False,
        source='E13 engineering draft; original SK30 remains; BT30 interface and tool orientation pending',
        sequence='Retracted low swing; extend only at endpoints; spindle vertical extraction; pocket retention before gripper release')

def check_recipe(p,parts=None):
    validate(p);v=all_values(p);ds=parts if parts is not None else recipe()
    assert len({d['id'] for d in ds})==len(ds)
    assert len({d['name'] for d in ds})==len(ds)
    for d in ds:
        assert d['group'] in GROUPS and d['material'] in PALETTE
        for op in d['ops']:
            for x in op['origin']:evaluate(x,v)
            for x in op.get('size',[]):assert evaluate(x,v)>0,d['name']
            for k in ('height','diameter','top_diameter'):
                if k in op:assert evaluate(op[k],v)>0,d['name']
            for pt in op.get('points',[]):
                for x in pt:evaluate(x,v)
    return v

def recipe():
    # Keep model12 original machine and chip trays. Replace obstructing ATC only.
    ds=[copy.deepcopy(d) for d in old.recipe() if d['group']!='20_ATC_Option'
        or d['name'].startswith('Spannpaket_')]
    # Relocate entire dry cabinet and its support, not only its visible shell.
    for d in ds:
        if d['group']=='16_Schaltschrank' or d['name'].startswith('Schrank_'):
            d['datum'][0]=f'({d["datum"][0]})+300'
            def shift(x):
                return [f'({x[0]})+300',x[1],x[2]]
            for op in d['ops']:
                op['origin']=shift(op['origin'])
                if 'points' in op:op['points']=[shift(pt) for pt in op['points']]
            d['note']+=' E13 Schrank samt Traegern300mm nach rechts versetzt.'
        if d['name'].startswith('Schrank_Traegerausleger_'):
            y=-40 if d['name'].endswith('_0') else 430
            d['ops']=[];base.box(d,(1160,y,-80),(329,60,60))
    ds=[d for d in ds if d['name'] not in ('Einhausung_Seitenwand_rechts','Einhausung_Rueckwand')]
    new=[]
    def part(name,mat='design_blue',kind='MAKE',group='20_ATC_Option',motion='fixed',item=None):
        d=dict(id='A13_%03d'%(len(new)+1),name='ATC13_'+name,group=group,material=mat,datum=['0','0','0'],ops=[],
            status='KONZEPT_13_UNBESTAETIGT',source='E13 dimensionierter Fertigungs-/Funktionsentwurf',
            note='Keine freigegebenen Passungen/Lasten/Steuerung. Lager, Greifernut und Retention brauchen Detailauslegung.',
            supply_kind=kind,item_id=item or ('F13-' if kind=='MAKE' else 'R13-')+name,
            purchase_instance=name,manufacturing_released=False,atc_operational=False,revision_added='13',atc_motion=motion)
        d['filename']=d['id']+'_'+d['name'];new.append(d);return d
    def box(name,o,s,**kw):
        d=part(name,**kw);base.box(d,o,s);return d
    def cyl(name,o,diam,h,**kw):
        d=part(name,**kw);base.cyl(d,o,diam,h,(0,0,1));return d
    def tube(name,o,s,t=4,**kw):
        d=box(name,o,s,**kw)
        base.box(d,(f'({o[0]})+{t}',f'({o[1]})+{t}',f'({o[2]})-.1'),
            (f'({s[0]})-{2*t}',f'({s[1]})-{2*t}',f'({s[2]})+.2'),'cut','Hohlprofil')
        return d
    def armpt(r,t,z):return (f'a13_pivot_x+({r})*a13_c-({t})*a13_s',f'a13_pivot_y+({r})*a13_s+({t})*a13_c',z)
    def armrect(d,r0,r1,t0,t1,z,h,op='add'):
        base.prism(d,[armpt(r0,t0,z),armpt(r1,t0,z),armpt(r1,t1,z),armpt(r0,t1,z)],h,(0,0,1),op,label='Armprofil_'+op)
    # Independently supported side/rear frame, joined to the existing stand at top level.
    for i,(x,y) in enumerate(((1130,-350),(580,1020),(1130,1020))):
        tube('Rahmenbein_'+str(i),(x-30,y-30,-720),(60,60,640),mat='frame')
        box('Fussplatte_'+str(i),(x-60,y-60,-730),(120,120,10),mat='steel')
    for name,o,s in [('Vorn',(887,-380,-80),(273,60,60)),('Hinten',(550,990,-80),(610,60,60)),
                     ('Rechts',(1100,-320,-80),(60,1310,60)),('Armseite',(827,525,-80),(60,465,60)),
                     ('Magazinquer',(887,759,-80),(213,60,60)),('MagazinquerLinks',(550,759,-80),(277,60,60))]:
        box('Rahmenholm_'+name,o,s,mat='frame')
    # Vertical mast at front-right: outside table travel, not on the chip sheet.
    box('Mastauflage',(975,-425,-20),(150,150,20),mat='steel')
    tube('Hubmast',(990,-410,12),(120,120,570),t=6,mat='frame')
    box('Mastfuss',(975,-425,0),(150,150,12),mat='steel')
    for side in (-1,1):
        box('Z_Fuehrung_'+str(side),(970,-350+side*45-10,210),(20,20,360),mat='steel',kind='RESERVE')
        for z in (270,400):box('Z_Wagen_%s_%s'%(side,z),(942,-350+side*45-20,f'{z}+a13_lift'),(28,40,55),kind='RESERVE')
    box('Hubplatte',(922,-430,'235+a13_lift'),(20,160,240))
    # Upper/lower bearing brackets reach backwards to the shaft at the mast axis.
    for z in (270,410):
        d=box('Lagertraeger_'+str(z),(790,-425,f'{z}+a13_lift'),(132,150,18))
        base.cyl(d,('a13_pivot_x','a13_pivot_y',f'{z}-.1+a13_lift'),70,18.2,(0,0,1),'cut')
        d=cyl('Drehlager_'+str(z),('a13_pivot_x','a13_pivot_y',f'{z}+a13_lift'),70,18,mat='steel',kind='RESERVE')
        base.cyl(d,('a13_pivot_x','a13_pivot_y',f'{z}-.1+a13_lift'),40,18.2,(0,0,1),'cut')
    cyl('Drehwelle',('a13_pivot_x','a13_pivot_y','260+a13_lift'),40,180,mat='steel',motion='lift')
    cyl('Hubspindel_Tr16_Entwurf',(962,-350,210),16,370,mat='steel',kind='RESERVE')
    d=box('Hubmutter_Entwurf',(942,-365,'320+a13_lift'),(40,30,35),mat='bronze',kind='RESERVE')
    base.cyl(d,(962,-350,'319.9+a13_lift'),16,35.2,(0,0,1),'cut')
    d=box('Hubmotor_Montageplatte',(922,-410,582),(188,120,3))
    base.cyl(d,(962,-350,581.9),32,3.2,(0,0,1),'cut')
    box('Hubmotor_Bremse_Reserve',(922,-390,585),(80,80,100),kind='RESERVE')
    cyl('Hubkupplung_Reserve',(962,-350,575),30,15,kind='RESERVE')
    box('Hubspindel_Lagerwinkel',(942,-380,190),(48,60,10))
    d=cyl('Hubspindel_Festlager_Reserve',(962,-350,200),40,10,kind='RESERVE')
    base.cyl(d,(962,-350,199.9),16,10.2,(0,0,1),'cut')
    cyl('Schwenkantrieb_Reserve',('a13_pivot_x','a13_pivot_y','428+a13_lift'),110,110,kind='RESERVE')
    cyl('Drehgeber_Reserve',('a13_pivot_x','a13_pivot_y','538+a13_lift'),50,20,kind='RESERVE')
    # Welded box arm 80 high x40 wide x4 wall, with integral hub and bored shaft seat.
    d=part('Schwenkarm_Kasten80x40',motion='swing')
    armrect(d,0,'a13_radius-110',-20,20,'a13_gauge-120',80)
    base.cyl(d,('a13_pivot_x','a13_pivot_y','a13_gauge-120'),120,80,(0,0,1))
    armrect(d,70,'a13_radius-114',-16,16,'a13_gauge-116',72,'cut')
    base.cyl(d,('a13_pivot_x','a13_pivot_y','a13_gauge-120.1'),40,80.2,(0,0,1),'cut')
    d=part('Radialfuehrung_Deckauflage',motion='swing')
    armrect(d,'a13_radius-350','a13_radius-160',-40,40,'a13_gauge-44',4)
    for t in (-24,24):
        d=part('Radialfuehrung_'+str(t),mat='steel',kind='RESERVE',motion='swing')
        armrect(d,'a13_radius-350','a13_radius-160',t-8,t+8,'a13_gauge-40',16)
    d=part('Radialschlitten',motion='feed')
    armrect(d,'a13_reach-240','a13_reach-40',-45,45,'a13_gauge-24',12)
    d=part('Radialzylinder_Reserve',kind='RESERVE',motion='swing')
    armrect(d,'a13_radius-380','a13_radius-220',52,88,'a13_gauge-40',32)
    d=part('Radialkolbenstange_Reserve',mat='steel',kind='RESERVE',motion='feed')
    armrect(d,'a13_radius-220','a13_reach-100',65,75,'a13_gauge-30',10)
    d=part('Zylinderkonsole',motion='swing')
    armrect(d,'a13_radius-350','a13_radius-320',20,88,'a13_gauge-70',30)
    d=part('Radialanlenkung',motion='feed')
    armrect(d,'a13_reach-100','a13_reach-70',45,85,'a13_gauge-30',18)
    d=part('Greifergehaeuse',motion='feed')
    armrect(d,'a13_reach-90','a13_reach-40',-70,70,'a13_gauge-35',20)
    for side in (-1,1):
        d=part('Greiferbacke_'+str(side),mat='steel',motion='feed')
        t0,t1=(-38,-1) if side<0 else (1,38)
        armrect(d,'a13_reach-45','a13_reach+25',f'{t0}+{side}*a13_jaw_open',f'{t1}+{side}*a13_jaw_open','a13_gauge-15',6)
        base.cyl(d,armpt('a13_reach',f'{side}*a13_jaw_open','a13_gauge-15.1'),40.5,6.2,(0,0,1),'cut','Flanschnut_Entwurf')
    d=part('Greifer_Federklemmung_Reserve',kind='RESERVE',motion='feed')
    armrect(d,'a13_reach-85','a13_reach-45',-30,30,'a13_gauge-15',15)
    # Magazine at low transfer height, isolated behind the complete machine sweep.
    box('Magazinauflage',('a13_mag_x-100','a13_mag_y-100',-20),(200,200,20),mat='steel')
    tube('Magazinstaender',('a13_mag_x-60','a13_mag_y-60',0),(120,120,320),t=6,mat='frame')
    box('Magazinlagerplatte',('a13_mag_x-100','a13_mag_y-100',320),(200,200,15))
    cyl('Magazinlager_Reserve',('a13_mag_x','a13_mag_y',335),130,55,kind='RESERVE')
    cyl('Magazinnabe',('a13_mag_x','a13_mag_y',390),100,13,mat='steel')
    d=cyl('Magazinscheibe_12',('a13_mag_x','a13_mag_y','a13_transfer_gauge-37'),390,10)
    base.cyl(d,('a13_mag_x','a13_mag_y','a13_transfer_gauge-37.1'),60,10.2,(0,0,1),'cut')
    for i in range(12):
        a=i*math.pi/6
        base.cyl(d,(f'a13_mag_x+{170*math.cos(a)}',f'a13_mag_y+{170*math.sin(a)}','a13_transfer_gauge-37.1'),6.5,10.2,(0,0,1),'cut','Indexbohrung_Entwurf')
    box('Magazin_Getriebemotor_Reserve',('a13_mag_x+75','a13_mag_y-40',210),(100,80,110),kind='RESERVE')
    box('Magazin_Motorflansch',('a13_mag_x+100','a13_mag_y-50',320),(85,100,15))
    box('Magazin_Indexverriegelung_Reserve',('a13_mag_x+140','a13_mag_y-15',350),(45,30,45),kind='RESERVE')
    box('Magazin_Indexhalter',('a13_mag_x+90','a13_mag_y-20',335),(100,40,15))
    cyl('Magazin_Indexstift',('a13_mag_x+170','a13_mag_y',395),6,10,mat='steel',kind='RESERVE')
    for i in range(12):
        ang=-math.pi/2+i*math.pi/6;cx=math.cos(ang);cy=math.sin(ang)
        def pt(r,t,z):return (f'a13_mag_x+({r})*({cx})-({t})*({cy})',f'a13_mag_y+({r})*({cy})+({t})*({cx})',z)
        d=part('Magazingabel_%02d'%(i+1),mat='white')
        base.prism(d,[pt(180,-32,'a13_transfer_gauge-24'),pt(245,-32,'a13_transfer_gauge-24'),pt(245,32,'a13_transfer_gauge-24'),pt(180,32,'a13_transfer_gauge-24')],4,(0,0,1))
        base.cyl(d,pt('a13_pitch',0,'a13_transfer_gauge-24.1'),35.5,4.2,(0,0,1),'cut')
        base.prism(d,[pt(220,-17.75,'a13_transfer_gauge-24.1'),pt(246,-17.75,'a13_transfer_gauge-24.1'),pt(246,17.75,'a13_transfer_gauge-24.1'),pt(220,17.75,'a13_transfer_gauge-24.1')],4.2,(0,0,1),'cut')
        base.prism(d,[pt(180,-32,'a13_transfer_gauge-27'),pt(195,-32,'a13_transfer_gauge-27'),pt(195,32,'a13_transfer_gauge-27'),pt(180,32,'a13_transfer_gauge-27')],3,(0,0,1))
        d=part('Taschenriegel_%02d'%(i+1),mat='orange',kind='RESERVE')
        base.prism(d,[pt(182,-12,'a13_transfer_gauge-20'),pt(195,-12,'a13_transfer_gauge-20'),pt(195,12,'a13_transfer_gauge-20'),pt(182,12,'a13_transfer_gauge-20')],24,(0,0,1))
        # Tool envelopes include explicit unverified stud; last primitive is the gauge cone.
        d=part('BT30_Werkzeug_%02d'%(i+1),mat='steel',kind='BUY',item='K09-BT30ER20',motion='tool' if i==0 else 'fixed')
        x,y=pt('a13_pitch',0,0)[:2];g='a13_transfer_gauge'
        if i==0:x,y,g='a13_tool_x','a13_tool_y','a13_tool_gauge';d['atc13_transfer_holder']=True
        base.cyl(d,(x,y,f'{g}-n09_tool_projection'),'n09_tool_nut_d','n09_tool_projection',(0,0,1))
        base.cyl(d,(x,y,f'{g}-20'),46,5,(0,0,1))
        base.cyl(d,(x,y,f'{g}-15'),40,6,(0,0,1))
        base.cyl(d,(x,y,f'{g}-9'),46,5,(0,0,1))
        base.cyl(d,(x,y,f'{g}-n09_tool_projection-a13_cutter_projection'),20,'a13_cutter_projection',(0,0,1))
        base.cone(d,(x,y,g),'n09_tool_d','n09_tool_d-(n09_tool_total-n09_tool_projection)*7/24','n09_tool_total-n09_tool_projection',(0,0,1))
        base.cyl(d,(x,y,f'{g}+n09_tool_total-n09_tool_projection-1'),12,'a13_stud_height+1',(0,0,1))
        d['note']+=' K09 holder main dimensions;46mm flange/groove and28mm pullstud are unconfirmed drafts;35mm cutter extension included.'
    # Native folded replacement/extension panels; unchanged front door remains.
    def panel(name,o,w,length,axes):
        d=part(name,mat='sheet',group='15_Einhausung');d['datum']=list(o)
        blech06.u_profile(d,o,w,25,length,axes=axes);return d
    panel('Wand_rechts',('a13_outer_right+sheet_t','enc_front-sheet_t',0),'a13_outer_back-enc_front+2*sheet_t','enclosure_h',((0,1,0),(-1,0,0),(0,0,1)))
    panel('Rueckwand_links',('enc_left+sheet_t','enc_back',0),'a13_bay_left-enc_left-2*sheet_t','enclosure_h',((1,0,0),(0,-1,0),(0,0,1)))
    panel('Magazinwand_links',('a13_bay_left','enc_back',0),'a13_outer_back-enc_back','enclosure_h',((0,1,0),(1,0,0),(0,0,1)))
    panel('Magazinwand_hinten',('a13_bay_left','a13_outer_back',0),'a13_outer_right-a13_bay_left','enclosure_h',((1,0,0),(0,-1,0),(0,0,1)))
    panel('Frontfluegel',('enc_right','enc_front',0),'a13_outer_right-enc_right','enclosure_h',((1,0,0),(0,1,0),(0,0,1)))
    panel('Dach_rechts',('enc_right+2*sheet_t','enc_front-sheet_t','enclosure_h+sheet_t'),'a13_outer_right-enc_right','a13_outer_back-enc_front',((1,0,0),(0,0,-1),(0,1,0)))
    panel('Dach_hinten',('a13_bay_left','enc_back+2*sheet_t','enclosure_h+sheet_t'),'enc_right-a13_bay_left+4*sheet_t','a13_outer_back-enc_back',((1,0,0),(0,0,-1),(0,1,0)))
    # Visible magazine splash shield; service seam/door and trough drain remain detail work.
    box('Magazinschutz_vorn',('a13_mag_x-280','a13_mag_y-280',120),(560,2,230),mat='sheet')
    d=box('Magazin_Tropfboden',('a13_mag_x-270','a13_mag_y-270',118),(540,540,2),mat='sheet')
    base.box(d,('a13_mag_x-62','a13_mag_y-62',117.9),(124,124,2.2),'cut','Stuetzausschnitt')
    for d in new:
        if d['item_id'] not in CAT:CAT[d['item_id']]=dict(name=d['name'],kind=d['supply_kind'],dims={},source_ids=['E13'],verified=False)
    return ds+new
