# -*- coding: utf-8 -*-
"""Create the editable engineering handbook from the same revision08 data as CAD/BOM.
Requires python-docx and Pillow, outside NX only. PDF rendering is a separate QA step.
"""
from pathlib import Path
import json, sys
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model, umbau_daten08 as ud
params=model.load_parameters(ROOT/'Parameter.json');values=model.all_values(params);defs=model.recipe()
cat=ud.catalog(ROOT)['items'];sources=json.loads((ROOT/'Quellen/Quellen_08.json').read_text())['sources']
measures=json.loads((ROOT/'Aufmass/Messwerte_08.json').read_text())['measurements']
gates=json.loads((ROOT/'Pruefung_08/Freigaben.json').read_text())['gates']
lengths=model.length_report(params)
doc=Document();sec=doc.sections[0]
sec.page_width=Mm(210);sec.page_height=Mm(297)
sec.top_margin=Mm(18);sec.bottom_margin=Mm(17);sec.left_margin=Mm(19);sec.right_margin=Mm(19)
sec.header_distance=Mm(8);sec.footer_distance=Mm(8)
styles=doc.styles
for name in ('Normal','Body Text'):
 styles[name].font.name='Calibri';styles[name].font.size=Pt(10.5)
 styles[name].paragraph_format.space_after=Pt(6);styles[name].paragraph_format.line_spacing=1.08
for n,size in [('Title',27),('Heading 1',20),('Heading 2',13),('Heading 3',11)]:
 styles[n].font.name='Calibri';styles[n].font.size=Pt(size);styles[n].font.color.rgb=RGBColor.from_string('173A4D')
 styles[n].paragraph_format.space_before=Pt(10);styles[n].paragraph_format.space_after=Pt(6)
 styles[n].paragraph_format.keep_with_next=True
styles['Caption'].font.size=Pt(8.5);styles['Caption'].font.color.rgb=RGBColor.from_string('536675')
header=sec.header.paragraphs[0];header.text='SX3.5Z  /  CNC-UMBAU                                      TECHNISCHER ARBEITSSTAND 08'
header.style=styles['Caption']
foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=foot.add_run('30.10.2026  ·  Anfrage-/Planungsstand  ·  ');r.font.size=Pt(8)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
doc.core_properties.title='SX3.5Z – Beschaffung, Bearbeitung und Montagevorbereitung 08'
doc.core_properties.subject='Gemeinsamer Datenstand für NX-Journal, Stückliste und Bauablauf; keine Freigabe'
doc.core_properties.author='CNC-Umbauprojekt'

def p(text='',bold=False,style=None):
 a=doc.add_paragraph(style=style);r=a.add_run(text);r.bold=bold;return a

def h(text,level=2):return doc.add_heading(text,level)

def page(num,title,subtitle=''):
 doc.add_page_break();p('UMSETZUNG 08  /  '+str(num).zfill(2),style='Caption');h(title,1)
 if subtitle:p(subtitle)

def note(text):
 t=doc.add_table(rows=1,cols=1);t.cell(0,0).text=text
 tcPr=t.cell(0,0)._tc.get_or_add_tcPr();sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'FFF0D6');tcPr.append(sh)
 for a in t.cell(0,0).paragraphs:
  a.paragraph_format.space_after=Pt(5);a.paragraph_format.space_before=Pt(5)
  for r in a.runs:r.font.size=Pt(10);r.bold=True
 p('')

def table(headers,rows,widths=None,size=9.3):
 t=doc.add_table(rows=1,cols=len(headers));t.autofit=False;t.style='Light Shading Accent 1'
 for i,x in enumerate(headers):t.rows[0].cells[i].text=str(x)
 for row in rows:
  for c,x in zip(t.add_row().cells,row):c.text='' if x is None else str(x)
 for ir,row in enumerate(t.rows):
  trPr=row._tr.get_or_add_trPr();no=OxmlElement('w:cantSplit');trPr.append(no)
  if ir==0:
   repeat=OxmlElement('w:tblHeader');trPr.append(repeat)
  for i,c in enumerate(row.cells):
   if widths:c.width=Mm(widths[i])
   if ir==0:
    sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'173A4D');c._tc.get_or_add_tcPr().append(sh)
   for a in c.paragraphs:
    a.paragraph_format.space_after=Pt(3);a.paragraph_format.space_before=Pt(3);a.paragraph_format.line_spacing=1.02
    for r in a.runs:
     r.font.size=Pt(size)
     if ir==0:r.font.color.rgb=RGBColor(255,255,255);r.bold=True
 return t

def image(file,width=171,caption=''):
 fp=ROOT/'Vorschau'/file
 if fp.exists():doc.add_picture(str(fp),width=Mm(width))
 if caption:p(caption,style='Caption')

p('SX3.5Z  ·  CNC-UMBAU',style='Subtitle')
doc.add_heading('Beschaffung und\nMontagevorbereitung',0)
p('Umsetzungsstand 08  |  30. Oktober 2026',bold=True)
p('Kaufteilbezogene Antriebe · parametrisierte Adapter · Originalteilprüfung · Bauablauf')
image('Gesamtansicht_offen.png',171,'Modellvorformen des Standes 08. Keine fertig montierte oder abgenommene reale Maschine.')
note('KEINE BESTELL- ODER BAUFREIGABE. Dieses Handbuch ist ein konkreter Arbeits- und Anfrageplan. Unbestätigte Maschinenanschlüsse, Spindelenden, Z-Motorrevision und Sicherheitsfunktionen dürfen nicht durch Annahmen ersetzt werden.')
p('435 modellierte Einzelkörper sind mit einer Beschaffungs-/Fertigungszuordnung verbunden. Die Liste umfasst 24 Herstellerpositionen bzw. Konfigurationen, 6 Normteilpositionen und 18 noch offene Beschaffungspakete. 29 Istaufmaße sind noch leer.')
p('Ein erfolgreicher vollständiger NX-Lauf dieses neuen Standes liegt hier nicht vor. Die bisherigen Fehlertests und unabhängigen Geometrieprüfungen sind getrennt vom praktischen Maschinen-Nachweis zu lesen.')

