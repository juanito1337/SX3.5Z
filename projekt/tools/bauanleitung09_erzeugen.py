# -*- coding: utf-8 -*-
"""Revision09 supplement. Documentation generation only, no NX calls."""
from pathlib import Path
import json,sys,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model
if model.VERSION!='CNC_UMSETZUNG_09':
    raise RuntimeError('Historischer09-Generator: aktuelle Anleitung unter Dokumentation/Entwicklungsstand_Teller_10.md;09-DOCX/PDF bleibt historisch.')
from docx import Document
from docx.shared import Mm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model,umbau_daten09 as ud
pms=model.load_parameters(ROOT/'Parameter.json');atc=model.atc_report(pms);bom=ud.bom_rows(model.recipe(),ROOT)
new=[x for x in bom if x['item_id'].startswith(('K09','N09'))]
qs=json.loads((ROOT/'Quellen/Quellen_09.json').read_text())['sources']
leads=json.loads((ROOT/'Werkzeugwechsler/AliExpress_Suchtreffer_09.json').read_text())['leads']
doc=Document();sec=doc.sections[0];sec.page_width=Mm(210);sec.page_height=Mm(297);sec.top_margin=Mm(17);sec.bottom_margin=Mm(17);sec.left_margin=Mm(18);sec.right_margin=Mm(18);sec.header_distance=Mm(7);sec.footer_distance=Mm(7)
for n in ['Normal','Body Text']:
 st=doc.styles[n];st.font.name='Calibri';st.font.size=Pt(10.5);st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.06
for n,size in [('Title',27),('Heading 1',20),('Heading 2',13),('Heading 3',11)]:
 st=doc.styles[n];st.font.name='Calibri';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('17354B');st.paragraph_format.space_after=Pt(7);st.paragraph_format.keep_with_next=True
h=sec.header.paragraphs[0];h.text='SX3.5Z  /  CNC-UMBAU                                         KONSTRUKTIONSSTAND 09';h.style='Caption'
f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT;f.add_run('30.10.2026 · Nicht freigegebener Arbeitsstand · ').font.size=Pt(8)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
doc.core_properties.title='SX3.5Z – Normteile, Verkleidung und Werkzeugwechseloption 09';doc.core_properties.author='CNC-Umbauprojekt'

def pretty(t):
 t=str(t)
 for a,b in {
  'Anleitung08':'Anleitung 08','Änderungen09':'Änderungen 09','Stand09':'Stand 09',
  'mit09':'mit 09','aus08':'aus 08','belegt620':'belegt 620','des740':'des 740',
  'aufbau135':'aufbau 135','Radius14':'Radius 14','Teilung160':'Teilung 160','Höhe51':'Höhe 51',
  'Serviceblech2':'Serviceblech 2','Hinterlegung190':'Hinterlegung 190','Griff2':'Griff 2',
  'mindestens12':'mindestens 12','LAPP531':'LAPP 531','Lochmitten70':'Lochmitten 70',
  'Gewindelänge9':'Gewindelänge 9','maximal37':'maximal 37','Kabel6':'Kabel 6','Höhe6':'Höhe 6',
  'je2':'je 2','und1':'und 1','Lochbild104':'Lochbild 104','Das90':'Das 90',
  'gemeinsame7':'gemeinsame 7','wird in09':'wird in 09','Entscheidung09':'Entscheidung 09',
  'Träger4':'Träger 4','Innenradius6':'Innenradius 6','Projektion70':'Projektion 70',
  'Hülle118':'Hülle 118','überstand35':'überstand 35','bolzen30':'bolzen 30',
  'abstand15':'abstand 15','mit70':'mit 70','und15':'und 15','sich513':'sich 513',
  'höhe530':'höhe 530','bleiben16':'bleiben 16','erste70':'erste 70','in16':'in 16','auf94':'auf 94',
  'um253':'um 253','Spindelsatz2':'Spindelsatz 2','Seitenpreis:90':'Seitenpreis: 90',
  'Mesa7':'Mesa 7','durch09':'durch 09','mit08':'mit 08','NX2406':'NX 2406',
  'die125':'die 125','anschließend20':'anschließend 20','stände4':'stände 4',
  'Blechadapter07':'Blechadapter 07','Formelpatch07':'Formelpatch 07','Alte07':'Alte 07',
  'Seite2':'Seite 2','Lochabstand160':'Lochabstand 160','min12':'min. 12','Eckradius14':'Eckradius 14',
  'Stock:SK':'Bestand: SK','Nut12':'Nut 12','e18':'e 18','h14':'h 14','k7':'k 7',
  'Höhe4':'Höhe 4','Längen25':'Längen 25','Geometrie6':'Geometrie 6','Abrufstand30':'Abrufstand 30',
  'Vergleich:2780':'Vergleich: 2780','Außendurchmesser29':'Außendurchmesser 29','Bund0':'Bund 0',
 }.items(): t=t.replace(a,b)
 t=re.sub(r'(?<=\d)(mm|kg|USD|rpm|kW|W)\b',r' \1',t)
 t=re.sub(r'(?<=[,;:])(?=[A-Za-zÄÖÜäöüß])',' ',t)
 t=t.replace(',1.829',', 1.829').replace(',293',', 293').replace(',148',', 148').replace(',560',', 560').replace(';35','; 35')
 return t

