# -*- coding: utf-8 -*-
"""Integrated CNC VIEW MODEL on the supplied SX3.5Z v4.8 reconstruction.
Not a machine-fit, manufacturing or purchasing release. Only stdlib required.
Axes use existing model coordinates. All unmeasured adapters are explicit designs.
"""
import copy, json, math, os, re
from collections import OrderedDict
import modell_v4 as base

VERSION='CNC_ANSICHT_01'
SPECS=copy.deepcopy(base.SPECS)
DERIVED=copy.deepcopy(base.DERIVED)
PALETTE=dict(base.PALETTE, design_blue=(0.17,0.38,0.62,1), cabinet=(0.54,0.55,0.53,1))
GROUPS=OrderedDict(base.GROUPS)
GROUPS['01_Basis']='Basis ohne manuellen Y-Vorschub'
GROUPS['02_Saeule']='Gusssaeule ohne Original-Hubmotor'
GROUPS['03_Kreuzschlitten']='Sattel und Fuehrungen'
GROUPS['04_Tisch']='Tisch ohne Handraeder und Originalgewindetriebe'
GROUPS.update([('11_CNC_X','CNC X – positionierter Ansichts-Entwurf'),
               ('12_CNC_Y','CNC Y – positionierter Ansichts-Entwurf'),
               ('13_CNC_Z','CNC Z – positionierter Ansichts-Entwurf')])
LAYERS={g:(i+1)*10 for i,g in enumerate(GROUPS)}
SOURCE='Integrierte Ansicht: Maschinenrezept v4.8 + Quellen aus Entwicklung03/09/10 + markierte Ansichtsannahmen.'
evaluate=base.evaluate
local_definition=base.local_definition

REMOVED_NAMES={
 'Z_Original_Gleitspindel','Z_Lagerbock_Original','Z_Lager_Stellring',
 'Z_Kupplung_Spindelseite','Z_Kupplungsstern','Z_Kupplung_Motorseite','Z_Motor_Adapterplatte',
 'Z_Motorplatte_Schraube_-48_-35','Z_Motorplatte_Schraube_-48_35',
 'Z_Motorplatte_Schraube_48_-35','Z_Motorplatte_Schraube_48_35',
 'GPG_4GN_18K_Getriebe_Huelle','GPG_4RK25GN_C_Motor_Huelle',
 'X_Original_Spindelmutter_Geteilt','Y_Original_Spindelmutter_Platzhalter',
 'X_Original_Gleitspindel','Y_Original_Gleitspindel','X_Lagerflansch_rechts',
 'X_Lagerabschluss_links','Y_Lagerflansch_vorn','X_Skalenring','Y_Skalenring',
 'Handrad_X','Handrad_Y','Handradgriff_X','Handradgriff_Y','Handradmutter_X','Handradmutter_Y',
 'Z_Mutterhalter_Original','Z_Original_Bronzemutter'}

NEW_DEFAULTS={}
def spec(name,value,note,source='Ansichts-Entwurf; nicht vermessen',status='ANSICHT_ENTWURF'):
    NEW_DEFAULTS[name]=value
    SPECS.append(dict(name=name,value=value,unit='mm',status=status,note=note,source=source,limits=None))