page(1,'Was dieser Stand verbindlich beschreibt')
table(['Bereich','Festgelegter Arbeitsansatz','Noch zu bestätigen'],[
 ('Grundmaschine','Vorhandene Foto-Rekonstruktion und Komponenten bleiben Grundlage. Originalguss wird nicht automatisch geändert.','Istmaße, Wandstärken, Gewinde und Führungsüberdeckung.'),
 ('Vorschub','X/Y: Closed-Loop-Schrittmotoren. Z: Bremsmotor aus derselben Motorfamilie. Direkte Kupplungen.','Dynamische Lastrechnung und konkrete Z-Lieferrevision.'),
 ('Führungen','Vorhandene Gleit-/Schwalbenschwanzführungen erhalten; einstellen und schmieren.','Zustand, Reibkräfte, Umkehrspiel und Lauf über den nutzbaren Hub.'),
 ('Spindelantrieb','W92-1000F mit vorhandener Originalelektronik zunächst erhalten.','CNC-Steuerschnittstelle und sichere Abschaltung.'),
 ('Einhausung','Breite Senktür, angelegter Schaltschrank und hinterer Spänerücklauf unverändert.','Türmechanik, Fangsicherung, Scheiben, Dichtheit und Statik.')],[28,77,67])
h('Dateien gehören zusammen')
p('Die Arbeitsmappe Einkauf_und_Aufmass_08.xlsx ist das lesbare Register. Einkauf/Kaufteile_08.json ist die Kaufteildatenbasis des Journals. Jede Modellkomponente besitzt eine Positionskennung; mehrere Hüllkörper eines Motors zählen nur als ein Motor. Modellzuordnung_08.csv bildet alle Körper ab.')
p('Herstellermaße werden nicht frei durch Maßänderungen ersetzt. Eine abweichende Lieferrevision braucht ein neues Maßblatt und einen aktualisierten Datenbankeintrag. In der Tabelle bedeutet ein leeres Istmaß „unbekannt“, nicht 0 mm.')
h('Drei Bearbeitungsarten unterscheiden')
p('KAUFTEIL: unverändert beschaffen, sofern Ausführung freigegeben. FERTIGUNGSTEIL: nach eigener vollständiger Zeichnung anfertigen. ORIGINALTEIL: nur nach tatsächlichem Aufmaß und belastbarer Freigabe ändern. Ein roter Gusskörper im Modell ist keine erlaubte Fräsvorlage.')

page(2,'Ausgewählte mechanische Kaufteile','Artikel- und Größenbezeichnungen aus Herstellerunterlagen; Lieferbarkeit und aktuelle Ausführung sind anzufragen.')
ids=['K-MOT-XY','K-MOT-Z','K-FK12','K-FK15','K-FF12','K-FF15','K-KUP-XY','K-KUP-Z','K-NUT16','K-NUT20','K-NUTH16','K-NUTH20']
table(['Pos.','Menge','Hersteller / Ausführung','Einsatz'],[(i,cat[i]['planned_quantity'],cat[i]['manufacturer']+' / '+cat[i]['article'],cat[i]['description']) for i in ids],[24,14,80,54],8.7)
p('Quellen: Motoren [S01,S02,S04], Lager [S05,S06], Kupplungen [S07], Muttern und Spannblöcke [S08,S09]. Originalhersteller-CAD wurde nicht beschafft; die Maßhüllen sind gekennzeichnete Ersatzmodelle.')
h('Keine frei austauschbaren Baureihen')
p('Die isel-Muttern müssen zum isel-Spindelprofil und zur Steigung passen. Eine beliebige „1605“-Spindel ist kein zugesichertes Gegenstück. Die KTR-Kupplung benötigt Größen-, Naben-, Elastomer- und Bohrungsangabe; die Familienbezeichnung allein reicht nicht zur Bestellung.')
p('THK FK/FF werden als komplette Stützeinheiten angefragt. Die im FK-Set enthaltenen Lager, Dichtungen und Sicherungsmutter werden nicht nochmals als zusätzliche Einzelkaufteile gezählt. Lieferumfang bestätigen. [S05,S06]')

page(3,'Montagekette der Achsen')
image('Antriebe.png',171,'Tatsächliche Rezeptgeometrie der drei Antriebe, ohne verdeckende Maschinenkörper. Blaue Teile sind Eigenentwürfe.')
h('Antriebsseite')
p('Maschinenguss → maschinenspezifische Anschlussfläche → neue Adapterplatte → FK-Zentriersitz und vier eigene Lagerschrauben. Von derselben Adapterplatte gehen vier Distanzsäulen zur Motorplatte. Vier zusätzliche Schrauben befestigen den Motorflansch. Keine der Schraubenreihen ersetzt die andere.')
h('Kraft- und Momentenweg')
p('Motorwelle → KTR-Kupplung → Spindel → Kugelmutter und ihr Spannblock → bewegtes Maschinenteil. Axialkraft aus der Spindel geht über Festlager und Adapter zurück in den Guss. Die Kupplung ist kein Axiallager. Das gegenüberliegende FF-Lager wird mit einer eigenen, noch maschinenspezifisch zu schließenden Brücke abgestützt.')
note('Die gussseitigen Lochbilder der neuen Adapter sind absichtlich noch nicht eingearbeitet. Die katalogseitige Verbindung ist konkreter; die vollständige tragende Verbindung zur realen Maschine ist damit noch nicht fertig.')
p('Für Z ist die Gusssäule der Lastpfad. Das Deckblech der Elektrik darf den Fräskopf nicht tragen. Die vorhandene Tragbrücke bleibt bis zum Aufmaß eine Anschlussstudie. Die Pinole muss eingefahren definiert geklemmt sein; das Entfernen des Handhebels allein hält sie nicht fest.')

