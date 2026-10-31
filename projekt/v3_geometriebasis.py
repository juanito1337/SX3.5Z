# -*- coding: utf-8 -*-
"""SX3.5Z: quellenbezogenes, vereinfachtes parametrisches Aussenmodell.

Keine Hersteller-CAD-Daten. Nicht zur Fertigung von Maschinenteilen freigegeben.
Einheiten: mm; X rechts, Y nach hinten, Z nach oben. Ursprung: Projektion der
Spindelachse bei Neutralstellung auf die Aufstellflaeche.
Nur Python-Standardbibliothek; gemeinsam von CadQuery und NX Open verwendet.
"""
import ast
import json
import math
import os
from collections import OrderedDict

VERSION = '3.0'
SOURCE = 'V3 Fotoabgleich: 16 Nutzerfotos Tisch/Basis/Saeule; SX3.5 Fraese.pdf; unvermessene Restgeometrie aus V2. Keine neuen Hersteller-Messdaten.'
SPECS = []

def param(name, value, status, note, unit='mm', source='', limits=None):
    SPECS.append(dict(name=name, value=value, unit=unit, status=status,
                      note=note, source=source, limits=limits))

D = 'DOKUMENT'
A = 'ANNAHME'
U = 'EINSTELLUNG'
P20 = 'PDF-Seite 21 / Druckseite 20, Abschnitt 3.4'
# Unveraenderte Zahlenwerte aus der technischen Datentabelle.
param('table_x', 740, D, 'Tischlaenge', source=P20)
param('table_y', 180, D, 'Tischbreite', source=P20)
param('slot_w', 12, D, 'Oeffnungsbreite der T-Nuten; Tabelle nennt 12 (M10)', source=P20)
param('slot_pitch', 53, D, 'Abstand der drei T-Nuten', source=P20)
param('travel_x', 500, D, 'Gesamtverfahrweg X', source=P20)
param('travel_y', 200, D, 'Gesamtverfahrweg Y', source=P20)
param('travel_z_min', 240, D, 'Unterer Wert des einstellbaren Z-Gesamtverfahrwegs', source=P20)
param('travel_z_max', 290, D, 'Oberer Wert des einstellbaren Z-Gesamtverfahrwegs', source=P20)
param('quill_travel', 78, D, 'Pinolenhub', source=P20)
param('throat', 210, D, 'Ausladung; Bezug auf Saeulenvorderseite im Modell angenommen', source=P20)
param('spindle_gap_max', 350, D, 'Maximale Distanz Spindel zu Arbeitstisch', source=P20)
param('base_long', 510, D, 'Langer Sockelwert; Zuordnung zu Y angenommen', source=P20)
param('base_short', 280, D, 'Kurzer Sockelwert; Zuordnung zu X angenommen', source=P20)
param('bolt_pitch_long', 360, D, 'Langer Lochabstand; Zuordnung zu Y und Symmetrie angenommen', source=P20)
param('bolt_pitch_short', 250, D, 'Kurzer Lochabstand; Zuordnung zu X und Symmetrie angenommen', source=P20)
param('ref_size_l', 940, D, 'Referenzwert L der Maschinenmasse; NICHT als Modell-Aussenmass erzwungen', source=P20)
param('ref_size_b', 820, D, 'Referenzwert B der Maschinenmasse; NICHT als Modell-Aussenmass erzwungen', source=P20)
param('ref_size_h', 930, D, 'Referenzwert H; hoechster Punkt des vereinfachten Saeulenmotors', source=P20)
# Modellstellung, keine rekonstruierten Maschinen-Nullpunkte.
param('pos_x', 0, U, 'Tischversatz in X, Neutralstellung in der Mitte', limits=[-250,250])
param('pos_y', 0, U, 'Tischversatz in Y, Neutralstellung in der Mitte', limits=[-100,100])
param('z_travel_used', 240, U, 'Fuer Modellpruefung gewaehlter Z-Hub, im Dokument 240 bis 290', limits=[240,290])
param('head_down',60, U, 'Kopfabsenkung ab oberster Modellstellung; 0 bis z_travel_used, positiv nach unten')
param('quill_down', 0, U, 'Pinolenauszug, positiv nach unten', limits=[0,78])
# Unbemasste Formen aus Uebersicht / Explosionsbildern, frei rekonstruierbar.
# Alle Zahlen unter diesem Abschnitt sind Entwurfsannahmen, KEINE Messwerte.
for name, value, note in [
 ('base_h',72,'Sockelhoehe'), ('base_flange_h',18,'Sockelflanschdicke'),
 ('base_inset_x',18,'Seitlicher Absatz am Sockel'), ('base_inset_y',25,'Endabsatz am Sockel'),
 ('mount_hole_d',14,'Durchmesser der vier Aufstellbohrungen; Lage nicht als Bohrschablone verwenden'),
 ('guide_h',12,'Y-Fuehrungsleistenhoehe'),
 ('guide_spacing',140,'Abstand Y-Fuehrungsleisten'), ('guide_length',330,'Laenge Y-Fuehrungsleisten'),
 ('saddle_x',260,'Kreuzschlittenbreite'), ('saddle_y',210,'Kreuzschlittentiefe'),
 ('saddle_h',42,'Kreuzschlittenhoehe'), ('cross_h',10,'Oberer Tischtraeger'),
 ('table_h',42,'Tischdicke'), ('slot_top_h',9,'Tiefe schmaler Nutenteil'),
 ('slot_under_w',22,'Breite T-Nuten-Hinterschnitt'), ('slot_under_h',10,'Hoehe T-Nuten-Hinterschnitt'),
 ('column_x',158,'Saeulenbreite'), ('column_y',145,'Saeulentiefe'),
 ('column_foot_h',18,'Saeulenfussdicke'), ('column_cap_h',15,'Saeulendeckeldicke'),
 ('column_guide_w',24,'Z-Fuehrungsleistenbreite'), ('column_guide_pitch',112,'Z-Fuehrungsleistenabstand'),
 ('head_x',164,'Kopfbreite'), ('head_h',230,'Kopfgehaeusehoehe'),
 ('head_front',64,'Vorderer Ueberstand des Kopfes vor Spindelachse'),
 ('head_quill_offset',32,'Kopfunterkante ueber Spindelstirn bei eingefahrener Pinole'),
 ('belt_cover_h',50,'Riemendeckelhoehe'), ('belt_cover_extra',0.8,'Deckelueberstand'),
 ('drawbar_cap_d',38,'Abdeckung Anzugspindel Durchmesser'), ('drawbar_cap_h',78,'Abdeckung Anzugspindel Hoehe'),
 ('quill_d',60,'Pinolenaussendurchmesser'), ('quill_bore_d',38,'Vereinfachte Innenbohrung der Pinole'),
 ('quill_body_h',110,'Dargestellte Pinolenlaenge'), ('spindle_nose_d',54,'Spindelnasendurchmesser'),
 ('spindle_nose_h',15,'Spindelnasenhoehe'), ('spindle_shaft_d',36,'Vereinfachter Spindelschaft'),
 ('z_motor_d',78,'Z-Motordurchmesser'), ('z_motor_h',91,'Z-Motorhoehe'),
 ('z_motor_flange_h',10,'Z-Motorflanschdicke'), ('z_motor_cap_h',8,'Z-Motordeckelhoehe'),
 ('panel_x',138,'Bedienpanelbreite'), ('panel_y',80,'Bedienpaneltiefe'), ('panel_h',174,'Bedienpanelhoehe'),
 ('panel_gap',28,'Abstand Bedienpanel zum Kopf'), ('panel_z_offset',96,'Panelunterkante ueber Kopfunterkante'),
 ('wheel_d',125,'X-/Y-Handraddurchmesser'), ('wheel_h',25,'Handraddicke'), ('wheel_rim',9,'Radkranzbreite'),
 ('wheel_hub_d',36,'Handradnabendurchmesser'),
 ('wheel_shaft_d',16,'Handradwellen-Durchmesser'), ('wheel_grip_d',16,'Handradgriff-Durchmesser'),
 ('wheel_grip_h',47,'Handradgrifflaenge'), ('x_wheel_offset',69,'X-Handradabstand vom Tischende'),
 ('y_wheel_offset',73,'Y-Handradabstand vor Sockelvorderkante'),
 ('star_hub_d',45,'Sternhebelnabendurchmesser'), ('star_hub_h',24,'Sternhebelnabenbreite'),
 ('star_bar_d',10,'Sternhebelstangendurchmesser'), ('star_radius',130,'Sternhebel-Laenge bis Griffanfang'),
 ('star_grip_d',19,'Sternhebelgriffdurchmesser'), ('star_grip_h',56,'Sternhebelgrifflaenge'),
 ('shield_w',152,'Schutzscheibenbreite'), ('shield_y',137,'Schutzscheibentiefe'),
 ('shield_h',125,'Schutzscheibenhoehe'), ('shield_t',2,'Schutzscheibendicke'),
 ('bellows_w',158,'Faltenbalgbreite'), ('bellows_depth',19,'Faltentiefe'),
]:
    param(name, value, A, note, source='Unbemasste Ansichten PDF 17/18 und Explosionsbilder PDF 54/57/59/61/63')

