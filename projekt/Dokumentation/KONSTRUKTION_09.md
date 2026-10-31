# Konstruktionsänderungen 09

Die 13-seitige PDF-/Word-Ergänzung und die konsolidierte Arbeitsmappe enthalten die vollständige Beschreibung. Dieses Dokument ist das Änderungsregister.

## Verbindungen

| Verbindung | Ausführung im Modell | Nachweisgrenze |
|---|---|---|
| Stationäre Servicebleche | GN425-NI-12-160-GS, zwei Ø6,6-Durchgänge, 190×30×2 Hinterlegung, M6×16 + ISO7089 | Eingriff 10,4 mm bei 2+2+1,6 mm Stapel; Bogen vereinfacht, Moment/Tragfähigkeit offen |
| Schrankboden | Eigene 120×160×2 Wechselplatte, 90×130 Fensterstudie, sechs M5×16 mit je zwei Scheiben und Mutter | Serien-Flanschplatte und Abdichtung am gelieferten Schrank prüfen |
| Kabelanschluss | 2× LAPP53111020, 2×53119020, 20,5-mm-Durchgang, Lochmitten70 | PA-Verschraubung, keine EMV-Klemme; Gesamtschutzart nicht belegt |
| Magazinfuss | 4× DIN508-12-M10-10, ISO4762 M10×25 10.9, ISO7089 | T-Nut-Istquerschnitt und reale Gewindeeingriffe bestätigen |
| Magazin-Lokatoren | Eigene 56×56×10 POM-Entwürfe, je 2×M5×25, zwei Scheiben/Verbindung und M5-Mutter | Noch keine Verdrehsicherung/positive Halterretention; nicht als reale DES-Gabel ausgegeben |

Die Kaufteile verwenden katalogbezogene Hauptmaße, nicht beschaffte Hersteller-STEP-Dateien. ISO-Gewinde sind nominelle Ersatzgeometrie. Gewindeaufrufe, Passungen und Fertigungstoleranzen werden dadurch nicht ersetzt.

## ATC-Entscheidung

Die Original-SK30/M12-Spindel wird weder umbenannt noch als BT30-Funktionsbauteil ersetzt. Eine räumliche Sechsplatzmagazinoption ist umgesetzt; passende Spindelspannung, Orientierung, Anzugsbolzen, Steuerung und Kegelabdeckung fehlen. Dieses Ergebnis ist kein Komplett-Werkzeugwechsler.

Drei untersuchte Ansätze: Original-SK30 automatisieren (keine belegte Lösung), BT30-Spindelsatz plus einfaches Magazin (als Raumentwurf verfolgt), BT30-Spindelsatz plus gekauftes Karussell/Seitenmagazin (mehr Mechanik/Kosten, Lieferantengeometrie noch offen). Die Wahl der Raumentwurfsrichtung ist eine Bearbeiterentscheidung, keine vom Anwender bestätigte endgültige Bestellung.

Das Magazin mit 620×100 mm Grundfläche beansprucht einen erheblichen Teil des Tisches. Die Endpunktprüfung führte von 70 auf 94 mm Teilung und zu einem gekürzten Rückenschutz. Dieser schützt die freiliegenden Kegel NICHT ausreichend. Typische Werkstücke/Spannmittel müssen als nächstes mit einer verifizierten Spindelgeometrie geprüft werden.

## Originalteilbearbeitung

Guss/Tisch/Kopf/Pinole werden durch diese Revision nicht angebohrt oder ausgefräst. Neue Löcher nur in den eigenen stationären Serviceblechen und der dargestellten Schrank-Wechselplattenstudie. Der tatsächliche ATC-Spindeleinbau kann Präzisionsbearbeitung oder einen neuen Kopfadapter erforderlich machen; hierzu fehlt noch eine verbindliche Schnittstelle.

## Steuerung

Dokumentiert sind die erforderlichen Zustände Stillstand, Orientierung, Werkzeug gespannt/gelöst, Druckluft, Taschenbelegung, Abdeckung und kontrollierte Störungsbergung. Keine reale Sicherheits-/Pinbelegung und kein M6-Makro geliefert. Die Optionen sind auf `machine_operation_enabled=false` und `purchase_released=false` gesetzt.

## Unverändert

49 bewegte Türteile, Originalguss, Werkzeugspindel, Antriebsauswahl08 und bewährte NX-Adapter4.8/07.2/07.3. Alte Prüfprobleme werden nicht durch neue Normteile beseitigt; sechs statische Grundmaschinenkonflikte bleiben bestehen.