page(4,'Adapter, Schrauben und Anschlussmaße','Alle Zahlen in mm. Eigenmaße sind Entwurf; katalogseitige Maße sind in [S01,S05,S06,S07] belegt bzw. bei Z als Familienmaß markiert.')
table(['Merkmal','X / Y','Z'],[
 ('Adapter-Grundkörper','84 × 84 × 17','108 × 108 × 17'),
 ('FK-Zentrieraufnahme, Nennmaß','Ø36; Passung H7 vorgesehen','Ø40; Passung H7 vorgesehen'),
 ('FK-Lochkreis / Gewinde','PCD44; 4×M4','PCD50; 4×M5'),
 ('Motorplatte','84 × 84 × 10','108 × 108 × 10'),
 ('Motorbund-Freibohrung','Ø38,3','Ø60,2; B-Lieferzeichnung bestätigen'),
 ('Motor-Schraubenbild','47,14 × 47,14; 4×M4','69,6 × 69,6; 4×M5; Revision offen'),
 ('Distanzsäule, Fertighülle','Ø12 / Ø6,6 innen; Länge57','Ø12 / Ø6,6 innen; Länge98'),
 ('Motorflanschlage zum Adapterbezug','84','125'),
 ('Gegenlageradapter','76 × 70 × 8; Ø34; PCD42/M4','76 × 70 × 8; Ø40; PCD50/M5')],[80,46,46],9)
p('Der Abstand der Distanzsäulen ist dem zugehörigen sx_-Parameter und dem Modell zu entnehmen. Die Kernlöcher stellen noch kein modelliertes Gewinde dar. Vor Fertigung fehlen insbesondere Bezugssystem, Lagetoleranzen, endgültige Passungs-/Gewindeangaben, Materialzustand und maschinenseitige Anschlüsse.')
table(['Normposition','Menge','Aufgabe'],[(i,cat[i]['planned_quantity'],cat[i]['article']) for i in cat if i.startswith('N-')],[37,18,117],9)
p('Die genannten Schraubenlängen sind aus der Entwurfsmaßkette abgeleitet, nicht als Festigkeitsnachweis freigegeben. Anzugsmomente werden nicht geraten: Werkstoff, Einschraublänge, Schmierung und Herstellerangaben müssen zur Verbindung passen. Zugangsfreistellungen im Motorersatzmodell sind keine Anweisung, den Kaufmotor zu bearbeiten.')

page(5,'Spindelsätze: Anfrage statt falscher Bestelllänge')
table(['Achse','Durchmesser / Steigung','Gewindekernhülle','Gesamthülle','Zielhub'],[(r['axis'],f"{r['nominal_diameter_mm']:g} × {r['lead_mm']:g}",f"{r['envelope_core_length_mm']:g}",f"{r['total_envelope_length_mm']:g}",{'X':'500','Y':'200','Z':'240'}[r['axis']]) for r in lengths],[18,48,36,34,36],9.5)
note('763/335/484 mm Gewindekern und 853/425/595 mm Gesamthülle sind aktuelle CAD-Raumwerte. KEINE BESTELL- ODER FERTIGLÄNGEN. Die alten BF20-Rohteilangaben sind ebenfalls kein Ersatz für SX3.5Z-Istmaße.')
h('Bestellzeichnung muss mindestens enthalten')
p('Gesamtlänge; tatsächlich befahrbare Gewindelänge; Muttertyp, Montageorientierung und nutzbare Positionen; Lage beider Lagerbezüge; Durchmesser, Länge und Passung jedes Lagersitzes; Schulterradius; Sicherungsmuttergewinde; Sicherungsringnut; Kupplungszapfen; Freistiche; Geradheit, Rundlauf und geforderte Spiel-/Genauigkeitsklasse.')
table(['Schnittstelle','X / Y','Z'],[
 ('THK Festlager-Wellendurchmesser','12','15'),
 ('THK Loslager-Wellendurchmesser','10','15 – nicht die alten12'),
 ('Kupplung: Spindel-/Motorbohrung','10 / 8','12 / 14'),
 ('Geplanter Abstand der Wellenenden','3','5'),
 ('Kleinste axiale Modellreserve','X20; Y25','23,25')],[78,47,47])
p('Die Schulter- und Zapfenlängen im Ersatzmodell dienen nur der räumlichen Darstellung. Die Zeichnung des konkreten THK-Montageverfahrens und die isel-Endenbearbeitung müssen gemeinsam freigegeben werden. Ein nominal passender Durchmesser allein sichert keine axial richtige Lagerklemmung. [S05,S06,S08,S19,S20]')
h('Reihenfolge für eine verwertbare Anfrage')
p('Zuerst X05/Y05/Z05 und nutzbare Endlagen messen. Dann die Lage von Mutter und Halter in der Maschine festlegen. Danach den Anbieter den kompletten Satz mit Endenzeichnung anbieten lassen. Erst bei abgestimmter Zeichnung und Lastrechnung werden K-SCREW-X/Y/Z bestellt; die Muttern gegebenenfalls montiert liefern lassen.')

page(6,'Müssen die Originalteile gefräst werden?','Antwort: Neue Adapter brauchen Bearbeitung. Eine CNC-Nacharbeit der Originalgusskörper ist dagegen noch nicht pauschal nachgewiesen.')
table(['Originalteil','Befund im aktuellen Modell','Praktische Entscheidung'],[
 ('Tischunterseite / X-Mutterraum','Mutterblock überschneidet Tisch und Sattel. Die Foto-Rekonstruktion enthält angenommene Freiräume.','Zuerst X01/X04/X07 messen. Kompaktere Aufnahme oder andere Einbaulage prüfen; erst danach gegebenenfalls Tasche.'),
 ('Kreuzschlitten / Sattel','X-Mutterblock und X-Spindelhülle haben lokale Überschneidungen.','Auflage, Nut und Wanddicke messen. Planfläche, Aufnahme oder Gewinde können erforderlich werden; Führungsflächen nicht pauschal abfräsen.'),
 ('Basis, Y-Durchführung','Y-Spindelhülle schneidet die modellierte Basis geringfügig.','Y01/Y04/Y07 prüfen. Durchbruch nur nach realer Vermessung und Wandprüfung erweitern; sonst Adapterlage ändern.'),
 ('Säulenkopf','Z-Adapter und Wellenhülle kollidieren mit dem angenommenen Deckelbereich.','Last in Gusssäule führen. Gussaufnahme nur bearbeiten, wenn vorhandene Auflagen/Gewinde nicht ausreichen.')],[35,68,69],9.2)
