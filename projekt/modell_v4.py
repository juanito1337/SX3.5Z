# -*- coding: utf-8 -*-
"""SX3.5Z v4: photo-based parts-first assembly definition, millimetres.
Only Python standard library. Geometry uses native-friendly primitives.
Not a manufacturer's model. No confirmed user measurements; every inferred
size remains explicitly tagged. Existing lead screws are NOT ball screws.
"""
import ast, copy, json, math, os, re
from collections import OrderedDict
import v3_geometriebasis as old
VERSION='4.8'
SOURCE='72 Nutzerfotos im Paket; Anleitung; Geometrie v3 als Ausgangspunkt. Nicht vermessene Rekonstruktion.'
SPECS=copy.deepcopy(old.SPECS)
DERIVED=copy.deepcopy(old.DERIVED)
PALETTE=dict(old.PALETTE, copper=(0.72,0.38,0.14,1), bronze=(0.48,0.36,0.13,1), pcb=(0.02,0.30,0.17,1), orange=(0.85,0.22,0.04,1), grey=(0.30,0.32,0.34,1), core=(0.38,0.39,0.36,1), white=(0.80,0.79,0.72,1), machine_red=(0.72,0.06,0.08,1), castiron=(0.36,0.37,0.39,1), aluminum=(0.76,0.76,0.74,1))
GROUPS=OrderedDict([
 ('01_Basis','Basis und Y-Lagerung'),('02_Saeule','Gusssaeule und Z-Originalantrieb'),
 ('03_Kreuzschlitten','Kreuzschlitten, Muttern und Y-Massstab'),('04_Tisch','X-Tisch, Originalspindeln und Handraeder'),
 ('05_Spindelkopf','Kopfguss, Pinole, Spindel und Bedienmechanik'),('06_Spindelmotor','W92-1000F und Riemenantrieb'),
 ('07_Bedienpanel','Bediengehaeuse, Frontplatte und Taster'),('08_Blechsaeule','Blechsaeule und Kabelanschluesse'),
 ('09_Elektrik','Elektrik-Einbaukoerper nach Fotos'),('10_Schutz','Faltenbaelge, Schutzhaube und Arbeitsleuchte')])
LAYERS={g:(i+1)*10 for i,g in enumerate(GROUPS)}
PH={
 'base':'1000047828.jpg;1000047829.jpg;1000047830.jpg;1000047831.jpg',
 'column':'1000047833.jpg;1000047834.jpg;1000047835.jpg;1000047836.jpg;1000047837.jpg;1000047838.jpg;1000047839.jpg;1000047840.jpg;1000047841.jpg;1000047842.jpg',
 'table':'1000047824.jpg;1000047826.jpg',
 'saddle':'1000047959.jpg;1000047960.jpg;1000047961.jpg;1000047962.jpg;1000047963.jpg',
 'head':'1000047964.jpg;1000047965.jpg;1000047966.jpg;1000047969.jpg;1000047970.jpg;1000047972.jpg;1000047981.jpg;1000047983.jpg;1000047985.jpg;1000047987.jpg;1000047988.jpg;1000047989.jpg;1000047990.jpg;1000047991.jpg',
 'screws':'1000047992.jpg;1000047993.jpg;1000047994.jpg;1000047999.jpg;1000048000.jpg;1000048001.jpg;1000048002.jpg;1000048003.jpg',
 'zmotor':'1000047995.jpg;1000047996.jpg;1000047997.jpg;1000047998.jpg',
 'motor':'1000048004.jpg;1000048006.jpg;1000048007.jpg;1000048008.jpg;1000048009.jpg',
 'elec':'1000048010.jpg;1000048011.jpg;1000048012.jpg;1000048013.jpg;1000048014.jpg;1000048015.jpg;1000048016.jpg;1000048017.jpg;1000048018.jpg',
 'panel':'1000048019.jpg;1000048020.jpg',
 'sheet':'1000048022.jpg;1000048024.jpg;1000048025.jpg;1000048026.jpg;1000048027.jpg;1000048028.jpg;1000048029.jpg;1000048031.jpg;1000048033.jpg',
 'manual':'SX3.5 Fraese.pdf: Uebersicht und Explosionsansichten. Nicht neu fotografierte Restdetails.'}

def spec(name,value,note,source,status='FOTO_ANNAHME'):
    item=dict(name=name,value=value,unit='mm',status=status,note=note,source=PH.get(source,source),limits=None)
    match=next((s for s in SPECS if s['name']==name),None)
    if match: match.update(item)
    else: SPECS.append(item)

for n,v,txt,src in [
 ('column_x',138,'Saeulenbreite: Einpassannahme passend zur fotografierten Blechhuelle, nicht vermessen','column'),
 ('saddle_x',220,'X-Laenge Kreuzschlitten; grobe Fotoablesung','saddle'),
 ('saddle_y',180,'Y-Breite Kreuzschlitten; grobe Fotoablesung','saddle'),
 ('saddle_h',42,'Sattelgrundhoehe: nicht abgelesen','saddle'),
 ('cross_h',4,'Hoehenversatz Fuehrung, konstruktive Einpassannahme','saddle'),
 ('head_x',150,'Kopfbreite aus Foto-Proportion; nicht vermessen','head'),
 ('head_h',220,'Gusshoehe Kopf; Foto-Proportion','head'),
 ('head_corner_r',7,'Gehaeuse-Eckfase; nicht gemessen','head'),
 ('spindle_nose_d',80,'Spindelnase Aussendurchmesser, Foto-Proportion','head'),
 ('spindle_nose_h',16,'Dicke Spindelnase; Foto-Proportion','head'),
 ('panel_x',138,'Breite Bedienfront; keine Messung','panel'),
 ('panel_h',174,'Hoehe Bedienfront; keine Messung','panel'),
 ('wheel_h',24,'Handrad Tiefe aus Fotos','screws'),
 ('table_channel_h',19,'Tischfreistellung: angenommener Bauraum','table'),
 ('head_wall',12,'Kopfwandstaerke sichtbar, Zahl angenaehert','head'),
 ('head_roof',18,'Kopf obere Lagerwand; angenommen','head'),
 ('head_quill_boss',92,'Aussendurchmesser Gussboss um Pinole','head'),
 ('head_window_y',96,'Laenge inneres hinteres Kopf-Fenster','head'),
 ('head_bottom_plate_t',2,'Abnehmbares gelochtes Unterblech','head'),
 ('quill_outer_length',158,'Pinolenhuelse Gesamtlaenge Modell','head'),
 ('spindle_top_shaft_d',28,'Laengsverzahnte Welle, Huellmass','head'),
 ('spindle_top_shaft_h',54,'Sichtbarer verzahnter Wellenabschnitt','head'),
 ('spindle_pulley_d',94,'Aussendurchmesser Spindelriemenscheibe','head'),
 ('spindle_pulley_h',27,'Spindelriemenscheibe Breite','head'),
 ('motor_frame',92,'Motor Gehaeusebreite; Typname und Fotos, keine Flanschnorm','motor'),
 ('motor_length',185,'Motorlaenge hinter Montageplatte; Fotoabschaetzung','motor'),
 ('motor_plate_x',150,'Spindelmotor Montageplatte Breite','motor'),
 ('motor_plate_y',132,'Spindelmotor Montageplatte Tiefe','motor'),
 ('motor_plate_t',6,'Montageplatte Dicke','motor'),
 ('motor_y',142,'Motorachsenabstand zur Spindel; Einpassannahme','motor'),
 ('motor_fins_t',2.2,'Rippendicke Motorprofil','motor'),
 ('motor_fins_depth',5,'Rippentiefe Motorprofil','motor'),
 ('motor_pulley_d',66,'Grosse Motorriemenscheibe Durchmesser','motor'),
 ('motor_timing_d',32,'Kleine Motorriemenscheibe Huellmass','motor'),
 ('z_gear_size',80,'Z-Getriebekopf Aussenbreite; Foto-Proportion','zmotor'),
 ('z_gear_h',48,'Z-Getriebe Bauhoehe ohne Motor','zmotor'),
 ('z_orig_motor_h',86,'Z-Originalmotor Gehaeuselaenge','zmotor'),
 ('z_plate_x',120,'Z-Motor Adapterplatte Breite','zmotor'),
 ('z_plate_y',100,'Z-Motor Adapterplatte Tiefe','zmotor'),
 ('z_plate_t',8,'Z-Motor Adapterplatte Dicke','zmotor'),
 ('lead_x_d',16,'Original-X-Gewinde Huellmass, nicht nachgemessen','screws'),
 ('lead_y_d',16,'Original-Y-Gewinde Huellmass, nicht nachgemessen','screws'),
 ('lead_z_d',20,'Original-Z-Gewinde Huellmass, nicht nachgemessen','screws'),
 ('lead_z_length',470,'Z-Spindel Wellenlaenge; unkalibrierte Fotoabschaetzung','screws'),
 ('saddle_channel_d',27,'Gerundete Spindelfreistellung Sattel','saddle'),
 ('saddle_pocket_depth',11,'Vertiefung neben Spindelkanal','saddle'),
 ('saddle_nut_x',34,'Original-X-Mutter Blocklaenge','saddle'),
 ('saddle_nut_w',32,'Original-X-Mutter Blockbreite','saddle'),
 ('saddle_nut_h',18,'Original-X-Mutter Blockhoehe','saddle'),
 ('cover_length',780,'Blechgehaeuse Laenge aus Foto, nicht bestaetigt','sheet'),
 ('cover_width',150,'Breite Blechgehaeuse Stirnseite; Fotoablesung','sheet'),
 ('cover_deep',215,'Tiefe grosser Bereich; Fotoablesung','sheet'),
 ('cover_shallow',125,'Tiefe kleiner Bereich; Fotoablesung','sheet'),
 ('cover_step_z',150,'Hoehe der seitlichen Stufe; angenommene Lage','sheet'),
 ('cover_slope_l',120,'Laenge der schraegen Kontur; angenommene Lage','sheet'),
 ('cover_sheet_t',1.5,'Blechdicke ungemessen','sheet'),
 ('electronics_board_w',118,'Hauptplatine Breite; Foto-Proportion','elec'),
 ('electronics_board_h',268,'Hauptplatine Laenge; Foto-Proportion','elec'),
 ('electronics_pcb_t',1.6,'Platinen Dicke angenommen','elec'),
 ('electronics_gap',9,'Abstand Platine zur Montagewand','elec'),
 ('z_nut_w',48,'Z-Mutterhalter Breite ungemessen','screws'),
 ('z_nut_h',60,'Z-Mutterhalter Hoehe ungemessen','screws'),
 ('z_nut_l',42,'Z-Mutterhalter Tiefe ungemessen','screws'),
 ('quill_spindle_upper_d',34,'Oberer Spindelwellen-Durchmesser als Huellmass bis zum Riemenscheiben-/Verzahnungsbereich','head'),
 ('quill_spindle_full_h',236,'Durchgehende Werkzeugspindel vom Nasenflansch bis in den oberen Antriebsbereich, aus Fotozusammenhang angenaehert','head'),
 ('quill_pinion_d',32,'Pinolenvorschub-Ritzel Durchmesser aus Hebel- und Zahnstangenlage angenaehert','head'),
 ('quill_pinion_w',16,'Pinolenvorschub-Ritzel Breite angenaehert','head'),
 ('quill_feed_shaft_d',18,'Innenwelle zwischen Dreisternhebel und Pinolenvorschubritzel, angenaehert','head'),
]: spec(n,v,txt,src)

