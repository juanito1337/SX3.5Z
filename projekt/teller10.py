"""Table-independent carousel and clamping SPACE STUDY, not supplier CAD.

Only existing primitive contracts are used. No machine control or force claims.
"""
import math
from collections import OrderedDict

DEFAULTS = dict(teller_radius=180., teller_park_distance=math.hypot(540,260),
    teller_dir_x=540/math.hypot(540,260), teller_dir_y=260/math.hypot(540,260),
    teller_feed=0., teller_index_cos=1., teller_index_sin=0., teller_gauge_z=370.,
    teller_plate_t=10., teller_post_side=40., teller_collar_top=125.,
    clamp_space_d=80., clamp_space_h=100., release_space_d=100., release_space_h=80.)
UNITLESS={'teller_dir_x','teller_dir_y','teller_feed','teller_index_cos','teller_index_sin'}
DERIVED=OrderedDict([
    ('teller_park_x','-teller_park_distance*teller_dir_x'),
    ('teller_park_y','-teller_park_distance*teller_dir_y'),
    ('teller_cx','-(teller_park_distance-teller_feed*(teller_park_distance-teller_radius))*teller_dir_x'),
    ('teller_cy','-(teller_park_distance-teller_feed*(teller_park_distance-teller_radius))*teller_dir_y'),
    ('teller_post_x','enc_left+tube_side/2'),
    ('teller_post_y','enc_front+115'),
])


def validate(p,v):
    for name in DEFAULTS:
        value=p[name]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError('Ungueltiger Tellerparameter: '+name)
        if name not in UNITLESS and value<=0:
            raise ValueError('Positive Tellerlaenge erforderlich: '+name)
    if not 0<=p['teller_feed']<=1:raise ValueError('Tellerzustellung muss0..1 sein')
    for a,b in [('teller_dir_x','teller_dir_y'),('teller_index_cos','teller_index_sin')]:
        if not math.isclose(p[a]**2+p[b]**2,1,abs_tol=1e-9):
            raise ValueError('Teller-Richtungsvektor muss normiert sein')
    if p['teller_dir_x']<=0 or p['teller_dir_y']<=0:raise ValueError('Parkrichtung vorn links erforderlich')
    if p['teller_radius']<170 or p['teller_park_distance']<=p['teller_radius']:
        raise ValueError('Teilkreis/Hub zu klein fuer Kopf- und Halterstudie')
    outer=p['teller_radius']+30
    if not (v['enc_left']+p['window_t']+p['sheet_t'] < v['teller_park_x']-outer
            and v['teller_park_y']-outer >= v['enc_front']+p['sheet_t']):
        raise ValueError('Geparkte Tellerhuelle ausserhalb Einhausung')
    max_z=v['spindle_face_z']+p['head_down']
    if not max_z-p['z_travel_used'] <= p['teller_gauge_z'] <= max_z:
        raise ValueError('Uebergabehoehe ausserhalb nominalem Spindelhub')
    if p['teller_gauge_z']-p['n09_tool_projection']-p['atc_tool_extra'] < v['table_top_z']+85:
        raise ValueError('Geparkte Werkzeughuelle unterschreitet85mm nominalen Tischabstand')
    if p['teller_post_side']!=40 or p['teller_plate_t']!=10:
        raise ValueError('Stuetzen-/Gabelanschluss fuer40mm-Stuetze und10mm-Teller ausgelegt; Neupruefung erforderlich')
    wet_edge_max=-8-.14*(v['teller_post_x']-24+227)-.025*(v['teller_post_y']-24-382)
    wet_edge_max+=p['sheet_t']*math.sqrt(1+.14**2+.025**2)
    if p['teller_collar_top'] < wet_edge_max+15 or p['teller_collar_top']>=250:
        raise ValueError('Kragen muss15mm ueber hoechster nasser Blechkante und unter Konsole enden')
    if v['head_top_z']+p['head_down']+70+p['clamp_space_h']+p['release_space_h'] >= p['enclosure_h']:
        raise ValueError('Spann-/Loesereserve reicht ueber Dach bei hoechstem Kopf')
    return True