h('Was die sechs Überschneidungen aussagen')
p('Sie sind ein Nachweis, dass der aktuelle Entwurf noch nicht montagefertig ist. Sie beweisen nicht, dass der reale Guss exakt dort Material enthält, und sie liefern keine zulässige Abtragstiefe. Der unabhängige Test prüfte ausgewählte Paare, nicht jede mögliche Kollision der vollständigen Maschine.')
h('Schonende Priorität')
p('1. Vorhandene Anschlüsse verwenden. 2. Eigenteile ändern, bevor Originalteile geändert werden. 3. Nur erforderliche Funktionsflächen bearbeiten. 4. Gussbearbeitung erst nach Zeichnung, Wandstärkennachweis und Aufspannplan. Anguss-, Rippen- und Schmierkanalbereiche beachten.')
note('Eine allgemeine Zusage „kein Fräsen nötig“ wäre derzeit genauso unbelegt wie eine fertige CNC-Fräsanweisung. CNC ist für reproduzierbare Bearbeitung sinnvoll, aber geeignete konventionelle Maschinen können die nötigen Flächen und Bohrungen ebenfalls herstellen.')

page(7,'Bearbeitungsplan und Fertigungsvergaben')
table(['Bauteil / Paket','Vorgesehener Prozess','Freigabebedingung'],[
 ('Spindelkopf und Pinole','Manuelle Betätigung ausbauen; Anschluss abdecken; vorhandene definierte Pinolenklemmung erhalten.','Z-Mutterbefestigung, Klemmfunktion und Tragfähigkeit prüfen. Keine neue Pinolenbohrung vorgesehen.'),
 ('Elektrik-Säulendeckel','Durchführung/Deckel neu als Blechteil ausführen.','Z-Anschluss und Kantenabstände festlegen. Lasern/Bohren/Kanten; keine zwingende CNC-Fräsbearbeitung.'),
 ('Motor- und Lageradapter','Rohmaterial zuschneiden, planfräsen, Pilotbohrungen ausarbeiten, Lochbilder bohren, Gewinde fertigen.','Vollständige Bezugs-/Passungszeichnung und Originalanschlüsse fehlen noch.'),
 ('Distanzsäulen','Drehen, beide Stirnflächen parallel planen, Durchgang bohren und entgraten.','Gemeinsame Länge innerhalb einer Achse, Material und tolerierte Parallelität festlegen.'),
 ('Kugelgewindespindelenden','Durch Anbieter präzisionsdrehen bzw. schleifen lassen; anschließend prüfen.','Freigegebene Endenzeichnung und passende Mutter vor Bearbeitung sicherstellen.'),
 ('Einhausung / Wanne','Blech lasern/kanten, gegebenenfalls dichtschweißen, Korrosionsschutz, Funktionsprobe.','Abwicklungen, Biegewerkzeug, Dichtnähte und Auflagen freigeben.')],[38,70,64],9)
h('Reale Aufspannung vor Bearbeitung')
p('Dem Fertiger Originalteile und Bezugsskizze geben. Gleitflächen schützen, mit spannungsarmer Aufspannung arbeiten und die Funktionsachsen zur Auflage beziehen. Keine Bauteile anhand der perspektivischen Fotomaße einrichten. Späne und Schleifmittel dürfen nicht in Führungen, Muttern oder Spindellager gelangen.')
p('Da die Maschine bereits zerlegt ist, werden Aufmaß und Fremdfertigung vor dem Wiederaufbau abgeschlossen. Sich selbst bearbeitende Umbauabläufe sind nicht vorausgesetzt. Bei einer Änderung am Originalteil muss anschließend eine Kopie als bearbeitetes Teil in der CNC-Baugruppe geführt werden; die unveränderte Ausgangsdatei bleibt erhalten.')
p('Das Register „Fertigung“ enthält 133 Modellpositionen mit Verfahren und Materialvorschlag. Es ersetzt keine Einzelteilzeichnungen. Rohrrahmen, Türprofile, Adapter und Scheiben dürfen nicht allein nach den dortigen Grundkörpermaßen bestellt werden.')

page(8,'Aufmaßblatt: X und Y','Die Maschine ist schon zerlegt. Die folgenden Messungen ergänzen die Fotos; vorhandene Informationen werden nicht erneut abgefragt.')
p('Pro Achse einen eindeutigen Bezug festlegen: bearbeitete Auflagefläche A, dazu passende rechtwinklige Fläche B und die bisherige Spindelachse C. Messrichtung und Nullpunkt auf einer Skizze eintragen. Messschieberwerte nicht als Präzisionspassung ausgeben.')
table(['Kennung','Messgröße','Aufnahmeverfahren'],[
 ('X01 / Y01','Achsposition zur Bezugsfläche','Höhenmessgerät bzw. Messuhr, Parallelunterlagen und zylindrischer Prüfdorn. Keine Ableitung aus grobem Gussrand.'),
 ('X02 / Y02','Antriebsseitiges Lochbild','Koordinaten zu A/B; Loch- oder Gewindegröße, nutzbare Tiefe und verfügbare Auflage angeben.'),
 ('X03 / Y03','Gegenlageranschluss','Auflagehöhe, Lochbild und erreichbare Schraubenlänge separat erfassen.'),
 ('X04 / Y04','Mutterraum und Befestigung','Breite/Höhe/Tiefe sowie die bewegte Hülle an mehreren gesicherten Schlittenpositionen aufnehmen.'),
 ('X05 / Y05','Lagerbezugsflächenabstand','Entlang der Spindelachse zwischen eindeutig benannten Flächen; Endüberstände mitnotieren.'),
 ('X06 / Y06','Nutzbarer Hub','Führungsüberdeckung, Anschläge, Messleisten, Bälge und Werkstück berücksichtigen; nicht bis zum Herausfallen schieben.'),
 ('X07 / Y07','Verbleibende Wand / Rippen','An zugänglichen Stellen messen, sonst geeignetes Prüfverfahren durch Fachbetrieb; nicht aus Außenhülle schätzen.'),
 ('X08 / Y08','Reib-/Losbrechkraft','Richtig eingestellte, geschmierte Führung ohne Spindelantrieb horizontal ziehen; Kraft und Position dokumentieren.')],[26,51,95],9.2)
