# -*- coding: utf-8 -*-
"""SX3.5Z concept assembly 07: attachment study, support frame, enclosure, cabinet.
Native NX recipe; all unmeasured interfaces remain explicitly unreleased.
Original reference model is retained in cnc_ansichtsmodell01.py.
"""
import copy, json, math, os
from collections import OrderedDict
import cnc_ansichtsmodell01 as old
base=old.base
VERSION='CNC_ANSICHT_07'
SPECS=copy.deepcopy(old.SPECS);DERIVED=copy.deepcopy(old.DERIVED)
GROUPS=OrderedDict(old.GROUPS)
GROUPS.update([('14_Untergestell','Untergestell – Strukturentwurf'),('15_Einhausung','Einhausung – Schutzkonzept ungeprüft'),('16_Schaltschrank','CNC-Schaltschrank – Layoutentwurf'),('17_KSS','KSS-Wanne und Rücklauf – Entwurf')])
LAYERS={g:(i+1)*10 for i,g in enumerate(GROUPS)}
PALETTE=dict(old.PALETTE,frame=(.17,.21,.25,1),sheet=(.76,.78,.78,1),reserviert=(.88,.42,.09,1))
DEFAULT_COLORS=dict(old.DEFAULT_COLORS,frame=31,sheet=36,reserviert=106)
SOURCE='K02: Originalfotomodell + dokumentierte Herstellerdaten + ausdrücklich ungeprüfte Entwurfsanschlüsse.'
from formeln07 import evaluate
local_definition=old.local_definition
EXTRAS={
 'cnc_x_extra_l':40.,'cnc_z_extra_l':20.,'axial_reserve':10.,
 'stand_h':750.,'stand_w':1650.,'stand_d':1000.,'stand_cx':62.,'stand_cy':25.,
 'tube_side':60.,'tube_wall':3.,'enclosure_h':1200.,'sheet_t':2.,'window_t':8.,
 'cab_w':600.,'cab_h':800.,'cab_d':300.,'cab_gap':0.,'cab_z':150.,
 'tank_w':500.,'tank_d':400.,'tank_h':250.,
 'chip_outlet_w':350.,'chip_outlet_d':60.,'chip_outlet_y':430.,
 'door_open':0.,'door_clear_w':1420.,'door_clear_h':1000.,'door_z':100.,
 'door_overlap':20.,'door_open_clearance':5.,'door_thickness':30.,
 'lift_guide_overrun':40.,'door_panel_overlap':20.,'door_lane_pitch':60.,'door_floor_clearance':250.,'bend_r':3.,'bend_k':0.4
}
for n,v in EXTRAS.items():
 SPECS.append(dict(name=n,value=v,unit='unitless' if n in ('door_open','bend_k') else 'mm',status='ANSICHT_ENTWURF',note='K02 Entwurfsmaß; keine Festigkeits-/Schutzfreigabe',source=SOURCE,limits=None))
NEW_DEFAULTS=dict(old.NEW_DEFAULTS,**EXTRAS)
DERIVED['cnc_x_core_l']='table_x-12+cnc_x_extra_l'
DERIVED['cnc_z_core_l']='lead_z_length+cnc_z_extra_l'
DERIVED.update([('enc_left','stand_cx-stand_w/2'),('enc_right','stand_cx+stand_w/2'),('enc_front','stand_cy-stand_d/2'),('enc_back','stand_cy+stand_d/2'),('cab_x','enc_right+sheet_t+cab_gap'),('cab_y','enc_back-cab_w'),('workheight','stand_h+table_top_z')])
DERIVED.update([
 ('door_leaf_w','door_clear_w+2*door_overlap'),
 ('door_leaf_h','(door_clear_h+2*door_overlap+door_panel_overlap)/2'),
 ('door_travel_lower','door_leaf_h-door_overlap+door_open_clearance'),
 ('door_travel_upper','2*door_travel_lower'),
 ('door_travel','door_travel_upper'),
 ('door_x','stand_cx-door_clear_w/2-door_overlap'),
 ('door_y','enc_front-50'),
 ('door_upper_y','door_y-door_lane_pitch'),
 ('door_closed_bottom','door_z-door_overlap'),
 ('door_closed_top','door_z+door_clear_h+door_overlap'),
 ('door_upper_closed_bottom','door_closed_top-door_leaf_h'),
 ('door_lower_bottom','door_closed_bottom-door_open*door_travel_lower'),
 ('door_lower_top','door_lower_bottom+door_leaf_h'),
 ('door_upper_bottom','door_upper_closed_bottom-door_open*door_travel_upper'),
 ('door_upper_top','door_upper_bottom+door_leaf_h'),
 ('door_open_lowest','door_upper_closed_bottom-door_travel_upper'),
 ('lift_guide_bottom','door_open_lowest-lift_guide_overrun'),
 ('lift_guide_top','door_closed_top+lift_guide_overrun'),
 ('lift_guide_length','lift_guide_top-lift_guide_bottom'),
 ('lift_total_top','lift_guide_top+30'),
 ('door_pocket_bottom','lift_guide_bottom-25'),
 ('door_pocket_top','door_z-door_open_clearance'),
 ('door_pocket_y','door_upper_y-95'),
 ('door_pocket_back','door_y+door_thickness+8'),
 ('door_pocket_depth','door_pocket_back-door_pocket_y'),
 ('door_pocket_height','door_pocket_top-door_pocket_bottom')])
MANUAL_NAMES={'Feinvorschub_Pinole','Pinolenvorschub_Welle_innen','Pinolenvorschub_Ritzel'}
REMOVED_NAMES=set(old.REMOVED_NAMES)|MANUAL_NAMES
REMOVED_PREFIX=('Sternhebel_','Kupplung_Kurzhebel_')


def load_parameters(path=None):
 p=OrderedDict(base.load_parameters(path));p.update(NEW_DEFAULTS)
 if path:
  for fn in ('CNC_Parameter.json','Ausbau_Parameter.json'):
   name=os.path.join(os.path.dirname(os.path.abspath(path)),fn)
   if os.path.isfile(name):
    with open(name,encoding='utf-8-sig') as f:q=json.load(f)
    if not isinstance(q,dict):raise ValueError('Parameterobjekt erwartet: '+fn)
    for k,v in q.items():
     if k.startswith('_'):continue
     if k not in NEW_DEFAULTS:raise ValueError('Unbekannter Parameter: '+k)
     if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError('Ungültiger Parameter: '+k)
     p[k]=float(v)
 validate(p);return p


