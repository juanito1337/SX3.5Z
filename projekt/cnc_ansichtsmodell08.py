# -*- coding: utf-8 -*-
"""Umsetzung08: catalogue-linked hardware; original castings/door unchanged.
Native NX recipe. Measured machine interfaces, load cases and release remain open.
"""
import copy, json, math, re
from pathlib import Path
from collections import OrderedDict
import cnc_ansichtsmodell07 as legacy
from cnc_ansichtsmodell01 import Frame
base=legacy.base
evaluate=legacy.evaluate
local_definition=legacy.local_definition
VERSION='CNC_UMSETZUNG_08'
ROOT=Path(__file__).resolve().parent
CAT=json.loads((ROOT/'Einkauf/Kaufteile_08.json').read_text(encoding='utf-8'))['items']
SPECS=copy.deepcopy(legacy.SPECS)
DERIVED=copy.deepcopy(legacy.DERIVED)
GROUPS=OrderedDict(legacy.GROUPS)
GROUPS.update([('11_CNC_X','X – Kaufteilanschlüsse / Maschinenmaß offen'),('12_CNC_Y','Y – Kaufteilanschlüsse / Maschinenmaß offen'),('13_CNC_Z','Z – Bremsmotor-Familie / Revision offen'),('16_Schaltschrank','Reale Gerätehüllen / Elektroplanung offen'),('18_Prueffeld','Referenzsensoren – noch nicht an Achsen montiert')])
LAYERS={g:(i+1)*10 for i,g in enumerate(GROUPS)}
PALETTE=dict(legacy.PALETTE)
DEFAULT_COLORS=dict(legacy.DEFAULT_COLORS)
NEW_DEFAULTS=dict(legacy.NEW_DEFAULTS)
SOURCE='Umsetzung08: Einkauf/Kaufteile_08.json und Quellen/Quellen_08.json. Kein Bestell-/Fertigungsnachweis.'
CATALOG_PARAMETER_MAP=[]
def param(name,value,item=None,key=None,note='Eigener Konstruktionswert; Freigabe offen'):
    NEW_DEFAULTS[name]=float(value)
    found=next((s for s in SPECS if s['name']==name),None)
    entry=dict(name=name,value=float(value),unit='mm',status='KATALOG_HAUPTMASS' if item else 'KONSTRUKTIONSENTWURF',note=note,source=item or SOURCE,limits=None)
    if found:found.update(entry)
    else:SPECS.append(entry)
    if item:CATALOG_PARAMETER_MAP.append((name,item,key))
for a in 'xyz':
    z=a=='z';n='cnc_'+a+'_';mid='K-MOT-Z' if z else 'K-MOT-XY';m=CAT[mid]['dims']
    for par,key in [('motor_w','width'),('motor_l','length'),('shaft_d','shaft_d'),('shaft_l','shaft_l'),('pilot_d','pilot_d'),('motor_pitch','pitch')]:
        param(n+par,m[key],mid,key,CAT[mid]['note'])
    for typ,id in [('fk','K-FK15' if z else 'K-FK12'),('ff','K-FF15' if z else 'K-FF12')]:
        for key,value in CAT[id]['dims'].items():param(n+typ+'_'+key,value,id,key)
    param(n+'free_journal_d',CAT['K-FF15' if z else 'K-FF12']['dims']['shaft_d'],'K-FF15' if z else 'K-FF12','shaft_d')
    kid='K-KUP-Z' if z else 'K-KUP-XY'
    for key,value in CAT[kid]['dims'].items():param(n+'kup_'+key,value,kid,key)
    param(n+'coupling_d',CAT[kid]['dims']['diameter'],kid,'diameter')
    param(n+'adapter_t',17)
    param(n+'fixed_shaft_end',80 if z else 60,note='Nur axiale Hülle; fertige Endenzeichnung fehlt')
    param(n+'core_end',-6 if z else -5,note='Schulter außerhalb FK-Hauptkörper; Projektion nominal, Lieferzeichnung erforderlich')
    param(n+'coupling_start',49 if z else 44,note='Axiale Entwurfsposition, nicht Maschinenmaß')
    DERIVED[n+'motor_front']='125' if z else '84'
    DERIVED[n+'spacer_l']=n+'motor_front-'+n+'plate_t-'+n+'adapter_t'
