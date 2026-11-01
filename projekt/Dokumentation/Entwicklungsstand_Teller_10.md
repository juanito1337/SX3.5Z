# Entwicklungsstand10: Teller, Spannpaket und Spaeneabfuhr

Datum: 01.11.2026. Ausgangsrevision: e87f522; Erweiterung auf Branch
`codex/tellerwechsler-20261101`. Exakte ausgefuehrte Quellen sind durch
`ergebnisse/entwicklung/20261101_teller/native_source_hashes.json` belegt.
Aktiver Modellstand: `CNC_UMSETZUNG_10_TELLER`, weiterhin auf der vorhandenen
SX3.5Z-Rezeptbasis09. Keine fremden oder alten CAD-Dateien eingelesen.

## Nutzeranforderung und Ergebnisgrenze

Der Wechsler steht nicht auf dem Tisch. Ein seitlicher Tellerentwurf mit acht
Plaetzen ersetzt die bisherige komplette Tischmagazinoption. Acht Plaetze und
radiale Zustellung sind bearbeitete Entwurfsannahmen, keine vom Nutzer festgelegte
Mindestzahl oder freigegebene Kaufteilabmessungen. Kauf oder Eigenbau sind erlaubt;
eine automatische Spindelspannung ist zwingend gefordert.

**Die automatische Werkzeugspannung ist noch nicht konstruktiv geloest.**
Die drei orangefarbenen Koerper zeigen Anschluss-, Federpaket- und Loeseraum.
Originalspindel SK30/M12 DIN2080 und Gusskopf bleiben unveraendert. BT30-Halter
im Teller sind Schnittstellenreferenzen und passen dadurch nicht automatisch
in die vorhandene Spindel. Kein Greifer, keine Zugstange, Federanzahl, Spannkraft,
Loesehub oder belastbare Kopfaufnahme wurde aus Annahmen fertig ausgelegt.

## Modell, Parameter und Lastpfad

511 Einzelteile in20 Unterbaugruppen;28 neue Teller-/Spannraumteile ersetzen
77 Teile der alten ATC-Option. Neue Parameter: `Teller_Parameter_10.json`;
Definitionen, Herleitung und Validierung: `teller10.py`. Bestehende Nutzerdateien
`Parameter.json`, `CNC_Parameter.json`, `Ausbau_Parameter.json` und
`Detail_Parameter_09.json` wurden nicht ueberschrieben. Historische09-ATC-Parameter
sind fuer die neue Tellergeometrie nicht massgeblich.

| Groesse | Entwurfswert / Herkunft |
|---|---|
| Magazin | 8 Plaetze, Teilkreisradius180mm, Entwurf |
| Parkzentrum | X=-540mm, Y=-260mm, Modellkoordinaten |
| Uebergabehoehe | 370mm, Entwurf; nominaler Kopfbereich290–530mm |
| Radialer Zustellweg | 419,33mm, aus Parkabstand und Teilkreis abgeleitet |
| Standstuetze | Vierkant40x40x3mm auf oberem Gestellholm, Entwurf |
| Tellerplatte | 10mm, Entwurf; Festigkeit und Antrieb offen |
| Dichtkragen | 2mm Blech; endet nominal bei125mm, ueber geneigtem Nassblech |
| Spann-/Loeseraum | Durchmesser80/100mm, Hoehe100/80mm, reine Reserve |

Der Lastpfad fuehrt ueber Fuss, Standstuetze und Konsole zum vorhandenen
Gestellholm. Das duenne Leitblech traegt den Wechsler nicht; es erhaelt eine
Durchfuehrung mit Dichtkragen. Schweiss-/Dichtdetail, Befestigung, Versteifung,
Lasten, Schwingungen und Teleskoplagerung fehlen. Die dargestellte Zustellung
ist eine Bewegungshuelle, kein erhaeltlicher419mm-Antrieb.

Der Spritzschirm bewegt sich in der Hoehenparametrik mit dem Teller. Er besitzt
eine offene Zustellseite und ist keine vollstaendig geschlossene Schutzkapsel.
Gabeln sind Retentionsraum-Entwuerfe, keine nachgewiesenen Haltefedern. Werkzeug-
und Anzugsbolzenzuschlaege im Bericht sind Freiraumannahmen, keine fertige Geometrie.

## Verkleidung und KSS

- Seitliche Leitbleche reichen jetzt bis an die Innenwand; die bisherige2mm-Luecke
  entfaellt im Nennmodell. Hintere Freistellungen bleiben erhalten. Reale Naht,
  Dichtung, Biegeradius und Montagefolge brauchen Detailzeichnungen.
- Schachtlage und vollstaendiger Ruecklaufausschnitt innerhalb der Tankinnenwand
  werden validiert. Zuvor akzeptierte ungueltige Parameter werden abgelehnt.
- Serviceklappe, Griff, Gegenplatte und Befestiger bilden eine gemeinsame
  Demontageeinheit. Der Korbauszugstest entfernt diese gesamte Einheit.
- Fertigungszuordnung betroffener KSS-Teile ist auf Blech korrigiert. Eine
  Blechvorform ist weiterhin nicht automatisch ein nativ konvertiertes Blech.