def validate(p):
 old.validate(p)
 for n in EXTRAS:
  if not math.isfinite(p[n]) or (n not in ('stand_cx','stand_cy','door_open','cab_gap') and p[n]<=0):raise ValueError('Ungültiger Ausbauparameter '+n)
 if p['cab_gap']<0:raise ValueError('cab_gap darf nicht negativ sein')
 if p['tube_side']<=2*p['tube_wall']:raise ValueError('Rohr ohne Wand/Innenraum')
 if p['stand_h']<450 or p['stand_w']<1600 or p['stand_d']<950 or p['enclosure_h']<1180:raise ValueError('Ansichtshülle zu klein für die Standardmaschine')
 if isinstance(p['door_open'],bool) or not 0<=p['door_open']<=1:raise ValueError('door_open muss zwischen 0 und 1 liegen')
 if p['door_thickness']!=30:raise ValueError('Fuer dieses Hubtuer-Fuehrungskonzept ist door_thickness=30 erforderlich')
 if not 15<=p['door_overlap']<=30:raise ValueError('Tuerueberdeckung ausserhalb Entwurfsbereich')
 if not 25<=p['lift_guide_overrun']<=55:raise ValueError('Fuehrungsueberlauf muss zwischen 25 und 55 mm liegen')
 if p['door_clear_w']/2+p['door_overlap']+80>p['stand_w']/2-10:raise ValueError('Hubtuer und Fuehrung passen nicht in die Gehaeusebreite')
 if p['door_z']-p['door_overlap']<60 or p['door_z']+p['door_clear_h']+p['door_overlap']>p['enclosure_h']-40:raise ValueError('Geschlossene Hubtuer passt nicht in die Einhausung')
 if p['door_clear_w']<500 or p['door_clear_h']<500:raise ValueError('Tuer fuer diesen Entwurf zu klein')
 if not p['door_overlap']<=p['door_panel_overlap']<=50:raise ValueError('Segmentueberdeckung muss mindestens der Randueberdeckung entsprechen und <=50 mm sein')
 if p['door_lane_pitch']<p['door_thickness']+p['window_t']+12:raise ValueError('Tiefenebenen bieten zu wenig Abstand fuer Scheibe und Rahmen')
 if p['door_floor_clearance']<100:raise ValueError('Bodenreserve im Ansichtsentwurf muss >=100 mm sein')
 v=all_values(p)
 if p['stand_h']+v['door_open_lowest']<p['door_floor_clearance']:raise ValueError('Nach unten fahrende Tuer unterschreitet die Bodenreserve')
 if p['stand_h']+v['door_pocket_bottom']<100:raise ValueError('Tuerkassette zu nahe am Boden')
 if v['lift_total_top']>p['enclosure_h']:raise ValueError('Fuehrungstraeger ragen ueber das Dach')
 if p['cab_w']<600 or p['cab_h']<800 or p['cab_d']<300:raise ValueError('Schrank kleiner als Layoutreferenz')
 if not 0.2<=p['bend_k']<=0.5 or not 1<=p['bend_r']<=5:raise ValueError('Biegewerte ausserhalb Studienbereich')
 if not 1<=p['sheet_t']<=3:raise ValueError('Kantblechdicke muss 1..3 mm sein')
 if p['sheet_t']>8 or p['window_t']>25:raise ValueError('Unplausible Wanddicke')
 import ruecklauf07
 ruecklauf07.validate(p,v)
 return True


def all_values(p):
 v=OrderedDict(p)
 for k,e in DERIVED.items():v[k]=evaluate(e,v)
 return v


def door_layout(p):
 v=all_values(p);leaves=[]
 for k,yy,zz,travel in [('LOWER','door_y','door_lower_bottom','door_travel_lower'),('UPPER','door_upper_y','door_upper_bottom','door_travel_upper')]:
  leaves.append(dict(leaf=k,xmin=v['door_x'],xmax=v['door_x']+v['door_leaf_w'],
    ymin=v[yy],ymax=v[yy]+p['door_thickness'],zmin=v[zz],zmax=v[zz]+v['door_leaf_h'],
    travel_mm=v[travel],motion_vector=[0,0,-1],bottom_from_floor_mm=p['stand_h']+v[zz]))
 return dict(door_open=p['door_open'],direction=[0,0,-1],type='TWO_PANEL_DOWNWARD_TELESCOPIC_STUDY',
  clear_width_mm=p['door_clear_w'],clear_height_mm=p['door_clear_h'],
  opening_xmin=p['stand_cx']-p['door_clear_w']/2,opening_xmax=p['stand_cx']+p['door_clear_w']/2,
  opening_zmin=p['door_z'],opening_zmax=p['door_z']+p['door_clear_h'],
  travels_mm={'LOWER':v['door_travel_lower'],'UPPER':v['door_travel_upper']},leaves=leaves,
  closed_leaf_top_from_floor_mm=p['stand_h']+v['door_closed_top'],
  open_leaf_top_from_floor_mm=p['stand_h']+max(v['door_closed_bottom']+v['door_leaf_h']-v['door_travel_lower'],v['door_closed_top']-v['door_travel_upper']),
  minimum_open_bottom_from_floor_mm=p['stand_h']+v['door_open_lowest'],
  pocket_bottom_from_floor_mm=p['stand_h']+v['door_pocket_bottom'],
  fixed_total_height_mm=p['stand_h']+max(p['enclosure_h']+p['sheet_t'],v['lift_total_top']),
  note='Zwei Segmente fahren nach UNTEN mit modelliertem Hubverhaeltnis 2:1 in eine Kassette VOR dem Gestell. Reine Sollkinematik; Kopplung, Gewichtsausgleich, Haltesicherung, Dichtungen und Verriegelung sind nicht ausgelegt. Kein Fertigungsdatensatz.')


def enclosure_report(p,definitions=None):
 import sys
 from enclosure_checks03 import sweep_report
 return sweep_report(sys.modules[__name__],p,recipe() if definitions is None else definitions)


def used_parameters(d):
 # Same dependency scanner with the combined parameter namespace.
 known={s['name'] for s in SPECS}|set(DERIVED);found=set()
 import re
 def scan(x):
  if isinstance(x,str):found.update(set(re.findall(r'\b[A-Za-z_]\w*\b',x))&known)
  elif isinstance(x,(list,tuple)):
   for y in x:scan(y)
  elif isinstance(x,dict):
   for k,y in x.items():
    if k not in ('name','label','source','note'):scan(y)
 scan(d['ops']);scan(d['datum'])
 while True:
  before=set(found)
  for k in list(found):
   if k in DERIVED:scan(DERIVED[k])
  if found==before:return found