for id in ('K-DRV-XY','K-DRV-Z','K-PS-AX','K-PS24','K-PS5','K-CABPL'):
    for key,val in CAT[id]['dims'].items():param('cat08_'+id[2:].lower().replace('-','_')+'_'+key,val,id,key)
# Do not silently accept arbitrary motor dimensions as a purchased article.
def assert_catalog_dimensions(p):
    for par,item,key in CATALOG_PARAMETER_MAP:
        if not math.isclose(p[par],CAT[item]['dims'][key],rel_tol=0,abs_tol=1e-9):
            raise ValueError('Kaufteilmaß stimmt nicht mit dokumentierter Revision überein: '+par)
def load_parameters(path=None):
    p=OrderedDict(legacy.load_parameters(path))
    # Catalog replaces exactly the historical nominal defaults; user geometry lives in Parameter/Ausbau files.
    p.update(NEW_DEFAULTS)
    if path:
        root=Path(path).resolve().parent
        for filename in ('CNC_Parameter.json','Ausbau_Parameter.json','Umsetzung_Parameter.json'):
            fp=root/filename
            if not fp.exists():continue
            q=json.loads(fp.read_text(encoding='utf-8-sig'))
            for k,val in q.items():
                if k.startswith('_'):continue
                if k not in p:raise ValueError('Unbekannter Parameter '+k)
                if isinstance(val,bool) or not isinstance(val,(float,int)) or not math.isfinite(val):raise ValueError('Ungültiger Parameter '+k)
                if k in {x[0] for x in CATALOG_PARAMETER_MAP}:
                    if val not in (NEW_DEFAULTS[k],legacy.NEW_DEFAULTS.get(k)):
                        raise ValueError('Individueller Kaufteil-Override: Lieferrevision zuerst dokumentieren: '+k)
                    p[k]=NEW_DEFAULTS[k]
                else:p[k]=float(val)
    validate(p);return p

def all_values(p):
    v=OrderedDict(p)
    for k,e in DERIVED.items():v[k]=evaluate(e,v)
    return v

def validate(p):
    legacy.validate(p);assert_catalog_dimensions(p)
    for par,_,_ in CATALOG_PARAMETER_MAP:
        if not math.isfinite(p[par]) or p[par]<=0:raise ValueError('Ungültiges Katalogmaß '+par)
    for a in 'xyz':
        n='cnc_'+a+'_';v=all_values(p)
        if v[n+'motor_front']-p[n+'shaft_l']-p[n+'fixed_shaft_end']<3:raise ValueError('Wellenenden stoßen zusammen: '+a)
    return True

def used_parameters(d):
    known={s['name'] for s in SPECS}|set(DERIVED);found=set()
    def scan(x):
        if isinstance(x,str):found.update(set(re.findall(r'\b[A-Za-z_]\w*\b',x))&known)
        elif isinstance(x,dict):
            for k,v in x.items():
                if k not in ('label','note','source','name'):scan(v)
        elif isinstance(x,(list,tuple)):
            for v in x:scan(v)
    scan(d['ops']);scan(d['datum'])
    while True:
        old=set(found)
        for k in list(found):
            if k in DERIVED:scan(DERIVED[k])
        if old==found:return found

def axis_frame(a):
    if a=='x':return Frame(('pos_x+table_x/2','pos_y','x_wheel_z'),((0,1,0),(0,0,1),(1,0,0)))
    if a=='y':return Frame((0,'base_front_y','y_wheel_z'),((1,0,0),(0,0,1),(0,-1,0)))
    return Frame((0,'column_screw_y','column_top_z+column_cap_h'),((1,0,0),(0,1,0),(0,0,1)))