h('Eintrag in der Arbeitsmappe')
p('Im Blatt „Aufmaß“ Istwert, Messdatum, Messperson und Bild-/Skizzenreferenz ausfüllen. Für Lochbilder ist eine Koordinatenliste besser als eine einzelne Zahl. Die Eingaben werden nicht automatisch in Fertigungsmaße oder eine Maschinenfreigabe umgewandelt.')

page(9,'Aufmaßblatt: Z und Versorgung')
p('Die Z-Messungen Z01–Z08 entsprechen den X/Y-Schnittstellen. Der Kopf muss vor jeder Messung gegen Absinken mechanisch gesichert sein. Eine Motorbremse oder stromloser Schrittmotor ist während des Umbaus keine sichere Abstützung.')
table(['Kennung','Zusatzgröße','Bedeutung'],[
 ('Z09','Bewegte Kopfmasse einschließlich Spindelmotor, Halter und Anbauteilen','Wiegen bzw. geeignet ermitteln. Grundlage für Hubkraft, Bremse, Antrieb, Spindel und Tragbrücke.'),
 ('C01','Vorhandene Netzversorgung und Schutzanlage','Vor Ort durch Elektrofachkraft aufnehmen. Keine Annahme über Leitungsschutz, RCD, Phasen oder zulässige Leistungsaufnahme.'),
 ('S01','Original-Spindelsteuerung: Typ, Schaltplan, sichere Schnittstellen','Bedienplatine/Controller identifizieren. Hall-Signale SA/SB/SC sind nicht automatisch Drehzahl-Sollwerte oder CNC-Eingänge.'),
 ('D01','Masse beider fertiger Türsegmente','Gewicht mit Scheiben, Rahmen, Führungen und Anbauteilen bestimmen, nicht aus unverifizierter Bildmasse ableiten.'),
 ('D02','Einbauraum für Feder, Synchronisierung und Fangsicherung','Geschlossene und offene Lage prüfen. Die vier gezeichneten Gasfederhüllen sind noch keine bestellten Federn.')],[20,69,83],9.5)
h('Auslegung mit fehlenden Daten nicht schönrechnen')
p('Das Blatt „Auslegung“ lässt Drehmomentbedarf und Reserve leer, solange Lastdaten fehlen. Eingetragen sind nur ein Planungsfall von 3.000 mm/min und 100 mm/s² sowie η=0,90 und Reserve1,5. Diese Werte sind keine zugesagten Maschinenleistungen.')
p('Berechnung: n = Vorschub / Steigung × Übersetzung. Axialkraft = m·a + Reibung + Bearbeitungskraft; bei Z kommt m·g hinzu. Lastmoment = F·p/(2π·η·i). Das rotierende Beschleunigungsmoment wird gesondert addiert. Rotor-/Spindelträgheit dürfen dabei nicht doppelt angesetzt werden.')
p('Danach sind zusätzlich kritische Spindeldrehzahl, Knickung, Lebensdauer, Haltersteifigkeit, Motor-Erwärmung und Bremsfähigkeit zu prüfen. Das Katalog-Haltemoment ist kein dynamisches Drehmoment bei 600 min⁻¹.')

page(10,'Beschaffen ohne Fehlbestellungen')
h('Stufe A – Anbieteranfragen')
p('Die 24 ausgewählten Herstellerpositionen und sechs Normteilpositionen können zur technischen und kaufmännischen Anfrage verwendet werden. Jede Anfrage nennt die Positions-ID, Stückzahl, aktuelle Zeichnungsrevision und benötigte Daten. Ein Angebotspreis wird im Blatt „Einkauf“ als Einzelpreis netto eingetragen; Summen rechnen automatisch. Ohne Angebot bleibt die Zelle leer.')
h('Stufe B – verbindliche Auswahl')
p('Vor der Bestellung werden die Gate-IDs jeder Zeile abgearbeitet. Ein real existierender Artikel ist noch kein für diese Maschine nachgewiesener Artikel. Die beiden CS-D508, die Z-Lieferrevision und die Rückspeisung sind insbesondere gemeinsam zu betrachten; Z-Datenkonflikte nicht durch einen ähnlichen Motor ersetzen.')
h('Textbaustein für die Antriebsanfrage')
p('„Bitte bestätigen Sie die Kombination CS-M22326/CS-D508 für X/Y und CS-M23445B/CS-D1008E für Z, jeweils Encoder- und Leistungskabel mit Steckerbelegung, dynamische Drehmomentkurven bei der vorgesehenen DC-Spannung, Bremsdaten und aktuelle Maßzeichnungen. Bei CS-M23445B sind 135/144 mm und 4/6 A widersprüchlich veröffentlicht. Bitte die lieferbare Revision verbindlich benennen.“')
h('Textbaustein für die Spindelanfrage')
p('„Bitte anbieten: zwei zusammenpassende isel16×5-Sätze mit Muttern213505 und ein20×5-Satz mit Mutter2134200005, mit Enden für THKFK12/FF12 bzw.FK15/FF15. Fertiglängen und Endenzeichnung erst nach beigefügtem tatsächlichem Aufmaß. Bitte Spielklasse, Tragzahlen, Schmierung, Befahrbereich, zulässige Drehzahl und die komplette Zeichnung der Halter213500/213600 bestätigen.“')
h('Noch offene Beschaffungspakete')
p('18 Zeilen bleiben bewusst ohne erfundene Bestellnummer: Kabel, Rückspeiseschutz, Sicherheitssystem, Z-Absturzschutz, Netzeingang, Klemmen-/Kanalzubehör, Rechner, Spindelschnittstelle, Schmierung, Abdeckungen, Türmechanik, Schutzscheiben, KSS-System, Füße und maschinenseitige Schrauben. Diese Zeilen zeigen den fehlenden Bedarf, nicht ein vollständiges bestellbares Set.')
note('Keine Bestellung aus alleiniger CAD-Länge. Keine Auswahl einer Gasfeder allein nach sichtbarem Hub. Keine Schutzscheibe allein nach nomineller8-mm-Dicke.')

