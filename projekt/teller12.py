"""RATTM BT30 placement study on a fixed column console, NOT supplier CAD.

Only base330x175x22 and disc280x16 are directly tied to image dimensions.
Stroke200 is a cylinder-code hypothesis; pitch, drive and bracket are drafts.
"""
import math
from collections import OrderedDict
import teller10

DEFAULTS=dict(atc12_stroke=200.,atc12_base_l=330.,atc12_base_w=175.,
    atc12_base_t=22.,atc12_disc_d=280.,atc12_carriage_offset=70.,
    teller_radius=180.,teller_plate_t=16.,teller_gauge_z=400.,
    teller_dir_x=-math.sqrt(3)/2,teller_dir_y=.5,teller_hood_radius=220.)
IMAGE_PARAMETERS={'atc12_base_l':330.,'atc12_base_w':175.,'atc12_base_t':22.,
                  'atc12_disc_d':280.,'teller_plate_t':16.}
DERIVED=OrderedDict([
    ('teller_park_x','-(teller_radius+atc12_stroke)*teller_dir_x'),
    ('teller_park_y','-(teller_radius+atc12_stroke)*teller_dir_y'),
    ('teller_cx','-(teller_radius+atc12_stroke*(1-teller_feed))*teller_dir_x'),
    ('teller_cy','-(teller_radius+atc12_stroke*(1-teller_feed))*teller_dir_y'),
    ('atc12_base_r','teller_radius+atc12_stroke/2+atc12_carriage_offset'),
    ('atc12_base_x','-atc12_base_r*teller_dir_x'),
    ('atc12_base_y','-atc12_base_r*teller_dir_y'),
    ('atc12_base_z','teller_gauge_z-190'),
    ('atc12_mount_x','column_x/2'),
])


def validate(p,v):
    for key in set(teller10.DEFAULTS)|set(DEFAULTS):
        val=p[key]
        if isinstance(val,bool) or not isinstance(val,(float,int)) or not math.isfinite(val):
            raise ValueError('Ungueltiger Tellerparameter12: '+key)
    for key,value in IMAGE_PARAMETERS.items():
        if not math.isclose(p[key],value,abs_tol=1e-9):
            raise ValueError('Bildmass12 nur mit neuer Quellenrevision aendern: '+key)
    if not 0<=p['teller_feed']<=1 or not 170<=p['teller_radius']<=185:
        raise ValueError('Tellerzustellung/Entwurfsradius ausserhalb Studienbereich')
    if not math.isclose(p['atc12_stroke'],200.) or p['atc12_carriage_offset']!=70:
        raise ValueError('Schlittenstudie nur fuer angenommene200mm und70mm Achsversatz')
    if not (math.isclose(p['teller_dir_x'],-math.sqrt(3)/2) and math.isclose(p['teller_dir_y'],.5)):
        raise ValueError('Saeulenkonsole12 fuer rechte30Grad-Zustellung ausgelegt')
    if not math.isclose(p['teller_index_cos']**2+p['teller_index_sin']**2,1.,abs_tol=1e-9):
        raise ValueError('Teller-Indexvektor muss normiert sein')
    if not 400<=p['teller_gauge_z']<=420:
        raise ValueError('Wechselhoehe12 muss400..420mm bleiben; Grundplatte ueber Tisch')
    if p['teller_hood_radius']-2 < math.hypot(p['teller_radius']+25,28)+10:
        raise ValueError('Parkhaube braucht10mm nominalen Gabeleckenabstand')
    h=p['teller_hood_radius']
    if not (v['teller_park_x']-h>75+10 and v['teller_park_x']+h<v['enc_right']-2
            and v['teller_park_y']-h>v['enc_front']+2 and v['teller_park_y']+h<v['enc_back']-2):
        raise ValueError('Parkhaube schneidet nominalen Kopf- oder Einhausungsraum')
    if v['atc12_base_z']<=v['table_top_z']+20:
        raise ValueError('Grundplatte braucht Abstand ueber nominalem Tisch')
    if v['head_top_z']+p['head_down']+70+p['clamp_space_h']+p['release_space_h']>=p['enclosure_h']:
        raise ValueError('Spann-/Loesereserve reicht ueber Dach')
    return True


