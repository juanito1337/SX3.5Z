from pathlib import Path
import sys, json, collections, math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model, umbau_daten08 as ud
from artifact_tool import Workbook, SpreadsheetFile
wb=Workbook.create()
params=model.load_parameters(ROOT/'Parameter.json')
defs=model.recipe()
bom=ud.bom_rows(defs,ROOT)
sources=json.loads((ROOT/'Quellen/Quellen_08.json').read_text())['sources']
measures=json.loads((ROOT/'Aufmass/Messwerte_08.json').read_text())['measurements']
gates=json.loads((ROOT/'Pruefung_08/Freigaben.json').read_text())['gates']
fab=ud.manufacturing_rows(defs,params,model)
mapping=ud.model_map(defs)
audit=json.loads((ROOT/'Aufmass/Bearbeitungsmatrix_08.json').read_text())
navy="#17354B";teal="#117C83"; pale="#EAF2F5";amber="#FFF0D6"; blue="#1454B7"
def col(n):
    s=''
    while n: n,r=divmod(n-1,26);s=chr(65+r)+s
    return s
def sheet_table(name,title,subtitle,headers,rows,widths):
    sh=wb.worksheets.add(name);last=col(len(headers));end=5+len(rows)
    sh.merge_cells(f'A1:{last}1');sh.get_range('A1').values=[[title]]
    sh.get_range(f'A1:{last}1').format={'fill':navy,'font':{'color':'#FFFFFF','bold':True},'row_height':32}
    sh.merge_cells(f'A2:{last}3');sh.get_range('A2').values=[[subtitle]]
    sh.get_range(f'A2:{last}3').format={'wrap_text':True,'fill':pale,'row_height':22}
    sh.get_range(f'A5:{last}{end}').values=[headers]+rows
    sh.get_range(f'A5:{last}5').format={'fill':teal,'font':{'bold':True,'color':'#FFFFFF'},'wrap_text':True,'row_height':32}
    if rows:
        sh.get_range(f'A6:{last}{end}').format={'wrap_text':True,'row_height':72,'vertical_alignment':'top'}
        sh.tables.add(f'A5:{last}{end}',True,'T_'+name.replace(' ','_'))
    for i,w in enumerate(widths,1):sh.get_range(f'{col(i)}1:{col(i)}{end}').format.column_width=w
    sh.freeze_panes.freeze_rows(5)
    return sh
summary=wb.worksheets.add('Start')
summary.merge_cells('A1:H2');summary.get_range('A1').values=[['SX3.5Z · Umsetzung 08 | Beschaffung und Bauvorbereitung']]
summary.get_range('A1:H2').format={'fill':navy,'font':{'color':'#FFFFFF','bold':True},'row_height':26}
summary.merge_cells('A3:H4');summary.get_range('A3').values=[['STAND 30.10.2026 · ANFRAGESTAND, NICHT BAUFREIGEGEBEN. Originalanschlüsse, Spindelenden, Z-Lieferrevision und Sicherheitskonzept sind noch zu bestätigen.']]
summary.get_range('A3:H4').format={'fill':amber,'wrap_text':True,'row_height':25}
summary.get_range('A6:D6').values=[['Katalogpositionen','Offene Beschaffungen','CAD-Einzelkörper','Fehlende Istaufmaße']]
summary.get_range('A7:D7').formulas=[['=COUNTIF(Einkauf!C6:C53,"Kaufteil")','=COUNTIF(Einkauf!C6:C53,"Offene Beschaffung")','=COUNTA(Modell!A6:A440)','=COUNTBLANK(Aufmass!F6:F34)']]
summary.get_range('A6:D7').format={'fill':pale,'font':{'bold':True},'row_height':28,'wrap_text':True}
summary.get_range('A10:D14').values=[
    ['Angebotssumme netto',None,'Nur eingetragene Einzelpreise; kein Vollbudget.',None],
    ['Positionen mit Preis',None,'Alle Preise sind zunächst leer, nicht 0 €.',None],
    ['Freigabestatus','NICHT FREIGEGEBEN','Checkboxen ersetzen keine Prüfung.',None],
    ['Datenbasis','Kaufteile_08.json','CAD-Zuordnung und CSVs aus derselben Datenquelle.',None],
    ['NX-Lauf Revision 08','NICHT AUSGEFÜHRT','Geometrieprüfung außerhalb NX ist getrennt dokumentiert.',None]]