# Quellenschluessel sind in Quellen_V2/Historische_Quellen_v2.md aufgeloest.
W = 'WEB_BESTAETIGT'
F = 'FOTO_ANNAHME'
N = 'NORMREFERENZ_KEIN_MASCHINENMESSWERT'
for spec in SPECS:
    if spec['status'] == D:
        spec['status'] = W
        spec['source'] = 'S1 (Paulimot SX3.5Z, Art. 41874230) + ' + spec['source']
    elif spec['status'] == A:
        spec['status'] = F
        spec['source'] = 'S2-S6 (Paulimot Detailfotos) / PDF-Explosionsansichten; KEIN abgelesenes Mass'
# In v2 werden nur positive Laengen als Expressions genutzt (mm-Konvention).
for name, value, note in [
 ('head_corner_r',6,'Verrundungsradius Kopf in Draufsicht'),
 ('frontplate_t',3,'Frontplatte am Kopf'),
 ('cover_t',2,'Darstellungsdicke Saeulenverkleidung'),
 ('cover_extra_x',12,'Verkleidung seitlicher Abstand zur Guss-Saeule'),
 ('cover_rear_extra',48,'Unterer hinterer Verkleidungsueberstand'),
 ('cover_taper_h',225,'Hoehe der Schraegung am oberen Verkleidungsruecken'),
 ('cover_top_extra',12,'Oberer hinterer Verkleidungsueberstand'),
 ('table_end_margin',12,'Tischrand bis zur Quertasche'),
 ('table_end_pocket_x',32,'Laenge einer Quertasche entlang X'),
 ('table_end_pocket_y',152,'Breite der Quertaschen entlang Y'),
 ('table_end_pocket_h',18,'Tiefe der Quertaschen'),
 ('table_end_pocket_r',5,'Eckradius der Quertaschen'),
 ('table_drain_w',3,'Schmale Randnut vorn und hinten'),
 ('table_drain_inset',7,'Lage der Randnut zur Tischkante'),
 ('wheel_dish_depth',16,'Tiefe der konischen Tellervertiefung'),
 ('wheel_dish_inner_d',56,'Kleiner Durchmesser der Tellervertiefung'),
 ('shield_corner',20,'Abgekantete vordere Ecken des Spindelschutzes'),
 ('shield_extension',30,'Untere Schutzscheibe: ausgezogene Zusatzhoehe'),
 ('shield_lower_h',55,'Hoehe der unteren Schutzscheibe'),
 ('bellows_sheet_t',1.1,'Darstellungsdicke der Faltenhaut in Y bzw. Z'),
 ('magnetpad_y',65,'Breite Werkzeug-Magnetpad an rechter Saeulenseite'),
 ('magnetpad_h',100,'Hoehe Werkzeug-Magnetpad'),
 ('sk_taper_length',48.4,'Modell-Laenge der Konusdarstellung; NICHT gemessene SX3.5Z Bohrung'),
 ('z_screw_d',18,'Symbolischer Durchmesser Z-Trapezspindel, ohne Gewinde'),
]:
    param(name,value,F,note,source='S2-S6 bzw. Modellannahme, siehe Quellen_V2/Historische_Quellen_v2.md')
param('sk_gauge_d',31.75,N,'SK30 Bezugsdurchmesser d1, kein Nachweis der realen Spindelstirnlage',source='S8, GEWEFA DIN2080, PDF S.57/58, Druck S.55/56')
# V3: Qualitative Rekonstruktion aus den 16 vom Nutzer hochgeladenen Fotos.
# Die Fotos zeigen Baumerkmale, sind aber KEINE kalibrierte Vermessung.
# Kein Parameter dieser Lieferung ist ein vom Nutzer bestaetigter Messwert.
PHOTO_TABLE='F01/F02: Nutzerfotos 1000047826.jpg / 1000047824.jpg'
PHOTO_BASE='F03-F06: Nutzerfotos 1000047828.jpg bis 1000047831.jpg'
PHOTO_COL='F07-F16: Nutzerfotos 1000047833.jpg bis 1000047842.jpg'
F3='NUTZERFOTO_ANNAHME'

def revise(name, value, note, source):
    spec=next(x for x in SPECS if x['name']==name)
    spec.update(value=value,status=F3,note=note,source=source)

# Dokumentierte Hauptmasse bleiben aus der Anleitung erhalten; keine scheinbar
# genau aus schraeg aufgenommenen Massstaeben ausgelesenen Werte einsetzen.
for spec in SPECS:
    if spec['status']==W:
        spec['status']=D
        spec['source']=P20+'; aus V2 uebernommen, NICHT am konkreten Exemplar bestaetigt'
    elif spec['status']==F:
        spec['source']='V2-Restannahme: '+spec['source']

revise('base_h',80,'Hoehe Guss-Basiskoerper; grobe Foto-Proportion, nicht abgelesen',PHOTO_BASE)
revise('column_y',112,'Tiefe des normalen Saeulengusskoerpers, ohne Z-Fuehrung; Foto-Annahme',PHOTO_COL)
revise('guide_length',360,'Y-Fuehrungslaenge; Foto-Annahme, kein freigegebener Verfahrweg',PHOTO_BASE)
revise('column_foot_h',18,'Dicke Saeulenfuss; Foto-Annahme',PHOTO_COL)