def report(p,v):
    validate(p,v)
    r=p['teller_radius']; ux=p['teller_dir_x'];uy=p['teller_dir_y']
    pockets=[]
    for i in range(8):
        angle=2*math.pi*i/8
        pockets.append(dict(pocket=i+1,index_rotation_deg=-i*45.,
            pickup_axis_xy_mm=[-ux*r+r*ux,-uy*r+r*uy],
            required_gauge_z_mm=p['teller_gauge_z']))
    return dict(schema='ATC10_SPACE_STUDY',layout='RADIAL_TELESCOPIC_CAROUSEL',
        original_spindle='SK30/M12 DIN2080',required_spindle_interface='BT30 automatic clamping',
        clamping_package_required=True,clamping_package_status='RESERVED_SPACE_NOT_ENGINEERED',
        machine_operation_enabled=False,spindle_clamping_verified=False,trajectory_verified=False,
        atc_operational=False,nominal_reach_ok=False,pockets=pockets,
        park_center_xy_mm=[v['teller_park_x'],v['teller_park_y']],
        pickup_center_xy_mm=[-ux*r,-uy*r],required_feed_mm=p['teller_park_distance']-r,
        reserved_table_strip_mm=[0,0],table_mounting=False,
        gauge_z_mm=p['teller_gauge_z'],
        nominal_local_workpiece_height_under_park_mm=p['teller_gauge_z']-p['n09_tool_projection']-p['atc_tool_extra']-v['table_top_z']-15,
        support='Upper left stand beam; strength, joints and sealed tray penetration unverified',
        required_sequence='Side-entry forks and separate magazine feed; no traverse above all stored tools',
        blockers=['Spannpaket/Patrone nicht ausgewaehlt oder ausgelegt',
          'SK30/M12 unveraendert; keine bestaetigte BT30-Schnittstelle',
          'Teleskopzustellung Eigenentwurfsraum; kein bestaetigtes Kaufteil',
          'Gabelretention, Orientierung, Sensoren, Verriegelung und Fehlerfaelle offen',
          'Vollstaendige Wechselbahn, Werkzeug/Werkstueck, Schutz und Belastung nicht freigegeben'])