def recipe():
    oldparts=legacy.recipe();ps=[]
    # Keep photo reconstruction, approved door and structural wet-room design unchanged.
    for src in oldparts:
        if src['group'] in ('11_CNC_X','12_CNC_Y','13_CNC_Z'):continue
        if src['group']=='16_Schaltschrank' and (src['name'].startswith('Treiber_') or src['name'] in ('48V_Achsenversorgung_BAURAUM','24V_Feldversorgung_BAURAUM','5V_Mesa_Versorgung_BAURAUM','Schaltschrank_Montageplatte')):continue
        d=copy.deepcopy(src);ps.append(d)
    def part(name,g,mat='steel',frame=None,at=(0,0,0),item=None,instance=None,kind='MAKE',note=None):
        p=dict(name=name,group=g,material=mat,datum=frame.point(at) if frame else list(map(str,at)),ops=[],status='ANFRAGESTAND_KEINE_FREIGABE',source=SOURCE,note=note or 'Eigener Entwurf; Maschinenanschluss und Festigkeit nicht bestätigt.',manufacturing_released=False,supply_kind='BUY' if item else kind,item_id=item or 'F-'+name,purchase_instance=instance or name)
        if item:p.update(source=(' '.join(CAT[item]['source_ids']) or 'Normteil ISO4762; nominale Hülle, Verbindungsauslegung offen'),note=note or CAT[item]['note'])
        ps.append(p);return p
    def bolt(name,g,f,u,v,head_z,d,l,item):
        p=part(name,g,'dark',f,(u,v,str(head_z)+'-'+str(l)),item,item+':'+name)
        f.cyl(p,(u,v,str(head_z)+'-'+str(l)),d,l,label='ISO4762_Schaft_ohne_Gewinde')
        f.cyl(p,(u,v,head_z),{4:7,5:8.5,6:10}[d],d,label='Kopf_vereinfacht')
        return p
    for a,g in zip('xyz',('11_CNC_X','12_CNC_Y','13_CNC_Z')):
        z=a=='z';A=a.upper();n='cnc_'+a+'_';pre='CNC_'+A+'_';f=axis_frame(a)
        revcols=(tuple(-x for x in f.columns[0]),f.columns[1],tuple(-x for x in f.columns[2]))
        ff=Frame(f.point((0,0,'-'+n+'core_l')),revcols)
        mitem='K-MOT-Z' if z else 'K-MOT-XY';mid=CAT[mitem]['dims'];ft=mid['flange_t']
        # Retain the catalogue-nut concept at the existing machine-coordinate datum; this is NOT a verified nut mount.
        for suffix,it in [('Rundmutter_Huelle','K-NUT20' if z else 'K-NUT16'),('Mutteraufnahme_Entwurf','K-NUTH20' if z else 'K-NUTH16')]:
            p=copy.deepcopy(next(x for x in oldparts if x['name']==pre+suffix));ps.append(p)
            p.update(supply_kind='BUY',item_id=it,purchase_instance=A+':'+it,note=CAT[it]['note'],source=' '.join(CAT[it]['source_ids']),manufacturing_released=False)
        # Retain unverified bridges as explicit custom interfaces, not fictitious catalogue supports.
        for suffix in ('Mutteranschluss_Kopf_Entwurf','Loslager_Brueckenwinkel','Tragbruecke_auf_Gusssaeule'):
            found=next((x for x in oldparts if x['name']==pre+suffix),None)
            if found:
                p=copy.deepcopy(found);ps.append(p);p['note']='BEIBEHALTENE ANSCHLUSSSTUDIE. Original-Aufmaß fehlt; passt nicht als bestätigter THK-Anschluss. Keine Bearbeitung des Gusses daraus ableiten.'
        # New machined adapter: bearing pilot, threaded bearing circle and independent rod threads.
        p=part(pre+'Anschlussplatte_Entwurf',g,'design_blue',f)
        f.box(p,('-'+n+'plate_w/2','-'+n+'plate_w/2',0),(n+'plate_w',n+'plate_w',n+'adapter_t'),label='Adapter_17mm_S355_ENTWURF')
        f.cyl(p,(0,0,-1),n+'fk_spigot_d',n+'adapter_t+2','cut','FK_Aufnahme_Nenn_H7_ENTWURF')
        for u,v in [(1,0),(0,1),(-1,0),(0,-1)]:
            f.cyl(p,(str(u)+'*'+n+'fk_pcd/2',str(v)+'*'+n+'fk_pcd/2',-1),4.2 if z else 3.3,n+'adapter_t+2','cut','FK_Gewindekern_M5' if z else 'FK_Gewindekern_M4')
        for i,(u,v) in enumerate([(u,v) for u in(-1,1) for v in(-1,1)],1):
            uu=f'{u}*{n}spacer_pitch/2';vv=f'{v}*{n}spacer_pitch/2'
            f.cyl(p,(uu,vv,-1),5,n+'adapter_t+2','cut','M6_Gewindekern_Distanzsaeule')
        p['note']='Neue17mm-Adapterplatte mit THK-Pilot und getrennten Gewinden. Gussseitige Befestigung fehlt bewusst bis X02/Y02/Z02; keine fertige Verbindung zur Maschine.'
        # Complete THK assemblies represented by one envelope, with sourced mounting holes.
        for typ,fr in [('fk',f),('ff',ff)]:
            it='K-'+typ.upper()+('15' if z else '12');k=n+typ+'_'
            p=part(pre+('THK_Festlager' if typ=='fk' else 'THK_Loslager'),g,'dark',fr,item=it,instance=A+':'+it)
            fr.cyl(p,(0,0,0),k+'spigot_d',k+'length',label='THK_Zentrierhuelle')
            fr.cyl(p,(0,0,k+'spigot_l'),k+'envelope_d',k+'flange_t',label='THK_Flansch_konservative_Rundhuelle')
            fr.cyl(p,(0,0,-1),k+'shaft_d',k+'length+2','cut','Lagerinnen_Darstellung')
            for i,(u,v) in enumerate([(1,0),(0,1),(-1,0),(0,-1)],1):
                uu=f'{u}*{k}pcd/2';vv=f'{v}*{k}pcd/2'
                fr.cyl(p,(uu,vv,k+'spigot_l-0.1'),k+'hole_d',k+'flange_t+0.2','cut','THK_Flanschbohrung')
                fr.cyl(p,(uu,vv,k+'length-'+k+'counter_depth'),k+'counter_d',k+'counter_depth+0.1','cut','THK_Senkung')
                bitem=('N-M5x20' if typ=='fk' else 'N-M5x16') if z else 'N-M4x16'
                bolt(pre+typ.upper()+'_Schraube_'+str(i),g,fr,uu,vv,k+'length-'+k+'counter_depth',5 if z else 4,20 if z and typ=='fk' else 16,bitem)
            if typ=='ff':
                q=part(pre+'Loslager_Adapterplatte',g,'design_blue',fr)
                fr.box(q,(-38,-35,0),(76,70,8),label='Loslageradapter_Eigenteil')
                fr.cyl(q,(0,0,-1),k+'spigot_d',10,'cut','FF_Aufnahme_Nenn_H7_ENTWURF')
                for u,v in[(1,0),(0,1),(-1,0),(0,-1)]:fr.cyl(q,(str(u)+'*'+k+'pcd/2',str(v)+'*'+k+'pcd/2',-1),4.2 if z else 3.3,10,'cut','FF_Gewindekern')
                q['note']='THK-seitige Maße modelliert. Lastabtrag/Brücke zur originalen Gegenlagerstelle fehlt; nicht als freitragende Platte bauen.'
        # Screw end is an envelope, NOT a fabricated final shaft. Unmachined core ends outside bearing body.
        p=part(pre+'Kugelspindel_Huelle',g,'steel',f,item='K-SCREW-'+A,instance=A+':Screw')
        f.cyl(p,(0,0,'-'+n+'core_l'),n+'screw_d',n+'core_l+'+n+'core_end',label='Gewindekern_Nennhuelle_ohne_Laufbahn')
        f.cyl(p,(0,0,n+'core_end'),n+'journal_d','(45)'+'-'+n+'core_end' if z else '(38)-'+n+'core_end',label='Festlagerzapfen_Huelle_KEINE_ENDENZEICHNUNG')
        f.cyl(p,(0,0,45 if z else 38),n+'kup_bore_a',35 if z else 22,label='Kupplungszapfen_Entwurf')
        f.cyl(p,(0,0,'-'+n+'core_l-25'),n+'free_journal_d',25,label='Loslagerzapfen_ohne_Sicherungsringnut')
        # Purchased coupling split into three model bodies, one purchase instance.
        ci='K-KUP-Z' if z else 'K-KUP-XY';c=n+'kup_';start=n+'coupling_start'
        for su,ww,bo in [('Spindel',start,c+'bore_a'),('Motor',start+'+'+c+'hub_l+'+c+'gap',c+'bore_b')]:
            q=part(pre+'Kupplung_'+su,g,'silver',f,(0,0,ww),ci,A+':Coupling')
            f.cyl(q,(0,0,ww),c+'diameter',c+'hub_l',label='KTR_Nabe_Hauptkontur')
            f.cyl(q,(0,0,'('+ww+')-1'),bo,c+'hub_l+2','cut','Klemmbohrung_Nenn')
            q['note']+=' Verzahnung/Klemmschlitz/Schraube fehlen; zusätzlicher Schraubenkopf-Hüllkreis '+str(CAT[ci]['dims']['head_envelope'])+'mm für Freiraum berücksichtigen.'
        ww=start+'+'+c+'hub_l'
        q=part(pre+'Kupplungsstern',g,'orange',f,(0,0,ww),ci,A+':Coupling')
        f.cyl(q,(0,0,ww),c+'diameter-2',c+'gap',label='Elastomer_Nur_Raumhuelle')
        f.cyl(q,(0,0,'('+ww+')-1'),18 if z else 10.5,c+'gap+2','cut','KTR_Mittenfreiraum')
        # Rods and two distinct fastener patterns.
        for i,(u,v) in enumerate([(u,v) for u in(-1,1) for v in(-1,1)],1):
            uu=f'{u}*{n}spacer_pitch/2';vv=f'{v}*{n}spacer_pitch/2'
            q=part(pre+'Distanzsaeule_'+str(i),g,'silver',f,(uu,vv,n+'adapter_t'))
            q['item_id']='F-SPACER-'+A
            f.cyl(q,(uu,vv,n+'adapter_t'),12,n+'spacer_l',label='Distanzrohr_Stahl_12x6_6')
            f.cyl(q,(uu,vv,n+'adapter_t-1'),6.6,n+'spacer_l+2','cut','Durchgang')
            bolt(pre+'Halteschraube_'+str(i),g,f,uu,vv,n+'motor_front',6,120 if z else 80,'N-M6x120' if z else 'N-M6x80')
        q=part(pre+'Motorplatte_Entwurf',g,'design_blue',f,(0,0,n+'motor_front-'+n+'plate_t'))
        f.box(q,('-'+n+'plate_w/2','-'+n+'plate_w/2',n+'motor_front-'+n+'plate_t'),(n+'plate_w',n+'plate_w',n+'plate_t'),label='Motorplatte_10mm_S355_ENTWURF')
        f.cyl(q,(0,0,n+'motor_front-'+n+'plate_t-1'),n+'pilot_d+0.2',n+'plate_t+2','cut','Motorbund_Freiraum_Nenn')
        for i,(u,v) in enumerate([(u,v) for u in(-1,1) for v in(-1,1)],1):
            for pitch,dd,label in [(n+'motor_pitch',4.2 if z else 3.3,'Motorgewindekern'),(n+'spacer_pitch',6.6,'Distanzschraube_Durchgang')]:
                f.cyl(q,(f'{u}*{pitch}/2',f'{v}*{pitch}/2',n+'motor_front-'+n+'plate_t-1'),dd,n+'plate_t+2','cut',label)
            bolt(pre+'Motorbefestigung_'+str(i),g,f,f'{u}*{n}motor_pitch/2',f'{v}*{n}motor_pitch/2',n+'motor_front+'+str(ft),5 if z else 4,20 if z else 12,'N-M5x20' if z else 'N-M4x12')
        # Motor front/body/rear are one purchase, not three motors.
        for suffix,w,h,mat in [('Frontflansch',n+'motor_front',str(ft),'silver'),('Gehaeuse',n+'motor_front+'+str(ft),n+'motor_l-'+str(ft+5),'black'),('Rueckdeckel',n+'motor_front+'+n+'motor_l-5','5','black')]:
            q=part(pre+'Motor_'+suffix,g,mat,f,(0,0,w),mitem,A+':Motor')
            f.box(q,('-'+n+'motor_w/2','-'+n+'motor_w/2',w),(n+'motor_w',n+'motor_w',h),label='Motor_Aussenhuelle')
            if suffix=='Frontflansch':
                f.cyl(q,(0,0,'('+w+')-1'),n+'shaft_d',str(ft+2),'cut','Welle_Durchgang')
                for u,v in[(u,v) for u in(-1,1) for v in(-1,1)]:f.cyl(q,(f'{u}*{n}motor_pitch/2',f'{v}*{n}motor_pitch/2','('+w+')-1'),mid['hole_d'],ft+2,'cut','Motor_Katalogloch')
            if suffix=='Gehaeuse':
                for u,v in[(u,v) for u in(-1,1) for v in(-1,1)]:f.cyl(q,(f'{u}*{n}motor_pitch/2',f'{v}*{n}motor_pitch/2','('+w+')-0.1'),10.5 if z else 9,7 if z else 6,'cut','Kopfzugang_nur_vereinfacht_NICHT_MOTOR_BEARBEITEN')
        q=part(pre+'Motorbund',g,'silver',f,(0,0,n+'motor_front-1.6'),mitem,A+':Motor')
        f.cyl(q,(0,0,n+'motor_front-1.6'),n+'pilot_d',1.6)
        f.cyl(q,(0,0,n+'motor_front-2'),n+'shaft_d',3,'cut','Welle')
        q=part(pre+'Motorwelle',g,'steel',f,(0,0,n+'motor_front-'+n+'shaft_l'),mitem,A+':Motor')
        f.cyl(q,(0,0,n+'motor_front-'+n+'shaft_l'),n+'shaft_d',n+'shaft_l')
    # Purchased cabinet and real device boxes. Coordinate axes: modelX=depth, Y=width, Z=height.
    for d in ps:
        if d['name'] in ('Schaltschrank_Hohlschale','Schaltschrank_Tuer'):
            d.update(supply_kind='BUY',item_id='K-CAB',purchase_instance='CAB1',note=CAT['K-CAB']['note']+' Außenabmessungen maßhaltig, einzelne Blechstärken/Scharnier vereinfacht.')
        if d['name'].startswith('Mesa_'):
            d.update(supply_kind='BUY',item_id='K-MESA',purchase_instance='MESA1',note=CAT['K-MESA']['note']+' NUR reservierte Hülle, keine genaue Leiterplattenkontur.')
    g='16_Schaltschrank'
    q=part('Schaltschrank_Montageplatte',g,'silver',at=('cab_x+18','cab_y+25','cab_z+25'),item='K-CABPL',instance='CABPL1')
    base.box(q,('cab_x+18','cab_y+25','cab_z+25'),('cat08_cabpl_thickness','cat08_cabpl_width','cat08_cabpl_height'))
    for name,it,yy,zz in [('Treiber_X_CS_D508_Huelle','K-DRV-XY',65,410),('Treiber_Y_CS_D508_Huelle','K-DRV-XY',130,410),('Treiber_Z_CS_D1008E_Huelle','K-DRV-Z',195,390),('Achsenversorgung_RSP50048','K-PS-AX',65,130),('24V_HDR6024','K-PS24',330,160),('5V_HDR155','K-PS5',430,160)]:
        q=part(name,g,'dark' if 'Treiber' in name else 'panel',at=('cab_x+35','cab_y+'+str(yy),'cab_z+'+str(zz)),item=it,instance=name)
        k='cat08_'+it[2:].lower().replace('-','_')+'_'
        base.box(q,q['datum'],(k+'depth',k+'width',k+'height'),label='Kaufteil_Aussenmasse_Anschluesse_vereinfacht')
    # Reference probes in a separate staging group, deliberately not falsely attached to guessed machine coordinates.
    for i in range(6):
        q=part('IFS206_Referenz_'+str(i+1),'18_Prueffeld','silver',at=('enc_left+80+'+str(i*30),'enc_front+120',30),item='K-SENSOR',instance='SENSOR'+str(i+1))
        base.cyl(q,q['datum'],12,45,(0,0,1),label='M12_Huelle_ohne_Gewinde_45mm')
    for i,d in enumerate(ps,1):
        d['id']='B%03d'%i;d['filename']=d['id']+'_'+d['name'];d['manufacturing_released']=False
        if 'supply_kind' not in d:
            original_group=int(d['group'].split('_')[0])<=10 and d['name'] not in ('Pinolenvorschub_Abdeckplatte','Pinole_Deckelschraube_1','Pinole_Deckelschraube_2')
            reserve=any(s in d['name'].lower() for s in ('reserve','bauraum','gasfeder','schrank_din','schrank_kabel','reihenklemme','pe_schiene','bedienpult','pumpen','schraube','scharnier','dichtung'))
            d['supply_kind']='EXISTING' if original_group else ('RESERVE' if reserve else 'MAKE')
            d['item_id']=('A-' if original_group else 'R-' if reserve else 'F-')+d['name']
            d['purchase_instance']=d['name']
    return ps

