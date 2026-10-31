# -*- coding: utf-8 -*-
"""09 geometry extension, uses only existing native primitive contracts.
Actual catalogue interfaces vs custom study geometry are explicitly separated.
No machine control is performed by this module.
"""
import math
from cnc_ansichtsmodell01 import Frame
from blech06 import u_profile

CATALOG_PARAMETERS={
 'n09_grip_pitch':('K09-GN425','pitch'), 'n09_grip_h':('K09-GN425','height'),
 'n09_grip_d':('K09-GN425','d'), 'n09_grip_threaddepth':('K09-GN425','thread_depth_min'),
 'n09_gland_thread':('K09-GLAND20','thread_d'),'n09_gland_l':('K09-GLAND20','thread_l'),
 'n09_gland_d':('K09-GLAND20','od'),'n09_gland_total_h':('K09-GLAND20','total_h_max'),
 'n09_tool_d':('K09-BT30ER20','gauge_d'),'n09_tool_projection':('K09-BT30ER20','projection'),
 'n09_tool_total':('K09-BT30ER20','total_l'),'n09_tool_nut_d':('K09-BT30ER20','nut_d')}
CUSTOM_DEFAULTS=dict(atc_pitch=94.,atc_pocket_count=6.,atc_y=-53.,atc_gauge_above_table=135.,
 atc_base_l=620.,atc_base_d=100.,atc_base_t=8.,atc_beam_t=4.,atc_bend_r=6.,
 atc_locator_h=10.,atc_locator_w=56.,atc_locator_bore=34.6,
 atc_flange_d_assumed=46.,atc_flange_h_assumed=8.,atc_tool_extra=35.,atc_pullstud_allowance=30.,atc_clearance=15.,
 cable_plate_t=2.,cable_plate_seal_t=.5)

def atc_report(p,v):
    count=int(p['atc_pocket_count'])
    if count!=p['atc_pocket_count'] or count!=6:raise ValueError('ATC-Platzzahl muss in dieser Revision genau6 sein.')
    if p['atc_pitch']<p['atc_locator_w']+8:raise ValueError('ATC-Teilung zu klein für Lokator und Montagezugang.')
    if p['atc_base_l']<max(480,(count-1)*p['atc_pitch']+140):raise ValueError('ATC-Grundplatte zu kurz.')
    if p['atc_locator_bore']<=p['n09_tool_nut_d']:raise ValueError('Werkzeughalter passt nicht durch Lokator.')
    gauge=v['table_top_z']+p['atc_gauge_above_table']
    # To traverse above OTHER pockets, lift the cutter tip above the highest retained holder.
    tallest_stored=gauge+(p['n09_tool_total']-p['n09_tool_projection'])+p['atc_pullstud_allowance']
    safe=tallest_stored+p['n09_tool_projection']+p['atc_tool_extra']+p['atc_clearance']
    max_face=v['spindle_face_z']+p['head_down'];min_face=max_face-p['z_travel_used']
    pockets=[]
    for i in range(count):
        xx=(i-(count-1)/2)*p['atc_pitch'];yy=p['atc_y']
        pockets.append(dict(pocket=i+1,table_local_x_mm=xx,table_local_y_mm=yy,
          required_pos_x_mm=-xx,required_pos_y_mm=-yy,required_gauge_z_mm=gauge,
          xy_in_nominal_travel=abs(xx)<=p['travel_x']/2 and abs(yy)<=p['travel_y']/2))
    return dict(schema='ATC09_PLANNING_ONLY',original_spindle='SK30/M12 DIN2080',
        required_spindle_interface='BT30 automatic clamping',machine_operation_enabled=False,
        spindle_clamping_verified=False,trajectory_verified=False,pockets=pockets,
        gauge_z_mm=gauge,highest_stored_holder_z_mm=tallest_stored,safe_traverse_gauge_z_mm=safe,
        min_gauge_z_mm=min_face,max_gauge_z_mm=max_face,
        nominal_reach_ok=all(q['xy_in_nominal_travel'] for q in pockets) and min_face<=gauge<=max_face and safe<=max_face,
        safe_retract_reserve_mm=max_face-safe,tool_length_extra_mm=p['atc_tool_extra'],
        reserved_table_strip_mm=[p['atc_base_l'],p['atc_base_d']],
        blockers=['Automatische Spindelspannung fehlt','BT30 passt nicht als bestätigtes System an DIN2080',
          'Spindelorientierung und Halterindexierung offen','Anzugsbolzen nur als 30mm-Reserve, Artikel unbestätigt',
          'Werkstück/Spannmittel und reale Wechselbahn nicht geprüft','Spänehaube oben/Antrieb fehlen',
          'Sichere Ventil-/Sensor-/Freigabekette fehlt'])