for a in 'xyz':
    z=a=='z';n='cnc_'+a+'_'
    for name,value,note in [
        ('screw_d',20 if z else 16,'Kugelspindel nur als Aussenzylinder; keine Laufbahn'),
        ('lead',5,'Steigung als Metadatum; keine Gewindegeometrie'),
        ('nut_od',33 if z else 28,'Rundmutter-Aussenmass aus uebernommener Katalogreferenz'),
        ('nut_l',50,'Mutternlaenge aus Entwicklung09; keine Detailinnenkontur'),
        ('nut_w',53 if z else 47,'Spannblock-Breite aus Entwicklung10'),
        ('nut_h',40 if z else 33,'Spannblock-Hoehe aus Entwicklung10'),
        ('nut_block_l',61.5 if z else 54,'Spannblock-Laenge aus Entwicklung10'),
        ('journal_d',15 if z else 12,'Lagerzapfen-ENTWURF; kein bestellbares Endenmass'),
        ('free_journal_d',12 if z else 10,'Loslagerzapfen-ENTWURF'),
        ('bearing_bore',32 if z else 28,'Lagerhuelle-ENTWURF; kein spezifiziertes Lager'),
        ('free_bearing_bore',28 if z else 24,'Loslager-Huellmass, nicht ausgelegt'),
        ('motor_w',86 if z else 56.4,'Z: reiner Motorbauraum; X/Y: CS-M22326 CAT2022'),
        ('motor_l',118 if z else 103,'Z: Bauraumannahme; X/Y: CAT2022, andere Revisionen koennen abweichen'),
        ('motor_pitch',69.6 if z else 47.14,'Z: unbestaetigtes Lochbild; X/Y: CAT2022'),
        ('pilot_d',73 if z else 38.1,'Z: Bauraumannahme; X/Y: CAT2022'),
        ('shaft_d',14 if z else 8,'Z: Bauraumannahme; X/Y: CAT2022'),
        ('shaft_l',32 if z else 21,'Z: Bauraumannahme; X/Y: CAT2022'),
        ('plate_w',108 if z else 84,'Motorhalterplatten als freie Entwurfsmassen'),
        ('plate_t',10,'Entwurfsdicke, keine Festigkeitsberechnung'),
        ('spacer_pitch',88 if z else 66,'Abstand der Halter-Distanzsaeulen'),
        ('coupling_d',40 if z else 32,'Kupplungshuelle, Hersteller/Baugroesse nicht ausgewaehlt'),
    ]:spec(n+name,value,note)
    DERIVED[n+'motor_front']=n+'shaft_l+57'
    DERIVED[n+'spacer_l']=n+'motor_front-'+n+'plate_t-10'
DERIVED.update([
 ('cnc_x_core_l','table_x-12'),('cnc_y_core_l','guide_length-20'),('cnc_z_core_l','lead_z_length'),
 ('cnc_x_nut_x','-saddle_x/2+9')])

DEFAULT_COLORS={'machine_red':186,'red':186,'cast':186,'steel':36,'silver':36,'aluminum':36,
 'castiron':36,'cabinet':36,'grey':36,'core':36,'panel':36,'white':1,
 'black':31,'dark':31,'design_blue':211,'orange':106,'yellow':6,'green':103,
 'pcb':103,'lcd':103,'bronze':100,'copper':100,'glass':36}


def load_parameters(path=None):
    p=OrderedDict(base.load_parameters(path));p.update(NEW_DEFAULTS)
    if path:
        fn=os.path.join(os.path.dirname(os.path.abspath(path)),'CNC_Parameter.json')
        if os.path.isfile(fn):
            with open(fn,encoding='utf-8-sig') as f: overrides=json.load(f)
            if not isinstance(overrides,dict):raise ValueError('CNC_Parameter.json muss ein Objekt sein')
            for k,v in overrides.items():
                if k.startswith('_'):continue
                if k not in NEW_DEFAULTS:raise ValueError('Unbekannter CNC-Parameter: '+k)
                if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError('Ungueltiger Wert: '+k)
                p[k]=float(v)
    validate(p);return p