def report(p,v):
    validate(p,v)
    return dict(schema='ATC12_COLUMN_PLACEMENT_STUDY',layout='RADIAL_LINEAR_CAROUSEL',
        selected_product='1005009887984460',selected_interface='BT30',
        supplier_geometry_verified=False,original_spindle='SK30/M12 DIN2080',
        required_spindle_interface='BT30 automatic clamping; replacement or retrofit remains open',
        clamping_package_required=True,clamping_package_status='RESERVED_SPACE_NOT_ENGINEERED',
        machine_operation_enabled=False,spindle_clamping_verified=False,trajectory_verified=False,
        atc_operational=False,nominal_reach_ok=False,
        pockets=[dict(pocket=i+1,index_rotation_deg=-i*45.,pickup_axis_xy_mm=[0.,0.],
                      required_gauge_z_mm=p['teller_gauge_z']) for i in range(8)],
        park_center_xy_mm=[v['teller_park_x'],v['teller_park_y']],
        pickup_center_xy_mm=[-p['teller_radius']*p['teller_dir_x'],-p['teller_radius']*p['teller_dir_y']],
        required_feed_mm=p['atc12_stroke'],stroke_status='200mm inferred from SU32X200-S; usable travel unconfirmed',
        tool_pitch_radius_mm=p['teller_radius'],tool_pitch_status='180mm draft; NOT the280mm disc diameter',
        reserved_table_strip_mm=[0,0],table_mounting=False,gauge_z_mm=p['teller_gauge_z'],
        support='Fixed right-column console; casting face, fasteners and strength unverified',
        spindle_choice_blocks_layout=False,
        blockers=['Herstellerbezuege/Greiferteilkreis/Lasten und nutzbarer Hub fehlen',
                  'Konsole und unbestaetigte Antriebs-/Greiferhuellen sind Entwurf',
                  'Spindel/Spannpaket spaeter auszulegen; kein Betriebsnachweis',
                  'Gesamte Bahn, Werkzeuge/Werkstuecke und Verriegelung noch nicht freigegeben'])