# Pose origin and physical groups remain in the same machine coordinate system.
DERIVED.update([
 ('motor_bottom_z','head_top_z-motor_length'),
 ('cover_bottom_z','column_seat_z+column_foot_h'),
 ('cover_top_z_v4','cover_bottom_z+cover_length'),
 ('cover_front_y_v4','column_front_y+2'),
 ('cover_back_y_v4','cover_front_y_v4+cover_deep'),
 ('pcb_plane_y','cover_back_y_v4-cover_sheet_t-electronics_gap'),
 ('z_drive_z','column_top_z+column_cap_h'),
 ('z_orig_shaft_top','z_drive_z-12'),
 ('z_orig_shaft_bottom','z_orig_shaft_top-lead_z_length'),
 ('z_nut_center','head_bottom_z+head_h*0.55'),
])
evaluate=old.evaluate

def load_parameters(path=None):
    p=OrderedDict((s['name'],float(s['value'])) for s in SPECS)
    if path and os.path.exists(path):
        with open(path,encoding='utf-8-sig') as f: data=json.load(f)
        for k,v in data.items():
            if k.startswith('_'): continue
            if k not in p: raise ValueError('Unbekannter Parameter: '+k)
            if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v): raise ValueError('Ungueltig: '+k)
            p[k]=float(v)
    validate(p);return p

def all_values(p):
    v=OrderedDict(p)
    for k,expr in DERIVED.items(): v[k]=evaluate(expr,v)
    return v

def validate(p):
    old.validate({s['name']:p[s['name']] for s in old.SPECS})
    for s in SPECS:
        if s['name'] not in ('pos_x','pos_y','head_down','quill_down','shield_extension') and p[s['name']]<=0:
            raise ValueError('Nichtpositives Mass: '+s['name'])
    if p['cover_width']<p['electronics_board_w']+2*p['cover_sheet_t']: raise ValueError('PCB zu breit fuer Gehaeuse')
    if p['cover_shallow']>=p['cover_deep']: raise ValueError('Gehaeusetiefen inkonsistent')
    if p['cover_step_z']+p['cover_slope_l']>p['cover_length']-50: raise ValueError('Gehaeusekontur ungueltig')
    if p['head_wall']*2>=p['head_x']-50: raise ValueError('Kopfwaende zu dick')
    return True

def s(x): return str(x)
def add(a,b): return '(%s)+(%s)'%(a,b)
def sub(a,b): return '(%s)-(%s)'%(a,b)
def mul(a,b): return '(%s)*(%s)'%(a,b)
def vecplus(o,d,l): return [add(a,mul(b,l)) for a,b in zip(o,d)]

def box(p,o,sz,op='add',label='Block'):
    p['ops'].append(dict(kind='box',origin=list(map(s,o)),size=list(map(s,sz)),op=op,label=label))
def cyl(p,o,d,h,axis=(0,0,1),op='add',label='Zylinder'):
    p['ops'].append(dict(kind='cylinder',origin=list(map(s,o)),diameter=s(d),height=s(h),direction=axis,op=op,label=label))
def cone(p,o,d,d2,h,axis=(0,0,1),op='add',label='Kegel'):
    p['ops'].append(dict(kind='cone',origin=list(map(s,o)),diameter=s(d),top_diameter=s(d2),height=s(h),direction=axis,op=op,label=label))
def prism(p,pts,h,axis,op='add',label='Profil'):
    pts=[list(map(s,q)) for q in pts]
    p['ops'].append(dict(kind='prism',origin=pts[0],points=pts,height=s(h),direction=axis,op=op,label=label))
def hex_hole(p,o,af,h,axis=(0,0,1),label='Innensechskant'):
    # axis aligned enough; generic perpendicular basis
    a=axis;ref=(1,0,0) if abs(a[0])<0.9 else (0,1,0)
    u=(a[1]*ref[2]-a[2]*ref[1],a[2]*ref[0]-a[0]*ref[2],a[0]*ref[1]-a[1]*ref[0]);n=math.sqrt(sum(t*t for t in u));u=tuple(t/n for t in u)
    v=(a[1]*u[2]-a[2]*u[1],a[2]*u[0]-a[0]*u[2],a[0]*u[1]-a[1]*u[0])
    pts=[]
    for i in range(6):
        ang=math.pi*i/3;pts.append([add(o[k],mul(af,(u[k]*math.cos(ang)+v[k]*math.sin(ang))/math.sqrt(3))) for k in range(3)])
    prism(p,pts,h,axis,'cut',label)