- **Tankauszug nach hinten ist nicht nachgewiesen:** Der untere hintere Holm
  blockiert ihn. Den Holm nicht ohne Tragwerksentwurf entfernen.
- Senktuer bleibt erhalten. Abtropfkante, Labyrinthdichtung, Endlagenentwaesserung,
  Spanfang an Teleskopfugen, Fuehrung und Gewichtsausgleich bleiben Detailaufgaben.

## Einkauf und Mengen

Aktueller Katalog bleibt aus Kompatibilitaetsgruenden `Einkauf/Kaufteile_09.json`;
sein Inhalt ist auf10 fortgeschrieben. Aktuell sind die neu erzeugten Dateien
`Einkaufsliste_10.csv`, `Modellzuordnung_10.csv`, `Fertigungsteile_10.csv`,
`Pruefung_10/` und `Werkzeugwechsler/ATC_Schnittstellenstatus_10.json`.
70 Katalogpositionen,144 Fertigungspositionen; Reserven fuer ein komplettes
Spannsystem und ein Tellerpaket sind getrennt von echten BUY-Teilen erfasst.
BT30-Halteranzahl8; entfallene Tischmagazinbefestiger haben aktuelle Menge0.
Historische09-Tabellen/DOCX/XLSX/PDF bleiben unveraendert und sind keine aktuelle
Montageanleitung. Alte09-Dokumentgeneratoren verweigern den neuen Modellstand
ausdruecklich, statt eine scheinbar passende veraltete Anleitung zu erzeugen.

Beschaffungsvergleich: `Werkzeugwechsler/Teller_Spannpaket_Vergleich_10.md`.
Quellen: `Quellen/Quellen_Teller_20261101.json`. Der Nutzerartikel
[1005009887984460](https://de.aliexpress.com/item/1005009887984460.html) ist mangels
auslesbarer Titel-/Variantenangaben noch nicht identifiziert. Historische
AliExpress-Indexpreise sind keine aktuellen Angebote. Kein belegter
Preis-Leistungs-Sieger und keine Bestellung. Ein200mm-Magazinhub aus der
untersuchten HOLRY-Produktfamilie reicht fuer den aktuellen419mm-Entwurf nicht.

## Pruefung und Montagevorbereitung

Rohprotokolle, Befehle, Laufzeit und Quellhashes liegen unter
`ergebnisse/entwicklung/20261101_teller/`; native Lieferdaten werden mit
`cad/README.md` verknuepft. Offline:163 Tests und91 Untertests bestanden.
Separater Tellercheck:552 Schnittpruefungen an acht indizierten Endpunkten gegen
Gusskopf, Frontplatte und Pinolenhuelse ohne Schnittvolumen. Er schliesst die
unpassende gewaehlte Halter-/Originalspindelverbindung bewusst aus; keine
vollstaendige Wechselbahn, Werkstueck-/Spannmittel-/Schutzhaubenpruefung.

KSS-Geometriecheck: Exit1 wegen sechs Schnittvolumen mit unmontierten
IFS206-Referenzkoerpern im Prueffeld (einmal83,29mm3, fuenfmal228,47mm3).
Achsstichproben und Korbauszug ohne Kollision. Diese sechs Referenzbefunde sind
**nicht** die sechs bekannten Maschinenanschluss-Konflikte; beide bleiben offen.
35 fehlende Istmasse sind weiterhin erforderlich.

Ein unabhaengiges Review fand vier Fehler: JSON-Tupel/Listenvergleich bei
Wiedereroeffnung, nicht mitwanderndes Haubendach, zu niedriger Dichtkragen und
inkompatible09-Dokumentgeneratoren. Alle vier wurden reproduziert und korrigiert;
Regressionspruefungen sind Teil der163 Tests. Rezeptvergleich ist jetzt kanonisch.

Vor praktischer Montage:

1. Artikelvariante und vollstaendige gemeinsame Spindel-/Spannpaketzeichnung
   bestimmen; Kopf, Pinole, Durchgang, Lagerbezug und zulaessige Bearbeitung messen.
2. Greifer/Bolzen, Zugstange, Federn, Loesekraft/-hub und lastentkoppelte
   Loeseabstuetzung zusammen auslegen. Spann-/Loese- und Orientierungsnachweis planen.
3. Daraus Halterhoehe, Tellerzustellung und Parkraum neu ableiten. Gesamte Bahn
   mit Spindelpatrone, Werkzeugen, Spannmitteln, Tischhub und Schutzhaube pruefen.
4. Stuetzen-/Teleskopmechanik, Retention und Schutzverschluss fertig zeichnen;
   KSS-Durchfuehrung, Tankwartung und Tuerentwaesserung detaillieren.
5. Erst nach diesen Nachweisen Fertigungs-/Montagezeichnungen und Freigaben
   erstellen. Alle Bau-, Bestell-, Betriebs- und ATC-Freigaben bleiben false.

Neue native PRT belegen CAD-Erzeugung und Persistenz, keine sichere Maschinenfunktion.