summary.get_range('B10').formulas=[['=IF(COUNT(Einkauf!K6:K53)=0,"",SUM(Einkauf!L6:L53))']]
summary.get_range('B11').formulas=[['=COUNT(Einkauf!K6:K53)']]
summary.get_range('B10').set_number_format('#,##0.00 "€"')
summary.get_range('A16:D22').values=[
    ['Arbeitsfolge','1. Aufmaß','2. Herstellerzeichnungen','3. Auslegung und Passprobe'],
    ['Danach','4. Sonderteile fertigen','5. Montage / Elektroprüfung','6. NX-/LinuxCNC-Abnahme'],
    ['Blaues Schriftbild','Eingaben durch dich','Preise, Angebote, Istmaße','Keine automatische Freigabe'],
    ['Einkauf','48 Positionen inkl. offener Systempakete','Bestellnummer ≠ Eignungsnachweis','Nur vollständig spezifizierte Positionen beauftragen'],
    ['Fertigung','133 Sonderteilpositionen','Rohkörpermaße sind keine fertigen Zeichnungen','Maschinenseitige Lochbilder fehlen'],
    ['Bearbeitung','8 Prüf-/Arbeitsbereiche','Sechs statische Modellüberschneidungen','Guss nicht nach Foto ausfräsen'],
    ['Quellen','20 Hersteller-/Fachquellen','Lieferrevision und Lieferbarkeit prüfen','Keine erfundenen Tagespreise']]
summary.get_range('A10:H24').format.wrap_text=True
summary.get_range('A10:H24').format.row_height=36
summary.get_range('A1:H24').format.column_width=23
summary.get_range('A12:H12').format.fill=amber
rows=[]
for b in bom:
    ids=b['source_ids'].split()
    urls='\n'.join(sources[x]['url'] for x in ids)
    rows.append([b['item_id'],b['quantity'],b['type'],b['manufacturer'],b['article'],b['description'],b['status'],b['model_quantity'],b['gates'],b['source_ids'],None,None,None,b['model_refs'],b['note'],urls])
buy=sheet_table('Einkauf','Einkaufsliste 08 · reale Artikel und offene Systempakete',
    'Mengen = Planstand. Katalogmaße bestätigen nicht die Eignung am Guss. Blaue Felder: Preise/Anbieter. KTR und Spindeln sind Konfigurationsanfragen, keine fertigen Bestellnummern.',
    ['ID','Menge','Art','Hersteller','Artikel / Konfiguration','Bezeichnung','Status','Im Modell, Einheiten','Offene Gates','Quellen','EP netto €','Positionswert €','Anbieter / Angebot','CAD-Körperreferenzen','Hinweise / Sperrgrund','Quellen-URLs'],
    rows,[18,8,22,22,40,38,29,14,19,13,13,15,28,40,48,48])
buy.get_range('K6:K53').format.font={'color':blue}
buy.get_range('M6:M53').format.font={'color':blue}
buy.get_range('K6:M53').format.fill='#F4F8FF'
buy.get_range('K6:L53').set_number_format('#,##0.00 "€"')
buy.get_range('L6:L53').formulas=[[f'=IF(ISNUMBER(K{r}),B{r}*K{r},"")'] for r in range(6,54)]
buy.get_range('A6:P53').format.row_height=108
buy.get_range('G6:G53').format.fill=amber
fsh=sheet_table('Fertigung','Sonderteile 08 · mit dem Modell verknüpft',
    'Keine Fertigungsfreigabe: Prozess/Werkstoff/Passungen und Gusslochbilder müssen in freigegebenen Einzelzeichnungen ergänzt werden. Angegebene Rohkörpermaße sind KEINE Zuschnittliste.',
    ['ID','Bauteil','Menge','Prozess','Werkstoff / Entwurf','Grundkörpermaß mm','CAD-IDs','Gates','Hinweise'],
    [[x['item_id'],x['name'],x['quantity'],x['process'],x['material'],x['blank_mm'],x['model_refs'],x['gates'],x['note']] for x in fab],
    [27,40,8,40,32,38,20,17,48])