def length_report(p):
 """Swept axial containment for body/nut envelope ONLY, no guide/bearing collision proof."""
 rows=[]
 for a in 'xyz':
  extremes=[-p['travel_x']/2,p['travel_x']/2] if a=='x' else ([-p['travel_y']/2,p['travel_y']/2] if a=='y' else [0,p['z_travel_used']])
  margins=[]
  for q in extremes:
   pp=dict(p);pp[{'x':'pos_x','y':'pos_y','z':'head_down'}[a]]=q;v=all_values(pp);n='cnc_'+a+'_'
   if a=='x':nut_local=v['cnc_x_nut_x']-(v['pos_x']+v['table_x']/2)
   elif a=='y':nut_local=-(v['pos_y']-v['base_front_y'])
   else:nut_local=v['z_nut_center']-(v['column_top_z']+v['column_cap_h'])
   half=max(v[n+'nut_l'],v[n+'nut_block_l'])/2
   margins.append({'pose_mm':q,'left_mm':nut_local-half+v[n+'core_l'],'right_mm':8-(nut_local+half)})
  v=all_values(p);l=v['cnc_'+a+'_core_l']
  rows.append(dict(axis=a.upper(),nominal_diameter_mm=p['cnc_'+a+'_screw_d'],lead_mm=p['cnc_'+a+'_lead'],envelope_core_length_mm=l+8,total_envelope_length_mm=l+73,required_reserve_mm=p['axial_reserve'],minimum_reserve_mm=min(min(x['left_mm'],x['right_mm']) for x in margins),poses=margins,status='AXIAL_ENVELOPE_ONLY_NOT_ORDER_LENGTH'))
 return rows