for name,value,note,source in [
 ('base_wall',12,'Angenommene seitliche Wandstaerke des unten offenen Sockels',PHOTO_BASE),
 ('base_roof_t',14,'Angenommene Dachstaerke oberhalb des Sockelhohlraums',PHOTO_BASE),
 ('base_end_wall',16,'Angenommene Stirnwandstaerke Sockel',PHOTO_BASE),
 ('base_slot_w',78,'Lichte Breite durchgehender Y-Aussparung, nicht gemessen',PHOTO_BASE),
 ('base_slot_l',258,'Laenge Y-Durchbruch, nicht gemessen',PHOTO_BASE),
 ('base_slot_front',85,'Abstand vordere Sockelstirn bis Beginn Durchbruch',PHOTO_BASE),
 ('base_rib_t',9,'Dicke der 4+4 modellierten inneren Dreiecksrippen',PHOTO_BASE),
 ('base_rib_reach',22,'Seitlicher Vorsprung der Sockelrippen in den Hohlraum',PHOTO_BASE),
 ('base_rib_h',26,'Hoehe Sockelrippen unter der Dachunterseite',PHOTO_BASE),
 ('base_y_bore_d',22,'Y-Spindeldurchfuehrung, KEINE Lagerpassung',PHOTO_BASE),
 ('base_y_boss_d',42,'Aussendurchmesser vereinfachter innerer Y-Durchfuehrung',PHOTO_BASE),
 ('base_y_axis_drop',14,'Y-Spindelachse unter Basisoberseite; Funktionsannahme',PHOTO_BASE),
 ('column_seat_h',4,'Erhoehung der beiden bearbeiteten Saeulen-Auflagepads',PHOTO_BASE),
 ('column_seat_w',34,'Breite je Auflagepad',PHOTO_BASE),
 ('column_mount_px',196,'Saeulenfuss-Lochabstand X; NICHT Bohrschablone',PHOTO_BASE+'; '+PHOTO_COL),
 ('column_mount_py',84,'Saeulenfuss-Lochabstand Y; NICHT Bohrschablone',PHOTO_BASE+'; '+PHOTO_COL),
 ('column_mount_d',11,'Saeulenfuss-Durchgangsbohrung, Gewinde nicht rekonstruiert',PHOTO_COL),
 ('column_length',780,'Saeulen-Gesamtlaenge inkl. Fuss: grobe Foto-Proportionsannahme; nicht kalibriert',PHOTO_COL),
 ('column_wall',12,'Seitenwandstaerke der hinten offenen Saeule',PHOTO_COL),
 ('column_front_wall',16,'Frontwandstaerke hinter der Z-Fuehrung',PHOTO_COL),
 ('column_end_wall',14,'Dicke oberer Gussabschluss',PHOTO_COL),
 ('column_slot_w',38,'Lichte Schlitzbreite in der Saeulenfront',PHOTO_COL),
 ('column_slot_l',510,'Laenge des durchgehenden Frontschlitzes',PHOTO_COL),
 ('column_slot_bottom',180,'Schlitzbeginn ueber unterer Saeulen-Anschlussflaeche',PHOTO_COL),
 ('column_guide_proj',12,'Vorsprung der angenaeherten Z-Schwalbenschwanzfuehrung',PHOTO_COL),
 ('column_guide_width',126,'Breite Z-Fuehrung an der vorstehenden Flaeche',PHOTO_COL),
 ('column_rib_t',12,'Dicke der zwei grossen Querrippen',PHOTO_COL),
 ('column_rib_z1',300,'Hoehe erste Querrippe ab Saeulen-Anschlussflaeche',PHOTO_COL),
 ('column_rib_z2',440,'Hoehe zweite Querrippe ab Saeulen-Anschlussflaeche',PHOTO_COL),
 ('column_rib_clear',52,'Freiraum zwischen Frontwand-Innenseite und Querrippen',PHOTO_COL),
 ('column_gusset_t',9,'Dicke der vereinfachten seitlichen Gussrippen',PHOTO_COL),
 ('column_gusset_reach',18,'Seitlicher Vorsprung kleiner Gussrippen',PHOTO_COL),
 ('column_inspect_d',32,'Seitliche Rundoeffnung: Durchmesser nur angenaehert, KEIN Lagersitz',PHOTO_COL),
 ('column_inspect_top',40,'Abstand seitliche Rundoeffnung unter oberer Stirn',PHOTO_COL),
 ('column_inspect_y',55,'Rundoeffnungsmitte hinter Frontflaeche',PHOTO_COL),
 ('column_screw_offset',38,'Symbolische Z-Spindelachse hinter Saeulenfront; zu vermessen',PHOTO_COL+' / PDF57'),
 ('column_top_bore_d',28,'Vereinfachte obere Spindeldurchfuehrung, keine Lagerpassung',PHOTO_COL+' / PDF57'),
 ('table_under_w',112,'Untere lichte Breite des angenommenen X-Fuehrungsprofils',PHOTO_TABLE),
 ('table_under_flare',7,'Seitliche Aufweitung pro Seite nach oben',PHOTO_TABLE),
 ('table_under_h',10,'Tiefe des X-Fuehrungsprofils von Tischunterkante',PHOTO_TABLE),
 ('table_channel_w',54,'Breite der mittleren Unterseiten-Freistellung',PHOTO_TABLE),
 ('table_channel_h',17,'Tiefe mittlere Unterseiten-Freistellung',PHOTO_TABLE),
 ('table_end_hole_d',5.5,'Symbolischer stirnseitiger Befestigungsdurchmesser, Gewinde unbekannt',PHOTO_TABLE),
 ('table_end_hole_pitch',110,'Lochabstand stirnseitiger Tischbefestigung, angenommen',PHOTO_TABLE),
 ('table_end_hole_depth',12,'Modellierte Tiefe Stirnbohrungen, nicht gemessen',PHOTO_TABLE),
 ('scale_depth',10,'Tiefe vorhandener seitlicher X-Massstabsdarstellung',PHOTO_TABLE),
 ('scale_h',20,'Hoehe vorhandener seitlicher X-Massstabsdarstellung',PHOTO_TABLE),
 ('scale_end_margin',16,'Abstand X-Massstab von Tischstirnseiten',PHOTO_TABLE),
 ('scale_reader_x',95,'X-Lage des feststehenden Lesekopfes relativ zum Sattel, angenommen',PHOTO_TABLE),
 ('scale_reader_l',58,'Laenge des stilisierten X-Lesekopfes',PHOTO_TABLE),
]:
    param(name,value,F3,note,source=source)

# Nicht mehr geometrisch verwendete V2-Parameter nicht als editierbare Masse anbieten.
SPECS[:]=[spec for spec in SPECS if spec['name'] not in ('base_inset_y','column_guide_w','column_guide_pitch')]
PHOTO_CASTINGS=('Basis_Guss_Foto','Saeule_Guss_Foto','Arbeitstisch_Foto')

# Kegelverhaeltnis 7:24 ist bewusst als exakte Zahl im Ausdruck hinterlegt.
# Ausdruecke sind absichtlich auf einfache, auch in NX gueltige Arithmetik begrenzt.
DERIVED = OrderedDict([
 ('column_front_y','throat'),
 ('column_back_y','column_front_y + column_y'),
 ('base_front_y','column_back_y - base_long'),
 ('base_center_y','column_back_y - base_long / 2'),
 ('saddle_bottom_z','base_h + guide_h'),
 ('table_bottom_z','saddle_bottom_z + saddle_h + cross_h'),
 ('table_top_z','table_bottom_z + table_h'),
 ('spindle_zero_z','table_top_z + spindle_gap_max - head_down'),
 ('spindle_face_z','spindle_zero_z - quill_down'),
 ('head_bottom_z','spindle_zero_z + head_quill_offset'),
 ('head_top_z','head_bottom_z + head_h'),
 ('head_depth','column_front_y + head_front'),
 ('column_top_z','base_h + column_seat_h + column_length'),
 ('column_bottom_z','base_h + column_seat_h + column_foot_h'),
 ('column_height','column_top_z - column_bottom_z'),
 ('panel_left_x','-head_x / 2 - panel_gap - panel_x'),
 ('panel_bottom_z','head_bottom_z + panel_z_offset'),
 ('x_wheel_x','pos_x + table_x / 2 + x_wheel_offset'),
 ('x_wheel_z','table_bottom_z + 10'),
 ('y_wheel_y','base_front_y - y_wheel_offset'),
 ('y_wheel_z','base_h - base_y_axis_drop'),
 ('star_x','head_x / 2 + 12'),
 ('star_y','-head_front + 112'),
 ('star_z','head_bottom_z + 62'),
 ('bellows_bottom_z','table_top_z + 34'),
 ('bellows_height','head_bottom_z - bellows_bottom_z - 6'),
 ('cover_x','column_x + 2*cover_extra_x'),
 ('cover_back_y','column_back_y + cover_rear_extra'),
 ('cover_top_back_y','column_back_y + cover_top_extra'),
 ('cover_shoulder_z','column_top_z + column_cap_h - cover_taper_h'),
 ('sk_small_d','sk_gauge_d - sk_taper_length*7/24'),
 ('head_face_y','-head_front-frontplate_t'),
 ('base_inner_x','base_short-2*base_inset_x-2*base_wall'),
 ('base_inner_z','base_h-base_roof_t'),
 ('column_seat_z','base_h+column_seat_h'),
 ('column_inner_x','column_x-2*column_wall'),
 ('column_inner_front_y','column_front_y+column_front_wall'),
 ('column_screw_y','column_front_y+column_screw_offset'),
 ('z_motor_top_z','column_top_z+column_cap_h+z_motor_flange_h+z_motor_h+z_motor_cap_h'),

])

# CAD-Farben sind an den Online-Fotos orientiert, keine gemessenen Farbwerte.
PALETTE = {
 'cast': (0.62,0.025,0.045,1), 'dark': (0.09,0.11,0.13,1),
 'steel':(0.63,0.68,0.71,1), 'panel':(0.81,0.83,0.82,1),
 'black':(0.055,0.064,0.070,1), 'red':(0.72,0.025,0.04,1),
 'yellow':(0.93,0.73,0.12,1), 'green':(0.10,0.47,0.25,1),
 'glass':(0.75,0.88,0.92,0.20), 'lcd':(0.40,0.62,0.24,1), 'silver':(0.72,0.74,0.76,1),
}
LAYERS = {'01_Gestell':10,'02_Kreuztisch':20,'03_Kopf':30,
          '04_Bedienung':40,'05_Schutz':50,'06_Details':60}