ash=sheet_table('Aufmass','Istaufmaß · zuerst an der zerlegten Maschine messen',
    'Unbekannt bleibt leer. Foto-/CAD-Annahmen nicht als Messwerte eintragen. Für Lochbilder eine Koordinatenliste oder eine Skizze mit Bezugsflächen verknüpfen.',
    ['ID','Teil','Messaufgabe','Methode / Bezug','Einheit','ISTWERT / Verweis','Datum','Gemessen durch','Beleg / Foto','Gates'],
    [[m['id'],m['part'],m['description'],m['method'],m['unit'],None,None,None,None,' '.join(m['used_by'])] for m in measures],
    [10,28,44,48,10,24,16,22,30,20])
ash.get_range('F6:I34').format={'font':{'color':blue},'fill':'#F4F8FF','wrap_text':True}
bsh=sheet_table('Bearbeitung','Originalteile · Bearbeitung prüfen, nicht voraussetzen',
    'CNC-Bearbeitung ist nicht grundsätzlich zwingend. Maßhaltige Neuteile sind erforderlich; Änderungen am Originalguss müssen erst am realen Bauteil begründet und freigegeben werden.',
    ['ID','Original / Bauteil','Befund im Modell','Mögliche Arbeit','Bearbeitung notwendig?','Muss es CNC sein?','Aufmaß-IDs','Hinweis'],
    [[x[k] for k in ('id','part','finding','possible_operation','machining_needed','cnc_needed','measurements','instruction')] for x in audit],
    [10,32,48,48,37,45,27,48])
bsh.get_range('A6:H13').format.row_height=106
gsh=sheet_table('Freigaben','Prüfschritte und Nachweise',
    'Status nur nach Prüfung mit Beleg ändern. Diese Tabelle erzeugt keine CE-/Sicherheits-/Fertigungsfreigabe. Freigabe erfolgt projektverantwortlich nach nachvollziehbarem Nachweis.',
    ['Gate','Titel','Erforderlicher Nachweis','Status','Beleg','Prüfer'],
    [[g['id'],g['title'],g['required_evidence'],'OFFEN',None,None] for g in gates],
    [10,32,65,20,40,25])
gsh.get_range('D6:D14').data_validation={'rule':{'type':'list','values':['OFFEN','IN PRUEFUNG','NACHWEIS VORHANDEN']}}
gsh.get_range('D6:F14').format.font={'color':blue}
msh=sheet_table('Modell','CAD-Körper → Beschaffungs-/Fertigungsposition',
    'Ein Kaufteil kann mehrere Darstellungskörper besitzen. Zählung erfolgt nach Kaufteil-Instanz, nicht nach Körperzahl. Gruppe18 enthält nur bereitgestellte Sensorsymbole, keine fertig montierten Sensoren.',
    ['CAD-ID','Name','Gruppe','Art','Positions-ID','Kaufteil-Instanz','Quellen','Modellgrenze'],
    [[x[k] for k in ('part_id','name','group','kind','item_id','instance','source','note')] for x in mapping],
    [11,44,28,14,40,35,24,52])
qsh=sheet_table('Quellen','Hersteller- und Fachquellen · Stand 30.10.2026',
    'Originalhersteller-CAD wurde nicht beschafft. Vereinfachte Hüllen sind gekennzeichnet. Ein fehlgeschlagener Zeichnungsabruf wird nicht als Sichtprüfung bezeichnet.',
    ['ID','Titel','URL','Prüfumfang / Einschränkung','Abgerufen'],
    [[k,s['title'],s['url'],s['evidence'],s['checked_on']] for k,s in sources.items()],
    [10,45,65,65,16])