def recipe():
    parts=[]
    def part(name,g,mat='steel',src='manual',note='Fotoform; Masse angenommen; kein Fertigungsdatensatz',datum=None,cls='FOTO_REKONSTRUKTION'):
        d=dict(name=name,group=g,material=mat,note=note,source=PH.get(src,src),status=cls,ops=[],datum=list(map(s,datum)) if datum else None)
        parts.append(d);return d
    def bolt(name,g,o,diam=5,length=12,axis=(0,0,1),src='manual'):
        p=part(name,g,'dark',src,'Schraubendarstellung: Geometrie und Groesse angenommen; kein modelliertes Gewinde',datum=o,cls='BEFESTIGER_ANNAHME')
        cyl(p,vecplus(o,axis,-length),diam,length,axis,label='Schaft_ohne_Gewinde')
        cyl(p,o,diam*1.7,diam,axis,label='Zylinderkopf')
        hex_hole(p,vecplus(o,axis,diam*0.4),diam*0.85,diam*0.7,axis)
        return p
    def washer(name,g,o,od,id_,h,axis=(0,0,1),src='manual'):
        p=part(name,g,'steel',src,datum=o);cyl(p,o,od,h,axis);cyl(p,vecplus(o,axis,-0.1),id_,add(h,0.2),axis,'cut','Bohrung');return p
    def keep(name,g,src):
        p=copy.deepcopy(next(d for d in old.recipe() if d['name']==name));p.update(group=g,source=PH[src],status='FOTO_REKONSTRUKTION',datum=None)
        parts.append(p);return p
    # 1. BASE: existing photo-derived hollow casting, with front connection holes.
    g='01_Basis';p=keep('Basis_Guss_Foto',g,'base');p['material']='castiron'
    for xx in [-28,28]:
        for zz in [-16,16]: cyl(p,(xx,'base_front_y-0.1','y_wheel_z+%s'%zz),5.2,14,(0,1,0),'cut','Y_Lager_Anschlussbohrung_ANNAHME')
    # 2. COLUMN: open casting, transverse ribs, guides, feet and end plates.
    g='02_Saeule';p=keep('Saeule_Guss_Foto',g,'column');p['material']='castiron'
    for side in [-1,1]:
        for zz in [55,270,530,715]:
            cyl(p,('%s*(column_x/2+0.1)'%side,'column_back_y-8','column_seat_z+%s'%zz),4.2,9,(-side,0,0),'cut','Blechbefestigung_ANNAHME')
    p=keep('Saeulendeckel',g,'column');p['material']='castiron'
    for xx in [-48,48]:
        for yy in [-35,35]:cyl(p,(xx,'column_screw_y+%s'%yy,'column_top_z-0.1'),6.5,'column_cap_h+0.2',op='cut',label='Flanschloch')
    for ix in [-1,1]:
        for iy in [-1,1]:bolt('Saeulenfuss_Schraube_%s_%s'%(ix,iy),g,('%s*column_mount_px/2'%ix,'column_front_y+column_y/2+%s*column_mount_py/2'%iy,'column_seat_z+column_foot_h'),10,28,src='column')
    # Z drive original: shaft envelope, stepped journal, hollow bearing housing, bronze nut.
    p=part('Z_Original_Gleitspindel',g,'steel','screws','Original-Gleitgewinde als Huellzylinder; keine Kugelspindel, Steigung nicht bekannt',datum=(0,'column_screw_y','z_orig_shaft_bottom'))
    cyl(p,(0,'column_screw_y','z_orig_shaft_bottom'),'lead_z_d','lead_z_length-38',label='Gewindebereich_HUELLE')
    cyl(p,(0,'column_screw_y','z_orig_shaft_top-39'),12,39,label='Abgesetzter_Zapfen')
    p=part('Z_Lagerbock_Original',g,'bronze','screws',datum=(0,'column_screw_y','z_orig_shaft_top-48'))
    box(p,(-48,'column_screw_y-20','z_orig_shaft_top-48'),(96,40,8))
    cyl(p,(0,'column_screw_y','z_orig_shaft_top-48'),38,36)
    cyl(p,(0,'column_screw_y','z_orig_shaft_top-49'),28,38,op='cut',label='Lageraufnahme_ANNAHME')
    for xx in [-37,37]:cyl(p,(xx,'column_screw_y','z_orig_shaft_top-49'),8.5,10,op='cut',label='Langloch_Huellbohrung')
    washer('Z_Lager_Stellring',g,(0,'column_screw_y','z_orig_shaft_top-48'),28,12,10,src='screws')
    p=part('Z_Kupplung_Spindelseite',g,'silver','screws',datum=(0,'column_screw_y','z_orig_shaft_top-4'))
    cyl(p,(0,'column_screw_y','z_orig_shaft_top-4'),32,17);cyl(p,(0,'column_screw_y','z_orig_shaft_top-5'),12,19,op='cut')
    p=part('Z_Kupplungsstern',g,'orange','screws',datum=(0,'column_screw_y','z_orig_shaft_top+13'))
    cyl(p,(0,'column_screw_y','z_orig_shaft_top+13'),29,7);cyl(p,(0,'column_screw_y','z_orig_shaft_top+12.9'),10,7.2,op='cut')
    p=part('Z_Kupplung_Motorseite',g,'silver','zmotor',datum=(0,'column_screw_y','z_orig_shaft_top+20'))
    cyl(p,(0,'column_screw_y','z_orig_shaft_top+20'),32,12);cyl(p,(0,'column_screw_y','z_orig_shaft_top+19.9'),12,12.2,op='cut')
    p=part('Z_Motor_Adapterplatte',g,'dark','zmotor',datum=(0,'column_screw_y','z_drive_z+22'))
    box(p,('-z_plate_x/2','column_screw_y-z_plate_y/2','z_drive_z+22'),('z_plate_x','z_plate_y','z_plate_t'))
    cyl(p,(0,'column_screw_y','z_drive_z+21.9'),36,'z_plate_t+0.2',op='cut')
    for xx in [-48,48]:
        for yy in [-35,35]:
            cyl(p,(xx,'column_screw_y+%s'%yy,'z_drive_z+21.9'),6.5,'z_plate_t+0.2',op='cut')
            bolt('Z_Motorplatte_Schraube_%s_%s'%(xx,yy),g,(xx,'column_screw_y+%s'%yy,'z_drive_z+22+z_plate_t'),6,18,src='zmotor')
    p=part('GPG_4GN_18K_Getriebe_Huelle',g,'grey','zmotor','Typ vom Foto; Innenverzahnung und Uebersetzung nicht geometrisch rekonstruiert',datum=(0,'column_screw_y','z_drive_z+22+z_plate_t'))
    box(p,('-z_gear_size/2','column_screw_y-z_gear_size/2','z_drive_z+22+z_plate_t'),('z_gear_size','z_gear_size','z_gear_h'))
    cyl(p,(0,'column_screw_y','z_drive_z+22'),12,'z_plate_t+1')
    for xx in [-30,30]:
        for yy in [-30,30]:cyl(p,(xx,'column_screw_y+%s'%yy,'z_drive_z+22+z_plate_t'),4.2,'z_gear_h',op='cut')
    p=part('GPG_4RK25GN_C_Motor_Huelle',g,'grey','zmotor','25 W Original-Hubmotor; Motor-Innenleben nicht sichtbar',datum=(0,'column_screw_y','z_drive_z+22+z_plate_t+z_gear_h'))
    cyl(p,(0,'column_screw_y','z_drive_z+22+z_plate_t+z_gear_h'),78,'z_orig_motor_h')
    for xx in [-1,1]:box(p,('%s*38-1'%xx,'column_screw_y-9','z_drive_z+23+z_plate_t+z_gear_h'),(2,18,'z_orig_motor_h-12'),label='Gehaeuseleiste')
    # 3. SADDLE: photo is X guide face. The unseen Y reverse is explicitly inferred.
    g='03_Kreuzschlitten';p=part('Kreuzschlitten_Guss_Detail',g,'castiron','saddle','Sichtseite fotoabgeglichen; Unterseiten-Y-Fuehrung und alle Passmasse angenommen',datum=(0,'pos_y','saddle_bottom_z'))
    box(p,('-saddle_x/2','pos_y-saddle_y/2','saddle_bottom_z-7'),('saddle_x','saddle_y','saddle_h+cross_h+7'),label='Sattelguss')
    prism(p,[('-guide_spacing/2-0.4','pos_y-saddle_y/2-1','base_h-1'),('guide_spacing/2+0.4','pos_y-saddle_y/2-1','base_h-1'),('guide_spacing/2+8.5','pos_y-saddle_y/2-1','base_h+guide_h+0.4'),('-guide_spacing/2-8.5','pos_y-saddle_y/2-1','base_h+guide_h+0.4')],'saddle_y+2',(0,1,0),'cut','Y_Gegenfuehrung_UNSICHTBAR_ANNAHME')
    prism(p,[('-saddle_x/2','pos_y-table_under_w/2+0.5','table_bottom_z'),('-saddle_x/2','pos_y+table_under_w/2-0.5','table_bottom_z'),('-saddle_x/2','pos_y+table_under_w/2+table_under_flare-0.5','table_bottom_z+table_under_h-0.5'),('-saddle_x/2','pos_y-table_under_w/2-table_under_flare+0.5','table_bottom_z+table_under_h-0.5')],'saddle_x',(1,0,0),label='X_Fuehrungsprofil')
    # Broad cast recess, rounded central lead clearance and a 4-hole mounting island.
    box(p,('-saddle_x/2+15','pos_y-table_under_w/2+12','table_bottom_z-saddle_pocket_depth'),('saddle_x-30','table_under_w-24','table_under_h+saddle_pocket_depth+1'),'cut','Gussfreistellung_Foto')
    cyl(p,('-saddle_x/2-0.1','pos_y','table_bottom_z-3'),'saddle_channel_d','saddle_x+0.2',(1,0,0),'cut','Gerundeter_Spindelkanal')
    box(p,('-saddle_x/2+70','pos_y+table_under_w/2-37','table_bottom_z-saddle_pocket_depth'),(40,25,7),label='Vierloch_Pad_Foto')
    for xx in [80,101]:
        for yy in [25,38]:cyl(p,('-saddle_x/2+%s'%xx,'pos_y+%s'%yy,'table_bottom_z-saddle_pocket_depth-1'),5.2,10,op='cut',label='Vierloch_Pad_Bohrung')
    for sy in [-1,1]:
        yy='pos_y+%s*(table_under_w/2-5)'%sy
        box(p,('-saddle_x/2+10',yy,'table_bottom_z+table_under_h-1'),('saddle_x-20',1,2),'cut','Schmiernut_laengs')
        for fx in ['-saddle_x/2+11','0','saddle_x/2-11']:
            box(p,(fx,sub(yy,4),'table_bottom_z+table_under_h-1'),(1,9,2),'cut','Schmiernut_quer')
            cyl(p,(fx,yy,'table_bottom_z+table_under_h-5'),2.5,6,op='cut',label='Oelbohrung')
    # Separate tapered gib on one X guide flank. Unmeasured cross section.
    gibpts=[('-saddle_x/2','pos_y+table_under_w/2-0.5','table_bottom_z'),('-saddle_x/2','pos_y+table_under_w/2+table_under_flare-0.5','table_bottom_z+table_under_h-0.5'),('-saddle_x/2','pos_y+table_under_w/2+table_under_flare-3','table_bottom_z+table_under_h-0.5'),('-saddle_x/2','pos_y+table_under_w/2-3','table_bottom_z')]
    prism(p,gibpts,'saddle_x',(1,0,0),'cut','Separate_Keilleiste_Freiraum')
    q=part('X_Keilleiste_Sattel',g,'steel','saddle','Separate Leiste sichtbar; Querschnitt angenommen',datum=('-saddle_x/2','pos_y+table_under_w/2','table_bottom_z'))
    prism(q,gibpts,'saddle_x',(1,0,0),label='Keilleistenprofil')
    bolt('X_Keilleiste_Einstellschraube',g,('-saddle_x/2-1','pos_y+table_under_w/2','table_bottom_z+3'),4,12,(-1,0,0),'saddle')
    # Visible original split X nut. Nut model has plain bore, unknown thread.
    p=part('X_Original_Spindelmutter_Geteilt',g,'steel','saddle','Geteilte Originalmutter. Bohrung als Huellmass, kein rekonstruiertes Gewinde',datum=('-saddle_x/2+8','pos_y','x_wheel_z'))
    box(p,('-saddle_x/2-8','pos_y-saddle_nut_w/2','x_wheel_z-saddle_nut_h/2'),('saddle_nut_x','saddle_nut_w','saddle_nut_h'))
    cyl(p,('-saddle_x/2-9','pos_y','x_wheel_z'),'lead_x_d','saddle_nut_x+2',(1,0,0),'cut','Gewindebohrung_Huelle')
    box(p,('-saddle_x/2-8.1','pos_y-saddle_nut_w/2-0.1','x_wheel_z+4'),(8,'saddle_nut_w+0.2',0.8),'cut','Sichtbarer_Klemmschlitz')
    for yy in [-10,10]:cyl(p,('-saddle_x/2-9','pos_y+%s'%yy,'x_wheel_z-8'),4.2,'saddle_nut_x+2',(1,0,0),'cut')
    p=part('Y_Original_Spindelmutter_Platzhalter',g,'bronze','screws','Mutter nicht einzeln fotografiert; Einbaulage und Form ANNAHME',datum=(0,'pos_y','y_wheel_z'),cls='UNSICHTBAR_ANNAHME')
    box(p,(-18,'pos_y-18','y_wheel_z-14'),(36,36,28));cyl(p,(0,'pos_y-19','y_wheel_z'),'lead_y_d',38,(0,1,0),'cut','Gewindebohrung_Huelle')
    # Rail measuring system seen attached to saddle, axis assignment provisional.
    p=part('Y_Massstab_Abdeckung',g,'silver','saddle','Fotografiert; Achszuordnung und Lage im montierten Zustand angenommen',datum=('saddle_x/2+18','pos_y','saddle_bottom_z+8'))
    box(p,('saddle_x/2+18','pos_y-saddle_y/2-35','saddle_bottom_z+8'),(12,'saddle_y+70',22));box(p,('saddle_x/2+17.9','pos_y-saddle_y/2-30','saddle_bottom_z+11'),(10,'saddle_y+60',15),'cut')
    for yy in [-55,55]:
        p=part('Y_Massstab_Distanz_%s'%yy,g,'steel','saddle',datum=('saddle_x/2','pos_y+%s'%yy,'saddle_bottom_z+18'))
        cyl(p,('saddle_x/2','pos_y+%s'%yy,'saddle_bottom_z+18'),10,18,(1,0,0))
    for i,xx in enumerate([-70,70]):
        p=part('X_Klemmhebel_%s'%i,g,'black','saddle',datum=(xx,'pos_y-saddle_y/2','table_bottom_z-12'))
        cyl(p,(xx,'pos_y-saddle_y/2','table_bottom_z-12'),8,20,(0,-1,0));cyl(p,(xx,'pos_y-saddle_y/2-16','table_bottom_z-12'),13,14,(0,-1,0));cyl(p,(xx,'pos_y-saddle_y/2-24','table_bottom_z-12'),8,42,(0.8,0,0.6))
    # 4. TABLE: retain all measured-document T-slots; detailed bores/scale/handwheels.
    g='04_Tisch';p=keep('Arbeitstisch_Foto',g,'table');p['material']='castiron'
    for side in [-1,1]:
        for yy in [-55,55]:bolt('X_Tisch_Stirnschraube_%s_%s'%(side,yy),g,('pos_x+%s*(table_x/2+8)'%side,'pos_y+%s'%yy,'table_bottom_z+table_h/2'),5,18,(side,0,0),'table')
    for nm in ['X_Massstab_Gehaeuse_Foto','X_Massstab_Dichtlippe','X_Massstab_Lesekopf_Foto','X_Massstab_Lesekopfhalter_ANNAHME']:
        pp=keep(nm,g if 'Gehaeuse' in nm or 'Dichtlippe' in nm else '03_Kreuzschlitten','table')
    # Two original lead screws: plain envelopes, no invented ball return geometry.
    p=part('X_Original_Gleitspindel',g,'steel','screws','Gewindebereich als Huellzylinder, Steigung unbekannt',datum=('pos_x','pos_y','x_wheel_z'))
    cyl(p,('pos_x-table_x/2-15','pos_y','x_wheel_z'),'lead_x_d','table_x+32',(1,0,0),label='Originalgewinde_Huelle')
    cyl(p,('pos_x+table_x/2+16','pos_y','x_wheel_z'),12,'x_wheel_offset+12',(1,0,0),label='Handradzapfen')
    p=part('Y_Original_Gleitspindel','01_Basis','steel','screws','Gewindebereich als Huellzylinder, Steigung unbekannt',datum=(0,'base_front_y','y_wheel_z'))
    cyl(p,(0,'base_front_y-16','y_wheel_z'),'lead_y_d','guide_length+10',(0,1,0),label='Originalgewinde_Huelle')
    cyl(p,(0,'base_front_y-y_wheel_offset-12','y_wheel_z'),12,'y_wheel_offset+1',(0,1,0),label='Handradzapfen')
    # Hollow bearing flanges; both are black in source photos.
    p=part('X_Lagerflansch_rechts',g,'dark','screws',datum=('pos_x+table_x/2','pos_y','x_wheel_z'))
    box(p,('pos_x+table_x/2','pos_y-36','x_wheel_z-25'),(10,72,50));cyl(p,('pos_x+table_x/2+9','pos_y','x_wheel_z'),40,45,(1,0,0));cyl(p,('pos_x+table_x/2-1','pos_y','x_wheel_z'),16,57,(1,0,0),'cut')
    for yy in [-27,27]:cyl(p,('pos_x+table_x/2-1','pos_y+%s'%yy,'x_wheel_z'),5.5,12,(1,0,0),'cut')
    p=part('X_Lagerabschluss_links',g,'dark','screws',datum=('pos_x-table_x/2-8','pos_y','x_wheel_z'))
    box(p,('pos_x-table_x/2-8','pos_y-32','x_wheel_z-21'),(8,64,42));cyl(p,('pos_x-table_x/2-9','pos_y','x_wheel_z'),16,10,(1,0,0),'cut')
    p=part('Y_Lagerflansch_vorn','01_Basis','dark','screws',datum=(0,'base_front_y','y_wheel_z'))
    box(p,(-40,'base_front_y-10','y_wheel_z-27'),(80,10,54));cyl(p,(0,'base_front_y-9','y_wheel_z'),40,46,(0,-1,0));cyl(p,(0,'base_front_y+1','y_wheel_z'),16,57,(0,-1,0),'cut')
    for xx in [-28,28]:
        for zz in [-16,16]:cyl(p,(xx,'base_front_y+0.1','y_wheel_z+%s'%zz),5.5,12,(0,-1,0),'cut')
    for nm in ['X_Skalenring','Y_Skalenring','Handrad_X','Handrad_Y','Handradgriff_X','Handradgriff_Y','Handradmutter_X','Handradmutter_Y']:
        pp=keep(nm,'04_Tisch' if nm.endswith('_X') or nm.startswith('X_') else '01_Basis','screws')
        if 'Skalenring' in nm:pp['material']='black'
    # 5. HEAD CASTING: outer chamfered perimeter, open pockets and central quill boss.
    g='05_Spindelkopf';p=part('Spindelkopf_Guss_Detail',g,'machine_red','head','Sichtbare Hohlraeume und Z-Fuehrung nach Fotos; Wanddicken, Lagerpassungen und Fensterlagen angenaehert',datum=(0,0,'head_bottom_z'))
    pts=[('-head_x/2+head_corner_r','-head_front','head_bottom_z'),('head_x/2-head_corner_r','-head_front','head_bottom_z'),('head_x/2','-head_front+head_corner_r','head_bottom_z'),('head_x/2','column_front_y','head_bottom_z'),('-head_x/2','column_front_y','head_bottom_z'),('-head_x/2','-head_front+head_corner_r','head_bottom_z')]
    prism(p,pts,'head_h',(0,0,1),label='Guss_Aussenkontur')
    box(p,('-head_x/2+head_wall','-head_front+head_wall','head_bottom_z-0.1'),('head_x-2*head_wall','head_depth-2*head_wall','head_h+0.2'),'cut','Offener_Kopfinnenraum')
    # Bearing bridge/boss tied to front and side walls, leaving rear window for motor.
    box(p,('-head_x/2+head_wall-0.1','-head_front+head_wall-0.1','head_top_z-head_roof'),('head_x-2*head_wall+0.2','head_front+55','head_roof'),label='Obere_Lagerbruecke')
    cyl(p,(0,0,'head_bottom_z'),'head_quill_boss','head_h',label='Pinolen_Gussboss')
    box(p,('-head_x/2+head_wall-0.1',-18,'head_bottom_z'),('head_x-2*head_wall+0.2',36,12),label='Untere_Querverbindung')
    cyl(p,(0,0,'head_bottom_z-0.2'),'quill_d+0.4','head_h+0.4',op='cut',label='Pinolenfuehrungsbohrung_ANNAHME')
    # Female Z dovetail accepts column; relief through central rear wall.
    prism(p,[('-column_guide_width/2+6.6','column_front_y+0.5','head_bottom_z-0.1'),('column_guide_width/2-6.6','column_front_y+0.5','head_bottom_z-0.1'),('column_guide_width/2+0.4','column_front_y-column_guide_proj-0.4','head_bottom_z-0.1'),('-column_guide_width/2-0.4','column_front_y-column_guide_proj-0.4','head_bottom_z-0.1')],'head_h+0.2',(0,0,1),'cut','Z_Gegenfuehrung_Foto_KEINE_PASSUNG')
    # Side functional bores: quill shaft, fine feed, clamping, all photo position estimates.
    for side in [-1,1]:
        cyl(p,('%s*(head_x/2+0.1)'%side,'star_y','star_z'),24,'head_wall+3',(-side,0,0),'cut','Vorschubwelle_Bohrung')
        cyl(p,('%s*(head_x/2+0.1)'%side,12,'head_bottom_z+46'),12,'head_wall+3',(-side,0,0),'cut','Pinolenklemmung_Bohrung')
        for yy in [-24,65,160]:
            for zz in [12,196]:cyl(p,('%s*(head_x/2+0.1)'%side,yy,'head_bottom_z+%s'%zz),4.2,9,(-side,0,0),'cut','Seitendeckel_Gewindekern_ANNAHME')
    for xx in [-1,1]:
        for zz in [15,115,205]:cyl(p,('%s*(head_x/2-9)'%xx,'-head_front-0.1','head_bottom_z+%s'%zz),4.2,10,(0,1,0),'cut','Frontplattenbefestigung')
    # separate Z gib, nut bracket and original bronze element
    p=part('Z_Keilleiste_Kopf',g,'steel','head',datum=('column_guide_width/2','column_front_y','head_bottom_z'))
    prism(p,[('column_guide_width/2-4','column_front_y-1','head_bottom_z+2'),('column_guide_width/2+1','column_front_y-1','head_bottom_z+2'),('column_guide_width/2+1','column_front_y-column_guide_proj+1','head_bottom_z+2')],'head_h-4',(0,0,1),label='Keilleiste_angenommen')
    p=part('Z_Mutterhalter_Original',g,'steel','screws','Blockform nach Spindelfotos, Verbindung zum Kopf NICHT bestaetigt',datum=(0,'column_screw_y','z_nut_center'))
    box(p,('-z_nut_w/2','column_screw_y-z_nut_l/2','z_nut_center-z_nut_h/2'),('z_nut_w','z_nut_l','z_nut_h'));cyl(p,(0,'column_screw_y','z_nut_center-z_nut_h/2-0.1'),'lead_z_d+1','z_nut_h+0.2',op='cut')
    box(p,(-14,'column_front_y-head_wall','z_nut_center-12'),(28,'column_screw_offset-z_nut_l/2+head_wall+1',24),label='Anschlusssteg_ANNAHME')
    p=part('Z_Original_Bronzemutter',g,'bronze','screws','Originalmutter Huellgeometrie; keine Kugelumlaufkonstruktion',datum=(0,'column_screw_y','z_nut_center+z_nut_h/2'))
    cyl(p,(0,'column_screw_y','z_nut_center+z_nut_h/2'),30,12);cyl(p,(0,'column_screw_y','z_nut_center+z_nut_h/2-0.1'),'lead_z_d',12.2,op='cut')
    # Faceplate, end cover and ventilated bottom panel.
    p=part('Kopf_Frontplatte_Detail',g,'machine_red','head',datum=(0,'head_face_y','head_bottom_z'))
    box(p,('-head_x/2+1','head_face_y','head_bottom_z'),('head_x-2','frontplate_t','head_h'))
    for xx in [-1,1]:
        for zz in [15,115,205]:cyl(p,('%s*(head_x/2-9)'%xx,'head_face_y-0.1','head_bottom_z+%s'%zz),5.5,'frontplate_t+0.2',(0,1,0),'cut')
    box(p,(-25,'head_face_y-0.1','head_bottom_z+18'),(43,'frontplate_t+0.2',54),'cut','Anzeigeausschnitt')
    p=part('Kopf_Unterblech_gelocht',g,'black','head',datum=(0,75,'head_bottom_z'))
    box(p,('-head_x/2+10',65,'head_bottom_z-2'),('head_x-20','head_depth-head_front-75',2))
    for xx in [-45,-27,-9,9,27,45]:
        for yy in [82,100,118,136,154,172,190]:cyl(p,(xx,yy,'head_bottom_z-2.1'),4.5,2.2,op='cut',label='Lueftungsloch')
    for xx in [-1,1]:
        for yy in [72,196]:bolt('Unterblech_Schraube_%s_%s'%(xx,yy),g,('%s*(head_x/2-16)'%xx,yy,'head_bottom_z-2'),4,9,(0,0,-1),'head')
    p=part('Pinole_Huelse_Detail',g,'steel','head','Pinolenhuelle nach Ansichten; Zahnstangenlage auf den Dreisternhebel abgestimmt. Teilung und Zahnprofil bleiben funktionale Annahmen.',datum=(0,0,'spindle_face_z'))
    cyl(p,(0,0,'spindle_face_z+spindle_nose_h'),'quill_d','quill_outer_length');cyl(p,(0,0,'spindle_face_z+spindle_nose_h-0.1'),'quill_bore_d','quill_outer_length+0.2',op='cut')
    # Zahnstange neu auf der Rueckseite der Pinole, damit sie logisch vom Dreisternhebel-Ritzel angetrieben werden kann.
    for i in range(16):box(p,(-7,'quill_d/2-5','spindle_face_z+spindle_nose_h+24+%s*5'%i),(14,7,2.8),label='Zahnstange_FUNKTIONSANNAHME')
    spindle_nose=keep('Spindelnase_SK30_Normreferenz',g,'head')
    p=part('Werkzeugspindel_Durchgehende_Huelle',g,'steel','head','Durchgehende Werkzeugspindel bis zum oberen Antriebsbereich. Lagerstellen, Innenkontur und Verzahnungsnorm nicht vollstaendig vermessen.',datum=(0,0,'spindle_face_z'))
    cyl(p,(0,0,'spindle_face_z+spindle_nose_h'),'spindle_shaft_d','quill_spindle_full_h',label='Spindelwelle_durchgehend')
    cyl(p,(0,0,'head_top_z-22'),'quill_spindle_upper_d','spindle_top_shaft_h+22',label='Spindelanschluss_oben')
    p=part('Pinolenvorschub_Welle_innen',g,'steel','head','Innenwelle vom Dreisternhebel bis zum Ritzel der Pinolenzahnstange; Foto-/Funktionsrekonstruktion',datum=(0,'star_y','star_z'))
    cyl(p,('-quill_pinion_w/2','star_y','star_z'),'quill_feed_shaft_d','head_x/2+quill_pinion_w/2+16',(1,0,0),label='Durchgehende_Vorschubwelle')
    p=part('Pinolenvorschub_Ritzel',g,'steel','head','Ritzel als Huelle zwischen Dreisternhebel und Zahnstange; Zahnzahl und Profil angenaehert',datum=(0,'star_y','star_z'))
    cyl(p,('-quill_pinion_w/2','star_y','star_z'),'quill_pinion_d','quill_pinion_w',(1,0,0),label='Ritzelgrundkoerper')
    # Radially oriented symbolic teeth: every tooth intersects the wheel and
    # extends outside it. v4.7 used fixed-axis boxes, some entirely buried.
    # Not an involute or manufacturing tooth profile; width follows the parameter.
    for i in range(12):
        ang=2*math.pi*i/12
        ca,sa=math.cos(ang),math.sin(ang)
        pts=[]
        for dr,tangential in [(-1,-1.5),(2,-0.9),(2,0.9),(-1,1.5)]:
            rr='quill_pinion_d/2+(%s)'%dr
            yy=add('star_y',add(mul(rr,ca),-tangential*sa))
            zz=add('star_z',add(mul(rr,sa),tangential*ca))
            pts.append(('-quill_pinion_w/2',yy,zz))
        prism(p,pts,'quill_pinion_w',(1,0,0),label='Ritzelzahn_SYMBOLISCH')
    for xx in [-1,1]:
        box(spindle_nose,('%s*(spindle_nose_d/2-9)-9'%xx,-7,'spindle_face_z-0.1'),(18,14,5),'cut','Mitnehmer_Tasche')
        q=part('SK30_Mitnehmer_%s'%xx,g,'steel','head',datum=('%s*(spindle_nose_d/2-9)'%xx,0,'spindle_face_z'))
        box(q,('%s*(spindle_nose_d/2-9)-8'%xx,-6,'spindle_face_z-3'),(16,12,7));cyl(q,('%s*(spindle_nose_d/2-9)'%xx,0,'spindle_face_z-3.1'),4.3,7.2,op='cut')
        bolt('Mitnehmer_Schraube_%s'%xx,g,('%s*(spindle_nose_d/2-9)'%xx,0,'spindle_face_z-3'),4,10,(0,0,-1),'head')
    # Spline as visible envelope with axial teeth, not an asserted spline standard.
    p=part('Spindel_Laengsverzahnung_Huelle',g,'steel','head',datum=(0,0,'head_top_z'))
    cyl(p,(0,0,'head_top_z-15'),'spindle_top_shaft_d-5','spindle_top_shaft_h+15');cyl(p,(0,0,'head_top_z-16'),12,'spindle_top_shaft_h+17',op='cut')
    for i in range(8):
        a=2*math.pi*i/8;x=math.cos(a);y=math.sin(a)
        cyl(p,('%s*(spindle_top_shaft_d/2-3)'%x,'%s*(spindle_top_shaft_d/2-3)'%y,'head_top_z-10'),5,'spindle_top_shaft_h+10',label='Verzahnungs_Huelse_angenommen')
    # existing detail mechanisms, correctly associated to new head dimensions
    old_head_names=['Kopf_Typenschild','Digitale_Bohrtiefenanzeige','Pinolenanzeige_LCD','Feinvorschub_Pinole','Sternhebel_Welle','Sternhebel_Nabe','Sternhebel_Kupplung']
    old_head_names += ['Pinolenanzeige_Taste_%s'%i for i in range(3)]
    for i in range(1,4):old_head_names += ['Sternhebel_Stange_%s'%i,'Sternhebel_Griff_%s'%i,'Sternhebel_Umschalttaster_%s'%i]
    old_head_names += ['Kupplung_Kurzhebel_%s'%i for i in range(3)]
    for nm in old_head_names:keep(nm,g,'head')
    p=part('Pinole_Messstange',g,'black','head',datum=(0,'head_face_y','head_bottom_z'))
    box(p,(-5,'head_face_y-3','spindle_face_z+spindle_nose_h'),(10,3,'head_bottom_z+35-spindle_face_z-spindle_nose_h'))
    for xx in [-1,1]:
        for zz in [15,115,205]:bolt('Frontplatten_Schraube_%s_%s'%(xx,zz),g,('%s*(head_x/2-9)'%xx,'head_face_y','head_bottom_z+%s'%zz),4,9,(0,-1,0),'head')
    # 6. MOTOR AND BELT TRAIN
    g='06_Spindelmotor';p=part('W92_1000F_Gehaeuse_Rippen',g,'black','motor','Typ W92-1000 F. Innenleben unsichtbar, keine Motor-Magnetgeometrie',datum=(0,'motor_y','motor_bottom_z'))
    box(p,('-motor_frame/2+motor_fins_depth','motor_y-motor_frame/2+motor_fins_depth','motor_bottom_z'),('motor_frame-2*motor_fins_depth','motor_frame-2*motor_fins_depth','motor_length-20'))
    for i in range(12):
        v='-motor_frame/2+6+%s*(motor_frame-12)/11'%i
        for side in [-1,1]:
            box(p,('%s*(motor_frame/2-motor_fins_depth)-motor_fins_depth*(%s)'%(side,1 if side<0 else 0),add('motor_y',v),'motor_bottom_z'),('motor_fins_depth+0.3','motor_fins_t','motor_length-20'),label='Kuehlrippe_X')
            box(p,(v,'motor_y+%s*(motor_frame/2-motor_fins_depth)-motor_fins_depth*(%s)'%(side,1 if side<0 else 0),'motor_bottom_z'),('motor_fins_t','motor_fins_depth+0.3','motor_length-20'),label='Kuehlrippe_Y')
    p=part('W92_1000F_Rueckdeckel',g,'black','motor',datum=(0,'motor_y','motor_bottom_z-16'))
    box(p,('-motor_frame/2','motor_y-motor_frame/2','motor_bottom_z-16'),('motor_frame','motor_frame',16))
    for xx in [-22,22]:cyl(p,(xx,'motor_y','motor_bottom_z-23'),15,8,label='Kabelabgang')
    p=part('W92_1000F_Frontflansch',g,'dark','motor',datum=(0,'motor_y','head_top_z-20'))
    box(p,('-motor_frame/2','motor_y-motor_frame/2','head_top_z-20'),('motor_frame','motor_frame',20));cyl(p,(0,'motor_y','head_top_z-20.1'),22,20.2,op='cut')
    p=part('W92_1000F_Motorwelle_Huelle',g,'steel','motor',datum=(0,'motor_y','head_top_z'))
    cyl(p,(0,'motor_y','head_top_z-15'),16,65);box(p,(-2,'motor_y+6','head_top_z+10'),(4,3,24),label='Passfeder_Huelle')
    p=part('Spindelmotor_Montageplatte',g,'dark','motor',datum=(0,'motor_y','head_top_z'))
    box(p,('-motor_plate_x/2','motor_y-motor_plate_y/2','head_top_z'),('motor_plate_x','motor_plate_y','motor_plate_t'));cyl(p,(0,'motor_y','head_top_z-0.1'),74,'motor_plate_t+0.2',op='cut')
    for xx in [-1,1]:
        for yy in [-1,1]:
            x='%s*(motor_plate_x/2-11)'%xx;y='motor_y+%s*(motor_plate_y/2-20)'%yy
            box(p,(sub(x,3.5),sub(y,10),'head_top_z-0.1'),(7,20,'motor_plate_t+0.2'),'cut','Spannlangloch')
            for dy in [-10,10]:cyl(p,(x,add(y,dy),'head_top_z-0.1'),7,'motor_plate_t+0.2',op='cut')
            bolt('Motorplatte_Schraube_%s_%s'%(xx,yy),g,(x,y,'head_top_z+motor_plate_t'),6,15,src='motor')
    # ring pulley grooves: real circumferential groove subtraction using ring tools
    for nm,y,diam,z in [('Spindel_Riemenscheibe',0,'spindle_pulley_d','head_top_z+5'),('Motor_Riemenscheibe','motor_y','motor_pulley_d','head_top_z+7')]:
        p=part(nm,g,'silver','head' if y==0 else 'motor','Rillen/Zaehne nach Fotos, Teilung und Zahnprofil angenommen',datum=(0,y,z))
        cyl(p,(0,y,z),sub(diam,3),22)
        # All rims intersect the continuous hub: no split intermediate bodies.
        for k in range(6):
            cyl(p,(0,y,add(z,k*3.5)),diam,2.0,label='Riemenrillen_Steg_%s'%k)
        cyl(p,(0,y,add(z,22)),42 if y==0 else 'motor_timing_d',14)
        for k in range(24):
            a=2*math.pi*k/24;r=21 if y==0 else 16
            cyl(p,(r*math.cos(a),add(y,r*math.sin(a)),add(z,22)),1.5,14.2,op='cut',label='Zahnprofil_SYMBOLISCH')
        cyl(p,(0,y,sub(z,0.1)),28 if y==0 else 16,36.2,op='cut',label='Durchgangsbohrung')
    p=part('Riemen_hoher_Bereich_Huelle',g,'black','motor','Riemenpfad schematisch; kein definiertes Riemenprofil',datum=(0,0,'head_top_z+12'),cls='FUNKTIONSANNAHME')
    # Polygonal tangent belt outline (nominal tangent angle); no tooth profile.
    outer=[];inner=[]
    theta=math.acos((94-66)/2/142)
    # front pulley exposed arc, then rear/motor exposed arc
    for center,diam,angles in [(0,'spindle_pulley_d',[math.pi/2-theta-(2*math.pi-2*theta)*i/24 for i in range(25)]),('motor_y','motor_pulley_d',[math.pi/2+theta-2*theta*i/20 for i in range(21)])]:
        for a in angles:
            outer.append(('%.12g*((%s)/2+2)'%(math.cos(a),diam),add(center,'%.12g*((%s)/2+2)'%(math.sin(a),diam)),'head_top_z+12'))
            inner.append(('%.12g*((%s)/2-0.1)'%(math.cos(a),diam),add(center,'%.12g*((%s)/2-0.1)'%(math.sin(a),diam)),'head_top_z+11.9'))
    prism(p,outer,8,(0,0,1),label='Riemen_Aussenkontur')
    prism(p,inner,8.2,(0,0,1),'cut','Riemen_Innenkontur')
    # hollow removable belt cover
    p=part('Riemenabdeckung_Blech',g,'machine_red','head',datum=(0,0,'head_top_z'))
    box(p,('-head_x/2-1','-head_front-1','head_top_z'),('head_x+2','head_depth+2','belt_cover_h'))
    box(p,('-head_x/2+1','-head_front+1','head_top_z-0.1'),('head_x-2','head_depth-2','belt_cover_h-1.4'),'cut')
    cyl(p,(0,0,'head_top_z+belt_cover_h-2'),42,3,op='cut',label='Anzugspindel_Durchlass')
    for nm in ['Anzugspindel_Abdeckung','Riemendeckel_Schraubknopf']:keep(nm,g,'head')
    p=part('Spindel_Drehzahlgeber_Huelle',g,'steel','head','Sensor sichtbar; Typ und Signal unbekannt',datum=(38,-23,'head_top_z+5'))
    cyl(p,(38,-23,'head_top_z+5'),8,27,(0,0,-1));cyl(p,(38,-23,'head_top_z+5'),13,3,(0,0,-1))
    # 7. PANEL: new front layout exactly oriented from panel photos
    g='07_Bedienpanel';keep('Panelhalter',g,'panel')
    p=part('Bediengehaeuse_Hohlschale',g,'machine_red','panel',datum=('panel_left_x','-head_front','panel_bottom_z'))
    box(p,('panel_left_x','-head_front','panel_bottom_z'),('panel_x','panel_y','panel_h'))
    box(p,('panel_left_x+2','-head_front-0.1','panel_bottom_z+2'),('panel_x-4','panel_y-2','panel_h-4'),'cut')
    p=part('Bedienfront_Aluminium',g,'panel','panel',datum=('panel_left_x','-head_front-3','panel_bottom_z'))
    box(p,('panel_left_x','-head_front-3','panel_bottom_z'),('panel_x',3,'panel_h'))
    for x,z,dd in [('panel_left_x+panel_x-35','panel_bottom_z+panel_h-34',22),('panel_left_x+28','panel_bottom_z+panel_h-35',16),('panel_left_x+28','panel_bottom_z+panel_h-68',16),('panel_left_x+panel_x/2','panel_bottom_z+76',12)]:
        cyl(p,(x,'-head_front-3.1',z),dd,3.2,(0,1,0),'cut')
    box(p,('panel_left_x+25','-head_front-3.1','panel_bottom_z+19'),('panel_x-50',3.2,20),'cut','LCD_Fenster_unten_Foto')
    for nm,xx,zz,diam,h,mat in [
        ('Not_Halt_Kragen','panel_left_x+panel_x-35','panel_bottom_z+panel_h-34',46,3,'yellow'),
        ('Not_Halt_Pilz','panel_left_x+panel_x-35','panel_bottom_z+panel_h-34',38,22,'red'),
        ('Start_Stop_Taster','panel_left_x+28','panel_bottom_z+panel_h-35',22,6,'steel'),
        ('Gewindetaster','panel_left_x+28','panel_bottom_z+panel_h-68',18,5,'steel'),
        ('Drehzahlsteller','panel_left_x+panel_x/2','panel_bottom_z+76',43,16,'steel')]:
        q=part(nm,g,mat,'panel',datum=(xx,'-head_front-3',zz));cyl(q,(xx,'-head_front-3',zz),diam,h,(0,-1,0))
        if nm=='Drehzahlsteller':cyl(q,(add(xx,10),'-head_front-18',add(zz,12)),2,1.1,(0,-1,0),'cut','Markierung')
    p=part('Drehzahlanzeige_LCD_Foto',g,'lcd','panel',datum=('panel_left_x+25','-head_front-2','panel_bottom_z+19'))
    box(p,('panel_left_x+25','-head_front-2','panel_bottom_z+19'),('panel_x-50',1.1,20))
    for nm in ['Z_Taster_Seitenplatte','Z_Taster_Auf','Z_Taster_Ab']:keep(nm,g,'panel')
    # 8. SHEET COLUMN: separate bent shell elements, tapered top, lower side notch.
    g='08_Blechsaeule'
    for side in [-1,1]:
        p=part('Blechsaeule_Seitenwand_%s'%('links' if side<0 else 'rechts'),g,'machine_red','sheet','3D-Blechkontur. Biegeradien/Abwicklung NICHT bestimmt.',datum=('%s*cover_width/2'%side,'cover_front_y_v4','cover_bottom_z'))
        x='-cover_width/2' if side<0 else 'cover_width/2-cover_sheet_t'
        yz=[('cover_front_y_v4','cover_bottom_z+cover_step_z'),('cover_front_y_v4+cover_deep-cover_shallow','cover_bottom_z+cover_step_z'),('cover_front_y_v4+cover_deep-cover_shallow','cover_bottom_z'),('cover_back_y_v4','cover_bottom_z'),('cover_back_y_v4','cover_top_z_v4-cover_slope_l'),('cover_front_y_v4+cover_shallow','cover_top_z_v4'),('cover_front_y_v4','cover_top_z_v4')]
        prism(p,[(x,y,z) for y,z in yz],'cover_sheet_t',(1,0,0),label='Seitenkontur_Foto')
        for zz in [190,420,650]:cyl(p,('%s*(cover_width/2+0.1)'%side,'cover_front_y_v4+18','cover_bottom_z+%s'%zz),5.5,'cover_sheet_t+0.2',(-side,0,0),'cut','Befestigung_ANNAHME')
        if side<0:
            for zz in [340,470]:cyl(p,('-cover_width/2-0.1','cover_front_y_v4+65','cover_bottom_z+%s'%zz),30,'cover_sheet_t+0.2',(1,0,0),'cut','Schlauchdurchfuehrung')
    p=part('Blechsaeule_Rueckwand',g,'machine_red','sheet',datum=(0,'cover_back_y_v4','cover_bottom_z'))
    box(p,('-cover_width/2','cover_back_y_v4-cover_sheet_t','cover_bottom_z'),('cover_width','cover_sheet_t','cover_length-cover_slope_l'))
    for x in [-1,1]:
        for zz in [30,180,370,570]:cyl(p,('%s*(cover_width/2-8)'%x,'cover_back_y_v4-cover_sheet_t-0.1','cover_bottom_z+%s'%zz),4.2,'cover_sheet_t+0.2',(0,1,0),'cut')
    p=part('Blechsaeule_Schraegblech',g,'machine_red','sheet',datum=(0,'cover_back_y_v4','cover_top_z_v4-cover_slope_l'))
    prism(p,[('-cover_width/2','cover_back_y_v4','cover_top_z_v4-cover_slope_l'),('-cover_width/2','cover_front_y_v4+cover_shallow','cover_top_z_v4'),('-cover_width/2','cover_front_y_v4+cover_shallow-cover_sheet_t','cover_top_z_v4'),('-cover_width/2','cover_back_y_v4-cover_sheet_t','cover_top_z_v4-cover_slope_l')],'cover_width',(1,0,0))
    for top in [False,True]:
        z='cover_top_z_v4-cover_sheet_t' if top else 'cover_bottom_z';y='cover_front_y_v4' if top else 'cover_front_y_v4+cover_deep-cover_shallow'
        p=part('Blechsaeule_Stirnblech_'+('oben' if top else 'unten'),g,'machine_red','sheet',datum=(0,y,z))
        box(p,('-cover_width/2',y,z),('cover_width','cover_shallow','cover_sheet_t'))
        if not top:
            for xx in [-45,-30,-15,0,15,30,45]:
                for yy in [25,38,51]:box(p,(xx,add(y,yy),sub(z,0.1)),(6,2,'cover_sheet_t+0.2'),'cut','Lueftungsschlitz')
    for zz in [210,530]:
        p=part('Blechsaeule_Querlasche_%s'%zz,g,'machine_red','sheet',datum=(0,'cover_front_y_v4','cover_bottom_z+%s'%zz))
        box(p,('-cover_width/2','cover_front_y_v4','cover_bottom_z+%s'%zz),('cover_width',24,'cover_sheet_t'))
    # Visible external cable glands / conduits, not a wiring model.
    for k,zz in enumerate([340,470]):
        p=part('Kabelverschraubung_%s'%k,g,'black','sheet',datum=('-cover_width/2','cover_front_y_v4+65','cover_bottom_z+%s'%zz))
        cyl(p,('-cover_width/2+3','cover_front_y_v4+65','cover_bottom_z+%s'%zz),39,23,(-1,0,0));cyl(p,('-cover_width/2+4','cover_front_y_v4+65','cover_bottom_z+%s'%zz),23,25,(-1,0,0),'cut')
    for label,zz in [('unten',190),('oben',650)]:
        p=part('Z_Endschalter_'+label,g,'black','sheet','Gehaeuse sichtbar, keine Sicherheitsfunktion spezifiziert',datum=('-cover_width/2','cover_front_y_v4+30','cover_bottom_z+%s'%zz))
        box(p,('-cover_width/2-20','cover_front_y_v4+15','cover_bottom_z+%s'%zz),(20,30,55));cyl(p,('-cover_width/2-10','cover_front_y_v4+30','cover_bottom_z+%s+55'%zz),6,8)
    # 9. ELECTRICAL FIT ENVELOPES, with photo-visible topology only.
    g='09_Elektrik'
    p=part('XMT_1000_DRIVER_Platine',g,'pcb','elec','Bestueckungs-Huellmodell, kein Schaltplan; keine Leiterbahnen rekonstruiert',datum=(0,'pcb_plane_y','cover_bottom_z+170'),cls='ELEKTRIK_HUELLMODELL')
    box(p,('-electronics_board_w/2','pcb_plane_y','cover_bottom_z+170'),('electronics_board_w','electronics_pcb_t','electronics_board_h'))
    for xx in [-1,1]:
        for zz in [8,260]:cyl(p,('%s*(electronics_board_w/2-7)'%xx,'pcb_plane_y-0.1','cover_bottom_z+170+%s'%zz),3.2,'electronics_pcb_t+0.2',(0,1,0),'cut','Platinenbefestigung')
    p=part('XMT_Steuer_Tochterplatine',g,'pcb','elec',datum=(-30,'pcb_plane_y-17','cover_bottom_z+230'),cls='ELEKTRIK_HUELLMODELL')
    box(p,(-53,'pcb_plane_y-17','cover_bottom_z+230'),(46,1.6,105))
    p=part('XMT_Mikrocontroller_Huelle',g,'black','elec',datum=(-30,'pcb_plane_y-23','cover_bottom_z+245'),cls='ELEKTRIK_HUELLMODELL');box(p,(-40,'pcb_plane_y-23','cover_bottom_z+245'),(20,6,65))
    for i,(xx,zz) in enumerate([(14,240),(34,290),(16,340),(33,384),(-17,425)]):
        p=part('XMT_Elko_%02d'%i,g,'dark','elec',datum=(xx,'pcb_plane_y','cover_bottom_z+%s'%zz),cls='ELEKTRIK_HUELLMODELL')
        cyl(p,(xx,'pcb_plane_y','cover_bottom_z+%s'%zz),12,23,(0,-1,0));cyl(p,(xx,'pcb_plane_y-23','cover_bottom_z+%s'%zz),10,0.5,(0,-1,0))
    p=part('XMT_Leistungsklemmenblock',g,'dark','elec',datum=(45,'pcb_plane_y','cover_bottom_z+235'),cls='ELEKTRIK_HUELLMODELL')
    box(p,(37,'pcb_plane_y-20','cover_bottom_z+235'),(20,20,92))
    for i in range(6):cyl(p,(47,'pcb_plane_y-20.1','cover_bottom_z+244+%s*14'%i),6,4,(0,1,0),'cut','Klemmschraubenmulde')
    p=part('XMT_Signalklemme',g,'green','elec',datum=(0,'pcb_plane_y','cover_bottom_z+178'),cls='ELEKTRIK_HUELLMODELL');box(p,(-18,'pcb_plane_y-16','cover_bottom_z+178'),(72,16,16))
    for i in range(8):cyl(p,('-13+%s*8.5'%i,'pcb_plane_y-16.1','cover_bottom_z+186'),4,4,(0,1,0),'cut')
    p=part('XMT_Netzdrossel_Huelle',g,'copper','elec',datum=(12,'pcb_plane_y','cover_bottom_z+409'),cls='ELEKTRIK_HUELLMODELL')
    cyl(p,(12,'pcb_plane_y','cover_bottom_z+409'),24,20,(0,-1,0));cyl(p,(12,'pcb_plane_y+0.1','cover_bottom_z+409'),13,20.2,(0,-1,0),'cut')
    p=part('EMI_Filter_Huelle',g,'dark','elec','Typenschild im Foto; interne Filterbauteile nicht modelliert',datum=(0,'pcb_plane_y','cover_bottom_z+35'),cls='ELEKTRIK_HUELLMODELL')
    box(p,(-57,'pcb_plane_y-36','cover_bottom_z+35'),(114,36,80))
    p=part('PE_Sammelschiene',g,'bronze','elec',datum=(0,'pcb_plane_y','cover_bottom_z+148'),cls='ELEKTRIK_HUELLMODELL');box(p,(-49,'pcb_plane_y-6','cover_bottom_z+148'),(98,6,9))
    for i in range(8):cyl(p,('-43+%s*12'%i,'pcb_plane_y-6.1','cover_bottom_z+152.5'),3,6.2,(0,1,0),'cut')
    p=part('TDE_2232_Transformator_Huelle',g,'core','elec',datum=(0,'pcb_plane_y','cover_bottom_z+450'),cls='ELEKTRIK_HUELLMODELL');box(p,(-43,'pcb_plane_y-44','cover_bottom_z+450'),(86,44,60))
    p=part('Relais_Huelle',g,'glass','elec',datum=(-23,'pcb_plane_y','cover_bottom_z+515'),cls='ELEKTRIK_HUELLMODELL');box(p,(-40,'pcb_plane_y-28','cover_bottom_z+515'),(34,28,40))
    p=part('Hilfsversorgung_Platine',g,'pcb','elec',datum=(0,'pcb_plane_y','cover_bottom_z+558'),cls='ELEKTRIK_HUELLMODELL');box(p,(-55,'pcb_plane_y','cover_bottom_z+558'),(110,1.6,100))
    p=part('Hilfsversorgung_Trafokern',g,'bronze','elec',datum=(18,'pcb_plane_y','cover_bottom_z+601'),cls='ELEKTRIK_HUELLMODELL');box(p,(-9,'pcb_plane_y-45','cover_bottom_z+573'),(56,45,62));box(p,(0,'pcb_plane_y-45.1','cover_bottom_z+587'),(36,25,32),'cut')
    p=part('Hilfsversorgung_Trafospule',g,'white','elec',datum=(18,'pcb_plane_y-35','cover_bottom_z+603'),cls='ELEKTRIK_HUELLMODELL');box(p,(0,'pcb_plane_y-43','cover_bottom_z+587'),(36,24,32))
    p=part('Hilfsversorgung_Kuehlkoerper',g,'black','elec',datum=(-40,'pcb_plane_y','cover_bottom_z+598'),cls='ELEKTRIK_HUELLMODELL');box(p,(-53,'pcb_plane_y-4','cover_bottom_z+578'),(23,4,55))
    for i in range(5):box(p,('-53+%s*5'%i,'pcb_plane_y-26','cover_bottom_z+578'),(2,23,55))
    p=part('Hilfsversorgung_USB_Buchse_Huelle',g,'steel','elec','Nur Gehaeuseform, keine PC-Schnittstellenzusage',datum=(-40,'pcb_plane_y','cover_bottom_z+563'),cls='ELEKTRIK_HUELLMODELL');box(p,(-48,'pcb_plane_y-16','cover_bottom_z+558'),(15,16,7));box(p,(-46,'pcb_plane_y-16.1','cover_bottom_z+560'),(11,12,3),'cut')
    # 10. Remaining actual machine guards; photo/manual-based outline only.
    g='10_Schutz'
    for nm in ['Spindelschutz_oben','Spindelschutz_unten','Schutz_Halter','Schutz_Klemmschraube_-1','Schutz_Klemmschraube_1','Faltenbalg_Z','Faltenbalg_Y_hinten','Lampenhalter','Arbeitslampe','Arbeitslampe_Linse']:
        keep(nm,g,'manual')
    p=part('Riemenhauben_Sicherheitsschalter',g,'orange','head','Sichtdarstellung des vorhandenen Schalters; keine sicherheitstechnische Bewertung',datum=(0,185,'head_top_z+7'))
    box(p,(-39,179,'head_top_z+7'),(78,29,23));box(p,(-39,178.9,'head_top_z+16'),(6,13,3),'cut','Betaetiger_Schlitz')
    # Photo-visible corrugated cable hoses. Neutral-pose envelope only.
    # 3D polyline with circular segments, not an electrical or fatigue model.
    for hi,zz in enumerate([340,470]):
        g='08_Blechsaeule'
        q=part('Wellschlauch_%s_Neutralstellung'%(hi+1),g,'black','sheet','Foto-basierte Kabelfuehrung, neutraler Bogen; keine kinematische Kabelsimulation',datum=('-cover_width/2-20','cover_front_y_v4+65','cover_bottom_z+%s'%zz),cls='KABEL_HUELLMODELL')
        # coordinates relative to gland. Loop returns toward head, short lower loop.
        path=[]
        for k in range(21):
            t=k/20.0
            path.append((-145*math.sin(math.pi*t/2),-170*t,85*math.sin(math.pi*t)+55*t))
        origin=q['datum']
        for k in range(len(path)-1):
            a=path[k];b=path[k+1];delta=[b[j]-a[j] for j in range(3)];ll=math.sqrt(sum(x*x for x in delta));axis=tuple(x/ll for x in delta)
            po=[add(origin[j],a[j]-axis[j]*0.6) for j in range(3)]
            cyl(q,po,23,ll+1.2,axis,label='Schlauchsegment_%s'%k)
            for f in [0.25,0.65]:
                rr=[add(origin[j],a[j]+axis[j]*ll*f) for j in range(3)]
                cyl(q,rr,27,1.8,axis,label='Wellrippe_%s'%k)
    # Common external fittings visible on the cabinet.
    g='08_Blechsaeule'
    q=part('Netzeinbaustecker_Huelle',g,'black','sheet','Nur Gehaeuseform; keine Netzverdrahtung',datum=('-cover_width/2','cover_front_y_v4+120','cover_bottom_z+100'))
    box(q,('-cover_width/2-4','cover_front_y_v4+108','cover_bottom_z+87'),(8,24,26))
    box(q,('-cover_width/2-4.1','cover_front_y_v4+112','cover_bottom_z+92'),(7,16,16),'cut','Steckoeffnung')
    for i in [0,1]:
        q=part('Sicherungshalter_Huelle_%s'%i,g,'black','sheet','Funktionszuordnung nach Aussenform, elektrisch nicht spezifiziert',datum=('-cover_width/2','cover_front_y_v4+120','cover_bottom_z+140+%s*25'%i))
        cyl(q,('-cover_width/2','cover_front_y_v4+120','cover_bottom_z+140+%s*25'%i),17,8,(-1,0,0))
    # Small photographed plunger switch and its mounting angle at the head.
    g='05_Spindelkopf'
    q=part('Spindelschutz_Schalterhalter',g,'dark','head',datum=('-head_x/2-12','-head_front+12','head_bottom_z-9'))
    box(q,('-head_x/2-16','-head_front+10','head_bottom_z-26'),(4,28,54))
    box(q,('-head_x/2-16','-head_front+10','head_bottom_z+24'),(16,28,4))
    q=part('Spindelschutz_Schalter_Huelle',g,'black','head','Foto-Sichtmodell; Kontaktfunktion und Sicherheitsklassifikation nicht modelliert',datum=('-head_x/2-18','-head_front+24','head_bottom_z-14'))
    box(q,('-head_x/2-37','-head_front+10','head_bottom_z-38'),(21,28,40))
    cyl(q,('-head_x/2-26','-head_front+24','head_bottom_z+2'),5,8)
    # Common normalization. Every part receives own datum and local parametric operations.
    for i,d in enumerate(parts,1):
        d['id']='P%03d'%i
        if d['datum'] is None:d['datum']=list(d['ops'][0]['origin'])
        d['filename']=d['id']+'_'+re.sub('[^A-Za-z0-9_]+','_',d['name'])
        if 'status' not in d:d['status']='FOTO_REKONSTRUKTION'
    return parts

