# RATTM-Bildmasse und Produktauswahl – Arbeitsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Den vom Nutzer gewaehlten Artikel1005009887984460 mit den sechs gelieferten Originalbildern, ablesbaren Angaben und erlaubter Maschinenbefestigung nachvollziehbar im Projekt fuehren.

**Architecture:** Belegbilder getrennt vom aktiven Modell sichern. Produktdaten und Katalog verknuepfen; die vorhandene NX-Geometrie11 bleibt als Eigenentwurf gekennzeichnet. Folgende konstruktive Integration auf Basis der Produktdaten wird getrennt beschrieben.

**Tech Stack:** Git, JSON/Markdown/CSV, bestehender Berichtsexport in Arbeitskopie. Kein neuer NX-Code in diesem Arbeitspaket.

**Spec:** Nutzerauftrag01.11.2026: diesen Wechsler vorerst verwenden; direkte Befestigung an der Fraese erlaubt. Rechte Parkseite bleibt verbindlich. Ausarbeitung siehe `projekt/Werkzeugwechsler/RATTM_1005009887984460_Bildauswertung.md`.

## Global Constraints

- Originalbilder bytegleich sichern; keine perspektivische Skalierung als Herstellerzeichnung verwenden.
- Artikelwahl ist belegt; konkrete Werkzeugaufnahme, Lieferumfang und nutzbarer Hub bleiben getrennte offene Angaben.
- Kein Bohren/Abtragen am Guss ohne Istaufmass; kein Hardwaretest, Einkauf oder Lieferantenkontakt.
- Aktive NX-Rezepte/Parameter und bisherige native Lieferstaende unveraendert erhalten.
- Katalog beschreibt die gewaehlte Beschaffungsrichtung und kennzeichnet separat, dass die Modellkoerper noch Eigenentwurf11 sind.

## Review Focus

1.280mm ist Tellerscheibe, nicht Greiferhuelle oder Werkzeugteilkreis.
2.145/88/37mm haben begrenzte Bezugssicherheit; keine erfundenen Lochbilder.
3.SU32X200-S liefert eine Hubhypothese, keinen Nachweis des nutzbaren Magazinwegs.
4.Direkte Maschinenmontage ist erlaubt; feste Saeule ist Bearbeitervorschlag, keine Nutzerfestlegung.
5.Katalogfortschreibung darf keinen neuen nativen NX-Nachweis behaupten oder alte Nachweise ueberschreiben.

## Task1: Belege, Auswahl und synchronisierte Dokumentation

**Files:** neue Bildkopien unter `referenzen/kaufteile/rattm_1005009887984460/`; Produktdaten/Bildauswertung und vorhandene Auswahl unter `projekt/Werkzeugwechsler/`; Katalog `projekt/Einkauf/Kaufteile_09.json`; Quellenregister `projekt/Quellen/Quellen_Teller_20261101.json`; aktuelle Status-/Entscheidungs-/CAD-Einstiegsdateien.

- [x] Sauberen Ausgangsstand2b83f2c feststellen und Arbeitsstand sichern.
- [x] Sechs Bilder kopieren, SHA256 von Quelle und Kopie vergleichen; alle Massangaben nach Quelle/Bezugssicherheit erfassen.
- [x] Auswahl, KatalogpositionO10-TELLER (ein Paket, kein zweiter Wechsler), Quellen und Anleitung aktualisieren.
- [x] Berichtsexport in Arbeitskopie ausfuehren; nur tatsaechlich geaenderte aktuelle Einkaufsliste/Abgleich uebernehmen.
- [x] Belegpfade/Hashes/JSON, Mengen und unveraenderte CAD-Quellen pruefen; Rohprotokoll mit Revision/Datum/Umgebung/Befehl/Exitcode speichern.
- [x] Aenderungen gegen Quellen pruefen, committen und in das bereits autorisierte Git-Repository uebernehmen.

## Nachfolgende konstruktive Integration (noch nicht erledigt)

1. Angebotsvariante und Werkzeugaufnahme bestaetigen. Tatsaechlichen Greiferteilkreis, Aussenhuelle, Aufnahmehoehe, Achslage zum Schlitten, nutzbaren Zustellhub, Betriebsorientierung und Masse belegen.
2. Feste rechte Saeulenkonsole als Vorzugsentwurf mit Gestellmontage vergleichen. Mitfahrender Kopf braucht gesondert eine vertikale Relativbewegung fuer den Werkzeugwechsel; keine solche Bewegung stillschweigend voraussetzen.
3. Parametrisches vereinfachtes Produktmodell aus belegten Massen erstellen; fehlende Masse als Entwurf kennzeichnen. Keine alten Eigenbau-Gabeln zu Herstellergeometrie umetikettieren. Konsole erst mit Anschlussaufmass detaillieren.
4. Park-/Wechselstellung neu berechnen; voller Kopf-/Tischhub, Werkzeuge, Spannmittel und Einhausung pruefen. Alte Gestellstuetze und KSS-Durchdringung erst mit ihrer tatsaechlichen Ablosung entfernen und Wanne schliessen. Beidseitigen Spaenefang erhalten.
5. Modell, Katalog, Mengen, Anleitung und Tests zusammen fortschreiben. NX2406-Journale in neuen Laufordnern ausfuehren und alle neuen Parts erneut oeffnen. Ergebnisse mit Stand11 getrennt vergleichen.

## Ausfuehrungsnotiz

Dieses kleine Paket uebernimmt die ausdrueckliche Produktauswahl und die gelieferten Belege. Es behauptet keine abgeschlossene konstruktive Integration. Keine Produktcodeaenderung, daher keine neuen Implementierungs- oder Schein-NX-Tests. Die automatische Spannung bleibt eigenstaendige Pflichtaufgabe.