page(11,'Bauablauf I – vorbereiten und montieren','Die Schritte sind erst nach den jeweils genannten Freigaben auszuführen. Der aktuelle Stand erfüllt diese Freigaben noch nicht.')
table(['Schritt','Ausführung','Abschluss / Stopp'],[
 ('M01','Maschine elektrisch trennen; Kopf und schwere Einzelteile mechanisch sichern. Originalteile und Keilleisten markieren, schützen und reinigen.','Keine Arbeiten an gespeicherter elektrischer oder mechanischer Energie.'),
 ('M02','Messplan X01–Z09 durchführen. Funktionsachsen und vorhandene Gewinde in NX abgleichen; Bearbeitungsmatrix entscheiden.','G02 erfüllt; keine ersetzten Istmaße durch Fotowerte.'),
 ('M03','Gussbearbeitungen und alle Adapterzeichnungen fertigstellen und prüfen lassen. Maßhaltige Liefermodelle gegen Ersatzhüllen abgleichen.','G01/G03/G04/G05 erfüllt; festgelegte Endenzeichnung.'),
 ('M04','Eigenteile fertigen; Spindelsätze mit bearbeiteten Enden beschaffen. Wareneingang: Maße, Gewinde, Oberflächen, Schäden, Artikelrevision.','Abweichungen sperren, nicht durch gewaltsames Montieren ausgleichen.'),
 ('M05','Grundmaschine auf geprüftem Unterbau ausrichten. Führungen zusammenbauen, schmieren und spielfrei ohne Klemmen einstellen.','Gleichmäßige Handbewegung ohne Antrieb; Messprotokoll.'),
 ('M06','Mutterhalter zunächst ausrichtbar montieren. Spindel/Festlager nach Lieferanweisung montieren, Loslager und Brücke fluchtend ansetzen.','Keine Kraft über Kugellaufbahn einpressen. Mutter nicht ohne geeignete Sicherung vom Gewinde drehen.')],[17,102,53],9.5)
p('Bei jeder Achse ohne Motor beginnen. Die Schraube muss über den vorgesehenen Bereich von Hand gleichmäßig laufen. Z nur bei gesichertem Kopf bewegen. Erst nach Ausrichtung und nach Lieferanweisung endgültig klemmen. Zwischen Montage und KSS-Betrieb dürfen keine Schleif- oder Fertigungsreste in den Muttern verbleiben.')

page(12,'Bauablauf II – ausrichten, schützen, prüfen')
table(['Schritt','Ausführung','Abschluss / Stopp'],[
 ('M07','FK-Adapter tragend am tatsächlichen Gussanschluss befestigen. FF-Brücke ergänzen. Beide Lagerachsen und Mutternachgiebigkeit prüfen.','Kein Festziehen zum „Geradeziehen“ einer versetzten Spindel.'),
 ('M08','Distanzsäulen, Motorplatte und Motorflansch mit getrennten Schrauben montieren. Kupplung gemäß aktueller KTR-Anleitung einsetzen.','Kupplungsspielraum, Eingriff, Wellenabstand und erreichbare Schrauben prüfen; keine Wellenvorspannung.'),
 ('M09','Z-Kopflast übernehmen und sichere Halte-/Absturzfunktion fertigstellen. Bremssteuerung und Stillstandsbedingungen dokumentieren.','Mechanische Hilfsabstützung erst nach validierter Sicherung entfernen.'),
 ('M10','Pinole definiert klemmen; manuelle Bedienteile ausbauen und offene Durchführungen abdecken. Anschläge, Referenz-/Endschalterhalter ergänzen.','Sechs IFS206 stehen im Modell bisher nur im Referenzfeld. Nicht nach dieser Ablageposition montieren.'),
 ('M11','Schmierleitungen, Abstreifer und Spindelabdeckungen montieren. Kabelwege mit Schleppketten und zulässigen Biegeradien planen.','Kein Kabel in bewegten Eingriffsstellen; keine KSS-Strahlbelastung ungeschützter Elektrik.'),
 ('M12','Einhausung und KSS-Rücklauf fertigstellen. Dichtheits- und Reinigungsprobe ohne Zerspanung; Türen gesichert testen.','Keine Span-/KSS-Freisetzung, kein unkontrolliertes Fallen, kein Eingriff in laufende Maschine.')],[17,101,54],9.3)
h('Einrichtprotokoll je Achse')
p('Datum, Bediener, Lager-/Mutterrevision, nutzbarer Weg, gleichmäßiges Losbrechmoment, Umkehrspiel und Messrichtung festhalten. Toleranzziele müssen vor der Abnahme festgelegt sein; die Tabelle erfindet keine geforderte Genauigkeit. Bei Ruckeln, Klemmen, zunehmendem Drehmoment oder Erwärmung Montageursache suchen, nicht einfach den Motorstrom erhöhen.')

page(13,'Elektronik: reale Geräte, noch kein Stromlaufplan')
ids=['K-MESA','K-DRV-XY','K-DRV-Z','K-PS-AX','K-PS24','K-PS5','K-CAB','K-CABPL','K-SENSOR']
table(['ID','Menge','Ausführung / Aufgabe'],[(i,cat[i]['planned_quantity'],cat[i]['article']+' — '+cat[i]['description']) for i in ids],[29,15,128],9.3)
p('Quellen: [S03,S04,S10–S16]. Der Schrank ist außen600B×800H×300T; NSYMM86 ist die separate Montageplatte550B×750H. Die Ersatzhülle bildet nicht jede Sicke, Befestigung und Türfuge nach. Eine Schutzart des unveränderten Kaufschranks gilt nicht automatisch nach neuen Durchführungen.')
h('Versorgung konsequent trennen')
p('LinuxCNC-PC → Ethernet → Mesa7i95T → Step/Dir → Motortreiber → Motor. Die Mesa-Karte liefert keine Motorleistung. 5V versorgen die Logik;24V Feldgeräte und passende Brems-/Relaisfunktionen. Motorleistung kommt separat aus dem DC-Leistungszweig. [S03,S04,S10]')
note('Die bisherige Planung verwendet CS-D508 mit maximal50VDC. RSP-500-48 ist deshalb NICHT einfach auf48V einzubauen und als sicher abzuhaken. Vorgesehen ist eine44-V-Studie; Rückspeisespitzen und Abschaltfälle bleiben rechnerisch und messtechnisch nachzuweisen. [S03,S11]')
p('Die RSP-Netzteilüberspannungsabschaltung ersetzt keinen geeigneten Rückspeiseschutz für50-V-Treiber. Leistungsbedarf und Verlustwärme sind ebenfalls noch offen. Eine Auswahl der Netz-/Motorschutzorgane, Leitungsquerschnitte und PE-Prüfungen erfolgt durch die Elektrofachkraft, nicht anhand der gezeichneten Gehäusequader.')