def extend(parts,base,cat):
    parts=[d for d in parts if d['group']!='20_ATC_Option']
    by={d['name']:d for d in parts};new=[]
    def part(name,mat='reserviert',kind='RESERVE',item='O10-TELLER',group='20_ATC_Option'):
        d=dict(id='D%03d'%(len(new)+1),name=name,group=group,material=mat,
            datum=['0','0','0'],ops=[],status='ENTWURF_10_UNBESTAETIGT',
            source='E10 Layoutannahme01.11.2026; keine Lieferantenzeichnung',
            note='Ungepruefter Entwurf/Bauraum. Keine Passung, Tragfaehigkeit, Retention oder automatische Spannung nachgewiesen.',
            supply_kind=kind,item_id=item if kind!='MAKE' else 'F10-'+name,
            purchase_instance=item if kind=='RESERVE' else name,
            manufacturing_released=False,atc_operational=False,revision_added='10')
        d['filename']=d['id']+'_'+name;new.append(d);return d
    # Foot on existing upper side beam, not on the wet sheet or table.
    d=part('ATC_Stuetzenfuss_Entwurf','design_blue','MAKE')
    base.box(d,('teller_post_x-30','teller_post_y-50',-20),(60,100,8))
    d=part('ATC_Standstuetze_Entwurf','design_blue','MAKE')
    base.box(d,('teller_post_x-20','teller_post_y-20',-12),(40,40,262))
    base.box(d,('teller_post_x-17','teller_post_y-17',-12.1),(34,34,262.2),'cut','Rohr_3mm_Entwurf')
    # Wet penetration: real opening, closed upstand, remaining gland/seal unselected.
    base.box(by['KSS_Leitblech_links_vorn'],('teller_post_x-24','teller_post_y-24',-30),
             (48,48,200),'cut','ATC_Stuetzendurchfuehrung')
    d=part('ATC_KSS_Dichtkragen_Entwurf','sheet','MAKE',group='17_KSS')
    base.box(d,('teller_post_x-24','teller_post_y-24',60),(48,48,'teller_collar_top-60'))
    base.box(d,('teller_post_x-22','teller_post_y-22',59.9),(44,44,'teller_collar_top-59.8'),'cut','Umlaufender_Kragen_2mm')
    d['note']+=' Stuetze40mm innen,44mm Innenoeffnung; Dichtmanschette und umlaufende Schweissnaht noch auszulegen.'
    # A structural console at the park point, cardinal outline avoids hidden rotation APIs.
    d=part('ATC_Standkonsole_Entwurf','design_blue','MAKE')
    pts=[('teller_post_x-20','teller_post_y-20',250),('teller_post_x+20','teller_post_y-20',250),
         ('teller_park_x+35','teller_park_y-30',250),('teller_park_x+35','teller_park_y+30',250),
         ('teller_post_x-20','teller_post_y+20',250)]
    base.prism(d,pts,15,(0,0,1),label='Konsole_Entwurf_ohne_Festigkeitsnachweis')
    # Explicit envelope only: no invented rail bearing or matching200mm supplier stroke.
    d=part('ATC_Teleskopzustellung_Bauraum')
    def feedpoint(cx,cy,longitudinal,lateral,z):
        return (f'({cx})+({longitudinal})*teller_dir_x-({lateral})*teller_dir_y',
                f'({cy})+({longitudinal})*teller_dir_y+({lateral})*teller_dir_x',z)
    pts=[feedpoint('teller_park_x','teller_park_y',-50,-30,265),
         feedpoint('teller_cx','teller_cy',50,-30,265),
         feedpoint('teller_cx','teller_cy',50,30,265),
         feedpoint('teller_park_x','teller_park_y',-50,30,265)]
    base.prism(d,pts,25,(0,0,1),label='Teleskop_Gesamthuelle_KEIN_Kaufteil')
    d=part('ATC_Indexierantrieb_Lager_Bauraum')
    base.cyl(d,('teller_cx','teller_cy',290),90,'teller_gauge_z-320',(0,0,1))
    d=part('ATC_Teller_Eigenentwurf','design_blue','MAKE')
    base.cyl(d,('teller_cx','teller_cy','teller_gauge_z-30'),'2*(teller_radius-25)','teller_plate_t',(0,0,1))
    d=part('ATC_Parkhaube_Ruecken_Entwurf','sheet','MAKE')
    base.cyl(d,('teller_park_x','teller_park_y','teller_gauge_z-95'),416,185,(0,0,1))
    base.cyl(d,('teller_park_x','teller_park_y','teller_gauge_z-95.1'),412,185.2,(0,0,1),'cut','Gerolltes_2mm_Blech_Entwurf')
    pts=[feedpoint('teller_park_x','teller_park_y',0,-220,'teller_gauge_z-95.1'),
         feedpoint('teller_park_x','teller_park_y',230,-220,'teller_gauge_z-95.1'),
         feedpoint('teller_park_x','teller_park_y',230,220,'teller_gauge_z-95.1'),
         feedpoint('teller_park_x','teller_park_y',0,220,'teller_gauge_z-95.1')]
    base.prism(d,pts,185.2,(0,0,1),'cut','Offene_Zustellseite_KEIN_dichter_Abschluss')
    d['note']+=' Stationaerer halboffener Spritzschirm; Klappe/Dichtung/Montage noch offen.'
    d=part('ATC_Parkhaube_Dach_Entwurf','sheet','MAKE')
    base.cyl(d,('teller_park_x','teller_park_y','teller_gauge_z+90'),416,2,(0,0,1))
    for i in range(8):
        c=round(math.cos(i*math.pi/4),12);s=round(math.sin(i*math.pi/4),12)
        ca=f'(({c})*teller_index_cos-({s})*teller_index_sin)'
        sa=f'(({s})*teller_index_cos+({c})*teller_index_sin)'
        dx=f'(teller_dir_x*({ca})-teller_dir_y*({sa}))'
        dy=f'(teller_dir_y*({ca})+teller_dir_x*({sa}))'
        def pt(rad,tangent,z):
            return (f'teller_cx+({rad})*({dx})-({tangent})*({dy})',
                    f'teller_cy+({rad})*({dy})+({tangent})*({dx})',z)
        d=part('ATC_Gabel_Raumreserve_'+str(i+1),'dark')
        pts=[pt('teller_radius-40',-28,'teller_gauge_z-20'),pt('teller_radius+25',-28,'teller_gauge_z-20'),
             pt('teller_radius+25',28,'teller_gauge_z-20'),pt('teller_radius-40',28,'teller_gauge_z-20')]
        base.prism(d,pts,10,(0,0,1),label='Gabel_Raumreserve_KEINE_Retention')
        base.cyl(d,pt('teller_radius',0,'teller_gauge_z-20.1'),'atc_locator_bore',10.2,(0,0,1),'cut','Halterdurchgang')
        pts=[pt('teller_radius', '-atc_locator_bore/2','teller_gauge_z-20.1'),
             pt('teller_radius+30','-atc_locator_bore/2','teller_gauge_z-20.1'),
             pt('teller_radius+30','atc_locator_bore/2','teller_gauge_z-20.1'),
             pt('teller_radius','atc_locator_bore/2','teller_gauge_z-20.1')]
        base.prism(d,pts,10.2,(0,0,1),'cut','Radial_offener_Entnahmeweg')
        d=part('ATC_BT30_ER20_70_Raumhuelle_'+str(i+1),'steel','BUY','K09-BT30ER20')
        d['source']=' '.join(cat['K09-BT30ER20']['source_ids'])
        d['note']+=' Halterhauptmasse ausK09-BT30ER20; Flansch nur unbestaetigte Raumhuelle.'
        base.cyl(d,pt('teller_radius',0,'teller_gauge_z-n09_tool_projection'),'n09_tool_nut_d','n09_tool_projection',(0,0,1))
        base.cyl(d,pt('teller_radius',0,'teller_gauge_z-10'),'atc_flange_d_assumed','atc_flange_h_assumed',(0,0,1))
        base.cone(d,pt('teller_radius',0,'teller_gauge_z'),'n09_tool_d',
                  'n09_tool_d-(n09_tool_total-n09_tool_projection)*7/24','n09_tool_total-n09_tool_projection',(0,0,1))
    # Three independent axial function envelopes, NOT a retrofit of the stock SK30 internals.
    for name,z,diam,height in [
        ('Spannpaket_Zugstangenanschluss_Reserve','head_top_z+54',28,16),
        ('Spannpaket_Federraum_Reserve','head_top_z+70','clamp_space_d','clamp_space_h'),
        ('Spannpaket_Loeseeinheit_Reserve','head_top_z+70+clamp_space_h','release_space_d','release_space_h')]:
        d=part(name,item='O09-SPINDEL')
        base.cyl(d,(0,0,z),diam,height,(0,0,1),label='UNBESTAETIGTER_Funktionsraum_KEIN_Spannnachweis')
    return parts+new