def validate(p):
    base.validate({s['name']:p[s['name']] for s in base.SPECS})
    for name in NEW_DEFAULTS:
        x=p[name]
        if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<=0:
            raise ValueError('Positives endliches CNC-Mass erforderlich: '+name)
    for a in 'xyz':
        n='cnc_'+a+'_';v=lambda k:p[n+k]
        if v('journal_d')>=v('bearing_bore') or v('free_journal_d')>=v('free_bearing_bore'):
            raise ValueError('Lagerhuelle ohne Wand: '+a)
        if v('screw_d')>=v('nut_od') or v('nut_od')>=min(v('nut_w'),v('nut_h')):
            raise ValueError('Mutter-/Aufnahmehuelle inkonsistent: '+a)
        if v('pilot_d')+.5>=v('plate_w') or v('motor_pitch')+6>=v('motor_w'):
            raise ValueError('Motoranschluss passt nicht in Huellmass: '+a)
        if v('spacer_pitch')+14>=v('plate_w'):
            raise ValueError('Distanzhuelsen ueber Plattenrand: '+a)
        if v('bearing_bore')>=52 or v('free_bearing_bore')>=44:
            raise ValueError('Lagergehaeuse fuer gewaehlte Huelle zu klein: '+a)
        if v('shaft_d')>=v('coupling_d') or v('journal_d')>=v('coupling_d'):
            raise ValueError('Kupplung ohne Wand: '+a)
        if v('nut_l')>v('nut_block_l'):
            raise ValueError('Diese Ansicht erwartet eine vollstaendig im Block liegende Mutter')
    if p['table_x']<=40 or p['guide_length']<=40:raise ValueError('Spindellaenge zu klein')


def all_values(p):
    v=OrderedDict(p)
    for k,expr in DERIVED.items():v[k]=evaluate(expr,v)
    return v


def used_parameters(d):
    known={s['name'] for s in SPECS}|set(DERIVED); found=set()
    def scan(x):
        if isinstance(x,str):found.update(set(re.findall(r'\b[A-Za-z_]\w*\b',x))&known)
        elif isinstance(x,(list,tuple)):
            for v in x:scan(v)
        elif isinstance(x,dict):
            for k,v in x.items():
                if k not in ('label','note','source','name'):scan(v)
    scan(d['ops']);scan(d['datum'])
    while True:
        old=set(found)
        for k in list(found):
            if k in DERIVED:scan(DERIVED[k])
        if found==old:return found


def _add(a,b):return '(%s)+(%s)'%(a,b)
def _neg(x):return '-(%s)'%x

class Frame:
    """Right-handed axis-aligned coordinate permutation: local W is drive axis."""
    def __init__(self,origin,columns):self.origin=list(map(str,origin));self.columns=columns
    def point(self,xyz):
        result=[]
        for k in range(3):
            terms=[self.origin[k]]
            for j in range(3):
                c=self.columns[j][k]
                if c:terms.append(str(xyz[j]) if c>0 else _neg(xyz[j]))
            result.append('+'.join('(%s)'%t for t in terms))
        return result
    @property
    def axis(self):return self.columns[2]
    def box(self,p,o,s,op='add',label='Entwurfsblock'):
        lo=[];size=[]
        for k in range(3):
            j=next(j for j in range(3) if self.columns[j][k])
            c=self.columns[j][k]
            lo.append(_add(self.origin[k],o[j] if c>0 else _neg(_add(o[j],s[j]))));size.append(str(s[j]))
        base.box(p,lo,size,op,label)
    def cyl(self,p,o,d,h,op='add',label='Huellzylinder'):
        base.cyl(p,self.point(o),d,h,self.axis,op,label)


