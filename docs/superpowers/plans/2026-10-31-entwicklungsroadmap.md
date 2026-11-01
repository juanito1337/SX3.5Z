# SX3.5Z – Entwicklungsroadmap und Arbeitsprompts

## Fortschritt01.11.2026

R00 erneut nativ fuer10: sieben Journale Exit0,511 Einzelteile/20 Unterbaugruppen
wieder geoeffnet,19 native Blechkonvertierungen;163 Tests +91 Untertests.
R02 teilweise: KSS-Fertigungszuordnung und aktuelle10-Mengen, historischer09-Export
geschuetzt. R07: weiterer Spannsystemvergleich, aber kein ausgelegtes Spannpaket.
R11: Seitenanschluss, Parametergrenzen und Korbauszug korrigiert; Tankauszug offen.
R13: seitlicher8er-Teller als vorlaeufige Raumstudie;552 Endpunktchecks, keine
vollstaendige Wechselbahn. R10 Tuerentwaesserung und Gestellnachweise weiter offen.
Eigenstaendiger Plan: `2026-11-01-teller-spannpaket-kss.md`.
Die nachfolgende Bestandszaehlung und Statusmatrix gelten fuer31.10./Stand09.

Stand: 31.10.2026. Auditbasis: Git `6631f8b`. Gilt fuer das aktive `projekt/`
und die daraus neu erzeugten CAD-Dateien im Git-Projekt. Alte CAD-Dateien an
anderen Orten des Rechners sind nach Nutzerentscheidung ausgeschlossen.

Diese Roadmap ist ein Arbeitsauftrag mit Nachweisgrenzen, keine Konstruktions-
oder Beschaffungsfreigabe. Reihenfolge nach Abhaengigkeiten statt erfundener
Terminzusagen. Das erste Paket wird in diesem Auftrag abgearbeitet; spaetere
Pakete werden nur nach Erfuellung ihrer Eingangsvoraussetzungen abgeschlossen.

## Gepruefter Ausgangsstand

560 native Einzelteile, 20 Unterbaugruppen, eine Hauptbaugruppe; 21 native
Blechkonvertierungen. Dateierzeugung und Wiedereroeffnung sind nachgewiesen.
Das sind weder vollstaendige Fertigungszeichnungen noch eine reale Maschinenabnahme.

Aus den vorhandenen Tabellen neu gezaehlt:

| Gegenstand | Befund | Bedeutung |
|---|---:|---|
| Modellzuordnung | 216 BUY, 131 EXISTING, 157 MAKE, 56 RESERVE | Koerperzahlen; keine Bestellmengen |
| Fertigungspositionen | 148 | 105 nennen fehlende Einzelzeichnung/Abwicklung ausdruecklich |
| Einkauf | 69 Positionen | 29 Kaufteile, 14 Normteile, 26 offene Beschaffungen |
| Messaufgaben | 35 ohne bestaetigten Messwert | Maschinenanschluesse noch nicht auslegbar |
| Grundmaschinenkonflikte | sechs historisch dokumentiert | Keine erneute Kollisionsberechnung in diesem Audit |

157 MAKE-Koerper und 148 Fertigungspositionen sind unterschiedliche Zaehlebenen.
Sechs ATC-Lokatoren nennen fehlende Verdrehsicherung; diese sechs sind nicht
zusaetzlich als ausdruecklich fehlende Zeichnungen gezaehlt.

Quellen: `projekt/Einkauf/Modellzuordnung_09.csv`, `Fertigungsteile_09.csv`,
`Einkaufsliste_09.csv`, `projekt/Aufmass/Messwerte_08.json`,
`Messwerte_09_Zusatz.json`, `uebergabe/BEKANNTE_PROBLEME.json`.
Audit und Rohprotokolle: `ergebnisse/entwicklung/20261031_134859/`.

## Reihenfolge und Status