def check_recipe(p,parts=None):
    validate(p);v=all_values(p);seen=set()
    for d in parts or recipe():
        if d['name'] in seen:raise ValueError('Doppelter Name '+d['name'])
        seen.add(d['name'])
        if d['group'] not in GROUPS or d['material'] not in PALETTE:raise ValueError('Gruppe/Farbe fehlt')
        for o in d['ops']:
            for x in o['origin']:evaluate(x,v)
            for x in o.get('size',[]):
                if evaluate(x,v)<=0:raise ValueError('Nichtpositive Länge '+d['name'])
            for key in ('height','diameter'):
                if key in o and evaluate(o[key],v)<=0:raise ValueError('Nichtpositive Abmessung '+d['name'])
            for pt in o.get('points',[]):
                for x in pt:evaluate(x,v)
    for row in length_report(p):
        if row['minimum_reserve_mm'] < row['required_reserve_mm']-1e-6:
            raise ValueError('Spindelreserve zu klein: '+row['axis'])
    envelope=enclosure_report(p, parts if parts is not None else recipe())
    if envelope['violations']:
        raise ValueError('Einhausung zu klein für Zielhübe: '+envelope['violations'][0]['name'])
    return v

def length_report(p):
    rows=legacy.length_report(p);v=all_values(p)
    for row in rows:
        a=row['axis'].lower();n='cnc_'+a+'_'
        row['note']='Entwurf: nominaler Gewindekern ohne Ausläufe; Lieferzeichnung und Maschinenaufmaß fehlen. Keine Bestelllänge.'
        row['envelope_core_length_mm']=v[n+'core_l']+p[n+'core_end']
        row['total_envelope_length_mm']=v[n+'core_l']+p[n+'fixed_shaft_end']+25
        for pose in row['poses']:pose['right_mm']+=p[n+'core_end']-8
        row['minimum_reserve_mm']=min(min(x['left_mm'],x['right_mm']) for x in row['poses'])
        row['order_length_mm']=None
    return rows
# Approved door/wet-room calculations use unchanged parameters.
door_layout=legacy.door_layout
spring_report=legacy.spring_report
drain_report=legacy.drain_report

def enclosure_report(p,definitions=None):
    import sys
    from enclosure_checks03 import sweep_report
    return sweep_report(sys.modules[__name__],p,recipe() if definitions is None else definitions)