def recipe():
    parts=[]
    for raw in base.recipe():
        if raw['name'] in REMOVED_NAMES:continue
        d=copy.deepcopy(raw)
        if d['name']=='Basis_Guss_Foto':d['material']='machine_red'
        if d['name'] in ('Saeule_Guss_Foto','Saeulendeckel'):d['material']='dark'
        if d['name'].startswith('Blechsaeule_'):d['material']='cabinet'
        parts.append(d)
    for a,group in zip('xyz',('11_CNC_X','12_CNC_Y','13_CNC_Z')):
        A=a.upper();n='cnc_'+a+'_'
        if a=='x':
            origin=['pos_x+table_x/2','pos_y','x_wheel_z'];cols=((0,1,0),(0,0,1),(1,0,0))
            nut_origin=['cnc_x_nut_x','pos_y','x_wheel_z']
        elif a=='y':
            origin=[0,'base_front_y','y_wheel_z'];cols=((1,0,0),(0,0,1),(0,-1,0))
            nut_origin=[0,'pos_y','y_wheel_z']
        else:
            origin=[0,'column_screw_y','column_top_z+column_cap_h'];cols=((1,0,0),(0,1,0),(0,0,1))
            nut_origin=[0,'column_screw_y','z_nut_center']
        f=Frame(origin,cols);nf=Frame(nut_origin,cols)
        def part(suffix,mat='steel',at=(0,0,0),frame=None,source=None,status='ANSICHT_ENTWURF',note=None):
            fr=frame or f
            p=dict(name='CNC_'+A+'_'+suffix,group=group,material=mat,ops=[],datum=fr.point(at),
                status=status,source=source or 'Bestehende Modell-Achslage v4.8; freie Ansichtsmasse',
                note=note or 'ANSICHT: Anschluss-/Lochmasse, Passungen und Freigaenge unbestaetigt. Keine Fertigungs- oder Bestellfreigabe.',
                manufacturing_released=False)
            parts.append(p);return p
        p=part('Kugelspindel_Huelle',at=(0,0,_neg(n+'core_l')),
               note='Durchgehende Aussenzylinder mit entworfenen Endzapfen. Keine Kugellaufbahn. Laenge aus Bestandsrezept, nicht aus Katalog-Rohlingsraster.')
        f.cyl(p,(0,0,_neg(n+'core_l')),n+'screw_d',n+'core_l+8',label='Kugelgewindebereich_HUELLE')
        f.cyl(p,(0,0,8),n+'journal_d',45,label='Antriebszapfen_ANNAHME')
        f.cyl(p,(0,0,_neg(n+'core_l+20')),n+'free_journal_d',20,label='Loslagerzapfen_ANNAHME')
        nut_article='213420 0005' if a=='z' else '213505'
        p=part('Rundmutter_Huelle','steel',frame=nf,source='Quellen/Quellen_09.json; isel '+nut_article,
               status='KATALOGHUELLE_UNGEPRUEFT',note='Nur Katalog-Aussenhuelle. Innenbohrung ist Darstellungsbohrung, keine Herstellerlaufbahn. Lieferung und Eignung unbestaetigt.')
        nf.cyl(p,(0,0,_neg(n+'nut_l/2')),n+'nut_od',n+'nut_l')
        nf.cyl(p,(0,0,_neg(n+'nut_l/2+0.5')),n+'screw_d',n+'nut_l+1','cut','Darstellungsbohrung')
        p=part('Mutteraufnahme_Entwurf','design_blue',frame=nf,
               source='Quellen/Quellen_10.json; vereinfachte Haupthuelle '+('213600' if a=='z' else '213500'),
               note='B/H/L nach uebernommener Spannblock-Tabelle; H1 und reale Klemm-/Fussgeometrie unbestaetigt. Kein maschinenspezifisches Lochbild.')
        nf.box(p,(_neg(n+'nut_w/2'),_neg(n+'nut_h/2'),_neg(n+'nut_block_l/2')),(n+'nut_w',n+'nut_h',n+'nut_block_l'))
        nf.cyl(p,(0,0,_neg(n+'nut_block_l/2+1')),n+'nut_od',n+'nut_block_l+2','cut','Mutteraufnahme_Nennhuelle')
        if a=='z':
            p=part('Mutteranschluss_Kopf_Entwurf','design_blue',frame=nf,at=(0,_neg(n+'nut_h/2'),0))
            base.box(p,('-'+n+'nut_w/2','column_front_y','z_nut_center-20'),(n+'nut_w','column_screw_y-column_front_y-'+n+'nut_h/2',40),label='Anschlussbruecke_ANNAHME')
        # Stationary / table-borne end bearing and flange, each separately editable.
        p=part('Anschlussplatte_Entwurf','design_blue')
        f.box(p,(_neg(n+'plate_w/2'),_neg(n+'plate_w/2'),0),(n+'plate_w',n+'plate_w',10))
        f.cyl(p,(0,0,-1),n+'screw_d+6',12,'cut','Spindelfreiraum')
        for u in (-1,1):
            for vv in (-1,1):f.cyl(p,(f'{u}*{n}spacer_pitch/2',f'{vv}*{n}spacer_pitch/2',-1),6.6,12,'cut','Entwurfsloch_KEIN_MASCHINENLOCHBILD')
        p=part('Festlager_Entwurf','dark',at=(0,0,10))
        f.box(p,(-30,-26,10),(60,52,24))
        f.cyl(p,(0,0,9),n+'bearing_bore',26,'cut','Lagersitz_NENN_KEINE_PASSUNG')
        p=part('Festlager_Ringhuelle','silver',at=(0,0,10))
        f.cyl(p,(0,0,10),n+'bearing_bore',24)
        f.cyl(p,(0,0,9),n+'journal_d',26,'cut','Lagerinnenring_HUELLE')
        p=part('Loslager_Entwurf','dark',at=(0,0,_neg(n+'core_l+20')))
        f.box(p,(-25,-22,_neg(n+'core_l+20')),(50,44,20))
        f.cyl(p,(0,0,_neg(n+'core_l+21')),n+'free_bearing_bore',22,'cut','Loslager_Durchgang')
        p=part('Loslager_Ringhuelle','silver',at=(0,0,_neg(n+'core_l+20')))
        f.cyl(p,(0,0,_neg(n+'core_l+20')),n+'free_bearing_bore',20)
        f.cyl(p,(0,0,_neg(n+'core_l+21')),n+'free_journal_d',22,'cut','Lagerinnenring_HUELLE')
        for name,start,d in [('Spindel',40,n+'journal_d'),('Motor',58,n+'shaft_d')]:
            p=part('Kupplung_'+name,'silver',at=(0,0,start))
            f.cyl(p,(0,0,start),n+'coupling_d',12)
            f.cyl(p,(0,0,start-1),d,14,'cut','Nabenbohrung_ANSICHT')
        p=part('Kupplungsstern','orange',at=(0,0,52))
        f.cyl(p,(0,0,52),n+'coupling_d-2',6)
        f.cyl(p,(0,0,51),n+'journal_d+4',8,'cut','Freiraum')
        for i,(u,vv) in enumerate([(u,vv) for u in (-1,1) for vv in (-1,1)],1):
            uv=(f'{u}*{n}spacer_pitch/2',f'{vv}*{n}spacer_pitch/2')
            p=part('Distanzsaeule_'+str(i),'silver',at=(*uv,10))
            f.cyl(p,(*uv,10),12,n+'spacer_l');f.cyl(p,(*uv,9),6.6,n+'spacer_l+2','cut','Schraubenkanal')
            p=part('Halteschraube_'+str(i),'dark',at=(*uv,n+'motor_front'))
            f.cyl(p,(*uv,3),6,n+'motor_front-3');f.cyl(p,(*uv,n+'motor_front'),10,6)
        p=part('Motorplatte_Entwurf','design_blue',at=(0,0,n+'motor_front-'+n+'plate_t'))
        f.box(p,(_neg(n+'plate_w/2'),_neg(n+'plate_w/2'),n+'motor_front-'+n+'plate_t'),(n+'plate_w',n+'plate_w',n+'plate_t'))
        f.cyl(p,(0,0,n+'motor_front-'+n+'plate_t-1'),n+'pilot_d+0.5',n+'plate_t+2','cut','Motorbund_Freiraum')
        for pitch,dia in [(n+'motor_pitch',5.5 if a!='z' else 6.6),(n+'spacer_pitch',6.6)]:
            for u in (-1,1):
                for vv in (-1,1):f.cyl(p,(f'{u}*{pitch}/2',f'{vv}*{pitch}/2',n+'motor_front-'+n+'plate_t-1'),dia,n+'plate_t+2','cut','Motorplatte_Lochbild')
        source='Quellen/Quellen_03.json; CS-M22326 CAT2022 Aussenmasse' if a!='z' else 'Z-Motor 86x86x118 ist NUR ein unbestimmter Bauraum, keine Kaufteilwahl'
        status='KATALOGHUELLE_UNGEPRUEFT' if a!='z' else 'ANSICHT_ENTWURF'
        p=part('Motor_Gehaeuse','black',at=(0,0,n+'motor_front+5'),source=source,status=status,
               note=source+'; Keine Last-/Dynamikauslegung. Stecker-/Rippendetails angenaehert.')
        f.box(p,(_neg(n+'motor_w/2'),_neg(n+'motor_w/2'),n+'motor_front+5'),(n+'motor_w',n+'motor_w',n+'motor_l-10'))
        for suf,st in [('Frontflansch',n+'motor_front'),('Rueckdeckel',n+'motor_front+'+n+'motor_l-5')]:
            p=part('Motor_'+suf,'silver',at=(0,0,st),source=source,status=status)
            f.box(p,(_neg(n+'motor_w/2'),_neg(n+'motor_w/2'),st),(n+'motor_w',n+'motor_w',5))
            if suf=='Frontflansch':
                f.cyl(p,(0,0,st+'-1'),n+'shaft_d',7,'cut','Wellenaufnahme')
                for u in (-1,1):
                    for vv in (-1,1):f.cyl(p,(f'{u}*{n}motor_pitch/2',f'{vv}*{n}motor_pitch/2',st+'-1'),5 if a!='z' else 6,7,'cut','Motorloch')
        p=part('Motorbund','silver',at=(0,0,n+'motor_front-1.6'))
        f.cyl(p,(0,0,n+'motor_front-1.6'),n+'pilot_d',1.6);f.cyl(p,(0,0,n+'motor_front-2'),n+'shaft_d',3,'cut')
        p=part('Motorwelle','steel',at=(0,0,57),source=source,status=status)
        f.cyl(p,(0,0,57),n+'shaft_d',n+'shaft_l',label='Motorwelle')
        p=part('Motor_Stecker_Bauraum','black',at=(n+'motor_w/2',0,n+'motor_front+'+n+'motor_l-15'))
        f.box(p,(n+'motor_w/2',-8,n+'motor_front+'+n+'motor_l-25'),(12,16,20),label='Stecker_UNVERMESSEN')
        if a=='z':
            p=part('Haltebremse_Bauraum','orange',at=(0,0,n+'motor_front+'+n+'motor_l'),
                note='Nur Platzreservierung fuer noch auszuwaehlende Halte-/Absturzsicherung. Keine Sicherheitsfunktion nachgewiesen.')
            f.cyl(p,(0,0,n+'motor_front+'+n+'motor_l'),70,25,label='Bremsbauraum_KEIN_KAUFTEIL')
    for i,d in enumerate(parts,1):
        if d['name'].startswith('CNC_'):
            d['id']='C%03d'%i
            d['filename']=d['id']+'_'+d['name']
        # Preserve all original identifiers even where earlier pieces were removed.
    return parts


def check_recipe(p,parts=None):
    validate(p);v=all_values(p);defs=parts if parts is not None else recipe();names=set();ids=set()
    for d in defs:
        if d['name'] in names or d['id'] in ids:raise ValueError('Doppelter Teilname / ID')
        names.add(d['name']);ids.add(d['id'])
        if d['group'] not in GROUPS:raise ValueError('Unbekannte Gruppe')
        for op in d['ops']:
            for c in op['origin']:evaluate(c,v)
            sizes=op['size'] if op['kind']=='box' else [op['height']]
            if op['kind'] in ('cylinder','cone'):sizes=sizes+[op['diameter']]
            for s in sizes:
                if evaluate(s,v)<=0:raise ValueError('Nichtpositive Groesse: '+d['name']+' '+str(s))
            if 'points' in op:
                for pt in op['points']:
                    for c in pt:evaluate(c,v)
    return v