def p(t='',bold=False,style=None):
 x=doc.add_paragraph(style=style);r=x.add_run(pretty(t));r.bold=bold;return x

def heading(t,l=2):return doc.add_heading(pretty(t),l)
def page(no,t):doc.add_page_break();p('UMSETZUNG 09 / '+str(no).zfill(2),style='Caption');heading(t,1)
def note(t):
 tb=doc.add_table(rows=1,cols=1);c=tb.cell(0,0);c.text=pretty(t);pr=c._tc.get_or_add_tcPr();sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'FFF0D6');pr.append(sh)
 for a in c.paragraphs:
  a.paragraph_format.space_after=Pt(5);a.paragraph_format.space_before=Pt(5)
  for r in a.runs:r.bold=True;r.font.size=Pt(10)
 p('')
def table(head,rows,widths=None,size=9):
 tb=doc.add_table(rows=1,cols=len(head));tb.autofit=False
 for i,x in enumerate(head):tb.cell(0,i).text=pretty(x)
 for row in rows:
  for c,x in zip(tb.add_row().cells,row):c.text='' if x is None else pretty(x)
 for n,row in enumerate(tb.rows):
  trp=row._tr.get_or_add_trPr();trp.append(OxmlElement('w:cantSplit'))
  if n==0:trp.append(OxmlElement('w:tblHeader'))
  for i,c in enumerate(row.cells):
   if widths:c.width=Mm(widths[i])
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'17354B' if n==0 else 'EDF3F6' if n%2 else 'FFFFFF');c._tc.get_or_add_tcPr().append(sh)
   for a in c.paragraphs:
    a.paragraph_format.space_before=Pt(3);a.paragraph_format.space_after=Pt(3);a.paragraph_format.line_spacing=1.02
    for r in a.runs:
     r.font.size=Pt(size)
     if n==0:r.bold=True;r.font.color.rgb=RGBColor(255,255,255)
 return tb

def image(fn,w=169,cap=''):
 doc.add_picture(str(ROOT/'Vorschau'/fn),width=Mm(w))
 if cap:p(cap,style='Caption')