| ID | Prioritaet | Arbeitspaket | Status / Voraussetzung |
|---|---|---|---|
| R00 | P0 | Journalmatrix und getrennte Offline-Umgebung | Erledigt: sieben Journale Exitcode 0; 112 Tests + 91 Untertests |
| R01 | P0 | Rezept-Hashabweichung diagnostizieren | Ursache nachgewiesen; produktive Referenzmigration offen |
| R02 | P1 | Fertigungsdaten und Nachweisstatus bereinigen | Naechstes ausfuehrbares Softwarepaket |
| R03 | P1 | Messplan auf konkrete CAD-Schnittstellen abbilden | Vorbereitbar; Istwerte vom Nutzer erforderlich |
| R04 | P1 | X-Achse fertig detaillieren | Nach X-Aufmass und Lieferantenanschluessen |
| R05 | P1 | Y-Achse fertig detaillieren | Nach Y-Aufmass und Lieferantenanschluessen |
| R06 | P1 | Z-Achse, Lasten und Spindelenden | Nach Z-Aufmass, Kopfmasse, Motorrevision |
| R07 | P1 | Spindel-/Spannpaket-Variantenentscheidung | Vergleich vorbereitbar; Kopfabmessungen/-masse und Zeichnungen fehlen |
| R08 | P2 | Native Zeichnungen, Abwicklungen und Export | API-Pilot jetzt moeglich; Fertigungsfreigabe nach R02–R07 |
| R09 | P2 | Referenzsensoren, Schmierung, Kabelfuehrung | Nach festgelegten Achslagen und Kaufteilen |
| R10 | P2 | Gestell und zweiteilige Senktuer | Nach Lasten, Segmentmassen und Fuehrungsauswahl |
| R11 | P2 | KSS, Filter, Tank und Wartung | Nach KSS-/Spanart, Durchsatz und Kaufteilen |
| R12 | P2 | Elektrik und LinuxCNC-Simulation | Planung jetzt; Pinbelegung nach Geraeterevisionen |
| R13 | P3 | ATC-Mechanik und vollstaendige Wechselbahn | Nach dokumentierter Entscheidung R07 |
| R14 | P3 | Revisionsgleicher Fertigungs-/Montagestand | Nach allen zugehoerigen Detail- und Realnachweisen |

## Gemeinsamer Arbeitsrahmen fuer alle Prompts

Vor jedem Paket AGENTS.md und dessen Pflichtdateien lesen. Nutzerentscheidungen
haben Vorrang vor alten Berichten. `brainstorming` fuer neue Entscheidungen,
`writing-plans` fuer das begrenzte Paket; Codefehler mit `systematic-debugging`
reproduzieren und vor der Korrektur einen fehlschlagenden Test schreiben
(`test-driven-development`). Kleine Aenderungen, Sicherung und keine alten
CAD-Eingaben. `verification-before-completion` vor Abschluss; groessere Aenderungen
mit `requesting-code-review`. Lokale NX-Dokumentation/Journale statt erfundener API.

NX-Journale in echter NX-Laufzeit pruefen, neu speichern und neu oeffnen.
Offline-Tests zusaetzlich, niemals als NX-Nachweis. Blech `required` bleibt aktiv.
Alle Ergebnisse mit Revision, Datum, Befehl, Umgebung, Umfang, Exitcode und
Rohprotokoll unter `ergebnisse/`. Fehlende Voraussetzungen konkret benennen.
Keine Maschinenbewegungen, Ventile, Spindelbefehle oder M6-Ausfuehrung.

Bei konstruktiven Aenderungen gemeinsam aktualisieren: Rezept/Parameter und
Herkunft, Kaufteile, Stueckliste/Mengen, Anleitung, Zeichnungen und Pruefungen.
Modellannahme, Herstellerwert, gemessen und vereinfachte Geometrie bleiben getrennt.
`build_ready`, `purchase_released`, `machine_operation_enabled`, `atc_operational`
bleiben ohne jeweils eigenstaendige Nachweise false.

## R00 – Journalmatrix und reproduzierbare Pruefumgebung

**Befund:** Der vorige Vollaufbau war nativ erfolgreich; die separaten Kern-/ATC-
Einstiegspunkte waren im letzten Arbeitsgang noch nicht einzeln nachgewiesen.
Standard-Python war ueber PATH nur ein Store-Alias.

**Entwicklungsprompt:**
> Pruefe alle sieben aktiven NX-Journale in frischen NX-2406-Prozessen. Nutze
> ausschliesslich aktuelle Projektdateien und neue Laufordner. Erfasse Exitcodes,
> Teilemanifeste und die erneute Oeffnung der neu erzeugten Gesamtbaugruppe.
> Richte eine getrennte lokale .venv ein und fuehre Paketpruefer, Hilfstests und
> die vollstaendige aktive pytest-Suite aus. Reproduziere Fehler vor Aenderungen;
> verstecke weder fehlende Abhaengigkeiten noch skips. Erhalte historische Nachweise.