def recipe():
 ps=[copy.deepcopy(d) for d in old.recipe() if d['name'] not in MANUAL_NAMES and not d['name'].startswith(REMOVED_PREFIX)]
 by={d['name']:d for d in ps}
 def part(name,g,mat='steel',at=(0,0,0),note='Entwurf. Anschlusslochbild, Belastung und Einbau vor Fertigung prüfen.',source=SOURCE):
  d=dict(name=name,group=g,material=mat,datum=list(map(str,at)),ops=[],status='ANSICHT_ENTWURF',source=source,note=note,manufacturing_released=False);ps.append(d);return d
 def box(name,g,o,sz,mat='steel',note=None):
  d=part(name,g,mat,o,**({'note':note} if note else {}));base.box(d,o,sz);return d
 def cyl(name,g,o,d,h,axis=(0,0,1),mat='steel',note=None):
  p=part(name,g,mat,o,**({'note':note} if note else {}));base.cyl(p,o,d,h,axis);return p
 def ring(name,g,o,od,id,h,axis=(0,0,1),mat='steel',note=None):
  p=cyl(name,g,o,od,h,axis,mat,note)
  start=[base.add(o[i],-axis[i]) for i in range(3)]
  base.cyl(p,start,id,base.add(h,2),axis,'cut','Durchgang');return p
 def bolt(name,g,fr,u,v,w,diam,length,head=None):
  p=part(name,g,'dark',fr.point((u,v,w)),note='Schraube vereinfacht, Gewinde nicht helikal; Nenndurchmesser überlappt Kernloch. Guss-Gegenloch unbestätigt.')
  fr.cyl(p,(u,v,w),diam,length);fr.cyl(p,(u,v,base.add(w,length)),head or diam*1.6,diam*.8);return p
 # Close the removed manual-feed shaft opening. Original pinole remains and must be clamped.
 p=part('Pinolenvorschub_Abdeckplatte','05_Spindelkopf','machine_red',('head_x/2','star_y','star_z'),note='Dreistern und Feinvorschub entfernt. Deckel auf originalem Bedienwellenanschluss. Pinole nur geklemmt nutzbar; Klemmkraft nicht nachgewiesen.')
 base.cyl(p,('head_x/2','star_y','star_z'),62,4,(1,0,0))
 for i,(yy,zz) in enumerate([(0,24),(0,-24)],1):
  base.cyl(p,('head_x/2-1',f'star_y+{yy}',f'star_z+{zz}'),5.5,6,(1,0,0),'cut','Deckelschrauben_Entwurf')
  fr=old.Frame(('head_x/2','star_y','star_z'),((0,1,0),(0,0,1),(1,0,0)))
  bolt('Pinole_Deckelschraube_'+str(i),'05_Spindelkopf',fr,yy,zz,-6,5,10)
 # Fully visible motor/plate/rod and fixed-bearing attachment chain.
 for a,g in zip('xyz',('11_CNC_X','12_CNC_Y','13_CNC_Z')):
  A=a.upper();n='cnc_'+a+'_';prefix='CNC_'+A+'_'
  if a=='x':o=('pos_x+table_x/2','pos_y','x_wheel_z');cols=((0,1,0),(0,0,1),(1,0,0))
  elif a=='y':o=(0,'base_front_y','y_wheel_z');cols=((1,0,0),(0,0,1),(0,-1,0))
  else:o=(0,'column_screw_y','column_top_z+column_cap_h');cols=((1,0,0),(0,1,0),(0,0,1))
  f=old.Frame(o,cols)
  ap=by[prefix+'Anschlussplatte_Entwurf']
  for op in ap['ops']:
   if op.get('label')=='Entwurfsloch_KEIN_MASCHINENLOCHBILD':op['diameter']='5';op['label']='M6_Kernloch_Entwurf_Distanzsaeulen'
  # Manufacturer drawing shows 4x diameter5 through holes for X/Y, NOT threads.
  # Proposed M4 fastening into tapped adapter plate; Z M5 remains an assumption.
  mp=by[prefix+'Motorplatte_Entwurf']
  for op in mp['ops']:
   if op.get('label')=='Motorplatte_Lochbild' and any(n+'motor_pitch' in str(x) for x in op['origin']):
    op['diameter']='3.3' if a!='z' else '4.2';op['label']='Motorplatte_Gewindekern_Entwurf'
  for i,(u,v) in enumerate([(u,v) for u in (-1,1) for v in (-1,1)],1):
   md=4 if a!='z' else 5
   uu=f'{u}*{n}motor_pitch/2';vv=f'{v}*{n}motor_pitch/2';ww=n+'motor_front-7'
   r=part(prefix+'Motorbefestigung_'+str(i),g,'dark',f.point((uu,vv,ww)),note='Durchgangs-Flanschverschraubung in Gewinde der Halterplatte. X/Y M4 als Entwurf durch Katalogloch Ø5; Z M5 unbestätigt. Kein Gewinde in den Kaufmotor erfunden.')
   f.cyl(r,(uu,vv,ww),md,12,label='Motorbefestigung_Schaft')
   f.cyl(r,(uu,vv,n+'motor_front+5'),md*1.8,md*.8,label='Motorbefestigung_Kopf_hinter_Flansch')
   # Purchased motor body is only a coarse envelope: represent access, NOT a machining instruction.
   f.cyl(by[prefix+'Motor_Gehaeuse'],(uu,vv,n+'motor_front+4.9'),md*1.8+2,md*.8+2,'cut','Kopfzugang_nur_Huellendarstellung')
  by[prefix+'Motor_Gehaeuse']['note']+=' K02: Schraubenkopf-Zugänge nur schematisch ausgespart; reale Außenform/Werkzeugzugang prüfen, NICHT am Kaufmotor nacharbeiten.'
  # Two bearing-ring envelopes and axial location: rear shoulder + front retaining lip.
  fixed=by[prefix+'Festlager_Entwurf'];fixed['ops']=[]
  f.box(fixed,(-30,-26,10),(60,52,24))
  f.cyl(fixed,(0,0,9),n+'journal_d+8',26,'cut','Zapfenfreiraum')
  f.cyl(fixed,(0,0,12),n+'bearing_bore',23,'cut','Lagersitz_mit_Schulter')
  bw=9 if a=='z' else 8;end=12+2*bw
  br=by[prefix+'Festlager_Ringhuelle'];br['ops']=[]
  f.cyl(br,(0,0,12),n+'bearing_bore',bw);f.cyl(br,(0,0,11),n+'journal_d',bw+2,'cut')
  br['note']='Nominale Lagerring-Hülle. Kontaktwinkel, Paarung, Vorspannung und Tragzahl offen; kein Kaufteilmodell.'
  r=part(prefix+'Festlager_Ringhuelle_2',g,'silver',f.point((0,0,12+bw)),note=br['note']);f.cyl(r,(0,0,12+bw),n+'bearing_bore',bw);f.cyl(r,(0,0,11+bw),n+'journal_d',bw+2,'cut')
  r=part(prefix+'Festlager_Deckel',g,'design_blue',f.point((0,0,34)))
  f.box(r,(-30,-26,34),(60,52,3));f.cyl(r,(0,0,end),n+'bearing_bore',34-end)
  f.cyl(r,(0,0,end-1),n+'journal_d+10',38-end,'cut','Freiraum_Sicherungsmutter')
  cap=r
  for i,(u,v) in enumerate([(u,v) for u in (-22,22) for v in (-17,17)],1):
   f.cyl(fixed,(u,v,9),5.5,26,'cut','Lagergehaeuse_Durchgang_M5')
   f.cyl(cap,(u,v,33),5.5,5,'cut','Deckelloch_M5')
   f.cyl(ap,(u,v,-1),4.2,12,'cut','M5_Kernloch_Lagerbefestigung')
   bolt(prefix+'Festlager_Befestigung_'+str(i),g,f,u,v,4,5,33)
  r=part(prefix+'Festlager_Sicherungsmutter',g,'dark',f.point((0,0,end)),note='Axiale Sicherungsmutter als Hülle. Endzapfengewinde und Vorspannung sind noch festzulegen.')
  f.cyl(r,(0,0,end),n+'journal_d+8',5);f.cyl(r,(0,0,end-1),n+'journal_d',7,'cut')
  r=part(prefix+'Festlager_Schulterring',g,'steel',f.point((0,0,8)))
  f.cyl(r,(0,0,8),n+'journal_d+6',4);f.cyl(r,(0,0,7),n+'journal_d',6,'cut')
  # Explicit attachment points to machine-side plate. Do not cut undocumented holes into castings.
  for i,(u,v) in enumerate([(u,v) for u in (-36,36) for v in (8,24)],1):
   f.cyl(ap,(u,v,-1),6.6,12,'cut','Gussanschluss_UNBESTAETIGT_M6')
   bolt(prefix+'Maschinenanschluss_'+str(i),g,f,u,v,-12,6,22)
  # Free support gets its own bridge and four fasteners. Geometry is a study, not a standard BF block.
  r=part(prefix+'Loslager_Anschlussbruecke',g,'design_blue',f.point((0,0,'-'+n+'core_l-28')),note='Brücke zum Maschinenende; X überbrückt Verlängerung der Spindel. Gegenbohrungen/Flächen real nachmessen.')
  f.box(r,(-34,-28,'-'+n+'core_l-28'),(68,56,8));f.cyl(r,(0,0,'-'+n+'core_l-29'),n+'free_journal_d+4',10,'cut')
  free=by[prefix+'Loslager_Entwurf']
  for i,(u,v) in enumerate([(u,v) for u in (-18,18) for v in (-15,15)],1):
   f.cyl(free,(u,v,'-'+n+'core_l-21'),4.5,22,'cut','Loslager_Durchgang')
   f.cyl(r,(u,v,'-'+n+'core_l-29'),3.3,10,'cut','M4_Kernloch_Entwurf')
   bolt(prefix+'Loslager_Befestigung_'+str(i),g,f,u,v,'-'+n+'core_l-26',4,26)
  # Protective sleeve leaves only motor rear and cable outlet exposed. No seal claim.
  r=part(prefix+'Motorschutz_Haube',g,'sheet',f.point((0,0,n+'motor_front-12')),note='Spritzschutz-Hülle mit unterseitigem Ablauf; keine bestätigte IP-Schutzart, keine thermische Freigabe.')
  f.box(r,('-'+n+'motor_w/2-8','-'+n+'motor_w/2-8',n+'motor_front-12'),(n+'motor_w+16',n+'motor_w+16',n+'motor_l+25'))
  f.box(r,('-'+n+'motor_w/2-6','-'+n+'motor_w/2-6',n+'motor_front-13'),(n+'motor_w+12',n+'motor_w+12',n+'motor_l+27'),'cut','Offene_Spritzhuelle')
  # Gusset linking extended free-bearing plate to left table face for X.
  if a=='x':
   r=part(prefix+'Loslager_Brueckenwinkel',g,'design_blue',('-table_x/2+pos_x-70','pos_y-35','x_wheel_z-40'))
   base.box(r,('pos_x-table_x/2-70','pos_y-35','x_wheel_z-40'),(80,70,10))
   base.box(r,('pos_x-table_x/2-4','pos_y-35','x_wheel_z-40'),(14,70,65))
 # Z load path: new bridge bears on CAST COLUMN, not on thin sheet cover.
 r=box('CNC_Z_Tragbruecke_auf_Gusssaeule','13_CNC_Z',('-column_x/2','column_front_y','column_top_z'),('column_x','column_y','column_cap_h'),'design_blue',note='Lastbrücke auf Säulenguss. Schraublochlage/Restwand des Gusses unbestätigt; nicht nur an Blechdeckel befestigen.')
 base.cyl(r,(0,'column_screw_y','column_top_z-1'),'cnc_z_screw_d+8','column_cap_h+2',(0,0,1),'cut','Spindeldurchgang')
 for i,(sx,sy) in enumerate([(x,y) for x in (-1,1) for y in (-1,1)],1):
  x=f'{sx}*(column_x/2-15)';y=f'column_screw_y+{sy}*25'
  base.cyl(r,(x,y,'column_top_z-1'),8.5,'column_cap_h+2',(0,0,1),'cut','M8_Gussanschluss_ANNAHME')
  fr=old.Frame((0,0,0),((1,0,0),(0,1,0),(0,0,1)))
  bolt('CNC_Z_Tragbruecke_Schraube_'+str(i),'13_CNC_Z',fr,x,y,'column_top_z-18',8,'column_cap_h+18')
 # Through-clearance in detachable covers only, never hidden machining of machine castings.
 for name in ('Saeulendeckel','Blechsaeule_Stirnblech_oben'):
  d=by[name]
  if name=='Saeulendeckel':
   # Existing spindle bore may already be larger; leave unchanged rather than add a no-op cut.
   d['note']+=' K02: Lastbrücke liegt auf Gusssäule; Deckel muss real angepasst werden.'
 # Stand: closed square tubes; local section follows global dimensions.
 g='14_Untergestell'
 def tube(name,o,length,axis):
  size=['tube_side']*3;size[axis]=length;p=box(name,g,o,size,'frame')
  inner=[base.add(o[i],'tube_wall') for i in range(3)];isz=['tube_side-2*tube_wall']*3
  inner[axis]=base.add(o[axis],-1);isz[axis]=base.add(length,2)
  base.box(p,inner,isz,'cut','Rohrinnenraum');return p
 for ix,x in enumerate(['enc_left','enc_right-tube_side']):
  for iy,y in enumerate(['enc_front','enc_back-tube_side']):
   tube('Staender_Bein_%s_%s'%(ix,iy),(x,y,'-stand_h+35'),'stand_h-115',2)
   p=cyl('Staender_Fuss_%s_%s'%(ix,iy),g,(base.add(x,'tube_side/2'),base.add(y,'tube_side/2'),'-stand_h'),100,20,mat='dark')
   base.cyl(p,(base.add(x,'tube_side/2'),base.add(y,'tube_side/2'),'-stand_h+20'),24,25)
 for j,z in enumerate(['-80','-stand_h+170']):
  for i,y in enumerate(['enc_front','enc_back-tube_side']):tube('Staender_Querholm_%s_%s'%(j,i),('enc_left',y,z),'stand_w',0)
  for i,x in enumerate(['enc_left','enc_right-tube_side']):tube('Staender_Laengsholm_%s_%s'%(j,i),(x,'enc_front+tube_side',z),'stand_d-2*tube_side',1)
 for i,x in enumerate([-140,80]):tube('Staender_Maschinentraverse_'+str(i),(x,'-230','-80'),600,1)
 p=box('Maschinen_Aufspannplatte',g,(-225,-220,-20),(450,600,20),'steel',note='20-mm-Tragplatte, zwei Quertraversen; Statik, Ebenheit, Schweißfolge und Bodenanker nicht nachgewiesen.')
 for x in (-1,1):
  for y in (-1,1):base.cyl(p,(f'{x}*bolt_pitch_short/2',f'base_center_y+{y}*bolt_pitch_long/2',-21),'mount_hole_d',22,(0,0,1),'cut','Maschinenfussloch_aus_Bestandsmodell')
 # Cabinet load carried by an additional framework, not by enclosure sheet.
 for i,y in enumerate(['cab_y+35','cab_y+cab_w-95']):
  tube('Schrank_Traegerausleger_'+str(i),('enc_right-tube_side',y,'-80'),'sheet_t+cab_gap+cab_d+tube_side',0)
  tube('Schrank_Stuetzbein_'+str(i),('cab_x+cab_d-tube_side',y,'-stand_h+35'),'stand_h+cab_z-35',2)
 # Separate folded wall panels, all with two parallel returns and open ends.
 from blech06 import u_profile
 def folded(name,g,o,w,depth,length,mat='sheet',axes=((1,0,0),(0,1,0),(0,0,1))):
  return u_profile(part(name,g,mat,o),o,w,depth,length,axes)
 g='15_Einhausung'
 for side,x,sign in [('links','enc_left-sheet_t',1),('rechts','enc_right+sheet_t',-1)]:
  p=folded('Einhausung_Seitenwand_'+side,g,(x,'enc_front-sheet_t',0),'stand_d+2*sheet_t',25,'enclosure_h',axes=((0,1,0),(sign,0,0),(0,0,1)))
  if side=='links':
   base.box(p,('enc_left-sheet_t-1','enc_front+160',300),('sheet_t+2','stand_d-320','enclosure_h-500'),'cut','Fensterausschnitt')
   box('Einhausung_Seitenscheibe_links',g,('enc_left+sheet_t','enc_front+145',285),('window_t','stand_d-290','enclosure_h-470'),'glass',note='8 mm nur Studienwert; keine Schutzfreigabe.')
  else:
   p['note']+=' K07: Fenster entfernt; geschlossene Trennwand zum direkt anliegenden Schaltschrank. Keine offene Verbindung zum Nassraum.'
 folded('Einhausung_Rueckwand',g,('enc_left+sheet_t','enc_back',0),'stand_w-2*sheet_t',25,'enclosure_h',axes=((1,0,0),(0,-1,0),(0,0,1)))
 folded('Einhausung_Dach',g,('enc_left-2*sheet_t','enc_front-sheet_t','enclosure_h+sheet_t'),'stand_w+4*sheet_t',25,'stand_d+2*sheet_t',axes=((1,0,0),(0,0,-1),(0,1,0)))
 for i,x in enumerate(['enc_left+sheet_t','enc_right-sheet_t-30']):box('Einhausung_Tuerpfosten_'+str(i),g,(x,'enc_front',0),(30,30,'enclosure_h'),'frame')
 for i,z in enumerate([0,'enclosure_h-30']):box('Einhausung_Tuerriegel_'+str(i),g,('enc_left','enc_front',z),('stand_w',30,30),'frame')
 # Wide opaque side jambs replace the former narrow service aperture.
 for side,x in [('links','enc_left'),('rechts','stand_cx+door_clear_w/2')]:
  folded('Einhausung_Festfeld_'+side,g,(x,'enc_front-sheet_t',0),'(stand_w-door_clear_w)/2',12,'enclosure_h',axes=((1,0,0),(0,-1,0),(0,0,1)))
 box('Einhausung_Frontschwelle',g,('stand_cx-door_clear_w/2','enc_front-sheet_t',0),('door_clear_w','sheet_t','door_z'),'sheet')
 box('Einhausung_Frontsturz',g,('stand_cx-door_clear_w/2','enc_front-sheet_t','door_z+door_clear_h'),('door_clear_w','sheet_t','enclosure_h-door_z-door_clear_h'),'sheet')
 # Downward telescopic door. Each segment has its own depth lane and -Z travel.
 def moving(d,leaf):
  d['door_leaf']=leaf;d['door_motion_vector']=[0,0,-1]
  d['door_shift_z']='-door_travel_'+leaf.lower()
  d['source']='K06: vom Nutzer verlangte Oeffnung nach unten. Zweiteilung erhaelt Oeffnung und Bodenfreiheit; Anschauungsentwurf.'
  return d
 for leaf,yy,bot,top in [('LOWER','door_y','door_lower_bottom','door_lower_top'),('UPPER','door_upper_y','door_upper_bottom','door_upper_top')]:
  prefix='Senktuer_'+leaf
  p=moving(folded(prefix+'_Rahmen',g,('door_x',yy,bot),'door_leaf_w','door_thickness','door_leaf_h'),leaf)
  base.box(p,('door_x+42',base.add(yy,-1),base.add(bot,55)),('door_leaf_w-84','door_thickness+2','door_leaf_h-110'),'cut','Sichtausschnitt')
  moving(box(prefix+'_Scheibe',g,('door_x+32',base.add(yy,'-window_t-1'),base.add(bot,45)),('door_leaf_w-64','window_t','door_leaf_h-90'),'glass',note='Nominelle Sichtscheibe. Halter, Material, Schutzwirkung und Dichtungen offen.'),leaf)
  for j,zz in enumerate([bot,base.add(top,-45)]):
   moving(folded(prefix+'_Kantquerholm_'+str(j),g,('door_x+sheet_t+0.5',base.add(yy,'sheet_t'),zz),45,'door_thickness-sheet_t','door_leaf_w-2*sheet_t-1',axes=((0,0,1),(0,1,0),(1,0,0))),leaf)
  r=moving(box(prefix+'_Fensterklemmrahmen',g,('door_x+10',base.add(yy,'-window_t-3'),base.add(bot,20)),('door_leaf_w-20',2,'door_leaf_h-40'),'frame'),leaf)
  base.box(r,('door_x+42',base.add(yy,'-window_t-4'),base.add(bot,55)),('door_leaf_w-84',4,'door_leaf_h-110'),'cut','Sichtausschnitt_Klemmrahmen')
  frame=p
  for i,(xx,zz) in enumerate([(x,z) for x in ['door_x+22','door_x+door_leaf_w-22'] for z in [base.add(bot,30),base.add(top,-30)]]):
   for target in (r,frame):base.cyl(target,(xx,base.add(yy,'-window_t-4'),zz),4.5,'window_t+sheet_t+8',(0,1,0),'cut','M4_Klemmrahmenloch')
   boltpart=moving(cyl(prefix+'_Fensterschraube_'+str(i),g,(xx,base.add(yy,'-window_t-3'),zz),4,'window_t+sheet_t+5',(0,1,0),'steel'),leaf)
   base.cyl(boltpart,(xx,base.add(yy,'-window_t-6'),zz),7,3,(0,1,0))
  if leaf=='UPPER':
   p=moving(box(prefix+'_Griff',g,('stand_cx-130',base.add(yy,-35),base.add(top,-60)),(260,20,20),'dark'),leaf)
   for xx in ['stand_cx-130','stand_cx+110']:
    base.box(p,(xx,base.add(yy,-16),base.add(top,-60)),(20,17,20),'add','Griffbefestigung_Entwurf')
  for side,rx in [('L','door_x-50'),('R','door_x+door_leaf_w+10')]:
   p=box('Senktuer_Fuehrung_'+leaf+'_'+side,g,(rx,base.add(yy,-2),'lift_guide_bottom'),(40,34,'lift_guide_length'),'steel',note='C-Fuehrung als separate Huelle, kein ausgewaehltes Kaufteil. Fixe Fuehrung vor dem Gestell, unter Dachniveau.')
   base.box(p,(base.add(rx,5),base.add(yy,3),'lift_guide_bottom-1'),(30,24,'lift_guide_length+2'),'cut','Fuehrungskanal')
   slotx=base.add(rx,34) if side=='L' else base.add(rx,-1)
   base.box(p,(slotx,base.add(yy,10),'lift_guide_bottom-1'),(7,10,'lift_guide_length+2'),'cut','Mitnehmerschlitz')
   for j,cz in enumerate([base.add(bot,95),base.add(top,-95)]):
    moving(box('Senktuer_Schlitten_'+leaf+'_'+side+'_'+str(j),g,(base.add(rx,7),base.add(yy,5),base.add(cz,-30)),(26,20,60),'dark',note='Gleitschlitten-Huelle; Reibung, Ausrichtung und Kraefte nicht bemessen.'),leaf)
    bx=base.add(rx,18) if side=='L' else 'door_x+door_leaf_w-5'
    moving(box('Senktuer_Mitnehmer_'+leaf+'_'+side+'_'+str(j),g,(bx,base.add(yy,11),base.add(cz,-5)),(37,8,10),'steel'),leaf)
  moving(box(prefix+'_Schaltfahne',g,('door_x+40',base.add(yy,-4),base.add(top,-30)),(12,3,20),'steel'),leaf)
  closed_top='door_closed_top' if leaf=='UPPER' else 'door_closed_bottom+door_leaf_h'
  box('Tuerueberwachung_'+leaf+'_Bauraum',g,('door_x+40','door_y+45',base.add(closed_top,-30)),(30,20,35),'reserviert',note='Eigener Bauraum fuer Geschlossenueberwachung/Zuhaltung je Segment. Keine wirksame Sicherheitsfunktion modelliert.')
 # Common left/right towers connect the depth-separated tracks to the stand beams.
 for side,tx in [('L','door_x-80'),('R','door_x+door_leaf_w+50')]:
  p=box('Senktuer_Traeger_'+side,g,(tx,'door_upper_y-2','-stand_h+170'),(30,'door_lane_pitch+45','lift_guide_top+stand_h-170'),'frame',note='Hohltraeger als unbemessener Strukturentwurf. Anschluss an Gestellholme, nicht an KSS-Wanne.')
  base.box(p,(base.add(tx,3),'door_upper_y+1','-stand_h+169'),(24,'door_lane_pitch+39','lift_guide_top+stand_h-168'),'cut','Hohlprofil')
  for j,zz in enumerate(['-stand_h+170','-80']):
   box('Senktuer_Anschlusskonsole_'+side+'_'+str(j),g,(tx,'door_y+43',zz),(30,'enc_front-door_y-33',20),'frame',note='Geometrischer Anschlusssteg zum vorderen Gestellholm. Schrauben/Schweissnaht und Tragfaehigkeit nicht festgelegt.')
  box('Senktuer_Fangsicherung_'+side+'_Bauraum',g,(tx,'door_upper_y-30',600),(25,25,70),'reserviert',note='Reservierter Raum fuer Halte-/Fangsicherung. Kein ausgewähltes oder wirksames Geraet; Bewegung darf real nicht frei fallen.')
 box('Senktuer_Obertraverse',g,('door_x-80','door_upper_y-2','lift_guide_top'),('door_leaf_w+160','door_lane_pitch+35',30),'frame',note='Festes Querprofil unter dem Einhausungsdach. Keine nach oben ausgefahrene Tuer.')
 # Guarded parking envelope IN FRONT of the stand, not through the coolant tank.
 box('Senktuer_Kassette_Front',g,('door_x-80','door_pocket_y','door_pocket_bottom'),('door_leaf_w+160','sheet_t','door_pocket_height'),'frame',note='Separate 2-mm-Servicefront vor den gekanteten Federkanaelen; keine Abwicklung erforderlich, Dichtung noch offen.')
 for side,xx in [('L','door_x-80'),('R','door_x+door_leaf_w+80-sheet_t')]:
  box('Senktuer_Kassette_Seite_'+side,g,(xx,'door_pocket_y+25','door_pocket_bottom'),('sheet_t','door_pocket_depth-25','door_pocket_height'),'frame')
 p=box('Senktuer_Kassette_Boden',g,('door_x-80+sheet_t','door_pocket_y+sheet_t','door_pocket_bottom'),('door_leaf_w+160-2*sheet_t','door_pocket_depth-sheet_t','sheet_t'),'frame',note='Kassettenboden mit Pfostenfreistellungen; Ablauf, Abstreifer und KSS-Rueckfuehrung offen.')
 for tx in ['door_x-80','door_x+door_leaf_w+50']:
  base.box(p,(base.add(tx,-2),'door_upper_y-4','door_pocket_bottom-1'),(34,'door_lane_pitch+49','sheet_t+2'),'cut','Pfostenfreistellung')
 # Separated side spring wells pass below the door cassette; guarded penetrations.
 for sign in (-1,1):
  for offset in (18,55):
   base.cyl(p,(f'stand_cx+{sign}*(door_leaf_w/2+{offset})','door_upper_y-45','door_pocket_bottom-1'),34,'sheet_t+2',(0,0,1),'cut','Federdurchfuehrung_D34_Schutzkanal')
 for xx in ['door_x-91','door_x+door_leaf_w-11']:
  base.box(p,(xx,'door_upper_y-76','door_pocket_bottom-1'),(102,38,'sheet_t+2'),'cut','Federkanal_Durchfuehrung_Servicefreistellung')
 # Rear protection between the towers; no cut across its entire height.
 box('Senktuer_Kassette_Rueckwand',g,('stand_cx-door_clear_w/2+2','door_pocket_back','door_pocket_bottom'),('door_clear_w-4','sheet_t','door_pocket_height'),'frame')
 # Four telescopic push-spring envelope studies. Cases move at upper ends,
 # rods point down. These exert upward support, NOT an opening drive.
 # No catalogue force/part number is inferred from the generated images.
 for side in (-1,1):
  for stage in (1,2):
   x=f'stand_cx+{side}*(door_leaf_w/2+{55 if stage==1 else 18})'
   y='door_upper_y-45'
   anchor='door_lower_bottom+490' if stage==1 else 'door_upper_bottom+490'
   rod_start='-stand_h+110' if stage==1 else 'door_lower_bottom-170'
   rodlen='door_closed_bottom+490-600+stand_h-110+25' if stage==1 else 'door_upper_closed_bottom+490-600-door_closed_bottom+170+25'
   label=f'Gasfeder06_S{stage}_{side}'
   note='KEIN KAUFTEIL: Gasdruckfeder-Einbaustudie; Zylinder 600 / D28, Stange D10. Gegenkraft nach oben. Kraft, Hubreserve, Endanschluesse, Synchronisierung und Fangsicherung nicht freigegeben.'
   case=ring(label+'_Zylinder_BAURAUM',g,(x,y,base.add(anchor,-600)),28,12,600,mat='reserviert',note=note)
   moving(case,'LOWER' if stage==1 else 'UPPER')
   rod=cyl(label+'_Kolbenstange_BAURAUM',g,(x,y,rod_start),10,rodlen,mat='steel',note=note)
   if stage==2:moving(rod,'LOWER')
   for end,z,leaf in [('oben',anchor,'LOWER' if stage==1 else 'UPPER'),('unten',base.add(rod_start,-8),None if stage==1 else 'LOWER')]:
    cap=cyl(label+'_Auge_'+end,g,(x,base.add(y,-8),z),20,16,(0,1,0),'steel',note=note)
    base.cyl(cap,(x,base.add(y,-9),z),6.5,18,(0,1,0),'cut','Bolzenloch_Studie')
    if leaf:moving(cap,leaf)
 # Removable front shields cover the long spring studies including their low anchors.
 for side,xx in [('L','door_x-90'),('R','door_x+door_leaf_w-10')]:
  folded('Senktuer_Federkanal06_'+side,g,(xx,'door_upper_y-75','-stand_h+70'),100,35,'door_closed_top+stand_h-70','frame')
 # Removable sheet skirts on sides of the load-bearing tubular frame.
 for side,x,sign in [('links','enc_left-2',-1),('rechts','enc_right+2',1)]:
  folded('Staender_Blechschuerze_'+side,g,(x,'enc_front+70','-stand_h+100'),'stand_d-140',25,'stand_h-200','frame',axes=((0,1,0),(sign,0,0),(0,0,1)))
 box('Einhausung_Tropfkante',g,('stand_cx-door_clear_w/2-20','enc_front+2',80),('door_clear_w+40',28,3),'sheet')
 # K07 replaces the entire obsolete narrow drain/filter path.
 from ruecklauf07 import add_return_parts
 add_return_parts(part,box,cyl,ring)
 # Cabinet external to wet area, front faces +X. Dedicated low-voltage and power zones.
 g='16_Schaltschrank'
 p=box('Schaltschrank_Hohlschale',g,('cab_x','cab_y','cab_z'),('cab_d','cab_w','cab_h'),'cabinet',note='600x800x300 Entwurf, keine ausgewählte IP-Gehäuseausführung. Außen auf Rahmen, nicht auf Nassraumblech.')
 base.box(p,('cab_x+3','cab_y+3','cab_z+3'),('cab_d+1','cab_w-6','cab_h-6'),'cut','Offene_Schrankfront')
 box('Schaltschrank_Tuer',g,('cab_x+cab_d','cab_y','cab_z'),(3,'cab_w','cab_h'),'cabinet')
 box('Schaltschrank_Montageplatte',g,('cab_x+18','cab_y+25','cab_z+25'),(3,'cab_w-50','cab_h-50'),'steel')
 for z in [110,320,600]:box('Schrank_DIN_Schiene_'+str(z),g,('cab_x+23','cab_y+40','cab_z+'+str(z)),(7,'cab_w-80',35),'silver')
 for y in [20,270,550]:box('Schrank_Kabelkanal_'+str(y),g,('cab_x+25','cab_y+'+str(y),'cab_z+45'),(40,30,'cab_h-90'),'panel')
 # Two real drive envelopes consistent with current X/Y closed-loop stepper concept.
 for i,a in enumerate('XY'):
  p=box('Treiber_'+a+'_CS_D508_Huelle',g,('cab_x+35',f'cab_y+{65+i*70}','cab_z+360'),(69.2,26.5,116),'dark',note='Leadshine CS-D508 116x69.2x26.5 mm laut Produktseite. Anschlussdetails/Einbauabstände vereinfacht; X/Y-Auslegung nicht freigegeben.')
  box('Treiber_'+a+'_Steckklemmen',g,('cab_x+104',f'cab_y+{65+i*70}','cab_z+372'),(10,26.5,70),'pcb')
 box('Treiber_Z_Reserve_KEIN_KAUFTEIL',g,('cab_x+35','cab_y+205','cab_z+340'),(170,50,180),'reserviert',note='Z-Motor noch nicht gewählt: reservierter Raum, kein belegtes Treibermodell. Nicht als CS-D508 oder Servo freigegeben.')
 box('Mesa_7i95T_Einbauraum',g,('cab_x+35','cab_y+320','cab_z+450'),(30,220,140),'pcb',note='Funktionszuordnung Mesa 7i95T belegt, geometrische 220x140x30 Reservierung NICHT Herstellermaß. 5-V-Logikversorgung separat; keine Motorleistung über Mesa.')
 for y in [330,380,430,480]:box('Mesa_Klemmen_Huelle_'+str(y),g,('cab_x+65','cab_y+'+str(y),'cab_z+450'),(12,32,12),'green')
 for nm,y,w,h,d in [('48V_Achsenversorgung',70,100,130,130),('24V_Feldversorgung',340,55,100,70),('5V_Mesa_Versorgung',430,35,90,55)]:
  box(nm+'_BAURAUM',g,('cab_x+35','cab_y+'+str(y),'cab_z+125'),(d,w,h),'panel',note='Spannungsebene vorgesehen, Hersteller/Leistung noch offen. Keine Verdrahtungs- oder Netzteilauslegung.')
 box('Sicherheitsgeraet_Reserve',g,('cab_x+35','cab_y+330','cab_z+315'),(100,90,85),'yellow',note='Sicherheitsrelais/Steuerung nur reserviert; Not-Halt, Tür, Nachlauf, Z-Haltung fachlich auslegen. LinuxCNC allein ist kein Sicherheitsnachweis.')
 box('Schuetz_Reserve',g,('cab_x+35','cab_y+65','cab_z+630'),(100,75,90),'dark')
 box('Sicherungen_Reserve',g,('cab_x+35','cab_y+160','cab_z+635'),(70,80,80),'panel')
 box('PE_Schiene_Schaltschrank',g,('cab_x+30','cab_y+60','cab_z+50'),(15,160,12),'bronze')
 box('EMV_Filter_Reserve',g,('cab_x+35','cab_y+330','cab_z+645'),(70,150,65),'silver')
 for i in range(9):box('Reihenklemme_'+str(i),g,('cab_x+35','cab_y+310+'+str(i*20),'cab_z+100'),(55,12,35),'panel')
 # Panel operator's UI outside enclosure; no mechanical handwheel remains.
 box('Bedienpult_Aussen_Reserve',g,('enc_right+25','enc_front-55',450),(140,110,220),'frame')
 for i,(z,mat) in enumerate([(600,'red'),(540,'green')]):cyl('Bedienpult_Taster_'+str(i),g,('enc_right+95','enc_front-65',z),30,10,(0,-1,0),mat)
 # All new names/IDs deterministic, no filename collisions with retained original parts.
 for i,d in enumerate(ps,1):
  d['id']='A%03d'%i;d['filename']=d['id']+'_'+d['name']
 return ps