page(14,'Signale und Z-Bremse')
h('Vorgesehene Niederspannungs-Schnittstellen')
table(['Signalpfad','Anforderung / Nachweis'],[
 ('Mesa → Treiber','Differenzielles5-V-Step/Dir. Tatsächliche Stecker-/Klemmenbelegung aus der Lieferrevision übernehmen; keine24V auf Mesa-Step/Dir-Ausgänge geben.'),
 ('CS-D1008E Signalpegel','Signalwahlschalter vor Anschluss auf5V stellen; dokumentieren. Die24-V-Voreinstellung ist nicht automatisch Mesa-kompatibel.'),
 ('Motorencoder → Treiber','Kommutierungs-/Positionsrückführung an den passenden Motortreiber. Nicht allein deshalb zusätzlich parallel an Mesa anschließen; Signalbelastung und Interface prüfen.'),
 ('Treiberalarm → Steuerung','Geeignet verschalten und Polarität/Bruchverhalten testen. Alarm muss eine definierte Maschinenreaktion auslösen, nicht nur eine Bildschirmanzeige.'),
 ('IFS206 → Mesa-Eingang','PNP-Öffner-Feldsignal mit passender gemeinsamer Bezugsklemme. Sensordaten10–30V beachten. Kein Sicherheits-Türschalter.'),
 ('Z-Bremse','24-V-Bremse nach Motorlieferdaten über geeignete Ausgangsstufe schalten. BRK-Ausgang des Treibers ist ein Signal, keine direkte Bremsspulenversorgung.')],[46,126],9.5)
p('CS-D1008E dokumentiert für seinen programmierbaren Ausgang maximal30V/100mA. Eine Lastrelais-/Treiberstufe mit geeigneter Entstörung und nachgewiesenen Schaltzeiten ist erforderlich. Datenquelle [S04]. Die konkrete Bremsstromaufnahme bleibt GateG01.')
h('Stillsetzen ist mehr als „Enable aus“')
p('Für die Z-Achse müssen Antriebskraft, Bremsenbetätigung, Energieausfall, Kupplungs-/Spindelfehler und sichere Wartungsabstützung gemeinsam betrachtet werden. Die Motorhaltebremse allein schützt nicht gegen alle mechanischen Fehler. Bei der breiten Senktür kommen Fang- und Gleichlauffunktion hinzu. [S18]')
note('Mesa/LinuxCNC sind hier keine nachgewiesene Sicherheitssteuerung. Dieses Dokument enthält weder einen fertigen Sicherheitsstromkreis noch eine zulässige Überbrückung von Tür- oder Not-Halt-Funktionen.')

page(15,'LinuxCNC: Vorbereitung und Erstprüfung')
h('Skalierung bleibt mit der Mechanik gekoppelt')
p('Bei5mm/U, direkter Kupplung und tatsächlich eingestellten2.000Schrittimpulsen pro Motorumdrehung ergibt sich400Imp/mm. Bei3.000mm/min sind20.000Impulse/s erforderlich. Die2.000Impulse/U sind nur ein Planungsparameter; Treibereinstellung und Vorzeichen jeder Achse müssen am realen Aufbau abgeglichen werden.')
p('Die Zeitparameter für Schrittimpuls, Pause, Richtungs-Vorlauf und Nachlauf stammen aus dem jeweils angeschlossenen Treiberhandbuch. Als gemeinsamer konservativer Startwert sind5µs Impuls/Pause sowie10µs Richtungszeiten vorgesehen; erst nach elektrischer Prüfung verwenden. Das ist keine vollständige HAL-/INI-Konfiguration. [S03,S04,S17]')
h('Erstprüfung in begrenztem, gesichertem Betrieb')
table(['Stufe','Prüfung'],[
 ('L01','Hardware-/Firmwarestand, Ethernetverbindung, Watchdog, Zuordnung der Achsen und Signale dokumentieren.'),
 ('L02','Alle Eingänge ohne Achsbewegung prüfen: Referenz, Endlage, Alarme und sichere Freigaben. Unterbrechung und Fehlerzustände testen.'),
 ('L03','Antrieb zunächst mit sicherer Umgebung und begrenzter Energie prüfen. Z mechanisch gesichert. Richtung und Skalierung anhand kurzer gemessener Strecke abgleichen.'),
 ('L04','Referenzfahrt langsam und mit kontrolliertem Abstand zu mechanischen Anschlägen einrichten. Softlimits aus realem Weg ableiten, nicht aus500/200/240-Zielwerten.'),
 ('L05','Messuhr-/Maßstabprüfung über mehrere Positionen; Umkehrspiel und Wiederholverhalten dokumentieren. Dann Geschwindigkeit und Beschleunigung stufenweise prüfen.'),
 ('L06','Fehlerreaktionen, Stillsetzen und Wiederanlaufschutz validieren. Erst danach Spindel- und KSS-Betrieb sowie Probezerpanung freigeben.')],[20,152],9.5)
p('Ein Spannungsabfall, Drive-Alarm oder Kommunikationsausfall darf nicht zu einem unerwarteten Wiederanlauf führen. Ein Neustart nach Fehler braucht einen definierten Wiederfreigabeablauf. Zusätzliche Spindelrückführung für synchrones Gewindeschneiden ist nicht Bestandteil dieses Standes.')