**Lieferung/Abnahme:** Journalmatrix und Rohprotokolle fuer Metadaten, Blech, KSS,
Umbau-Kern, Normteile/ATC, Gesamtaufbau und Wiedereroeffnung; keine fehlenden
Komponenten. Aussage nur ueber den geprueften Stand. Ergebnis in
`docs/superpowers/plans/2026-10-31-journalpruefbericht.md`.

## R01 – Stabile Nachweisidentitaet ohne Geometrieaenderung

**Befund, diagnostiziert:** `nx_geometry.py:20` hasht ungerundetes Rezept-JSON.
`modell_v4.py:381`, `:425`, `:547` schreibt sin/cos-Ergebnisse in Formeln.
Historischer Hash und echter NX-Hash sind aus denselben Quelldateien durch
unterschiedliche Rechenpfade reproduziert. 49 Zahlenabweichungen in fuenf Teilen;
maximale ausgewertete Laengendifferenz 2,84e-14 mm. Parameter identisch.

**Entwicklungsprompt fuer die noch offene Umsetzung:**
> Entwirf einen versionierten, plattformstabilen Nachweis-Fingerprint getrennt
> vom unveraenderten Geometrierezept. Verwende unter
> ergebnisse/entwicklung/20261031_134859/ die Dateien recipe_nx310.json und
> hashdiagnose/recipe_historical_reconstructed.json als Regression. Erhalte
> den historischen exakten Hash und zeige jeden Normalisierungsschritt. Tests
> muessen reine numerische Darstellungsabweichungen erkennen, echte Aenderungen
> an Parametern, Formeln, Operationen, Teilidentitaeten und Geometrie aber ablehnen.
> Aktiviere den alten Referenzvergleich nicht allein durch Hash-Angleichung;
> erzeuge/validiere einen neuen unabhaengigen Referenznachweis und pruefe nativ.

**Abnahme:** dokumentierte Identitaetsregel mit Negativtests, kein globales
FMA-Umschalten, keine Rundung des eigentlichen Modells, keine Lockerung nativer
Geometrietoleranzen. Bis dahin bleibt die bestehende Sperre wirksam.

## R02 – Fertigungsmetadaten und aktuelle Nachweise

**Befund:** `umbau_daten08.py:36–57` bestimmt Verfahren/Werkstoff teilweise aus
Namen. KSS-Ruecklaufkasten-Stirnwand, Tank und Tankdeckel werden als Fraesteile
mit allgemeinem S355-Haltertext ausgegeben. `umbau_daten09.py:21` liefert
`native_nx_run_this_revision=False` fest; dieser Planungsexport ist kein aktuelles
Laufregister. Diese Probleme durch Quellenzuordnung beheben, nicht durch Freigabeflags.

**Entwicklungsprompt:**
> Reproduziere die fehlerhaften Fertigungszuordnungen in Tests. Fuehre explizite
> Fertigungsmetadaten fuer die betroffenen Teile ein: Verfahren, Materialstatus,
> Blechdicke, Zeichnungsstatus und Quelle. Leite keine bestaetigte Guete aus
> einem Farbnamen ab. Exportiere auf einer Arbeitskopie und pruefe CSV/JSON-
> Differenzen sowie Mengen gegen den unveraenderten Modellstand. Ergaenze ein
> revisionsgebundenes Laufregister neben historischen Berichten; lies native
> Nachweise, setze Betriebs-/Beschaffungsfreigaben niemals automatisch.

**Abnahme:** falsche Standard-Fraeszuordnung behoben, Mengen unveraendert,
unbekannte Werkstoffe explizit unbekannt, aktuelle Nachweise ohne Widerspruch
auffindbar. Betroffene Excel-/Anleitungsinhalte synchronisieren oder veraltet markieren.

## R03 – Messplan und Herkunft der Anschlussparameter

**Befund:** 35 leere Aufgaben; M09-02 buendelt mehrere Kopf-/Spindelmasse in
einem Eintrag (`Aufmass/Messwerte_09_Zusatz.json`). Zuordnung auf Mess-ID,
Parameter, Part und Bezugsflaeche muss detaillierter werden.