def extend(parts,base,cat):
    # Use only the established holder/fork/clamping envelope recipes and park screen.
    # Discard the old table magazine, frame post, wet cut, telescope and disc.
    import copy
    old=teller10.extend(copy.deepcopy(parts),base,cat)
    keep=[d for d in old if d['name'].startswith(('ATC_Gabel_','ATC_BT30_','Spannpaket_','ATC_Parkhaube_'))]
    result=[d for d in parts if d['group']!='20_ATC_Option']
    for d in keep:
        if d['name'].startswith('ATC_Gabel_'):
            d['ops'][0]['points']=[[x.replace('teller_radius-40','atc12_disc_d/2-5') if isinstance(x,str) else x for x in pt] for pt in d['ops'][0]['points']]
        d['revision_added']='12'
        d['status']='EINBAUSTUDIE_12_UNBESTAETIGT'
        d['note']+=' Revision12: uebernommene Entwurfshuelle, keine RATTM-Herstellergeometrie.'
        d['atc_motion']='feed' if d['name'].startswith(('ATC_Gabel_','ATC_BT30_')) else 'head' if d['name'].startswith('Spannpaket_') else 'fixed'
        if d['supply_kind']=='MAKE':d['item_id']='F12-'+d['name']
    new=[]
    def part(name,mat='reserviert',kind='RESERVE',motion='fixed',source='E12 Entwurf'):
        d=dict(id='T%03d'%(len(new)+1),name=name,group='20_ATC_Option',material=mat,
            datum=['0','0','0'],ops=[],status='EINBAUSTUDIE_12_UNBESTAETIGT',source=source,
            note='Vereinfachte Einbaustudie. Fehlende Kaufteilmasse/Anschluesse sind Entwurf; keine Passungs-/Festigkeits-/Betriebsfreigabe.',
            supply_kind=kind,item_id='F12-'+name if kind=='MAKE' else 'O10-TELLER',
            purchase_instance=name if kind=='MAKE' else 'O10-TELLER',
            manufacturing_released=False,atc_operational=False,revision_added='12',atc_motion=motion)
        d['filename']=d['id']+'_'+name;new.append(d);return d
    def pt(cx,cy,r,t,z):
        return (f'({cx})-({r})*teller_dir_x+({t})*teller_dir_y',
                f'({cy})-({r})*teller_dir_y-({t})*teller_dir_x',z)
    def rect(d,cx,cy,r0,r1,t0,t1,z,height,label):
        base.prism(d,[pt(cx,cy,r0,t0,z),pt(cx,cy,r1,t0,z),pt(cx,cy,r1,t1,z),pt(cx,cy,r0,t1,z)],height,(0,0,1),label=label)
    d=part('ATC_Saeulenanschluss_Entwurf','design_blue','MAKE')
    base.box(d,('atc12_mount_x',212,'atc12_base_z-70'),(12,100,210))
    d['note']+=' Liegt an nominaler rechter Saeulenflaeche; keine Gussbohrungen. Reales Aufmass und Befestigung fehlen.'
    d=part('ATC_Saeulenkonsole_Entwurf','design_blue','MAKE')
    points=[('atc12_mount_x+12',212,'atc12_base_z-15'),('atc12_mount_x+12',312,'atc12_base_z-15'),
            pt('atc12_base_x','atc12_base_y',90,140,'atc12_base_z-15'),
            pt('atc12_base_x','atc12_base_y',90,-100,'atc12_base_z-15'),
            pt('atc12_base_x','atc12_base_y',-90,-100,'atc12_base_z-15')]
    base.prism(d,points,15,(0,0,1),label='Tragplatte15mm_Entwurf')
    # Upper webs stay behind the product base's +87.5mm lateral edge.
    # Underside webs interfered with the table and X drive in the first screen.
    for i,ys,lateral in [(1,225,100),(2,275,120)]:
        d=part('ATC_Konsolenrippe_'+str(i)+'_Entwurf','design_blue','MAKE')
        ex=350*math.sqrt(3)/2+lateral*.5;ey=-175+lateral*math.sqrt(3)/2
        vx,vy=ex-81,ey-ys;length=math.hypot(vx,vy)
        base.prism(d,[('atc12_mount_x+12',ys,'atc12_base_z'),('atc12_mount_x+12',ys,'atc12_base_z+130'),
                      (ex,ey,'atc12_base_z')],8,(-vy/length,vx/length,0),label='Obere_Konsolenrippe8mm_Entwurf')
    d=part('ATC_RATTM_Grundplatte_Bildmasse',source='S11-RATTM-BILDER Bild4; Aussenmasse330x175x22')
    rect(d,'atc12_base_x','atc12_base_y','-atc12_base_l/2','atc12_base_l/2',
         '-atc12_base_w/2','atc12_base_w/2','atc12_base_z','atc12_base_t','Grundplatte_ohne_unbestaetigtes_Lochbild')
    for i,t in [(1,-60),(2,60)]:
        d=part('ATC_RATTM_Fuehrungshuelle_'+str(i))
        rect(d,'atc12_base_x','atc12_base_y',-165,165,t-10,t+10,'atc12_base_z+22',20,'Fuehrung_Entwurf20mm')
    d=part('ATC_RATTM_Schlittenhuelle',motion='feed')
    rect(d,'teller_cx','teller_cy','atc12_carriage_offset-60','atc12_carriage_offset+60',-84,84,
         'atc12_base_z+42',12,'Schlitten120x168x12_Entwurf_KEINE_Herstellerzeichnung')
    d=part('ATC_RATTM_Lagerhuelle',motion='feed')
    base.cyl(d,('teller_cx','teller_cy','atc12_base_z+54'),90,106,(0,0,1))
    d=part('ATC_RATTM_Motorhuelle',motion='feed')
    base.cyl(d,pt('teller_cx','teller_cy',100,0,'atc12_base_z+54'),80,86,(0,0,1))
    d['note']+=' Typenschild ZD4RK25GN-CM25W220V; dargestellte Abmessungen sind NICHT Typenschildwerte.'
    d=part('ATC_RATTM_Traegerhuelle',motion='feed')
    rect(d,'teller_cx','teller_cy',-45,145,-75.5,75.5,'teller_gauge_z-50',12,
         'Traeger190x151x12_Entwurf_KEINE_Herstellerzeichnung')
    d=part('ATC_RATTM_Tellerscheibe_Bildmasse','design_blue',motion='feed',source='S11-RATTM-BILDER Bild5; Scheibe280x16')
    base.cyl(d,('teller_cx','teller_cy','teller_gauge_z-30'),'atc12_disc_d','teller_plate_t',(0,0,1))
    d=part('ATC_RATTM_Zylinderhuelle')
    rect(d,'atc12_base_x','atc12_base_y',165,415,40,80,'atc12_base_z+28',40,'SU32X200_S_Bauraum_250x40_Entwurf')
    d=part('ATC_RATTM_Kolbenstangenhuelle',motion='feed')
    base.cyl(d,pt('atc12_base_x','atc12_base_y',165,60,'atc12_base_z+48'),12,
             '65+atc12_stroke*teller_feed',(-math.sqrt(3)/2,.5,0))
    return result+keep+new