qsh.get_range('A6:E25').format.row_height=98
# Engineering sheet: transparent editable assumptions, missing loads stop the calculation.
cal=wb.worksheets.add('Auslegung')
cal.merge_cells('A1:F1');cal.get_range('A1').values=[['Antriebsrechnung · Parameterblatt, kein Leistungsnachweis']]
cal.get_range('A1:F1').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':32}
cal.merge_cells('A2:F4');cal.get_range('A2').values=[['Bewegte Masse, Reib-/Schnittkraft, Trägheit und verfügbares Drehmoment fehlen. 3000 mm/min, 100 mm/s², η=0,90 und Reservefaktor1,5 sind nur editierbare Planungsannahmen. Haltemoment nicht als dynamisches Drehmoment einsetzen.']]
cal.get_range('A2:F4').format={'fill':amber,'wrap_text':True,'row_height':24}
cal.get_range('A6:F6').values=[['Größe','X','Y','Z','Einheit','Bedeutung']]
cal.get_range('A6:F6').format={'fill':teal,'font':{'bold':True,'color':'#FFFFFF'},'row_height':24}
labels={
8:('Spindelsteigung',5,5,5,'mm/U','Planung: isel16×5 /20×5; source S08'),
9:('Motor-/Spindelübersetzung',1,1,1,'1','Direktantrieb'),
10:('Vorschubziel',3000,3000,3000,'mm/min','Nicht bestätigtes Ziel, keine freigegebene Eilgangrate'),
11:('Beschleunigungsziel',100,100,100,'mm/s²','Nicht bestätigtes Ziel'),
12:('Bewegte Masse',None,None,None,'kg','Messen; Werkstück/Spannmittel beiXY einbeziehen'),
13:('Reib-/Losbrechkraft',None,None,None,'N','Bei richtig eingestellter geschmierter Führung messen'),
14:('Axiale Bearbeitungskraft',None,None,None,'N','Aus geplantem Bearbeitungsfall festlegen'),
15:('Rotierende Trägheit am Motor',None,None,None,'kg·m²','Rotor, Kupplung, Schraube auf Motorseite bezogen'),
16:('Wirkungsgrad η',0.9,0.9,0.9,'1','Annahme; Spindel-/Lager-/Dichtungsdaten prüfen'),
17:('Schwerebeschleunigung',9.81,9.81,9.81,'m/s²','NurZ erhält Gewichtskraft'),
18:('Planungsreserve',1.5,1.5,1.5,'1','Annahme, kein Nachweisfaktor einer Norm'),
20:('Motordrehzahl',None,None,None,'1/min','T = dynamisches Drehmoment bei dieser Drehzahl'),
21:('Axialkraft',None,None,None,'N','Trägheit + Reibung + Bearbeitung; Z zusätzlich Gewicht'),
22:('Lastmoment',None,None,None,'Nm','F·p /(2π·η·i)'),
23:('Beschleunigungsmoment',None,None,None,'Nm','J·α am Motor'),
24:('Benötigtes Moment mit Reserve',None,None,None,'Nm','(Lastmoment + Beschleunigungsmoment) × Reserve'),
25:('Dynamisches verfügbares Moment',None,None,None,'Nm','Vom Lieferanten für Spannung/Strom/Drehzahl nachweisen'),
26:('Verhältnis verfügbar / benötigt',None,None,None,'1','Kein umfassender Auslegungsnachweis'),
28:('Prüfstatus','DATEN FEHLEN','DATEN FEHLEN','DATEN FEHLEN','','Keine Aussage aus Haltemoment'),
30:('Eingestellte Impulse je Umdrehung',2000,2000,2000,'Imp/U','Planungswert; tatsächlichen Treiberparameter abgleichen'),
31:('Schrittmaßstab',None,None,None,'Imp/mm','Impulse/U × Übersetzung / Steigung'),
32:('Impulsfrequenz beim Vorschubziel',None,None,None,'Hz','Vorschub/60 × Maßstab')}
for r,row in labels.items():cal.get_range(f'A{r}:F{r}').values=[list(row)]
for c in 'BCD':
    cal.get_range(f'{c}20').formulas=[[f'={c}10/{c}8*{c}9']]
    cal.get_range(f'{c}21').formulas=[[f'=IF(COUNT({c}12:{c}14)<3,"",{c}12*{c}11/1000+{c}13+{c}14'+(f'+{c}12*{c}17' if c=='D' else '')+')']]
    cal.get_range(f'{c}22').formulas=[[f'=IF({c}21="","",{c}21*({c}8/1000)/(2*PI()*{c}16*{c}9))']]
    cal.get_range(f'{c}23').formulas=[[f'=IF(ISNUMBER({c}15),{c}15*({c}11/1000)*(2*PI())/({c}8/1000)*{c}9,"")']]
    cal.get_range(f'{c}24').formulas=[[f'=IF(COUNT({c}22:{c}23)<2,"",SUM({c}22:{c}23)*{c}18)']]
    cal.get_range(f'{c}26').formulas=[[f'=IF(AND(ISNUMBER({c}24),ISNUMBER({c}25),{c}24>0),{c}25/{c}24,"")']]
    cal.get_range(f'{c}28').formulas=[[f'=IF(COUNT({c}24:{c}25)<2,"DATEN FEHLEN","NACHWEIS PRUEFEN")']]
    cal.get_range(f'{c}31').formulas=[[f'={c}30*{c}9/{c}8']]
    cal.get_range(f'{c}32').formulas=[[f'={c}10/60*{c}31']]