**Entwicklungsprompt:**
> Erstelle aus dem aktuellen Git-CAD eine Messmatrix mit Bezugsskizzen und
> Mess-ID → Parameter → betroffene Parts/Verbindungen. Zerlege Sammelaufgaben
> in eindeutig messbare Groessen. Erfasse Einheit, Bezug, Messmittel, Unsicherheit,
> Datum, Bearbeiter und Quellenbeleg. Lasse reale Werte leer, bis der Nutzer sie
> liefert. Pruefe Eingabefehler und widerspruechliche Werte; keine automatische
> Uebernahme von Fotoannahmen als Istmass. Priorisiere die sechs Anschlusskonflikte.

**Abnahme:** jede geforderte Messung praktisch ausfuehrbar und nachvollziehbar;
Original-CAD-Import ist nicht Voraussetzung. Reale Messung bleibt Nutzerarbeit.

## R04 – X-Achse

**Befund:** Mutteraufnahme kollidiert mit Tisch/Sattel, Spindelhuelle mit Sattel.
Gussseitige Befestigung fehlt (`cnc_ansichtsmodell08.py:151`); Loslager-Lastabtrag
ist offen (`:170`).

**Entwicklungsprompt:**
> Schließe die X-Masskette anhand X01–X07 und belegter Lager-/Spindeldaten.
> Detailliere Mutterhalter, Fest-/Loslageranschluss, Schrauben, Gewindeeingriffe,
> Montagezugang und reale Hubreserven. Loese jede der drei X-Ueberschneidungen
> oder belege sie als Rekonstruktionsabweichung. Originalbearbeitungen nur mit
> gemessener Wandstaerke und Zeichnung. Pruefe nativ End- und Zwischenstellungen;
> aktualisiere Bearbeitungsmatrix, Fertigungsteile, Stueckliste und Montagefolge.

**Abnahme:** geschlossene Befestigungs-/Lastkette, dokumentierte Kollisionspaare
und freier Nutzweg; kein Abtragen von Guss nach Fotoannahme.

## R05 – Y-Achse

**Entwicklungsprompt:**
> Bearbeite Y01–Y07 wie R04 fuer die Y-Achse. Loese Spindelhuelle gegen Basis
> anhand realer Innenkontur und Wandstaerke. Detailliere Mutterzugang, Lager-
> anschluesse und Montage von unten/innen. Pruefe den gesamten vorgesehenen Hub
> mit benachbarten X-Teilen, Abdeckungen und Schmierleitungen. Synchronisiere
> Rezept, Parameterherkunft, Zeichnung, Stueckliste und Montageanleitung.

**Abnahme:** gemessene Anschlussflaechen, tragfaehige Verbindung, belegte
Freistellung oder alternative Konstruktion; keine angenommene Fraestiefe.

## R06 – Z-Achse, Spindelsaetze und Antriebsauslegung

**Befund:** Z-Adapter/Spindel schneiden oberes Saeulenblech; Kopfmasse und
Z-Motorrevision offen. Spindelzapfen sind Huellen ohne vollstaendige Nut-/Sitz-
ausarbeitung (`cnc_ansichtsmodell08.py:173–177`).

**Entwicklungsprompt:**
> Klaere Z01–Z09 und die genaue Motorrevision. Rechne Lastfaelle fuer Reibung,
> Schnittlast, Beschleunigung, Drehzahl/Drehmoment, Spindelknickung, kritische
> Drehzahl, Lager und Kupplung. Trenne Z-Absturzschutz von Motorhaltebremse.
> Detailliere tragende Z-Anschluesse und fuer alle Achsen die Spindelenden mit
> Schultern, Sitzen, Gewinden, Sicherung, Vorspannung und Laengenausgleich.
> Verwende Lieferantenzeichnungen; nominale Huelllaengen sind keine Bestelllaengen.

**Abnahme:** nachvollziehbare Last-/Massketten, native Anschlusspruefung,
vollstaendige Endenzeichnungen; keine Bestellung ohne Artikel-/Revisionsbezug.

## R07 – Spindel und automatische Spannung entscheiden

**Entwicklungsprompt:**
> Vergleiche Original-SK30/M12-Umbau und komplette BT30-ATC-Patrone anhand der
> Messmatrix aus R03 und echter Herstellerzeichnungen. Stelle Schnittstellen,
> Kraftfluss, Spann-/Loesehub, Lagerabstuetzung, Kopfanschluss, Masse, Drehzahl,
> Motorweiterverwendung und Orientierung gegenueber. Dokumentiere benoetigte
> Originalbearbeitung und verbleibende Risiken. Fuehre keine Lieferantenanfrage
> ohne Auftrag aus. Lege die Entscheidung dem Nutzer mit konkreten Varianten vor.