def evaluate(text, values):
    """Sicherer Evaluator fuer Zahlen, Namen und +-*/; keine Python-eval-Ausfuehrung."""
    if isinstance(text, (int,float)):
        return float(text)
    root = ast.parse(str(text), mode='eval')
    def rec(n):
        if isinstance(n, ast.Expression): return rec(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int,float)): return float(n.value)
        if isinstance(n, ast.Num): return float(n.n)
        if isinstance(n, ast.Name) and n.id in values: return float(values[n.id])
        if isinstance(n, ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            return rec(n.operand) * (-1 if isinstance(n.op,ast.USub) else 1)
        if isinstance(n, ast.BinOp):
            a,b=rec(n.left),rec(n.right)
            if isinstance(n.op,ast.Add): return a+b
            if isinstance(n.op,ast.Sub): return a-b
            if isinstance(n.op,ast.Mult): return a*b
            if isinstance(n.op,ast.Div): return a/b
        raise ValueError('Nicht unterstuetzter Ausdruck: '+str(text))
    result=rec(root)
    if not math.isfinite(result): raise ValueError('Nicht endlicher Zahlenwert: '+str(text))
    return result


def load_parameters(path=None):
    p=OrderedDict((s['name'],float(s['value'])) for s in SPECS)
    if path and os.path.exists(path):
        with open(path, encoding='utf-8-sig') as f: overrides=json.load(f)
        if not isinstance(overrides,dict): raise ValueError('Parameterdatei muss ein JSON-Objekt sein.')
        for key,value in overrides.items():
            if key.startswith('_'): continue
            if key not in p: raise ValueError('Unbekannter Parameter: '+key)
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
                raise ValueError('Ungueltiger Zahlenwert: '+key)
            p[key]=float(value)
    validate(p)
    return p


def all_values(p):
    v=OrderedDict(p)
    for k,expr in DERIVED.items(): v[k]=evaluate(expr,v)
    return v


def validate(p):
    for s in SPECS:
        n=s['name']
        if n not in ('pos_x','pos_y','head_down','quill_down','shield_extension') and p[n]<=0:
            raise ValueError(n+' muss groesser als Null sein.')
    if abs(p['pos_x'])>p['travel_x']/2+1e-8: raise ValueError('pos_x ausserhalb +/- travel_x/2')
    if abs(p['pos_y'])>p['travel_y']/2+1e-8: raise ValueError('pos_y ausserhalb +/- travel_y/2')
    if not p['travel_z_min']<=p['z_travel_used']<=p['travel_z_max']: raise ValueError('z_travel_used ausserhalb dokumentiertem Bereich')
    if not 0<=p['head_down']<=p['z_travel_used']: raise ValueError('head_down ausserhalb Z-Hub')
    if not 0<=p['quill_down']<=p['quill_travel']: raise ValueError('quill_down ausserhalb Pinolenhub')
    if p['spindle_gap_max']-p['head_down']-p['quill_down']<0: raise ValueError('Spindelstirn unter Tischoberkante; unzulaessige Stellung')
    if p['slot_under_w']<=p['slot_w']: raise ValueError('Hinterschnitt muss breiter als Nut sein')
    if p['slot_under_w']>=p['slot_pitch']: raise ValueError('T-Nuten-Hinterschnitte ueberlappen')
    if p['slot_pitch']+p['slot_under_w']/2>=p['table_y']/2: raise ValueError('T-Nuten liegen ausserhalb der Tischbreite')
    if p['slot_top_h']+p['slot_under_h']>=p['table_h']-5: raise ValueError('T-Nuten zu tief fuer Tischdicke')
    if p['base_flange_h']>=p['base_h']: raise ValueError('Sockelflansch muss niedriger als Sockel sein')
    if p['bolt_pitch_short']+p['mount_hole_d']>=p['base_short']: raise ValueError('Aufstellbohrungen verlassen den Sockel')
    if p['bolt_pitch_long']+p['mount_hole_d']>=p['base_long']: raise ValueError('Aufstellbohrungen verlassen den Sockel')
    if p['quill_bore_d']>=p['quill_d']: raise ValueError('Pinolenwanddicke negativ')
    if p['wheel_rim']>=p['wheel_d']/2: raise ValueError('Handradkranz zu breit')
    if not 0 <= p['shield_extension'] <= p['shield_lower_h']-5: raise ValueError('Unzulaessiger Schutzscheibenauszug')
    if p['wheel_dish_depth'] >= p['wheel_h']-2: raise ValueError('Handradteller zu duenn')
    if p['table_end_pocket_h'] >= p['table_h']-5: raise ValueError('Tisch-Quertaschen zu tief')
    v=all_values(p)
    if v['sk_small_d']<=0: raise ValueError('SK-Konuslaenge unzulaessig')
    if v['bellows_height']<=0: raise ValueError('Faltenbalghoehe nicht positiv')
    if v['column_height']<=0: raise ValueError('Saeulenhoehe nicht positiv')
    if p['base_roof_t'] >= p['base_h']-p['base_flange_h']: raise ValueError('Sockelhohlraum zu flach')
    if p['base_slot_w'] >= p['guide_spacing']-10: raise ValueError('Y-Durchbruch zu breit')
    if p['base_slot_front']+p['base_slot_l'] >= p['guide_length']+8: raise ValueError('Y-Durchbruch verlaesst Fuehrungsbereich')
    if p['base_rib_reach']*2+p['base_slot_w'] >= v['base_inner_x']: raise ValueError('Sockelrippen zu breit')
    if not p['column_foot_h'] < p['column_slot_bottom'] < p['column_length']-p['column_end_wall']: raise ValueError('Schlitzbeginn unzulaessig')
    if p['column_slot_bottom']+p['column_slot_l'] >= p['column_length']-p['column_end_wall']: raise ValueError('Z-Schlitz zu lang')
    if p['column_rib_z2']-p['column_rib_z1'] <= p['column_rib_t']: raise ValueError('Querrippen ueberlappen')
    if p['column_rib_z1'] < p['column_foot_h'] or p['column_rib_z2']+p['column_rib_t'] >= p['column_length']-p['column_end_wall']: raise ValueError('Querrippen ausserhalb der Saeule')
    if p['column_front_wall']+p['column_rib_clear'] >= p['column_y']-5: raise ValueError('Kein Raum fuer Querrippen')
    if p['column_slot_w'] >= p['column_guide_width']-20: raise ValueError('Z-Schlitz zu breit')
    if p['table_under_h'] >= p['table_channel_h']: raise ValueError('Mittlere Tischfreistellung muss tiefer als Fuehrung sein')
    if p['table_channel_h']+p['slot_top_h']+p['slot_under_h'] > p['table_h']-3: raise ValueError('Zu geringe Wand unter mittlerer T-Nut')
    if p['table_under_w']+2*p['table_under_flare'] >= p['table_y']-12: raise ValueError('Tischfuehrung zu breit')
    return True


def recipe():
    """V3: gemeinsames BRep/NX-Rezept. Alle unbemassten Details sind Annahmen.

    box, cylinder, cone und prism werden als echte Volumen-Features aufgebaut.
    Prismen verwenden parametrisch verknuepfte Polygonpunkte, keine Netze.
    """
    parts=[]
    def part(name,group,material='cast',note='FOTO-ANNAHME; Abmessungen nicht gemessen',source='S2-S6'):
        d=dict(name=name,group=group,material=material,note=note,source=source,ops=[])
        parts.append(d);return d
    def box(p,origin,size,op='add',label='Block'):
        p['ops'].append(dict(kind='box',origin=list(map(str,origin)),size=list(map(str,size)),op=op,label=label))
    def cyl(p,origin,diameter,height,direction=(0,0,1),op='add',label='Zylinder'):
        p['ops'].append(dict(kind='cylinder',origin=list(map(str,origin)),diameter=str(diameter),height=str(height),direction=direction,op=op,label=label))
    def cone(p,origin,d1,d2,height,direction=(0,0,1),op='add',label='Kegel'):
        p['ops'].append(dict(kind='cone',origin=list(map(str,origin)),diameter=str(d1),top_diameter=str(d2),height=str(height),direction=direction,op=op,label=label))
    def prism(p,points,height,direction,op='add',label='Profil_Extrusion'):
        points=[list(map(str,v)) for v in points]
        p['ops'].append(dict(kind='prism',points=points,origin=points[0],height=str(height),direction=direction,op=op,label=label))
    def rounded_xy(p,x,y,z,w,d,h,r,op='add'):
        # Gemeinsam benutzte Rundkontur; jeder Baustein verbindet sich flaechig.
        box(p,('(%s)+(%s)'%(x,r),y,z),('(%s)-2*(%s)'%(w,r),d,h),op)
        box(p,(x,'(%s)+(%s)'%(y,r),z),(w,'(%s)-2*(%s)'%(d,r),h),op)
        for dx in [str(r),'(%s)-(%s)'%(w,r)]:
            for dy in [str(r),'(%s)-(%s)'%(d,r)]:
                cyl(p,('(%s)+(%s)'%(x,dx),'(%s)+(%s)'%(y,dy),z),'2*(%s)'%r,h,op=op)
    # GESTELL, SCHWALBENSCHWANZFUEHRUNGEN UND VERKLEIDUNG
    g='01_Gestell'
    p=part('Basis_Guss_Foto',g,'cast',note='Foto-Topologie: unten hohl, 4+4 Dreiecksrippen, Y-Durchbruch, Saeulenpads. Alle inneren Masse ANNAHMEN.',source=PHOTO_BASE)
    rounded_xy(p,'-base_short/2','base_front_y',0,'base_short','base_long','base_flange_h',2)
    box(p,('-base_short/2+base_inset_x','base_front_y','base_flange_h'),('base_short-2*base_inset_x','base_long','base_h-base_flange_h'),label='Basiskoerper')
    box(p,('-base_inner_x/2','base_front_y+base_end_wall',-1),('base_inner_x','base_long-2*base_end_wall','base_inner_z+1'),op='cut',label='Hohlraum_unten_Foto')
    # Vier Dreiecksrippen je Laengswand; Zahl/Form aus Fotos, Masse angenommen.
    for side in [-1,1]:
        for i in range(1,5):
            yy='base_front_y+base_end_wall+%d*(base_long-2*base_end_wall)/5-base_rib_t/2'%i
            xx='%d*base_inner_x/2'%side
            pts=[(xx,yy,'base_inner_z-base_rib_h'),(xx,yy,'base_inner_z+0.3'),
                 ('(%s)-%d*base_rib_reach'%(xx,side),yy,'base_inner_z+0.3')]
            prism(p,pts,'base_rib_t',(0,1,0),label='Gussrippe_%d_%d'%(side,i))
    # Bohrungsboss und nachfolgende Durchfuehrung fuer die ORIGINAL-Y-Spindel.
    cyl(p,(0,'base_front_y','y_wheel_z'),'base_y_boss_d','base_slot_front+8',(0,1,0),label='Y_Durchfuehrungsboss_ANNAHME')
    # Dovetail is part of casting, not a floating steel rail.
    prism(p,[('-guide_spacing/2','base_front_y+8','base_h'),('guide_spacing/2','base_front_y+8','base_h'),
             ('guide_spacing/2+8','base_front_y+8','base_h+guide_h'),('-guide_spacing/2-8','base_front_y+8','base_h+guide_h')],
          'guide_length',(0,1,0),label='Y_Fuehrungsprofil_ANNAHME')
    # Two pads on the rear deck. Bosses under their screw holes reconnect to sidewall/roof.
    for ix in [-1,1]:
        xx='%d*column_mount_px/2'%ix
        box(p,('(%s)-column_seat_w/2'%xx,'column_front_y-2','base_h'),
            ('column_seat_w','column_y+4','column_seat_h'),label='Saeulenauflage_%d'%ix)
        for iy in [-1,1]:
            yy='column_front_y+column_y/2+%d*column_mount_py/2'%iy
            box(p,('(%s)-column_seat_w/2'%xx,'(%s)-17'%yy,'base_inner_z-14'),('column_seat_w',34,14.3),label='Saeulenbohrungsboss')
            cyl(p,(xx,yy,'base_inner_z-15'),'column_mount_d','base_roof_t+column_seat_h+16',op='cut',label='Saeulenbefestigung_symbolisch')
    box(p,('-base_slot_w/2','base_front_y+base_slot_front',-1),('base_slot_w','base_slot_l','base_h+guide_h+2'),op='cut',label='Y_Durchbruch_Foto')
    cyl(p,(0,'base_front_y-1','y_wheel_z'),'base_y_bore_d','base_slot_front+3',(0,1,0),op='cut',label='Y_Durchfuehrung_KEIN_Lagersitz')
    for ix in [-1,1]:
        for iy in [-1,1]:
            cyl(p,('%d*bolt_pitch_short/2'%ix,'base_center_y+%d*bolt_pitch_long/2'%iy,-1),'mount_hole_d','base_h+2',op='cut',label='Aufstellbohrung_ANNAHME')

    p=part('Saeule_Guss_Foto',g,'dark',note='Foto-Topologie: hinten offen, zwei Querrippen, seitliche Rippen, Z-Schlitz, Rundoeffnung und Fuss. Innenmasse/Lochbilder nicht gemessen.',source=PHOTO_COL)
    box(p,('-base_short/2+20','column_front_y-8','column_seat_z'),('base_short-40','column_y+8','column_foot_h'),label='Saeulenfuss')
    box(p,('-column_x/2','column_front_y','column_bottom_z'),('column_x','column_y','column_height'),label='Saeulenkoerper')
    # Hinten und unten offene U-Schale; oberer Abschluss bleibt stehen.
    box(p,('-column_inner_x/2','column_inner_front_y','column_seat_z-1'),
        ('column_inner_x','column_y-column_front_wall+1','column_length-column_end_wall+1'),op='cut',label='Offene_Rueckseite_Foto')
    # Full-width female/male profile approximation, cut through again below.
    prism(p,[('-column_guide_width/2+7','column_front_y','column_bottom_z+28'),
             ('column_guide_width/2-7','column_front_y','column_bottom_z+28'),
             ('column_guide_width/2','column_front_y-column_guide_proj','column_bottom_z+28'),
             ('-column_guide_width/2','column_front_y-column_guide_proj','column_bottom_z+28')],
          'column_height-50',(0,0,1),label='Z_Fuehrungsprofil_ANNAHME')
    box(p,('-column_slot_w/2','column_front_y-column_guide_proj-1','column_seat_z+column_slot_bottom'),
        ('column_slot_w','column_front_wall+column_guide_proj+2','column_slot_l'),op='cut',label='Durchgehender_Z_Schlitz_Foto')
    for i in [1,2]:
        box(p,('-column_inner_x/2-0.3','column_inner_front_y+column_rib_clear','column_seat_z+column_rib_z%d'%i),
            ('column_inner_x+0.6','column_y-column_front_wall-column_rib_clear','column_rib_t'),label='Querrippe_%d_Foto'%i)
    for side in [-1,1]:
        xx='%d*column_inner_x/2'%side
        for i,fraction in enumerate(['0.14','0.30','0.66','0.84']):
            zz='column_bottom_z+%s*column_height'%fraction
            # Triangular gussets extend inward from sidewalls; do not fill the axial corridor.
            pts=[(xx,'column_inner_front_y',zz),
                 (xx,'column_back_y-10',zz),
                 ('(%s)-%d*column_gusset_reach'%(xx,side),'column_inner_front_y',zz)]
            prism(p,pts,'column_gusset_t',(0,0,1),label='Seitliche_Gussrippe_%d_%d'%(side,i+1))
    # Four pads/fastener bosses visible at the rear of the casting are simplified.
    for side in [-1,1]:
        for frac in ['0.12','0.74']:
            xx='-column_inner_x/2' if side<0 else 'column_inner_x/2-22'
            box(p,(xx,'column_inner_front_y-0.2','column_bottom_z+%s*column_height'%frac),
                (22,8.2,24),label='Innenpad_Foto_ANNAHME')
    for ix in [-1,1]:
        for iy in [-1,1]:
            cyl(p,('%d*column_mount_px/2'%ix,'column_front_y+column_y/2+%d*column_mount_py/2'%iy,'column_seat_z-1'),
                'column_mount_d','column_foot_h+2',op='cut',label='Fuss_Durchgangsbohrung_ANNAHME')
    cyl(p,('-column_x/2-1','column_front_y+column_inspect_y','column_top_z-column_inspect_top'),
        'column_inspect_d','column_wall+2',(1,0,0),op='cut',label='Seitliche_Rundoeffnung_KEIN_Lagersitz')
    cyl(p,(0,'column_screw_y','column_top_z-column_end_wall-1'),'column_top_bore_d','column_end_wall+2',op='cut',label='Obere_Durchfuehrung_ANNAHME')
    p=part('Z_Spindel_symbolisch',g,'steel',note='Nur Lage und Funktion aus PDF-Explosionsbild; kein rekonstruiertes Gewinde',source='PDF57')
    cyl(p,(0,'column_screw_y','column_bottom_z+30'),'z_screw_d','column_height-50')
    p=part('Saeulendeckel',g,'steel')
    box(p,('-column_x/2-3','column_front_y-3','column_top_z'),('column_x+6','column_y+6','column_cap_h'))
    cyl(p,(0,'column_screw_y','column_top_z-1'),'column_top_bore_d','column_cap_h+2',op='cut',label='Spindeldurchfuehrung')
    p=part('Saeulenverkleidung_silber',g,'silver',note='U-foermige Blechhuelle mit schraegem oberen Ruecken, Foto-Nachbildung',source='S3,S4,S5')
    yz=[('column_front_y+2','base_h+column_seat_h+column_foot_h'),('cover_back_y','base_h+column_seat_h+column_foot_h'),('cover_back_y','cover_shoulder_z'),('cover_top_back_y','column_top_z+column_cap_h'),('column_front_y+2','column_top_z+column_cap_h')]
    prism(p,[('-cover_x/2',y,z) for y,z in yz],'cover_x',(1,0,0))
    yz=[('column_front_y-2','base_h+column_foot_h-1'),('cover_back_y-cover_t','base_h+column_foot_h-1'),('cover_back_y-cover_t','cover_shoulder_z'),('cover_top_back_y-cover_t','column_top_z+column_cap_h-cover_t'),('column_front_y-2','column_top_z+column_cap_h-cover_t')]
    prism(p,[('-cover_x/2+cover_t',y,z) for y,z in yz],'cover_x-2*cover_t',(1,0,0),op='cut',label='Blechhuelle_ANNAHME')
    p=part('Z_Motorflansch',g,'steel')
    box(p,('-z_motor_d/2-8','column_screw_y-z_motor_d/2-8','column_top_z+column_cap_h'),('z_motor_d+16','z_motor_d+16','z_motor_flange_h'))
    p=part('Z_Hubmotor',g,'steel')
    cyl(p,(0,'column_screw_y','column_top_z+column_cap_h+z_motor_flange_h'),'z_motor_d','z_motor_h')
    p=part('Z_Motordeckel',g,'dark')
    cyl(p,(0,'column_screw_y','z_motor_top_z-z_motor_cap_h'),'z_motor_d+1','z_motor_cap_h')
    p=part('Z_Motor_Klemmenkasten',g,'black')
    box(p,('-z_motor_d/2-25','column_screw_y-26','z_motor_top_z-z_motor_h-z_motor_cap_h'),(28,52,48))
    for ix in [-1,1]:
        for iy in [-1,1]:
            p=part('Saeulenfuss_Schraube_%d_%d'%(ix+1,iy+1),g,'steel')
            cyl(p,('%d*column_mount_px/2'%ix,'column_front_y+column_y/2+%d*column_mount_py/2'%iy,'base_h+column_seat_h+column_foot_h'),14,9)
    # KREUZTISCH
    g='02_Kreuztisch'
    p=part('Kreuzschlitten',g,'steel',source='S6')
    box(p,('-saddle_x/2','pos_y-saddle_y/2','saddle_bottom_z-7'),('saddle_x','saddle_y','saddle_h+7'))
    prism(p,[('-guide_spacing/2-0.4','pos_y-saddle_y/2-1','base_h-1'),('guide_spacing/2+0.4','pos_y-saddle_y/2-1','base_h-1'),('guide_spacing/2+8.5','pos_y-saddle_y/2-1','base_h+guide_h+0.4'),('-guide_spacing/2-8.5','pos_y-saddle_y/2-1','base_h+guide_h+0.4')],'saddle_y+2',(0,1,0),op='cut',label='Y_Fuehrungsprofil_ANNAHME')
    prism(p,[('-saddle_x/2+10','pos_y-table_under_w/2+0.5','saddle_bottom_z+saddle_h'),
             ('-saddle_x/2+10','pos_y+table_under_w/2-0.5','saddle_bottom_z+saddle_h'),
             ('-saddle_x/2+10','pos_y+table_under_w/2+table_under_flare-0.5','table_bottom_z+table_under_h-0.5'),
             ('-saddle_x/2+10','pos_y-table_under_w/2-table_under_flare+0.5','table_bottom_z+table_under_h-0.5')],
          'saddle_x-20',(1,0,0),label='X_Gegenfuehrung_NICHT_FOTOGRAFIERT')
    box(p,('-saddle_x/2-1','pos_y-table_channel_w/2','table_bottom_z-4'),
        ('saddle_x+2','table_channel_w','table_channel_h+5'),op='cut',label='Spindelfreiraum_NICHT_VERIFIZIERT')
    p=part('Arbeitstisch_Foto',g,'steel',note='Tischhauptmasse aus Anleitung; Unterseitenprofil, Freistellung, Taschen und Stirnbohrungen nur Foto-Annahmen.',source=PHOTO_TABLE+' / '+P20)
    box(p,('pos_x-table_x/2','pos_y-table_y/2','table_bottom_z'),('table_x','table_y','table_h'))
    for i in [-1,0,1]:
        y='pos_y+%d*slot_pitch'%i
        start='pos_x-table_x/2+table_end_margin+table_end_pocket_x/2'
        length='table_x-2*table_end_margin-table_end_pocket_x'
        box(p,(start,y+'-slot_w/2','table_top_z-slot_top_h'),(length,'slot_w','slot_top_h+1'),op='cut',label='T_Nut_Oeffnung_12')
        box(p,(start,y+'-slot_under_w/2','table_top_z-slot_top_h-slot_under_h'),(length,'slot_under_w','slot_under_h'),op='cut',label='T_Nut_Hinterschnitt_ANNAHME')
    for ix in [-1,1]:
        x='pos_x-table_x/2+table_end_margin' if ix<0 else 'pos_x+table_x/2-table_end_margin-table_end_pocket_x'
        rounded_xy(p,x,'pos_y-table_end_pocket_y/2','table_top_z-table_end_pocket_h','table_end_pocket_x','table_end_pocket_y','table_end_pocket_h+1','table_end_pocket_r',op='cut')
    for iy in [-1,1]:
        box(p,('pos_x-table_x/2+table_end_margin','pos_y+%d*(table_y/2-table_drain_inset)-table_drain_w/2'%iy,'table_top_z-3'),('table_x-2*table_end_margin','table_drain_w',4),op='cut',label='Randnut_ANNAHME')
    prism(p,[('pos_x-table_x/2-1','pos_y-table_under_w/2','table_bottom_z-1'),
             ('pos_x-table_x/2-1','pos_y+table_under_w/2','table_bottom_z-1'),
             ('pos_x-table_x/2-1','pos_y+table_under_w/2+table_under_flare','table_bottom_z+table_under_h'),
             ('pos_x-table_x/2-1','pos_y-table_under_w/2-table_under_flare','table_bottom_z+table_under_h')],
          'table_x+2',(1,0,0),op='cut',label='Unterseiten_Fuehrungsprofil_Foto_ANNAHME')
    box(p,('pos_x-table_x/2-1','pos_y-table_channel_w/2','table_bottom_z-1'),
        ('table_x+2','table_channel_w','table_channel_h+1'),op='cut',label='Mittlere_Freistellung_Foto_ANNAHME')
    for ix in [-1,1]:
        for iy in [-1,1]:
            cyl(p,('pos_x+%d*(table_x/2+1)'%ix,'pos_y+%d*table_end_hole_pitch/2'%iy,'table_bottom_z+table_h/2'),
                'table_end_hole_d','table_end_hole_depth+1',(-ix,0,0),op='cut',label='Stirnbohrung_ANNAHME')
    p=part('X_Lagerbock_rechts',g,'dark')
    box(p,('pos_x+table_x/2','pos_y-36','x_wheel_z-25'),(17,72,50))
    p=part('X_Lagerabschluss_links',g,'dark')
    box(p,('pos_x-table_x/2-8','pos_y-32','x_wheel_z-21'),(8,64,42))
    p=part('X_Welle_aussen',g,'dark')
    cyl(p,('pos_x+table_x/2+17','pos_y','x_wheel_z'),30,'x_wheel_offset-17',(1,0,0))
    p=part('Y_Lagerbock_vorn',g,'dark')
    box(p,(-34,'base_front_y-16','y_wheel_z-24'),(68,18,48))
    p=part('Y_Welle_aussen',g,'dark')
    cyl(p,(0,'base_front_y-16','y_wheel_z'),30,'y_wheel_offset-16',(0,-1,0))
    # Geschlossene Teller, keine Speichen. Alle Handradmasse sind FOTO-ANNAHMEN.
    for ax in ['X','Y']:
        direction=(1,0,0) if ax=='X' else (0,-1,0)
        def at(offset,zoff='0'):
            return ('x_wheel_x+(%s)'%offset,'pos_y','x_wheel_z+(%s)'%zoff) if ax=='X' else (0,'y_wheel_y-(%s)'%offset,'y_wheel_z+(%s)'%zoff)
        p=part(ax+'_Skalenring',g,'red',source='S2,S6')
        cyl(p,at('-24'),'wheel_hub_d+12',21,direction)
        p=part('Handrad_'+ax,g,'red',note='Geschlossenes Tellerhandrad nach S2/S6; Masse und Kegelvertiefung angenaehert',source='S2,S6')
        cyl(p,at('0'),'wheel_d','wheel_h',direction)
        cone(p,at('wheel_h-wheel_dish_depth'),'wheel_dish_inner_d','wheel_d-2*wheel_rim','wheel_dish_depth+1',direction,op='cut',label='Tellervertiefung_ANNAHME')
        cyl(p,at('0'),'wheel_hub_d','wheel_h',direction)
        cyl(p,at('-1'),'wheel_shaft_d','wheel_h+2',direction,op='cut')
        p=part('Handradgriff_'+ax,g,'steel')
        cyl(p,at('wheel_h-1','-wheel_d/2+wheel_rim+2'),'wheel_grip_d','wheel_grip_h+1',direction)
        p=part('Handradmutter_'+ax,g,'steel')
        cyl(p,at('wheel_h'),24,8,direction)
        cyl(p,at('wheel_h-1'),10,10,direction,op='cut')
    for x in [-65,82]:
        p=part('Klemmhebel_Tisch_'+str(x).replace('-','M'),g,'black')
        cyl(p,(x,'pos_y-saddle_y/2-2','saddle_bottom_z+saddle_h/2'),13,15,(0,-1,0))
        cyl(p,(x,'pos_y-saddle_y/2-12','saddle_bottom_z+saddle_h/2'),8,48,(-0.87,0,-0.493))
    p=part('X_Massstab_Gehaeuse_Foto',g,'silver',note='Am realen Tisch sichtbar; Typ, Laenge, Schnittstelle und Lage nicht vermessen.',source=PHOTO_TABLE)
    box(p,('pos_x-table_x/2+scale_end_margin','pos_y-table_y/2-scale_depth','table_bottom_z+3'),
        ('table_x-2*scale_end_margin','scale_depth','scale_h'),label='X_Massstabhuelle_ANNAHME')
    box(p,('pos_x-table_x/2+scale_end_margin+3','pos_y-table_y/2-scale_depth-0.2','table_bottom_z+7'),
        ('table_x-2*scale_end_margin-6','scale_depth-2','scale_h-8'),op='cut',label='Massstab_Laengsschlitz')
    p=part('X_Massstab_Dichtlippe',g,'black',note='Reine Sichtdarstellung, kein spezifizierter Messgeber',source=PHOTO_TABLE)
    box(p,('pos_x-table_x/2+scale_end_margin+3','pos_y-table_y/2-scale_depth+1','table_bottom_z+8'),
        ('table_x-2*scale_end_margin-6',1,'scale_h-10'))
    p=part('X_Massstab_Lesekopf_Foto',g,'steel',note='Lesekopf fest am angenommenen Sattel; Gehaeuse bewegt sich mit X. KEINE Encoder-Spezifikation.',source=PHOTO_TABLE)
    box(p,('scale_reader_x-scale_reader_l/2','pos_y-table_y/2-scale_depth-7','table_bottom_z+6'),
        ('scale_reader_l',6,'scale_h-4'))
    p=part('X_Massstab_Lesekopfhalter_ANNAHME',g,'dark',note='Halter als Platzhalter: Anschraublage nicht fotografisch belegt',source=PHOTO_TABLE)
    box(p,('scale_reader_x-16','pos_y-table_y/2-scale_depth-7','table_bottom_z-8'),(32,6,14))
    box(p,('scale_reader_x-16','pos_y-table_y/2-scale_depth-7','table_bottom_z-9'),(32,'scale_depth+15',2))
    p=part('Saeule_Seitenplakette_Foto','06_Details','panel',note='Seitliches helles Rechteck sichtbar; Funktion/Abmessungen nicht belegt.',source=PHOTO_COL)
    box(p,('-column_x/2-0.6','column_front_y+30','column_seat_z+column_length*0.56'),(0.6,50,100))
    # BOHR-/FRAESKOPF
    g='03_Kopf'
    p=part('Bohr_Fraeskopf',g,'cast',source='S2,S3,S5')
    rounded_xy(p,'-head_x/2','-head_front','head_bottom_z','head_x','head_depth','head_h','head_corner_r')
    cyl(p,(0,0,'head_bottom_z-1'),'quill_d+0.6','head_h+2',op='cut',label='Pinolenbohrung_ANNAHME')
    p=part('Riemengehaeuse',g,'cast',source='S3,S5')
    rounded_xy(p,'-head_x/2-belt_cover_extra/2','-head_front-belt_cover_extra/2','head_top_z+0.5','head_x+belt_cover_extra','head_depth+belt_cover_extra/2','belt_cover_h','head_corner_r')
    p=part('Kopf_Frontplatte',g,'cast',source='S2,S5')
    box(p,('-head_x/2+1','head_face_y','head_bottom_z+2'),('head_x-2','frontplate_t','head_h+belt_cover_h-1.5'))
    p=part('Anzugspindel_Abdeckung',g,'steel',source='S5')
    cyl(p,(0,0,'head_top_z+belt_cover_h+0.5'),'drawbar_cap_d+10',4)
    cyl(p,(0,0,'head_top_z+belt_cover_h+4.5'),'drawbar_cap_d','drawbar_cap_h-4')
    p=part('Riemendeckel_Schraubknopf',g,'black',source='S5')
    cyl(p,(0,95,'head_top_z+belt_cover_h+0.5'),18,26)
    p=part('Pinole',g,'steel')
    cyl(p,(0,0,'spindle_face_z+spindle_nose_h'),'quill_d','quill_body_h')
    cyl(p,(0,0,'spindle_face_z+spindle_nose_h-1'),'quill_bore_d','quill_body_h+2',op='cut')
    p=part('Spindelnase_SK30_Normreferenz',g,'steel',note='Konus d1=31.75 und 7:24 nach S8. Tiefe, Stirnbezug, Aussenkontur, Mitnehmer nicht an Maschine gemessen; KEIN Fertigungsmodell.',source='S1,S8')
    cyl(p,(0,0,'spindle_face_z'),'spindle_nose_d','spindle_nose_h')
    cyl(p,(0,0,'spindle_face_z+spindle_nose_h'),'spindle_shaft_d','quill_body_h')
    cone(p,(0,0,'spindle_face_z-0.1'),'sk_gauge_d+0.1*7/24','sk_small_d','sk_taper_length+0.1',op='cut',label='SK30_Konus_7zu24')
    cyl(p,(0,0,'spindle_face_z+sk_taper_length-0.1'),'sk_small_d','quill_body_h+spindle_nose_h-sk_taper_length+1',op='cut',label='Fortsetzung_ANNAHME')
    p=part('Kopf_Typenschild',g,'panel',source='S2,S5')
    box(p,('-head_x/2+32','head_face_y-0.6','head_bottom_z+122'),('head_x-64',0.6,108))
    # BEDIENUNG
    g='04_Bedienung'
    p=part('Panelhalter',g,'dark')
    cyl(p,('panel_left_x+panel_x',-6,'panel_bottom_z+panel_h/2'),23,'panel_gap',(1,0,0))
    p=part('Bediengehaeuse',g,'cast',source='S4')
    box(p,('panel_left_x','-head_front','panel_bottom_z'),('panel_x','panel_y','panel_h'))
    p=part('Bedienfront',g,'panel',source='S2,S4')
    box(p,('panel_left_x','-head_front-3','panel_bottom_z'),('panel_x',3,'panel_h'))
    p=part('Drehzahlanzeige_Rahmen',g,'black')
    box(p,('panel_left_x+24','-head_front-4','panel_bottom_z+panel_h-37'),('panel_x-48',1,24))
    p=part('Drehzahlanzeige_LCD',g,'lcd')
    box(p,('panel_left_x+26','-head_front-4.3','panel_bottom_z+panel_h-35'),('panel_x-52',0.3,20))
    p=part('Drehzahlregler',g,'steel')
    cyl(p,('panel_left_x+panel_x/2','-head_front-3','panel_bottom_z+panel_h-76'),44,16,(0,-1,0))
    p=part('Not_Halt_Kragen',g,'yellow')
    cyl(p,('panel_left_x+38','-head_front-3','panel_bottom_z+34'),46,5,(0,-1,0))
    p=part('Not_Halt',g,'red')
    cyl(p,('panel_left_x+38','-head_front-8','panel_bottom_z+34'),35,23,(0,-1,0))
    for label,z,mat in [('Start_Stop',28,'steel'),('Gewindeschneiden',58,'steel')]:
        p=part(label,g,mat)
        cyl(p,('panel_left_x+panel_x-24','-head_front-3','panel_bottom_z+'+str(z)),18,9,(0,-1,0))
    p=part('Z_Taster_Seitenplatte',g,'panel',source='S4')
    box(p,('panel_left_x-1','-head_front+18','panel_bottom_z+24'),(1,43,120))
    for i in [0,1]:
        p=part('Z_Taster_'+('Ab' if i==0 else 'Auf'),g,'steel',source='S4')
        cyl(p,('panel_left_x-1','-head_front+39','panel_bottom_z+48+%d*65'%i),23,5,(-1,0,0))
    p=part('Digitale_Bohrtiefenanzeige',g,'black',source='S2,S5')
    box(p,(-26,'head_face_y-2','head_bottom_z+6'),(44,2,72))
    p=part('Pinolenanzeige_LCD',g,'panel')
    box(p,(-20,'head_face_y-2.4','head_bottom_z+44'),(32,0.4,15))
    for i in range(3):
        p=part('Pinolenanzeige_Taste_%d'%i,g,'red' if i==0 else 'panel')
        cyl(p,(-12,'head_face_y-2.4','head_bottom_z+15+%d*9'%i),4,0.7,(0,-1,0))
    p=part('Feinvorschub_Pinole',g,'steel',source='S2,S5')
    cyl(p,('head_x/2-32','head_face_y','head_bottom_z+62'),43,18,(0,-1,0))
    p=part('Sternhebel_Welle',g,'steel')
    cyl(p,('head_x/2','star_y','star_z'),28,16,(1,0,0))
    p=part('Sternhebel_Nabe',g,'steel',source='S5')
    cyl(p,('star_x','star_y','star_z'),60,14,(1,0,0))
    cyl(p,('star_x+14','star_y','star_z'),'star_hub_d','star_hub_h',(1,0,0))
    for i,angle in enumerate([12,132,252]):
        a=math.radians(angle);dy=math.sin(a);dz=math.cos(a);d=(0,dy,dz)
        p=part('Sternhebel_Stange_%d'%(i+1),g,'steel')
        cyl(p,('star_x+22','star_y','star_z'),'star_bar_d','star_radius',d)
        p=part('Sternhebel_Griff_%d'%(i+1),g,'black')
        cone(p,('star_x+22','star_y+%.12g*star_radius'%dy,'star_z+%.12g*star_radius'%dz),'star_grip_d-3','star_grip_d','star_grip_h',d)
        p=part('Sternhebel_Umschalttaster_%d'%(i+1),g,'green')
        cyl(p,('star_x+22','star_y+%.12g*(star_radius+star_grip_h)'%dy,'star_z+%.12g*(star_radius+star_grip_h)'%dz),'star_grip_d-7',3,d)
    p=part('Sternhebel_Kupplung',g,'steel')
    cyl(p,('star_x+star_hub_h+14','star_y','star_z'),30,10,(1,0,0))
    for i,angle in enumerate([45,165,285]):
        dy=math.sin(math.radians(angle));dz=math.cos(math.radians(angle))
        p=part('Kupplung_Kurzhebel_%d'%i,g,'steel')
        cyl(p,('star_x+star_hub_h+19','star_y','star_z'),8,53,(0,dy,dz))
    p=part('Lampenhalter',g,'steel',source='S4')
    box(p,('-head_x/2-4',25,'head_bottom_z+42'),(4,45,43))
    cyl(p,('-head_x/2-4',47,'head_bottom_z+60'),16,80,(-0.707,0,-0.707))
    p=part('Arbeitslampe',g,'black',source='S4')
    cyl(p,('-head_x/2-61',47,'head_bottom_z-32'),62,35)
    p=part('Arbeitslampe_Linse',g,'panel')
    cyl(p,('-head_x/2-61',47,'head_bottom_z-33'),53,1)
    # SCHUTZ UND FALTENBALGE
    g='05_Schutz'
    def u_profile(w,front,back,corner,thickness,z):
        # U mit gefasten Frontkanten, Rueckseite offen; ein geschlossener Polygonzug.
        w=str(w);f=str(front);b=str(back);c=str(corner);t=str(thickness)
        pts=[('-(%s)/2'%w,b),('-(%s)/2'%w,'(%s)+(%s)'%(f,c)),('-(%s)/2+(%s)'%(w,c),f),('(%s)/2-(%s)'%(w,c),f),('(%s)/2'%w,'(%s)+(%s)'%(f,c)),('(%s)/2'%w,b),('(%s)/2-(%s)'%(w,t),b),('(%s)/2-(%s)'%(w,t),'(%s)+(%s)'%(f,c)),('(%s)/2-(%s)'%(w,c),'(%s)+(%s)'%(f,t)),('-(%s)/2+(%s)'%(w,c),'(%s)+(%s)'%(f,t)),('-(%s)/2+(%s)'%(w,t),'(%s)+(%s)'%(f,c)),('-(%s)/2+(%s)'%(w,t),b)]
        return [(x,y,z) for x,y in pts]
    p=part('Spindelschutz_oben',g,'glass',note='Mehrteilige transparente U-Huelle mit gefasten Frontkanten. Masse angenaehert; keine Schutzfunktionspruefung.',source='S3,S4,S5,S6')
    prism(p,u_profile('shield_w','-head_front-26','-head_front-26+shield_y','shield_corner','shield_t','head_bottom_z-shield_h'),'shield_h',(0,0,1))
    p=part('Spindelschutz_unten',g,'glass',note='Teleskopisches Unterteil, Auszug sx_shield_extension; angenaehert.',source='S3,S4')
    prism(p,u_profile('shield_w-2*shield_t-1','-head_front-26+shield_t+0.5','-head_front-26+shield_y-2','shield_corner','shield_t','head_bottom_z-shield_h-shield_extension'),'shield_lower_h',(0,0,1))
    p=part('Schutz_Halter',g,'steel')
    cyl(p,('-shield_w/2-9','-head_front+20','head_bottom_z-shield_h+4'),8,'shield_h+4')
    cyl(p,('-shield_w/2-9','-head_front+20','head_bottom_z+5'),8,21,(1,0,0))
    for ix in [-1,1]:
        p=part('Schutz_Klemmschraube_'+str(ix),g,'black')
        cyl(p,('%d*(shield_w/2-18)'%ix,'-head_front-28','head_bottom_z-shield_h+28'),15,9,(0,-1,0))
    p=part('Faltenbalg_Z',g,'black',note='Parametrischer gefalteter Querschnitt, 18 Falten; keine gemessene Balggeometrie',source='S3,S4,S5')
    yz=[]
    for i in range(37):
        y='column_front_y-10' if i%2==0 else 'column_front_y-10-bellows_depth'
        yz.append((y,'bellows_bottom_z+%d*bellows_height/36'%i))
    pts=[('-bellows_w/2',y,z) for y,z in yz]+[('-bellows_w/2','(%s)+bellows_sheet_t'%y,z) for y,z in reversed(yz)]
    prism(p,pts,'bellows_w',(1,0,0))
    p=part('Faltenbalg_Y_hinten',g,'black',note='Parametrische gefaltete Huelle, 12 Falten, Laenge folgt Y-Stellung',source='S6')
    yz=[]
    for i in range(25):
        y='pos_y+table_y/2+%d*(column_front_y-pos_y-table_y/2)/24'%i
        z='table_top_z-7' if i%2==0 else 'table_top_z+4'
        yz.append((y,z))
    pts=[('-bellows_w/2',y,z) for y,z in yz]+[('-bellows_w/2',y,'(%s)-bellows_sheet_t'%z) for y,z in reversed(yz)]
    prism(p,pts,'bellows_w',(1,0,0))
    # DETAILTEILE; aus Fotos in ihrer Existenz belegt, nicht in den Massen.
    g='06_Details'
    p=part('Magnetpad_rechts',g,'black',source='S1,S3,S5')
    box(p,('cover_x/2+0.2','column_front_y+22','column_bottom_z+185'),(1.5,'magnetpad_y','magnetpad_h'))
    p=part('Magnetpad_T_Symbol',g,'panel',note='Stilisiertes Orientierungssymbol, kein Labelmass',source='S3,S5')
    box(p,('cover_x/2+1.7','column_front_y+30','column_bottom_z+185+magnetpad_h-15'),(0.3,'magnetpad_y-16',5))
    box(p,('cover_x/2+1.7','column_front_y+22+magnetpad_y/2-2.5','column_bottom_z+208'),(0.3,5,'magnetpad_h-33'))
    for label,z in [('unten','column_bottom_z+180'),('oben','column_top_z-180')]:
        p=part('Z_Endschalter_'+label,g,'black',source='S4')
        box(p,('-cover_x/2-12','column_front_y+33',z),(12,34,22))
        p=part('Z_Endschalter_Rolle_'+label,g,'steel',source='S4')
        cyl(p,('-cover_x/2-6','column_front_y+28','(%s)+11'%z),6,8,(0,1,0))
    for ix in [-1,1]:
        for zh in [12,122,264]:
            p=part('Frontplatten_Schraube_%d_%d'%(ix+1,zh),g,'black')
            cyl(p,('%d*(head_x/2-8)'%ix,'head_face_y', 'head_bottom_z+%d'%zh),5.5,1.7,(0,-1,0))
    return parts


def check_recipe(p, parts=None):
    validate(p)
    v=all_values(p)
    for definition in parts or recipe():
        for op in definition['ops']:
            for c in op['origin']: evaluate(c,v)
            if op['kind']=='box': sizes=op['size']
            elif op['kind']=='prism':
                sizes=[op['height']]
                if len(op['points'])<3: raise ValueError('Polygon hat zu wenige Punkte')
                for pt in op['points']:
                    for c in pt: evaluate(c,v)
            else:
                sizes=[op['diameter'],op['height']]
                if op['kind']=='cone': sizes.append(op['top_diameter'])
            if any(evaluate(s,v)<=0 for s in sizes):
                raise ValueError('Nicht positive Featuregroesse in '+definition['name'])
    return v