def link(par,text,url):
 hy=OxmlElement('w:hyperlink');hy.set(qn('r:id'),par.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');pr=OxmlElement('w:rPr');co=OxmlElement('w:color');co.set(qn('w:val'),'1454B7');pr.append(co);r.append(pr);tx=OxmlElement('w:t');tx.text=text;tx.set(qn('xml:space'),'preserve');r.append(tx);hy.append(r);par._p.append(hy)

p('ENTWICKLUNG / NATIVE NX-BAUGRUPPE',style='Subtitle');heading('Normteile und\nWerkzeugwechseloption',0);p('SX3.5Z · Umsetzung 09 · Ergänzung zur Bau- und Beschaffungsanleitung 08',True)
image('Gesamtansicht_offen.png',169,'Vorschau aus dem tatsächlich berechneten Modellrezept, kein KI-Konzeptbild und kein NX-Screenshot.')
note('Das Sechsplatzmagazin ist eine Machbarkeitsoption. Die vorhandene SK30/M12-Spindel bleibt unverändert und ist damit NICHT automatisch wechselbar. Keine Betriebs-, Fertigungs- oder Bestellfreigabe.')
p('Ergebnis: 560 Einzelkörper in 20 Gruppen; 13 zusätzliche Kauf-/Normteilkonfigurationen, acht offene Systempakete und 15 neue Fertigungsteile. Das komplette NX-Journalprojekt und die konsolidierte Einkaufsliste liegen bei.')
p('Die Arbeitsmappe ist die tabellarische Referenz für Artikel, Quellen, Stückzahlen und Istaufmaße. Anleitung08 gilt für die unveränderte Grundmaschine weiter; diese Ergänzung beschreibt die Änderungen09 und ihre Grenzen.')

page(1,'Was gebaut wurde – und was nicht')
table(['Bereich','Stand09','Noch offen'],[
 ['Verkleidung','3 Servicegriffe, Hinterlegungen und reale Verschraubungen','Dichtungen der Serviceflächen, Trag-/Ergonomieprüfung'],
 ['Schaltschrank','2 M20-Einführungen mit Gegenmuttern auf Wechselplatte','Reale Serien-Flanschöffnung, Kabel, Flächendichtung und EMV'],
 ['Werkzeugmagazin','6 Plätze, Tischmontage, Normschrauben und T-Nutsteine','Taschenindexierung, formschlüssige Halterretention und Deckel'],
 ['ATC-Spindel','Nicht eingebaut, ursprüngliche SK30-Referenz erhalten','Geeigneter Spindelsatz, Antrieb, Löseeinheit und Sensorik'],
 ['Steuerung','Signal-/Funktionsanforderungen dokumentiert','Kein ausführbares M6-Makro oder fertiger Stromlaufplan'],
 ['NX','Bestehender nativer Builder mit09-Rezept erweitert','Realer NX2406-Lauf dieser Revision nicht ausgeführt']], [32,70,72])
heading('Bewusst getrennte Nachweise')
p('Katalogmaße belegen nur die genannten Artikelabmessungen. Die Einbaupositionen der neuen Blechteile sind eigene Konstruktion. Der Maschinenguss bleibt eine Fotorekonstruktion mit offenen Anschlussmaßen. Ein gültiger Volumenkörper ist weder eine Festigkeitsprüfung noch eine Betriebsfreigabe.')
p('Die alte Tür wird nicht durch einen neuen Mechanismus ersetzt: Alle 49 als bewegtes Türteil gekennzeichneten Körper behalten Geometrie und Lageformeln aus08. Gasdruckfedern, Gleichlauf und Fangsicherung bleiben weiterhin offen.')
heading('Praktischer Nachteil der günstigen Magazinvariante')
p('Die Grundplatte belegt620 ×100mm des740 ×180mm Tisches. Für breite Spannmittel ist das ungünstig; außerdem ragt der Magazinaufbau135mm bis zur Halter-Bezugsebene über den Tisch. Vor einer endgültigen Auswahl muss ein typischer Bearbeitungsauftrag mit Schraubstock und Werkzeugen eingeplant werden. Ein ausfahrbares Seitenmagazin wäre platzsparender auf dem Tisch, benötigt aber eigene Bewegung, Führung, Sensorik und verifizierte Anbietermaße.')

page(2,'Neue Kauf- und Normteile')
table(['Menge','Artikel / Norm','Einbau'],[[x['quantity'],x['article'],x['description']] for x in new],[16,94,64],8.9)
p('Zu jeder Position stehen Quellen-URLs, Artikel-ID und CAD-Körper in Einkauf_und_Aufmass_09.xlsx. Mengen beziehen sich auf reale Kaufteilinstanzen, nicht auf die Zahl geometrischer Unterkörper. Die sechs BT30-Halter und die Magazinbefestigung sind bedingte ATC-Optionen, keine freigegebene Bestellung.')
p('Gewinde werden als nominale Zylinder-/Bohrungsgeometrie dargestellt. Schrauben besitzen Kopf und Innensechskant, Scheiben eine echte Bohrung und Muttern die Sechskantkontur. Für eine Fertigungszeichnung müssen Gewindeaufruf, Toleranz und Werkstoff ergänzt werden. Ein dargestelltes M5-Nennloch ist ausdrücklich kein M5-Kernloch.')
p('Der Griffbogen ist vereinfacht; Katalog-Radius14mm ist nicht als exakte Bogenkontur konstruiert. Die BT30-Aufnahme ist nur hinsichtlich der genannten Hauptmaße katalogbezogen; Flansch- und Greifdetails sind noch Annahmen. [S09-01, S09-05…10, S09-15/16]')

page(3,'Servicebleche mit befestigten Griffen')
image('Servicegriff_09.png',155,'GN425-Referenzgriff und Schraubverbindung; Serviceblech zur Darstellung ausgeblendet. Griffbogen vereinfacht.')
table(['Verbindung','Maß / Ausführung'],[
 ['Griff','GN425-NI-12-160-GS; Ø12, Teilung160, Höhe51, M6'],
 ['Bleche','Serviceblech2mm + Hinterlegung190 ×30 ×2mm'],
 ['Bohrungen','Je zwei Durchgänge Ø6,6mm in beiden Blechen'],
 ['Schrauben','Je Griff2 × ISO4762 M6×16, dazu ISO7089 M6'],
 ['Gewindeeingriff','16 −1,6 −2 −2 =10,4mm; Katalogtiefe mindestens12mm']], [44,130])
p('Die Griffe sitzen an beiden seitlichen Untergestellschürzen und an der hinteren KSS-Serviceklappe. Die bewegte Fronttür wird nicht angebohrt. Die Hinterlegung verteilt die Handkräfte auf eine größere Fläche; ein Tragfähigkeitsnachweis liegt noch nicht vor. Nicht als Hebeöse oder Verzurrpunkt verwenden. [S09-01, S09-05, S09-16]')
p('Vor Montage Kanten entgraten, Blechdicken und Schraubeneingriff am gelieferten Griff prüfen. Kopf, Scheibe und Werkzeug müssen innen erreichbar bleiben. Das Anzugsmoment ist nach tatsächlichem Gewinde-/Werkstoffzustand festzulegen; keine pauschale Drehmomentfreigabe aus diesem Modell.')

page(4,'Kabeleinführungsplatte am Schaltschrank')
image('Kabeleinfuehrung_09.png',150,'Unterseite der neuen Wechselplattenstudie mit zwei LAPP-Kabelverschraubungen; Schrankkörper zur Ansicht ausgeblendet.')
table(['Merkmal','Geometrie / Grenze'],[
 ['Neue Platte','120 ×160 ×2mm, eigene Konstruktion'],
 ['Durchführung','2 ×Ø20,5mm, Lochmitten70mm auseinander'],
 ['LAPP53111020','M20×1,5; Gewindelänge9; Gesamthöhe maximal37; Kabel6–13mm'],
 ['LAPP53119020','M20×1,5; SW27; Höhe6; BundØ29,7'],
 ['Plattenbefestigung','6 × M5×16, je2 Scheiben und1 Mutter; Lochbild104 ×144mm mit mittleren Seitenpunkten'],
 ['Dichtungsreserve','0,5mm Flachdichtung; Artikel/Werkstoff unbestätigt']], [43,131],8.9)
p('Das90 ×130mm Fenster im modellierten Schrankboden ist ein eigener Anschlussvorschlag, KEINE bestätigte Serienöffnung des Schneider-Schrankes. Vor Bearbeitung die reale Flanschplatte prüfen; gegebenenfalls eine passende Ersatzplatte statt Bearbeitung der Schrankhülle verwenden.')
p('Die Kabelverschraubung ist aus Polyamid, keine EMV-Schirmklemme. Flächendichtung der M20-Verschraubungen, Kabelwahl und Gesamt-IP-Nachweis fehlen. Die Schutzart des Kaufteils wird nicht auf die selbst gefertigte Baugruppe übertragen. [S09-02/03]')

page(5,'Werkzeugwechsler: die richtige Schnittstelle')
p('Die SX3.5Z wird von paulimot mit SK30/M12 nach DIN2080 angegeben. Ein BT30-Magazin ersetzt weder die manuelle Zugstange noch eine automatische Spanneinheit. Der gemeinsame7:24-Kegel macht Halter, Anzugsbolzen, Greifnut und Einzugsmechanik nicht automatisch austauschbar. Die vorhandene Spindel wird in09 daher bewusst nicht als BT30-ATC-Spindel umdeklariert. [S09-11]')
table(['Ansatz','Vorteil','Entscheidung09'],[
 ['Automatisieren der Original-SK30-Zugstange','Erhält mehr Originalmechanik','Keine belastbare Spann-/Löse-Lösung belegt; nicht konstruktiv freigegeben.'],
 ['BT30-Spindelsatz + einfaches Pickup-Magazin','Spindelschnittstelle und Magazin getrennt beschaffbar','Als Machbarkeitsrichtung untersucht; Spindel vor Bestellung eindeutig auswählen.'],
 ['BT30-Spindelsatz + Kauf-Karussell/Seitenmagazin','Tisch besser nutzbar','Mehr Kosten und zusätzliche Mechanik; AliExpress-Magazin bislang nur Suchhinweis.']], [48,54,72])
image('Magazin_09.png',163,'Nur Magazinoption: Träger, Locator-Blöcke und vereinfachte BT30-ER20-70-Halter. Kein lieferbares Komplett-ATC dargestellt.')
p('Die sechs Locator-Blöcke sind eigene POM-Entwürfe mit Ø34,6mm Durchgang, keine nachgebauten RicoCNC-Gabeln. Eine Verdrehsicherung, positive Halterretention und geeignete automatische Späneabdeckung sind noch erforderlich. Die Wangenanschlüsse des Magazins sind als Schweißkonstruktion gedacht; Nahtauslegung und Fertigungszeichnung fehlen.')

page(6,'Magazinmaße und Wechselraum')
table(['Entwurfsgröße','Wert'],[
 ['Plätze / Teilung','6 /94mm'],['Fußplatte / Träger','620 ×100 ×8mm / U-Träger4mm, Innenradius6mm im NX-Blechauftrag'],['Halter-Bezugsebene','135mm über Tisch =315mm im Maschinenmodell'],['Katalog-Halter','BT30-ER20-70; Projektion70mm, gesamte Hülle118,4mm, KonusbezugØ31,75 [S09-10]'],['Zusätzliche Reserven','Werkzeugüberstand35mm; Anzugsbolzen30mm; Freifahrabstand15mm – alles Entwurfsannahmen']], [60,114])
table(['Tasche','Tischlokal X','Tischlokal Y','benötigt X','benötigt Y'],[[x['pocket'],x['table_local_x_mm'],x['table_local_y_mm'],x['required_pos_x_mm'],x['required_pos_y_mm']] for x in atc['pockets']],[22,38,38,38,38])
heading('Nominelle Höhenrechnung')
p('Oberste gespeicherte Hülle:315 +(118,4 −70) +30 =393,4mm. Für eine Querfahrt mit70mm Halterprojektion,35mm Werkzeugüberstand und15mm Abstand ergibt sich513,4mm. Gegenüber der angenommenen maximalen Spindel-Bezugshöhe530mm bleiben16,6mm. Ein längeres Werkzeug oder ein anderer Spindelsatz kann diese Reserve aufbrauchen.')
note('Diese Modellkoordinaten NICHT in LinuxCNC übernehmen. Ein neuer Spindelsatz verändert Bezugshöhe und Kopfhülle. Es wurde keine vollständige Wechselbahn, Werkstückkollision oder sichere Wiederanlaufsequenz nachgewiesen.')
p('Der erste70mm-Teilungsentwurf kollidierte in16 geprüften Kombinationen mit Nachbarhaltern/Spritzblech. Die Teilung wurde auf94mm erweitert und das hintere Schutzblech gekürzt. Danach bestehen die dokumentierten Endpunktprüfungen gegen drei Bestands-Kopfkörper; der ausgewählte Halter selbst ist wegen der noch inkompatiblen Spindelschnittstelle aus dieser Prüfung ausgenommen.')

page(7,'AliExpress-Recherche und Kostenvergleich')
p('Die direkten AliExpress-Angebote konnten nicht vollständig geöffnet bzw. verifiziert werden. Die folgenden Daten stammen aus Preisindex-Suchtreffern und sind nur Startpunkte für eine Lieferantenanfrage. Sie belegen weder technische Maße noch einen aktuellen Endpreis oder die passende Variante.')
table(['Hinweis','Historischer Preis','Einordnung'],[[q['article_id']+'\n'+q['label'],f"{q['historical_price_usd']:.2f} USD\n{q['price_date']}",q['assessment']] for q in leads],[66,32,76],8.8)
p('Der Hinweis um253USD ist der günstigste hier gefundene Indexwert, nicht ein bestätigtes vollständiges System. Zu rechnen wären zusätzlich gegebenenfalls Antrieb, Riemen, Lager-/Kopfadapter, Löseeinheit, Werkzeughalter, Anzugsbolzen, Pneumatik, Sensorik, Abdeckung, Steuerungsintegration und Versand/Abgaben.')
p('Zum Lieferumfangvergleich nennt Automation Technology für einen kompletten BT30-Riemenspindelsatz2.780USD Seitenpreis:90mm,6.000min⁻¹,2,2kW, Spindel/Antrieb, Befestigung und pneumatische Löseeinrichtung. Das ist kein SX3.5Z-Einbaunachweis und keine Empfehlung zum ungeprüften Ersatz des vorhandenen1-kW-Antriebs. [S09-12]')
p('Die exakten AliExpress-Links und Indexbelege stehen im Tabellenblatt ATC_Suche und in AliExpress_Suchtreffer_09.json. Die englische Anfragevorlage Lieferantenanfrage_ATC_09.txt fragt Variantenpreis, Zeichnungen, Schnittstellen, Sensorik und vollständigen Lieferumfang gezielt ab.')

page(8,'Steuerung und Pneumatik – Voraussetzungen')
p('LinuxCNC unterstützt die projektspezifische Neubelegung von M6. Das ist ein Softwaremechanismus, kein fertiger Werkzeugwechsel. Für diese Revision wird bewusst kein Makro mit unbestätigten Maschinenkoordinaten oder ungesicherten Lösebefehlen geliefert. [S09-13]')
table(['Funktion','Erforderlicher Nachweis'],[
 ['Spindel steht','Zuverlässige Stillstandserkennung; ein gesendetes Stoppsignal allein genügt nicht.'],
 ['Spindel orientiert','Geber/Antrieb und bestätigte Winkelstellung passend zu Mitnehmern und Taschenindexierung.'],
 ['Werkzeug gespannt / gelöst','Unabhängige, eindeutige Rückmeldungen, Plausibilitätsprüfung und Zeitüberwachung.'],
 ['Druckluft bereit','Druckbereich und Verhalten bei Energieverlust nach gewähltem Spindelhersteller.'],
 ['Werkzeug / Tasche','Belegung, eindeutige Werkzeugnummer und sichere Aufnahme bei Störung.'],
 ['Magazinabdeckung','Offen/geschlossen rückmelden; Konen dürfen nicht offen im Spänestrom stehen.'],
 ['Lösefreigabe','Nur in bestätigter Wechselposition, bei Stillstand und mit gesicherter Werkzeugaufnahme.'],
 ['Wiederanlauf','Nach Abbruch Zustand erfassen und kontrolliert bergen; kein blindes Fortsetzen.']], [48,126])
p('Die Signale sind Funktionsanforderungen, keine Klemmen-/Pinbelegung. Die verbleibenden Ein-/Ausgänge der Mesa7i95T müssen gegen Achsfreigaben, Bremse, Spindel, KSS und Türschaltung bilanziert werden. Erweiterungsbedarf ist offen. Netz-, Motor- und Sicherheitsverdrahtung muss durch eine geeignete Elektrofachkraft ausgearbeitet und geprüft werden.')
note('Spannkraft, Druck, Ventilstellung und Anzugsbolzen sind sicherheitsrelevant. Kein frei gewählter Zylinder und keine nur softwareseitige Verriegelung wird hier als sichere Lösung ausgegeben. Vor Eingriffen Maschine sichern und Energiequellen fachgerecht trennen.')

page(9,'Montagevorbereitung und Originalbearbeitung')
heading('Servicebleche und Kabeleinführung')
p('1. Reale Blechstärken, vorhandene Öffnungen und Schraubenzugänglichkeit prüfen. 2. Griff- und Plattenzeichnungen anhand der Artikelzeichnung vervollständigen. 3. Eigene Blechteile fertigen, Bohrungen entgraten, Korrosionsschutz festlegen. 4. Griffe mit Hinterlegung und passenden Scheiben montieren; Eingriff und Nicht-Aufsetzen prüfen. 5. Wechselplatte und Dichtkonzept an den tatsächlich gelieferten Schrank anpassen. 6. Kabeldurchmesser, Schirmung und Dichtheitsprüfung separat abschließen.')
heading('Magazin zunächst als Passprobe')
p('1. T-Nutquerschnitt einschließlich Tiefe aufnehmen. 2. Spindelsatz und vollständige Halterzeichnungen wählen. 3. Typische Werkstücke und Spannmittel im Modell ergänzen. 4. Magazin- und Wechselpositionen neu prüfen. 5. Erst danach Grundplatte, Wangen, Träger, Locator-Halterungen und Schutzdeckel fertigungsgerecht auslegen. 6. Statische Passprobe ohne Maschinenbewegung durchführen. Kein automatischer Lauf allein aufgrund der Bildschirmansicht.')
table(['Originalteil','Bearbeitung durch09'],[
 ['Frästisch','Für den gezeigten Magazinfuß keine neuen Bohrungen vorgesehen; vier vorhandene T-Nutbefestigungen. Istnut und Schraubenlänge prüfen.'],
 ['Spindelkopf / Pinole','Unverändert im gelieferten Modell. Für ein tatsächliches BT30-ATC kann ein neuer Kopfadapter oder Präzisionsbearbeitung nötig werden; derzeit nicht festgelegt.'],
 ['Basis / Sattel / Säule','Sechs bekannte Anschlussüberschneidungen des Grundumbaus bleiben offen. Nicht nach Fotoangaben ausfräsen.'],
 ['Verkleidungsbleche','Neue Griffdurchgänge und Hinterlegungen; keine Änderung an der bewegten Tür.'],
 ['Schaltschrank','Neue Wechselplattenstudie; Serien-Flanschöffnung zuerst prüfen statt den gelieferten Schrank blind auszuschneiden.']], [43,131])
p('Die neuen einfachen Bleche und Bohrbilder verlangen nicht zwangsläufig CNC-Bearbeitung. Die Genauigkeit zukünftiger Spindel-/Lagersitze kann dagegen externe Präzisionsbearbeitung erfordern. Dafür fehlen noch belastbare Bezugs- und Toleranzangaben.')

page(10,'NX-Aufbau, Daten und Prüfstand')
p('Das komplette ZIP in einen neuen lokalen Ordner entpacken; keine Module mit08 vermischen. In NX2406 über Journal wiedergeben starten:',True)
p('NX_CNC_Gesamtansicht.py',True)
p('Alternativ zuerst NX_Normteile_ATC_Pruefen.py: Es baut die125 neuen Körper und die vier geänderten Anschlusskörper als Einzelteile auf. Der vollständige Ablauf erzeugt anschließend20 Unterbaugruppen und eine neue Hauptbaugruppe. Erst nach vollständig erfolgreichem Journallauf gilt die Ausgabe als aufgebaut.')
p('Standardausgabe: %LOCALAPPDATA%\\SX35Z\\NX_Output\\SX35Z_CNC_UMSETZUNG_09_<Zeitstempel>_<Kennung>\\. HAUPTBAUGRUPPE.txt nennt die Hauptdatei. Teile, Unterbaugruppen und Hauptdatei zusammenhalten. Bereits vorhandene Dateien bleiben unverändert.')
p('Die Bibliotheksstände4.8, Blechadapter07.2 und Formelpatch07.3 bleiben absichtlich erhalten. Detail_Parameter_09.json enthält die zusätzlichen Entwurfsmaße. Hersteller-Hauptmaße sind gegen stilles Überschreiben gesperrt. Eine Änderung von Nutlage oder Verbindungsdicken verlangt neue Verbindungsauslegung.')
table(['Prüfung','Ergebnis / Grenze'],[
 ['Einzelkörper','560 gültige Einzelkörper,1.829 Operationen im unabhängigen Geometrieaufbau. Keine native NX-Ausführung.'],
 ['Neue Teile, statisch','62.125 Paar-Vorprüfungen,293 genaue Schnittprüfungen; keine Überschneidung der neuen Körper im Standardzustand.'],
 ['ATC-Endpunkte','1.368 Paarprüfungen an sechs Positionen; keine gefundene Überschneidung im ausgewiesenen Teilumfang. Keine vollständige Bahnprüfung.'],
 ['Bestandskonflikte','Sechs bekannte statische Anschlusskonflikte bleiben dokumentiert.'],
 ['Datenabgleich','69 Beschaffungspositionen,148 Fertigungspositionen,560 Körperzuordnungen;35 fehlende Istaufmaße.'],
 ['Automatik / Sicherheit','Nicht ausgeführt / nicht freigegeben. Ergebnisse in Pruefung_09 lesen.']], [47,127])
p('Der ausführliche Prüfbericht unterscheidet aktuellen Testumfang und historische Fehlernachweise. Alte07-Tests bleiben als Archiv erhalten, sind nicht als bestandene aktuelle Tests mitgezählt. Die Abschlussprüfung ist eine Autoren-Selbstprüfung, keine unabhängige Maschinenabnahme.')

for n,subset in enumerate([qs[:10],qs[10:]],11):
 page(n,'Quellen und Beleggrenzen')
 p('Technische Hauptmaße stammen aus den verlinkten Hersteller-/Anbieterunterlagen. Preisindexseiten dienen nur der Angebotssuche. Vollständige URLs stehen außerdem in Quellen_09.json und in der Arbeitsmappe.')
 for q in subset:
  a=p(q['id']+' · '+q['title'],True);link(a,'  [Quelle öffnen]',q['url']);p(q['scope'])
 p('Abrufstand30.10.2026. Lieferrevision, Ausführung und Verfügbarkeit erneut vor Bestellung bestätigen. Es wurde kein originales Hersteller-STEP-Modell dieser neuen Kaufteile beschafft. Vereinfachungen sind im Modell und in der Artikelzuordnung gekennzeichnet.',style='Caption')

out=ROOT/'Bauanleitung/Normteile_und_Werkzeugwechsler_09.docx';doc.save(out);print(out)