**Abnahme:** eine begruendete Nutzerentscheidung mit belastbarer Einbaugrundlage.
BT30 bleibt bis dahin Untersuchungsoption; keine umetikettierte DIN2080-Schnittstelle.

## R08 – Native Zeichnungen, Abwicklungen, STEP/PDF/DXF

**Befund:** Native Parts vorhanden; keine entsprechende aktive Export-/Drafting-
Implementierung im Pythonbestand gefunden. 21 Blechkonvertierungen bedeuten
keine 21 geprueften Abwicklungen.

**Entwicklungsprompt:**
> Baue einen kleinen NX-2406-API-Piloten fuer ein Fraesteil, ein konvertiertes
> Kantblech und eine geneigte Blechvorform. Nutze lokale Dokumentation und
> aufgezeichnete Journale. Erzeuge native Zeichnungen mit Ansichten/Schnitten,
> Bemaßung und Entwurfskennzeichnung; untersuche echte Abwicklung getrennt von
> der Vorform. Exportiere STEP sowie passende PDF/DXF und oeffne die Ergebnisse
> zur visuellen und maßlichen Kontrolle. Erst nach Pilotabnahme auf die
> 148 Fertigungspositionen ausdehnen; Toleranzen und Werkstoffe nicht erfinden.

**Abnahme:** reale gespeicherte/geoeffnete Zeichnungen und Exporte, pro Teil
eindeutiger Status; keine unbestätigte Kontur als Fertigungs-DXF ausgeben.

## R09 – Sensoren, Schmierung und bewegte Versorgung

**Befund:** IFS206 stehen im Prueffeld (`cnc_ansichtsmodell08.py:230–232`),
noch ohne Achshalter; Schmierung und Schleppketten sind offene Pakete.

**Entwicklungsprompt:**
> Integriere jeden Referenz-/Grenzsensor funktional an einer festgelegten Achse:
> Halter, Betaetiger, Einstellbereich, Schalt-/Ueberlaufraum und Stecker. Plane
> Schmierstellen, Kabel, Schlaeuche, Biegeradien, Befestigungen und bewegte
> Schutzteile mit Wartungszugang. Pruefe die Hüllen nativ ueber den Hub und
> ergaenze alle Nebenartikel in der Stueckliste. Keine reale Referenzfahrt.

**Abnahme:** alle Sensoren zugeordnet, Versorgung ohne unzulaessige Biegung/
Kollision, Montage-/Wartungsweg vorhanden; I/O-Simulation getrennt vom Betrieb.

## R10 – Gestell, Senktuer, Scheiben und Dichtungen

**Befund:** Tuerkinematik ohne ausgelegte Kopplung/Fangsicherung;
Gasfedern sind Bauräume (`cnc_ansichtsmodell07.py:358–403`, `blech06.py:48`).

**Entwicklungsprompt:**
> Detailliere nach D01/D02 Gestell, Maschinenauflage und zweiteilige nach unten
> oeffnende Tuer. Waehle belegte Fuehrungen, Kopplung, Gewichtsausgleich und
> Fangsicherung; rechne Massen, Reibung, Temperatur-/Kraftstreuung und Fehlerfaelle.
> Plane Schweißfolge, Ebenheit, Bodenanschluss, Scheibenhalter, Dichtungen und
> Verriegelung. Pruefe Bewegungs-/Wartungsraeume nativ. Aendere die akzeptierte
> Oeffnungsrichtung nicht ohne Nutzerentscheidung.

**Abnahme:** Detailzeichnungen und Last-/Kraftnachweise; reale Fang-, Schutz-
und Dichtheitspruefungen separat erforderlich.

## R11 – KSS und Spaene

**Befund:** Pumpenleistung, Feinfilter, Dichtungen/Schweißnähte, Ueberlauf und
Durchsatz offen (`ruecklauf07.py:81–112`).

**Entwicklungsprompt:**
> Erstelle ein vollstaendiges KSS-/Spaenefließschema mit belegter Pumpe, Filter,
> Tankvolumen, Ruecklauf, Entlueftung, Ueberlauf, Reinigung und Wechselzugang.
> Beruecksichtige Spanart, KSS-Vertraeglichkeit und gewuenschten Durchsatz.
> Detailliere Blechanschluesse, Dichtungen, Ablass und Tank-/Korbausbau, ohne
> den Senktuerraum zu blockieren. Aktualisiere die fehlerbereinigten
> Fertigungsmetadaten aus R02 und pruefe Geometrie/Servicebewegung in NX.