def local_definition(d):
    n=copy.deepcopy(d);datum=d['datum']
    for op in n['ops']:
        op['origin']=[sub(q,a) for q,a in zip(op['origin'],datum)]
        if 'points' in op:op['points']=[[sub(q,a) for q,a in zip(pt,datum)] for pt in op['points']]
    return n

def used_parameters(d):
    names=set();known={x['name'] for x in SPECS}|set(DERIVED)
    def scan(x):
        if isinstance(x,str):names.update(t for t in re.findall(r'\b[A-Za-z_]\w*\b',x) if t in known)
        elif isinstance(x,(list,tuple)):
            for v in x:scan(v)
        elif isinstance(x,dict):
            for k,v in x.items():
                if k not in ('label','note','source','name'):scan(v)
    scan(d['ops']);scan(d['datum'])
    while True:
        n=len(names)
        for k in list(names):
            if k in DERIVED:scan(DERIVED[k])
        if len(names)==n:break
    return names

def check_recipe(p,parts=None):
    validate(p);v=all_values(p);names=set()
    for d in (parts if parts is not None else recipe()):
        if d['name'] in names:raise ValueError('Doppelter Teilname: '+d['name'])
        names.add(d['name'])
        for op in d['ops']:
            for c in op['origin']:evaluate(c,v)
            sizes=op['size'] if op['kind']=='box' else [op['height']]
            if op['kind'] in ('cylinder','cone','ringcut'):sizes=sizes+[op['diameter']]
            if op['kind']=='ringcut' and evaluate(op['inner_diameter'],v)>=evaluate(op['diameter'],v):raise ValueError('Ungueltige Ringnut')
            for s_ in sizes:
                if evaluate(s_,v)<=0:raise ValueError('Nichtpositive Groesse: '+d['name']+' '+op['label']+' '+s_)
            if 'points' in op:
                for pt in op['points']:
                    for c in pt:evaluate(c,v)
    return v