def extend(parts,base,cat):
    """Adds source-linked bodies, plus genuine bores in the affected OWN sheet parts."""
    by={d['name']:d for d in parts};new=[]
    def part(name,group='19_Normdetails',mat='silver',at=(0,0,0),item=None,instance=None,note='Eigener Entwurf; Einzelzeichnung und Verbindungsauslegung offen.'):
        q=dict(name=name,group=group,material=mat,datum=[str(x) for x in at],ops=[],
          status='KATALOGSCHNITTSTELLE_VEREINFACHT' if item else 'KONSTRUKTIONSENTWURF',
          source=' '.join(cat[item]['source_ids']) if item else 'Eigener Konstruktionsentwurf 09',
          note=(cat[item]['note']+' '+note) if item else note,
          supply_kind='BUY' if item else 'MAKE',item_id=item or 'F09-'+name,
          purchase_instance=instance or name,manufacturing_released=False,revision_added='09')
        new.append(q);return q
    def hexagon(f,q,o,af,h,op='add',label='Sechskant_Nenn'):
        rad=af/math.sqrt(3)
        pts=[f.point((f'({o[0]})+({rad*math.cos(math.pi/6+i*math.pi/3):.12g})',f'({o[1]})+({rad*math.sin(math.pi/6+i*math.pi/3):.12g})',o[2])) for i in range(6)]
        base.prism(q,pts,h,f.axis,op,label)
    def screw(name,f,seat,d,l,group='19_Normdetails'):
        item=f'N09-S{d}x{l}';k=cat[item]['dims'];q=part(name,group,at=f.point((0,0,f'({seat})-{l}')),item=item)
        f.cyl(q,(0,0,f'({seat})-{l}'),d,l,label='ISO4762_Nennschaft_kein_Gewindegang')
        f.cyl(q,(0,0,seat),k['head_d'],k['head_h'],label='ISO4762_Kopf')
        hexagon(f,q,(0,0,f'({seat})+{d*.5}'),k['socket'],d*.5+.2,'cut','Innensechskant_vereinfacht')
        return q
    def washer(name,f,z,d,group='19_Normdetails'):
        item=f'N09-W{d}';k=cat[item]['dims'];q=part(name,group,at=f.point((0,0,z)),item=item)
        f.cyl(q,(0,0,z),k['do'],k['h'],label='ISO7089')
        f.cyl(q,(0,0,f'({z})-0.1'),k['di'],k['h']+.2,'cut','Bohrung')
        return q
    def nut5(name,f,z,group='19_Normdetails'):
        q=part(name,group,at=f.point((0,0,z)),item='N09-N5');hexagon(f,q,(0,0,z),8,4.7)
        f.cyl(q,(0,0,f'({z})-0.1'),5,4.9,'cut','M5_Nenn_kein_Kernloch');return q
    # Stationary service handles. Approved moving front door remains byte-identical.
    locs=[('links','Staender_Blechschuerze_links',('enc_left-2-sheet_t','stand_cy',-250),((0,1,0),(0,0,-1),(-1,0,0))),
          ('rechts','Staender_Blechschuerze_rechts',('enc_right+2+sheet_t','stand_cy',-250),((0,1,0),(0,0,1),(1,0,0))),
          ('KSS','KSS_Serviceklappe_hinten',(0,567,-225),((1,0,0),(0,0,-1),(0,1,0)))]
    for tag,target,origin,cols in locs:
        f=Frame(origin,cols)
        q=part('Servicegriff_'+tag,at=f.point((0,0,0)),item='K09-GN425',note='Schnittstellen Ø12/160/H51. Bogen R14 durch überlappende Zylinder vereinfacht, keine exakte Sichtkontur.')
        f.cyl(q,('-n09_grip_pitch/2',0,0),'n09_grip_d','n09_grip_h-n09_grip_d/2',label='Grifffuss_links')
        base.cyl(q,f.point(('-n09_grip_pitch/2',0,'n09_grip_h-n09_grip_d/2')),'n09_grip_d','n09_grip_pitch',cols[0],label='Griffsteg_Radien_vereinfacht')
        f.cyl(q,('n09_grip_pitch/2',0,0),'n09_grip_d','n09_grip_h-n09_grip_d/2',label='Grifffuss_rechts')
        for side in(-1,1):f.cyl(q,(f'{side}*n09_grip_pitch/2',0,-.1),6,'n09_grip_threaddepth+0.1','cut','M6_Nenngewinde')
        back=part('Griff_Hinterlegung_'+tag,at=f.point(('-n09_grip_pitch/2-15',-15,'-sheet_t-2')))
        f.box(back,('-n09_grip_pitch/2-15',-15,'-sheet_t-2'),('n09_grip_pitch+30',30,2),label='Hinterlegblech_2mm')
        for i,side in enumerate((-1,1),1):
            u=f'{side}*n09_grip_pitch/2'
            f.cyl(by[target],(u,0,'-sheet_t-.1'),6.6,'sheet_t+.2','cut','09_Griffdurchgang_'+str(i))
            f.cyl(back,(u,0,'-sheet_t-2.1'),6.6,2.2,'cut','09_Griffdurchgang_'+str(i))
            # Reverse frame, screws enter from inside toward exterior handle.
            rf=Frame(f.point((u,0,'-sheet_t-2')), (cols[0],tuple(-a for a in cols[1]),tuple(-a for a in cols[2])))
            washer('Griffscheibe_'+tag+str(i),rf,0,6);screw('Griffschraube_'+tag+str(i),rf,1.6,6,16)
        by[target]['note']+=' 09: zwei Ø6.6-Durchgänge für GN425 und 2mm-Hinterlegung; keine Hebefunktion.'
    # Gland plate on dry cabinet bottom: mounting hole in shell and six real through connections.
    g='19_Normdetails';f=Frame(('cab_x+190','cab_y+190','cab_z-2.5'),((1,0,0),(0,1,0),(0,0,1)))
    shell=by['Schaltschrank_Hohlschale']
    f.box(shell,(-45,-65,2.4),(90,130,3.2),'cut','09_Kabeleinfuehrungsfenster')
    plate=part('Kabelplatte_09',at=f.point((-60,-80,0)),note='Neue 2mm-Platte unter Schrankboden. Serienmäßige Flanschöffnung der realen NSYCRN86300 zuerst messen; diese Fensterform ist ein eigener Vorschlag.')
    f.box(plate,(-60,-80,0),(120,160,'cable_plate_t'),label='Blechplatte_2mm')
    seal=part('Kabelplatte_Flachdichtung_09',mat='dark',at=f.point((-60,-80,2)),note='Reservierte Flachdichtung 0.5mm; Material/Artikel und IP-Nachweis offen.')
    seal.update(supply_kind='RESERVE',item_id='R09-PLATESEAL')
    f.box(seal,(-60,-80,2),(120,160,'cable_plate_seal_t'))
    f.box(seal,(-45,-65,1.9),(90,130,'cable_plate_seal_t+.2'),'cut','Dichtungsfenster')
    # gland thread 9mm enters upward; external shell below panel, total catalogue height37 includes thread.
    for i,yy in enumerate((-35,35),1):
        f.cyl(plate,(0,yy,-.1),20.5,'cable_plate_t+.2','cut','M20_Durchgang')
        q=part('LAPP_53111020_'+str(i),at=f.point((0,yy,'-n09_gland_total_h+n09_gland_l')),item='K09-GLAND20')
        f.cyl(q,(0,yy,'-n09_gland_total_h+n09_gland_l'),'n09_gland_d','n09_gland_total_h-n09_gland_l',label='LAPP_Gehause_Huellprofil')
        f.cyl(q,(0,yy,0),'n09_gland_thread','n09_gland_l',label='M20_Nenngewindehalse')
        f.cyl(q,(0,yy,'-n09_gland_total_h+n09_gland_l-.1'),10,'n09_gland_total_h+.2','cut','Kabeldurchgang_Darstellung_10mm')
        q=part('LAPP_53119020_'+str(i),at=f.point((0,yy,2)),item='K09-LOCK20')
        f.cyl(q,(0,yy,2),29.7,.9,label='LAPP_Bund')
        hexagon(f,q,(0,yy,2.9),27,5.1)
        f.cyl(q,(0,yy,1.9),20,6.2,'cut','M20_Nenndurchgang')
    for i,(xx,yy) in enumerate([(x,y) for x in(-52,52) for y in(-72,0,72)],1):
        for target in [plate,seal,shell]:f.cyl(target,(xx,yy,-.1),5.5,5.8,'cut','09_Plattenverschraubung_'+str(i))
        # stack: lower washer1, plate2, seal.5, shell3, upper washer1, nut4.7
        sf=Frame(f.point((xx,yy,0)),((1,0,0),(0,-1,0),(0,0,-1)))
        washer('Kabelplatte_Scheibe_unten_'+str(i),sf,0,5)
        screw('Kabelplatte_Schraube_'+str(i),sf,1,5,16)
        uf=Frame(f.point((xx,yy,5.5)),((1,0,0),(0,1,0),(0,0,1)))
        washer('Kabelplatte_Scheibe_oben_'+str(i),uf,0,5);nut5('Kabelplatte_Mutter_'+str(i),uf,1)
    # Six-pocket TABLE-MOUNTED magazine study. Stock spindle remains unmodified and NOT ATC compatible.
    g='20_ATC_Option';f=Frame(('pos_x','pos_y','table_top_z'),((1,0,0),(0,1,0),(0,0,1)))
    note='ATC-Einbaustudie, NICHT einsatzfähig mit SK30/M12. BT30-Spannung, Orientierung, Anzugsbolzen, Indexierung, Schutzdeckel und Steuerung offen.'
    q=part('ATC_Grundplatte',g,'design_blue',f.point(('-atc_base_l/2',-90,0)),note=note)
    f.box(q,('-atc_base_l/2',-90,0),('atc_base_l','atc_base_d','atc_base_t'),label='Grundplatte_Eigenteil')
    for i,(xx,yy) in enumerate([(x,y) for x in('-atc_base_l/2+15','atc_base_l/2-15') for y in(-53,0)],1):
        f.cyl(q,(xx,yy,-.1),11,'atc_base_t+.2','cut','M10_Befestigung_Nut')
        sf=Frame(f.point((xx,yy,0)),f.columns)
        washer('ATC_Fussscheibe_'+str(i),sf,'atc_base_t',10,g)
        screw('ATC_Fussschraube_'+str(i),sf,'atc_base_t+2',10,25,g)
        tn=part('ATC_DIN508_'+str(i),g,'dark',sf.point((-9,-9,-16)),item='K09-TNUT10',note=note)
        sf.box(tn,(-9,-9,-16),(18,18,7),label='DIN508_Fuss_Maximalhuelle')
        sf.box(tn,(-9,-5.85,-9),(18,11.7,7),label='DIN508_Hals')
        sf.cyl(tn,(0,0,-16.1),10,14.2,'cut','M10_Nenngewinde')
    for i,xx in enumerate(('-atc_base_l/2+25','atc_base_l/2-33'),1):
        q=part('ATC_Staenderwange_'+str(i),g,'design_blue',f.point((xx,-70,'atc_base_t')),note=note+' Geschweißter Konsolenentwurf.')
        f.box(q,(xx,-70,'atc_base_t'),(8,60,'atc_gauge_above_table-20-atc_beam_t-atc_base_t'),label='Stehblech_8mm')
    beam=part('ATC_Magazintraeger_Kantblech',g,'sheet',f.point(('-atc_base_l/2+20',-90,'atc_gauge_above_table-20')),note=note)
    u_profile(beam,f.point(('-atc_base_l/2+20',-90,'atc_gauge_above_table-20')),100,20,'atc_base_l-40',axes=((0,1,0),(0,0,-1),(1,0,0)),thickness='atc_beam_t')
    beam['sheetmetal']['bend_radius']='atc_bend_r'
    # Axial plan: support block top at gauge-10, flange envelope starts gauge-10.
    for i in range(6):
        xx=f'({i}-2.5)*atc_pitch';yy='atc_y';gz='atc_gauge_above_table'
        f.cyl(beam,(xx,yy,gz+'-25'),'atc_locator_bore',6,'cut','Tasche_Durchlass_'+str(i+1))
        loc=part('ATC_Lokator_Entwurf_'+str(i+1),g,'dark',f.point((xx,yy,gz+'-20')),note=note+' Eigene Schwerkraftablage, KEINE kopierte DES-Gabel. Formschluss gegen Verdrehen fehlt.')
        f.box(loc,(xx+'-atc_locator_w/2',yy+'-atc_locator_w/2',gz+'-20'),('atc_locator_w','atc_locator_w','atc_locator_h'),label='Lokator_Alu_POM_Auswahl_offen')
        f.cyl(loc,(xx,yy,gz+'-20.1'),'atc_locator_bore','atc_locator_h+.2','cut','Halter_Durchlass')
        for j,side in enumerate((-1,1),1):
            sx=xx+f'+({side}*21)';sy=yy+'-19'
            f.cyl(loc,(sx,sy,gz+'-20.1'),5.5,'atc_locator_h+.2','cut','M5_Lokatorbefestigung')
            f.cyl(beam,(sx,sy,gz+'-25'),5.5,6,'cut','M5_Gegenbohrung_Lokator')
            sf=Frame(f.point((sx,sy,gz+'-10')),f.columns)
            washer(f'ATC_Lokator_Scheibe_oben_{i+1}_{j}',sf,0,5,g)
            screw(f'ATC_Lokator_Schraube_{i+1}_{j}',sf,1,5,25,g)
            uf=Frame(f.point((sx,sy,gz+'-20-atc_beam_t')),((1,0,0),(0,-1,0),(0,0,-1)))
            washer(f'ATC_Lokator_Scheibe_unten_{i+1}_{j}',uf,0,5,g)
            nut5(f'ATC_Lokator_Mutter_{i+1}_{j}',uf,1,g)
        tool=part('ATC_BT30_ER20_70_Raumhuelle_'+str(i+1),g,'steel',f.point((xx,yy,gz+'-n09_tool_projection')),item='K09-BT30ER20',note=note+' 7:24-Konus und Flansch vereinfachte Raumkontur. Kein Anzugsbolzen/Spannzangensatz enthalten.')
        f.cyl(tool,(xx,yy,gz+'-n09_tool_projection'),'n09_tool_nut_d','n09_tool_projection',label='ER20_Nut_Koerper_Raumhuelle')
        f.cyl(tool,(xx,yy,gz+'-10'),'atc_flange_d_assumed','atc_flange_h_assumed',label='Flansch_ANNAHME_NICHT_KATALOGDETAIL')
        base.cone(tool,f.point((xx,yy,gz)),'n09_tool_d','n09_tool_d-(n09_tool_total-n09_tool_projection)*7/24',
                  'n09_tool_total-n09_tool_projection',(0,0,1),label='BT30_Nennkonus_Raumstudie')
    # Three-sided swarf shield; deliberately no fake automatic lid mechanism.
    sh=part('ATC_Ruecken_Spritzschutz_Kantblech',g,'sheet',f.point(('-atc_base_l/2-2',-92,0)),note=note+' Oben offen; kein ausreichender Schutz freiliegender Kegel bei Bearbeitung.')
    u_profile(sh,f.point(('-atc_base_l/2-2',-92,0)),'atc_base_l+4',25,'atc_gauge_above_table-25',axes=((1,0,0),(0,1,0),(0,0,1)))
    # rear shield and base share seam only, weld sketch; not a bolt connection falsely shown.
    for idx,q in enumerate(new,1):
        q['id']='C%03d'%idx;q['filename']=q['id']+'_'+q['name']
        if q['group']=='20_ATC_Option':q['atc_operational']=False
    return parts+new