**Abnahme:** geschlossener Fließ- und Wartungsweg, ausgewiesene Durchsatz-/Dichtheits-
nachweise; eine Gefaelleskizze ersetzt keinen realen Pumpen-/Filtertest.

## R12 – Elektrik, Versorgung und LinuxCNC-Simulation

**Befund:** Vorlaeufige DC-Versorgung ohne fertige Rueckspeisebegrenzung,
24-V-Lastbilanz und Schutzplanung offen; produktive Pinbelegung nicht belegt
(`Einkauf/Kaufteile_09.json`, G06/G07 in `Pruefung_08/Freigaben.json`).

**Entwicklungsprompt:**
> Erstelle I/O-, Funktions-, Leistungs-/Rueckspeise-, Klemmen-, Kabel-, PE- und
> Waermeplan aus exakten Geraeterevisionen. Pruefe Pegel, Isolation, Bremslast,
> Fehlerausgaenge und Fehlerzustaende. Lege danach eine explizit hardwarefreie
> LinuxCNC-Simulation fuer Achsskalierung, Zustandslogik und Verriegelungen an.
> Keine Mesa-Verbindung, keine realen Pin-/Spindel-/Ventilbefehle und kein
> automatisches Aktivieren eines Maschinenprofils. Unbekannte Pins bleiben offen.

**Abnahme:** jedes Signal hat Quelle, Senke, Pegel, Anschluss und Fehlerverhalten;
Simulationsprotokolle; reale Elektropruefung durch geeignete Fachperson bleibt offen.

## R13 – ATC nach ausgewaehlter Spindel

**Befund:** automatische Spannung fehlt; 620×100-mm-Magazin, nur nominale
16,6-mm-Rueckzugsreserve; Halternut/Bolzen/Retention/Indexierung und Kegelschutz
offen (`Werkzeugwechsler/ATC_Schnittstellenstatus_09.json`).

**Entwicklungsprompt:**
> Integriere ausschliesslich das in R07 beschlossene System mit Hersteller-
> zeichnungen. Detailliere Zug-/Loesemechanik, Kraefte, Sensorik, Orientierung,
> Halter/Bolzen, Retention, Verdrehsicherung, Kegelschutz und Stoerungsbergung.
> Pruefe komplette Wechselwege aller Taschen inklusive Zielhalter, Werkzeug,
> Werkstueck und Spannmitteln in NX; Endpunktpruefung allein reicht nicht.
> Erstelle den Ablauf zunaechst als hardwarefreie Zustands-/Fehlersimulation.

**Abnahme:** nachvollziehbare mechanische und funktionale Nachweise. Reale
Wechslerabnahme gesondert; kein betriebsfaehiges M6 aus geschaetzten Koordinaten.

## R14 – Gemeinsamer Lieferstand und Montagefolge

**Entwicklungsprompt:**
> Fuehre die abgeschlossenen Teilpakete zu einem revisionsgleichen Lieferstand
> zusammen: native Baugruppe/Einzelteile, Parameterherkunft, Kaufteile mit Mengen,
> Fertigungszeichnungen, Abwicklungen, Exporte, Elektrik und Montage-/Pruefanleitung.
> Pruefe Bauteil-/Artikel-/Zeichnungszuordnung, Montagezugang, alle kritischen
> Bewegungen, Toleranzketten und die noch offenen Gates. Trenne Software-, CAD-,
> mechanische und reale Betriebsnachweise. Liste Restpunkte ohne grüne Ersatzbehauptung.

**Abnahme:** keine widerspruechlichen Revisionen oder unmarkierten Annahmen;
Freigaben nur fuer den tatsaechlich belegten jeweiligen Umfang.

## Fortsetzungsregel

Als naechstes R02 begrenzt ausarbeiten; R03-Messvorbereitung kann unabhaengig
folgen. R04–R07 erst mit ihren Eingaben. API-Pilot R08 darf parallel zur
Messvorbereitung geplant werden. NX-Lizenz/Sitzung nur seriell nutzen.
Nach jedem Paket Status, Nachweise und naechsten ausfuehrbaren Prompt hier
aktualisieren. Ein offenes Paket ist kein erledigtes Projektziel.