cal.get_range('A7:F33').format={'row_height':30,'wrap_text':True,'vertical_alignment':'center'}
for c,w in [('A',43),('B',18),('C',18),('D',18),('E',14),('F',62)]:cal.get_range(f'{c}1:{c}33').format.column_width=w
for r in [10,11,12,13,14,15,16,18,25,30]:cal.get_range(f'B{r}:D{r}').format={'font':{'color':blue},'fill':'#F4F8FF'}
cal.get_range('B8:D32').set_number_format('0.000')
cal.get_range('B28:D28').set_number_format('@');cal.get_range('B28:D28').format.fill=amber
cal.freeze_panes.freeze_rows(6)
print(wb.inspect({'kind':'region','sheet_id':'Start','range':'A6:D14','include':'values,formulas','max_chars':3500}).ndjson)
print(wb.inspect({'kind':'region','sheet_id':'Auslegung','range':'B20:D32','include':'values,formulas','max_chars':3500}).ndjson)
# Presentation/export: all data are drawn from the shared JSON and recipe.
summary.unmerge_cells('A1:H2'); summary.merge_cells('A1:D2')
summary.unmerge_cells('A3:H4'); summary.merge_cells('A3:D4')
summary.get_range('A1:D2').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF','size':18},'vertical_alignment':'center','wrap_text':True}
summary.get_range('A3:D4').format={'fill':amber,'font':{'size':11},'vertical_alignment':'center','wrap_text':True}
for c,width in [('A',28),('B',30),('C',36),('D',36)]:summary.get_range(f'{c}1:{c}24').format.column_width=width
summary.get_range('A6:D7').format.vertical_alignment='center'
summary.get_range('A7:D7').format.font={'bold':True,'size':20}
summary.get_range('A7:D7').format.row_height=36
summary.get_range('A10:D22').format.vertical_alignment='center'
for rr in range(10,15):summary.merge_cells(f'C{rr}:D{rr}')
summary.get_range('E1:H24').clear()
for row,x in enumerate(bom,6):
    ids=[a.split(':',1)[0] for a in x['model_refs'].split(' | ') if a]
    buy.get_range(f'N{row}').values=[[', '.join(ids)]]
    urls=[sources[s]['url'] for s in x['source_ids'].split()]
    buy.get_range(f'P{row}').values=[[urls[0] if urls else None]]
buy.get_range('A6:P53').format.row_height=92
buy.get_range('A6:P53').format.font={'size':10}
buy.get_range('K6:K53').format.font={'size':10,'color':blue}
buy.get_range('M6:M53').format.font={'size':10,'color':blue}
msh.get_range('A6:H440').format.font={'size':10}
msh.get_range('A6:H440').format.row_height=104
fsh.get_range(f'A6:I{5+len(fab)}').format.font={'size':10}
SpreadsheetFile.export_xlsx(wb).save(str(ROOT/'Einkauf/Einkauf_und_Aufmass_08.xlsx'))
