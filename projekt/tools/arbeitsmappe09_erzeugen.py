"""Normal Python + artifact_tool only. Shared09 catalog -> consolidated planning workbook."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as model,umbau_daten09 as ud
from artifact_tool import Workbook,SpreadsheetFile
wb=Workbook.create();p=model.load_parameters(ROOT/'Parameter.json');ds=model.recipe();b=ud.bom_rows(ds,ROOT);sources=ud.sources(ROOT);fab=ud.manufacturing_rows(ds,p,model);mapping=ud.model_map(ds)
measures=json.loads((ROOT/'Aufmass/Messwerte_08.json').read_text())['measurements']+json.loads((ROOT/'Aufmass/Messwerte_09_Zusatz.json').read_text())['measurements']
gates=json.loads((ROOT/'Pruefung_08/Freigaben.json').read_text())['gates']+json.loads((ROOT/'Pruefung_09/Freigaben_09.json').read_text())['gates']
leads=json.loads((ROOT/'Werkzeugwechsler/AliExpress_Suchtreffer_09.json').read_text())['leads'];atc=model.atc_report(p)
navy='#17354B';teal='#117C83';pale='#EAF2F5';amber='#FFF0D6';blue='#1454B7'
def col(n):
 s=''
 while n:n,r=divmod(n-1,26);s=chr(65+r)+s
 return s

def table(name,title,sub,headers,rows,widths,height=70):
 sh=wb.worksheets.add(name);last=col(len(headers));end=5+len(rows)
 sh.merge_cells(f'A1:{last}1');sh.get_range('A1').values=[[title]]
 sh.get_range(f'A1:{last}1').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':32}
 sh.merge_cells(f'A2:{last}3');sh.get_range('A2').values=[[sub]];sh.get_range(f'A2:{last}3').format={'fill':pale,'wrap_text':True,'row_height':24}
 sh.get_range(f'A5:{last}{end}').values=[headers]+rows
 sh.get_range(f'A5:{last}5').format={'fill':teal,'font':{'bold':True,'color':'#FFFFFF'},'wrap_text':True,'row_height':32}
 if rows:
  sh.get_range(f'A6:{last}{end}').format={'wrap_text':True,'row_height':height,'vertical_alignment':'top'}
  sh.tables.add(f'A5:{last}{end}',True,'T09_'+name)
 for i,w in enumerate(widths,1):sh.get_range(f'{col(i)}1:{col(i)}{end}').format.column_width=w
 sh.freeze_panes.freeze_rows(5);return sh

s=wb.worksheets.add('Start');s.get_range('A1:H24').format.column_width=16
s.merge_cells('A1:H2');s.get_range('A1').values=[['SX3.5Z | Umsetzung 09 – Normteile und ATC-Option']];s.get_range('A1:H2').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':26}
s.merge_cells('A3:H4');s.get_range('A3').values=[['30.10.2026 · KONSTRUKTIONS-/ANFRAGESTAND. Das Magazin macht die originale SK30/M12-Spindel NICHT automatisch wechselbar. Keine Bestell-, Fertigungs- oder Betriebsfreigabe.']];s.get_range('A3:H4').format={'fill':amber,'wrap_text':True,'row_height':28}
end=5+len(b);me=5+len(mapping);ae=5+len(measures)
for rg,title,form in [('A6:B6','Beschaffungspositionen',f'=COUNTA(Einkauf!A6:A{end})'),('C6:D6','Neue Norm-/Kaufteile','=COUNTA(Neu09!A6:A18)'),('E6:F6','CAD-Einzelkörper',f'=COUNTA(Modell!A6:A{me})'),('G6:H6','Fehlende Istaufmaße',f'=COUNTBLANK(Aufmass!F6:F{ae})')]:
 s.merge_cells(rg);a=rg.split(':')[0];s.get_range(a).values=[[title]];r7=rg.replace('6','7');s.merge_cells(r7);s.get_range(a.replace('6','7')).formulas=[[form]]
s.get_range('A6:H7').format={'fill':pale,'font':{'bold':True},'wrap_text':True,'row_height':32}
for r,l,t in [(10,'ATC-Stand','Sechsplatz-Tischmagazin; automatische Spindelspannung, Indexierung und Abdeckung fehlen.'),(12,'Flächenbedarf','620 × 100 mm auf dem 740 × 180 mm Tisch. Deutlich reduzierte Spannfläche.'),(14,'AliExpress','Historische USD-Indexpreise stehen getrennt in ATC_Suche. Keine bestätigten Liveangebote.'),(16,'Modellbindung','69 Beschaffungspositionen; Kaufmengen über Instanzen, nicht über Darstellungskörper zählen.'),(18,'Konstruktion','Bestehende Tür und Gusskörper unverändert; drei Servicegriffe und zwei Kabeleinführungen ergänzt.'),(20,'NX-Ausführung','Journal erzeugt native Dateien lokal. Revision09 hier NICHT in Siemens NX ausgeführt.'),(22,'Datenquelle','Kaufteile_09.json + Rezept; Auftragspreise und Istmaße bleiben bis zur Bestätigung leer.')]:
 s.merge_cells(f'A{r}:B{r+1}');s.get_range(f'A{r}').values=[[l]];s.merge_cells(f'C{r}:H{r+1}');s.get_range(f'C{r}').values=[[t]]
s.get_range('A10:H23').format={'wrap_text':True,'row_height':22}

urls=lambda ids:'\n'.join(sources[k]['url'] for k in ids.split())
rows=[[x['item_id'],x['quantity'],x['unit'],x['type'],x['article'],x['manufacturer'],x['description'],x['status'],x['model_quantity'],None,None,None,x['option'],urls(x['source_ids']),x['gates'],x['note']] for x in b]
sh=table('Einkauf','Einkauf09 | konsolidiert, keine Bestellfreigabe','Blaue Zellen: bestätigte Angebote eintragen. Mengen enthalten die ATC-OPTION und offene Pakete; keine automatische Bestellsumme aus Indexpreisen.',['ID','Planmenge','Einheit','Art','Artikel / Konfiguration','Hersteller','Bauteil','Status','Modellmenge','EP netto EUR','Positionswert EUR','Anbieter / Angebot','Zuordnung','Quellen-URLs','Gates','Hinweise'],rows,[20,10,10,22,40,24,40,32,12,15,18,32,19,48,16,52],100)
sh.get_range(f'J6:J{end}').format={'font':{'color':blue},'fill':'#F4F8FF'};sh.get_range(f'L6:L{end}').format={'font':{'color':blue},'fill':'#F4F8FF'}
sh.get_range(f'K6:K{end}').formulas=[[f'=IF(ISNUMBER(J{r}),B{r}*J{r},"")'] for r in range(6,end+1)];sh.get_range(f'J6:K{end}').set_number_format('#,##0.00 "€"')
s.merge_cells('A25:D25');s.get_range('A25').values=[['Summe bestätigter Preisfelder (kein Vollbudget)']];s.merge_cells('E25:H25');s.get_range('E25').formulas=[[f'=IF(COUNT(Einkauf!J6:J{end})=0,"",SUM(Einkauf!K6:K{end}))']];s.get_range('A25:H25').format={'fill':pale,'wrap_text':True,'row_height':30};s.get_range('E25').set_number_format('#,##0.00 "€"')
new=[x for x in b if x['item_id'].startswith(('K09','N09'))]
table('Neu09','Neue Norm-/Kaufteilkonfigurationen','Reale Artikel bzw. Normkonfigurationen; genaue Lieferrevision, Material und Verwendungsprüfung weiterhin bestätigen.',['ID','Menge','Artikel','Einbau / Bauteil','Option','Modellkörper','Quellen','Modellgrenze'],[[x['item_id'],x['quantity'],x['article'],x['description'],x['option'],x['model_bodies'],urls(x['source_ids']),x['note']] for x in new],[20,9,40,38,18,12,48,56],100)
table('ATC_Suche','AliExpress | Suchhinweise, keine freigegebenen Angebote','Indexpreise beziehen sich nicht zwingend auf die benötigte Variante. Versand, Steuern, Rückgabe und Vollständigkeit ungeprüft. KEINE technischen Maße aus diesen Indexseiten.',['ID','Bezeichnung','Artikel-ID','Indexpreis USD','Preisstand','AliExpress-Link','Indexbeleg','Bewertung'],[[x['id'],x['label'],x['article_id'],x['historical_price_usd'],x['price_date'],x['url'],x['evidence_url'],x['assessment']] for x in leads],[15,44,23,16,16,49,49,62],115).get_range('D6:D9').set_number_format('0.00 "USD"')
g=wb.worksheets.add('ATC_Raum');g.get_range('A1:F29').format.column_width=22;g.merge_cells('A1:F1');g.get_range('A1').values=[['ATC-Wechselraum | nominelle Rechnung, keine reale Bahnfreigabe']];g.get_range('A1:F1').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':32};g.merge_cells('A2:F3');g.get_range('A2').values=[['Werte in mm; Maschinenbezug = Modellbasis, NICHT Boden. Keine Eingabe für Maschinensteuerung. Die neue ATC-Spindel kann die Bezugshöhe und Grenzen ändern.']];g.get_range('A2:F3').format={'fill':amber,'wrap_text':True,'row_height':24}
items=[['Größe','Wert','Bedeutung'],['Tischhöhe im Maschinenmodell',model.all_values(p)['table_top_z'],'Nicht die Arbeitshöhe über Boden'],['Bezugshöhe über Tisch',p['atc_gauge_above_table'],'Magazin-Entwurf'],['Haltehöhe des Werkzeughalters',None,'Tisch + Bezugshöhe'],['Halterschaft über Bezug',p['n09_tool_total']-p['n09_tool_projection'],'118,4 − 70 aus Halterkatalog'],['Anzugsbolzenreserve',p['atc_pullstud_allowance'],'30 mm ANNAHME, kein ausgewählter Bolzen'],['Höchste gespeicherte Hülle',None,'Haltehöhe + Schaft + Bolzenreserve'],['Halterprojektion unter Bezug',p['n09_tool_projection'],'70 mm aus Halterkatalog'],['Zusätzlicher Werkzeugüberstand',p['atc_tool_extra'],'35 mm Entwurfsgrenze; reale Werkzeuge messen'],['Freifahrabstand',p['atc_clearance'],'15 mm Annahme'],['Nominelle sichere Querfahrhöhe',None,'Höchste Hülle + Projektion + Werkzeug + Abstand'],['Maximale Bezugshöhe im Bestand',atc['max_gauge_z_mm'],'530 mm rekonstruiertes Modell'],['Nominelle Restreserve',None,'Max. Bezugshöhe − Querfahrhöhe'],['Betriebsfreigabe','GESPERRT','Spannsystem, Orientierung, Bahn und Werkzeuggrenzen fehlen']]
g.get_range('A5:C18').values=items;g.get_range('A5:C5').format={'fill':teal,'font':{'bold':True,'color':'#FFFFFF'}};g.get_range('A6:C18').format={'wrap_text':True,'row_height':33};g.get_range('A5:A18').format.column_width=40;g.get_range('C5:C18').format.column_width=65
for cell,formula in [('B8','=B6+B7'),('B11','=B8+B9+B10'),('B15','=B11+B12+B13+B14'),('B17','=B16-B15')]:g.get_range(cell).formulas=[[formula]]
g.get_range('A21:F27').values=[['Tasche','lokal X','lokal Y','erforderlich X','erforderlich Y','Bezugshöhe']]+[[x['pocket'],x['table_local_x_mm'],x['table_local_y_mm'],x['required_pos_x_mm'],x['required_pos_y_mm'],x['required_gauge_z_mm']] for x in atc['pockets']];g.get_range('A21:F21').format={'fill':teal,'font':{'bold':True,'color':'#FFFFFF'},'wrap_text':True,'row_height':35};g.freeze_panes.freeze_rows(5)
ash=table('Aufmass','Aufmaß08 plus Ergänzungen09','ISTWERT leer bedeutet unbekannt. Fotos, Nominalkatalog und Modellwerte nicht als gemessene Werte eintragen. Einträge dienen dem Rücklauf, keine automatische Freigabe.',['ID','Teil','Messaufgabe','Methode / Bezug','Einheit','ISTWERT / Verweis','Datum','Gemessen durch','Beleg','Gates'],[[x['id'],x['part'],x['description'],x['method'],x['unit'],None,None,None,None,' '.join(x['used_by'])] for x in measures],[12,30,45,52,13,28,16,24,30,20],100);ash.get_range(f'F6:I{ae}').format={'font':{'color':blue},'fill':'#F4F8FF','wrap_text':True}
table('Fertigung','Sonderteile | aktuelle Modellzuordnung','Grundkörperangaben sind keine freigegebenen Zuschnitte. Blechteile brauchen geprüfte Abwicklungen, Biegeradien, Werkstoff und Toleranzen.',['ID','Bauteil','Menge','Prozess','Werkstoff','Modell-Grundkörper mm','CAD-IDs','Gates','Grenzen'],[[x[k] for k in ('item_id','name','quantity','process','material','blank_mm','model_refs','gates','note')] for x in fab],[30,45,9,45,40,42,22,18,55],95)
table('Modell','560 CAD-Körper → Artikel / Sonderteil','Eine reale Kaufteilinstanz kann aus mehreren Darstellungskörpern bestehen. Gewinde und Herstellerdetails sind teilweise vereinfacht.',['CAD-ID','Name','Gruppe','Art','Artikel / Fertigungs-ID','Kaufinstanz','Quellen','Grenzen'],[[x[k] for k in ('part_id','name','group','kind','item_id','instance','source','note')] for x in mapping],[11,44,25,12,38,36,22,64],90)
table('Freigaben','Voraussetzungen | offen bleibt offen','Diese Liste ist ein Nachweisregister, kein automatisches Sicherheits- oder Fertigungsfreigabesystem.',['Gate','Titel','Erforderlicher Nachweis','Status','Beleg','Prüfer'],[[x['id'],x['title'],x['required_evidence'],'OFFEN',None,None] for x in gates],[10,37,70,18,42,24],100)
table('Quellen','Quellenregister | Technik primär, Preise getrennt','Herstellerkataloge belegen Auswahlmaße; Original-CAD nicht beschafft. AliExpress-Indexseiten sind ausschließlich Anfragestartpunkte.',['ID','Titel','URL','Belegumfang / Grenze','Abruf'],[[k,x['title'],x['url'],x.get('evidence',''),x.get('checked_on','2026-10-30')] for k,x in sources.items()],[15,46,66,70,16],105)
# Current base machining matrix plus new non-destructive magazine approach.
audit=json.loads((ROOT/'Aufmass/Bearbeitungsmatrix_08.json').read_text())
rr=[[x[k] for k in ('id','part','finding','possible_operation','machining_needed','cnc_needed','measurements','instruction')] for x in audit]
rr.extend([['M09','Tisch für Magazin','T-Nuten werden genutzt; keine neuen Tischbohrungen','T-Nuten reinigen/vermessen, Neuteil verschrauben','Keine Gussbearbeitung im09-Magazinentwurf','Neuteile auch konventionell herstellbar','M09-01 M09-06','Nicht am Nutgrund verspannen; Magazin erst nach vollständiger Auslegung einsetzen.'],['S09','Originalspindel / Kopf','SK30/M12 manuell ≠ BT30-ATC','Geeigneten neuen Spindelsatz und Kopfadapter auslegen','Noch offen; keine Gussabtragszeichnung','Externe Präzisionsbearbeitung kann nötig werden','M09-02 M09-03','Keinen Zugstangen-/Greiferumbau nach Hüllmodell fertigen.']])
table('Bearbeitung','Originalteile | zusätzlicher Bearbeitungsbedarf','Die sechs bekannten Grundmaschinen-Anschlusskonflikte bleiben offen. Neue Magazinplatte nutzt vorhandene Nuten; ATC-Spindelumbau ist davon getrennt.',['ID','Bauteil','Befund','Mögliche Arbeit','Bearbeitung nötig?','CNC nötig?','Aufmaß','Anweisung'],rr,[12,30,45,45,35,38,25,55],108)
# Formula checks in final Excel caches and visual QA are performed separately.
wb.render({'sheet_name':'Start','range':'A1:H25','scale':1.6}).save(str(ROOT/'Pruefung_09/Arbeitsmappe_Start.png'))
wb.render({'sheet_name':'ATC_Raum','range':'A5:C18','scale':1.4}).save(str(ROOT/'Pruefung_09/Arbeitsmappe_ATC.png'))
SpreadsheetFile.export_xlsx(wb).save(str(ROOT/'Einkauf/Einkauf_und_Aufmass_09.xlsx'))
print(wb.inspect({'kind':'region','sheet_id':s.id,'range':'A6:H7','include':'values,formulas'}).ndjson)
print(wb.inspect({'kind':'region','sheet_id':g.id,'range':'B15:B17','include':'values,formulas'}).ndjson)