page(16,'Tür, Untergestell und KSS: unverändert, nicht fertig')
image('Spaene_KSS_Ruecklauf.png',171,'Gezeichnete Spänesammlung, Grobkorb und getrennter KSS-Rücklauf. Leitblechneigungen sind Entwurfsmaße.')
p('Die genehmigte Grundform bleibt:1650×1000mm Einhausung, Tischhöhe930mm, große1420×1000mm Öffnung und zwei nach unten teleskopierende Türsegmente. Die Türtasche wird nicht mit dem Spänerücklauf verwechselt; der Korb ist hinten entnehmbar.')
h('Noch notwendige echte Komponenten')
p('Gasdruckfederartikel, mechanische Segmentkopplung, Gleichlauf, Fangsicherung und Verriegelung sind noch nicht ausgewählt. Die vier gezeichneten Federhüllen dürfen daher weder in Stückzahl noch Federkraft als fertige Bestellung behandelt werden. Türmassen und Kräfte werden zuerst aus fertigen Segmenten bzw. gesicherter Massenrechnung bestimmt.')
p('Schutzscheiben brauchen eine zum Bearbeitungsrisiko passende Auslegung und Halterung. Die gezeichnete Dicke ist kein Schutzversuch. Untergestell und Maschinenverankerung benötigen einen Last-/Kippnachweis einschließlich Tür, Schaltschrank, Werkstück und Betriebsbelastung. [S18]')
p('Grobsieb, Feinfilter, Pumpe, Schlauch und Reinigungszugang müssen zur Späneart und KSS-Menge passen. Die geneigten Bleche garantieren keine automatische Abfuhr langer oder verklemmter Späne. Dichtheits- und Rücklaufprobe vor Betrieb, Wartungsfreiraum hinten erhalten.')

page(17,'Abnahmepunkte und Nachweise')
table(['Gate','Abschlusskriterium'],[(g['id']+' · '+g['title'],g['required_evidence']) for g in gates],[49,123],8.8)
h('Prüfungen dieses Pakets')
p('Lokale Vertragstests sichern Daten-/Artikelzuordnung, Parametergrenzen und Schutz der Originalrezepte. Eine unabhängige Geometrieprüfung hat435 gültige Einzelkörper aus1470 Operationen erzeugt. Sie ist kein NX-Lauf und keine praktische Passprobe. Sechs statische Überschneidungen ausgewählter Anschlusskörper bleiben dokumentiert.')
p('Die acht Eckstellungen prüfen nur die angesetzten Hüllen im vorhandenen Innenraum. Flexible Kabel, echte Bälge, Werkzeuge, Werkstücke, mechanische Sicherheitsfunktionen und reale Herstellertoleranzen werden damit nicht vollständig geprüft. Die gezeichneten Sensoren sind noch nicht funktionsrichtig montiert.')
note('Auch vollständig ausgefüllte Tabellenfelder erzeugen hier keine automatische Bau-, Sicherheits- oder Bestellfreigabe. Nachweise müssen fachlich geprüft und dem tatsächlichen Maschinenstand zugeordnet werden.')

page(18,'NX-Aufbau und Änderungsführung')
h('Gesamtbaugruppe erzeugen')
p('Das gesamte Paket in einen neuen lokalen Ordner entpacken. In NX2406 „Journal wiedergeben / Play Journal“ aufrufen und NX_CNC_Gesamtansicht.py wählen. Eine geöffnete Ausgangsbaugruppe wird nicht überschrieben. Dieser Stand baut aus den mitgelieferten Rezepten neu auf; eigene manuelle Änderungen an alten .prt-Dateien werden nicht automatisch übernommen.')
p('Für einen kürzeren Kaufteil-/Anschlusslauf kann NX_Umbau_Kern_Pruefen.py verwendet werden. Es erzeugt nur die gefilterten Einzelteile der Antriebe, Elektronik und Sensorreferenzen, nicht eine abgeschlossene Gesamtmaschine. Beide Abläufe behalten die vorhandenen API- und Geometrieprüfungen bei.')
h('Ausgabe und Zuordnung')
p('%LOCALAPPDATA%\\SX35Z\\NX_Output\\SX35Z_CNC_UMSETZUNG_08_<Zeitstempel>_<Kennung>\\',style='Caption')
p('Nach vollständigem Erfolg nennt HAUPTBAUGRUPPE.txt die Hauptdatei. Erzeugte_Teile.json verbindet Modell-ID, Datei, Gruppe, Positions-ID und Kaufteilinstanz. Einkauf_Modellbindung08.json enthält den beim Aufbau verwendeten Katalog und Status. Den gesamten Ausgabeordner zusammenhalten.')
h('Welche Datei steuert was?')
table(['Datei','Verwendung'],[
 ('Parameter.json','Bestands-/Stellungsparameter der Foto-Rekonstruktion; nicht automatisch Istaufmaß.'),
 ('CNC_Parameter.json / Ausbau_Parameter.json','Bestehende Entwurfswerte; ausgewählte historische Kaufteilmaße werden dokumentiert auf Katalogstand migriert.'),
 ('Einkauf/Kaufteile_08.json','Verbindliche Maßquelle für die gemappten Kaufteilhüllen dieser Revision; keine stillen individuellen Änderungen.'),
 ('Aufmass/Messwerte_08.json','Messprotokoll mit unbekannten Istwerten; keine automatische Gussnachbearbeitung.'),
 ('Blech_Optionen.json','Native Blechkonvertierung weiterhin required. Kein heimlicher Solid-Ersatz bei Fehlschlag.')],[64,108],9.2)
p('Quellcode, Zeichnungsrevision, Messprotokoll, Lieferbestätigung und Einkaufsliste müssen denselben Stand tragen. Neue Liefermaße erfordern Modelländerung und erneute geometrische Prüfung. Fehlgeschlagene oder nicht ausgeführte Prüfungen bleiben offen.')

for section,keys in enumerate([list(sources)[:10],list(sources)[10:]],19):
 page(section,'Quellen und Nachweisgrenzen '+('I' if section==19 else 'II'),'Herstellerquellen und Fachinformationen; Zugriff30.10.2026. Keine ungeprüfte Lieferzusage.')
 for sid in keys:
  s=sources[sid]
  a=p(sid+'  '+s['title'],bold=True);a.paragraph_format.space_before=Pt(5);a.paragraph_format.keep_with_next=True
  a=p(s['evidence']);a.paragraph_format.space_after=Pt(2)
  a=p(s['url'],style='Caption');a.paragraph_format.space_after=Pt(6)
  for r in a.runs:r.font.size=Pt(7.6)

out=ROOT/'Bauanleitung/Bau_und_Beschaffungsanleitung_08.docx';out.parent.mkdir(exist_ok=True)
doc.save(out)
print(out)