def check_recipe(p,parts=None):
 validate(p);v=all_values(p);ds=parts if parts is not None else recipe();names=set()
 for d in ds:
  if d['name'] in names:raise ValueError('Doppelter Name '+d['name'])
  names.add(d['name'])
  if d['group'] not in GROUPS or d['material'] not in PALETTE:raise ValueError('Gruppe/Farbe fehlt '+d['name'])
  for op in d['ops']:
   for q in op['origin']:evaluate(q,v)
   sizes=op['size'] if op['kind']=='box' else [op['height']]
   if op['kind'] in ('cylinder','cone'):sizes=sizes+[op['diameter']]
   for q in sizes:
    if evaluate(q,v)<=0:raise ValueError('Nichtpositive Geometrie '+d['name']+' '+str(q))
   for pt in op.get('points',[]):
    for q in pt:evaluate(q,v)
 for r in length_report(p):
  if r['minimum_reserve_mm']<r['required_reserve_mm']-1e-6:raise ValueError('Spindelreserve für Zielhub zu klein: '+r['axis'])
 r=enclosure_report(p,ds)
 if r['violations']:raise ValueError('Einhausung zu klein fuer Zielhuebe: '+r['violations'][0]['name'])
 return v


def spring_report(p):
 from blech06 import spring_balance
 v=all_values(p);w=v['door_leaf_w'];h=v['door_leaf_h'];t=p['sheet_t']
 # Pre-conversion mass estimate. Density assumptions: steel 7850, glazing 1200 kg/m3.
 front=(w*h-(w-84)*(h-110))*t+2*(p['door_thickness']-t)*h*t
 rail=2*(45*t+2*(p['door_thickness']-2*t)*t)*(w-2*t-1)
 retainer=((w-20)*(h-40)-(w-84)*(h-110))*2
 glass=(w-64)*(h-90)*p['window_t']
 lower=(front+rail+retainer)*7.85e-6+glass*1.2e-6+2.0
 upper=lower+0.6
 r=spring_balance(lower,upper,v['door_travel_lower'])
 r['mass_basis']='sharp precursor / nominal 2-mm sheet; assumed steel 7850 and PC 1200 kg/m3; +2 kg fittings per segment, +0.6 kg handle. No NX measured mass.'
 return r


def drain_report(p):
 import ruecklauf07
 return ruecklauf07.report(p,all_values(p))
