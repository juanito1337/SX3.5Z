# Wechselstellung, beidseitiger Spaenefang und Demontagestand11

> Ausfuehrung mit superpowers:executing-plans, TDD, systematic-debugging und abschliessendem unabhaengigem Review.

**Goal:** Nutzerkorrekturen aus drei markierten NX-Bildern umsetzen und neue native Park-/Wechselbaugruppen liefern.
**Architecture:** Basis10 behalten; ausdrueckliche Demontageliste, vier zusaetzliche geneigte Fangbleche und zwei aus demselben Rezept erzeugte Stellungen. Bestehende Motoren/Gusskoerper/Fuehrungsbaelge bleiben erhalten.
**Tech Stack:** NX2406/Python3.10.15; separate Offline-CadQuery-Pruefung.
**Spec:** Nutzer01.11.: Wechsler bis Spindel, Spaene links/rechts fangen; Originalabdeckungen/Elektroanbauten duerfen entfallen. Rechte Parkseite durch ausdrueckliche Nutzerantwort bestaetigt. Keine Freigabe zur Entfernung von Guss, Antrieben oder benoetigter Elektrik.

## Entscheidungen und Grenzen

- Ausgang7bffcd4; saubere Arbeitskopie, Branch codex/wechselstellung-spaenefang-11, Sicherung unter ergebnisse/entwicklung/20261101_revision11.
- Alternativen: reine Darstellung der bisherigen linken Zustellung loest die Positionsmarkierung nicht; starrer Teller unter der Spindel blockiert Bearbeitung. Gewaehlt: rechts parkender Teller, getrennte ausfahrbare Wechselstellung. Rechte vordere Diagonale ist Entwurfswahl fuer Kopf-/Nachbarhalterfreiheit.
- Vier Fangblech-Vorformen ueber der vorhandenen dichten Sammelwanne, beidseitig als nach hinten fallende Rinnen. Keine behauptete automatische Spanfoerderung oder Abwicklung.
- Originalpanel, alte Blech-Elektrosaeule/Elektrik, Spindelschutz und Riemenhauben entfallen aus neuem Rezept. Fuehrungsbaelge und Motorgehaeuse schuetzen weiterhin im Nassraum; Neu-CNC-Schaltschrank/Aussenpult bleiben.
- Spannpaket bleibt ungeklaert; keine Betriebsfreigabe, keine Hardware oder Lieferantenaktionen.

## Task1: Modell und Darstellung

- [x] RED: alte Anbauten entfernt und aufgelistet, Motor/Guss/Fuehrungsbaelge erhalten; Fangbleche links/rechts mit Gefaelle; echte Werkzeuggeometrie in Wechselstellung auf Spindelachse.
- [x] GREEN: revision11.py fuer Filter/Fangbleche/Posen; Teller nach rechts spiegeln mit passendem Stuetzenloch und validierter Parkhuelle. Neue Layout_Parameter_11.json, alte Nutzerdateien unveraendert.
- [x] Journal mit pose=park/wechsel; eigenstaendiges Wechseljournal, Ausgaben eindeutig benennen. Gemessene native Halterachse/Hoehe in Wechselstellung pruefen.

## Task2: Nachweise und Abgleich

- [x] Offline-Suite sowie KSS-/Teller-Kollisionsstichproben ueber Zustellweg und Tischhub; Befunde explizit dokumentieren, nicht durch Filter verstecken.
- [x] Einkauf/Mengen, Demontageliste, neue11-Berichte und Anleitung gemeinsam fortschreiben; Export nur auf Arbeitskopie.
- [x] Unabhaengiges Review; reproduzierte wichtige Fehler mit RED/GREEN beheben.

## Task3: Native Lieferung

- [x] Geaenderte KSS-/ATC-Journale nativ pruefen, beide Gesamtstellungen neu speichern und jeweils frisch oeffnen.
- [x] Quellhashes, Revision, Befehle, Datum, Umgebung, Exitcodes und Rohprotokolle sichern. Alte CAD-Laeufe erhalten.
- [x] Status/Roadmap/CAD-Einstieg aktualisieren.
- [ ] Git synchronisieren nach Liefercommit.

## Review-Fokus

Rechte Stuetzenlage/Schaltschrankkonflikt; bewegter Teller gegen andere Halter/Spindelkopf; Fangbleche gegen X/Y-Endlagen; entfernte Originalteile vs benoetigte CNC-Funktionen; veraltete Berichte/Posenverwechslung. Teilpruefungen sind keine volle Wechselbahn-/Sicherheitsfreigabe.

## Ledger

Task1: 5 neue Verhaltenstests zuerst fehlgeschlagen, nach Implementierung bestanden.
Gesamtsuite fand gespiegelt selbstschneidende Konsole: Kontur korrekt gespiegelt.
Wegpruefung/Review fanden5 Hauben-Gabelkollisionen aus Stand10. OCP-Regressionstest
mit66,64mm3 rot; Haubenradius220mm und Parkabstand30mm geringer umgesetzt.
Ruling: Zustellwinkel beibehalten, Distanz verkuerzt; vermeidet neue Kopf-Nachbarhalterlage.
Task2:173 Tests +99 Untertests bestanden;9 Wegstichproben/87 BRep-Pruefungen und
552 Endpunktchecks0 Kollisionen. KSS Exit1 nur6 bekannte Sensorreferenzen.
Review unabhaengig; keine weiteren wichtigen Aenderungsfehler. Elektrischer
Funktionsersatz und nicht gepruefte mechanische Grenzen in Anleitung aufgefuehrt.

Task3: Neun native Journallaeufe Exit0; PARK/WECHSEL je454 Parts und17 Gruppen
frisch geoeffnet.19 native Blechkonvertierungen je Lauf,4 neue Fangblechvorformen.
Halterkegelachse/-hoehe nativ gegen nominelle Spindellage gemessen.
