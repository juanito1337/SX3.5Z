# Tellerwechsler, Spannpaket und KSS â€“ Ausfuehrungsplan

> **For agentic workers:** Use superpowers:executing-plans task by task; TDD and a final independent review are required.

**Goal:** Tischmagazin durch einen ausserhalb des Tisches getragenen Tellerentwurf ersetzen, automatische Spindelspannung als zwingende Schnittstelle behandeln, belegte KSS-Fehler beheben und neue native NX-Dateien erzeugen.

**Architecture:** Vorhandenes aktives Rezept und bewaehrte NX-Primitiven erhalten. Neue Entwurfsbauteile und Parameter gesondert kennzeichnen; keine Herstellergeometrie aus unbestaetigten Bildern erfinden. Code, Parameterherkunft, Einkauf, Fertigung und Anleitung gemeinsam fortschreiben.

**Tech Stack:** NX2406 / NX Open Python3.10.15; separate .venv Python3.12.14/CadQuery fuer ergaenzende Offlinepruefung.

**Spec:** Nutzerauftrag01.11.2026: kein Tischmagazin; Teller, Kauf oder Eigenbau; kein vorgegebenes Budget, Spannpaket zwingend. Nutzerkandidat AliExpress1005009887984460 ist noch nicht identifiziert. Lieferantenrecherche und konkrete Entwurfsentscheidungen werden im zugehoerigen Entwicklungsbericht dokumentiert.

## Grenzen und Ausgangssicherung

- Basis e87f522; sauberer Ausgangsstand auf Branch codex/tellerwechsler-20261101.
- Arbeitsort bleibt der vom Nutzer verlangte Git-Ordner. Sicherung der Projektquellen und Parameterhashes unter ergebnisse/entwicklung/20261101_teller/.
- Baseline:112 Tests und91 Untertests bestanden. Keine globale/NX-Python-Aenderung.
- SK30/M12 ist keine automatische BT30-Schnittstelle. Spannpaket-/Patronenentscheidung und reale Kopfmasse fehlen.
- Neue .prt in neuem Laufordner. Blechmodus required. Keine Hardware, Bestellungen oder Lieferantenkontakte.
- Unbelegte Kaufteilgeometrie nur als RESERVE/Einbauraum, keine Fertigungs-/Betriebsfreigabe.

## Task1: Recherche und ATC-Entwurf

- [x] Drei AliExpress-Tellerkandidaten und passende technische Primaerquellen recherchieren; aktuelle Preise/Lieferumfang und historische Indexwerte trennen.
- [ ] Nutzerkandidat1005009887984460 identifizieren: Titel/Variante weiterhin fehlen.
- [x] Spannpaketoptionen vergleichen; fehlende Angaben offen markieren. Funktionale Auslegung bleibt offen.
- [x] Radial-/Schwenkzustellung, Parkraum, Kopf-Nachbarhalter und Lastpfad bewerten; gewaehlte Entwurfsannahmen schriftlich festhalten.

## Task2: KSS und Verkleidung â€“ belegte Fehler

Dateien: projekt/ruecklauf07.py, projekt/normteile09.py, projekt/tools/pruefen07.py, projekt/umbau_daten09.py; neue Tests unter projekt/tests09/.

- [x] RED: Schacht stand_d1400/chip_outlet_y600 muss abgelehnt werden; tank_d300 muss abgelehnt werden; Standard bleibt gueltig.
- [x] GREEN: vollstaendige Bereichsnegation sowie Ruecklaufloch innerhalb Tankinnenraum pruefen.
- [x] RED/GREEN: seitliche Leitbleche erreichen die Innenwand; hintere Freistellungen bleiben erhalten. Geometrie offline und nativ pruefen.
- [x] RED/GREEN: Serviceklappe samt Griff/Hinterlegung/Schrauben/Scheiben als eine Demontageeinheit behandeln, Korbauszug pruefen.
- [x] Fertigungszuordnung fuer betroffene KSS-Bleche korrigieren; Tankauszug hinterem Holm als offen/blockiert ausweisen.

## Task3: Neues Teller-/Spannpaketrezept

- [x] RED: kein Tischmagazin, keine XY-Tischkopplung der ATC-Gruppe; eindeutige IDs, Originalguss/Spindel nicht unbelegt veraendern.
- [x] Parametrischen Teller mit separater Zustellung und Herkunft/Kaufteilstatus implementieren; Spannsystemstatus und Bauraum dokumentieren.
- [x] Reale Mengen synchronisieren, alte Magazinbefestigungen aus aktueller Menge entfernen; aktuelle Tabellen auf Arbeitskopie erzeugen.
- [x] NX-Wiedereroeffnung auf exakten aktuellen Rezeptumfang statt feste560 Teile binden; Modul-Neuladen/Filter aktualisieren.

## Task4: Abnahme und Lieferung

- [x] Gesamte aktive Offline-Suite; relevante KSS-/ATC-Geometriepruefungen mit klaren Ausschluessen.
- [x] Native Teiljournale, Gesamtjournal, frisches vollstaendiges Wiedereroeffnen; Fehler nach systematic-debugging beheben.
- [x] Neue native .prt-Dateien, Parameter, Quellrevision/Hashes, BOM und Rohprotokolle gemeinsam liefern.
- [x] Unabhaengiges Review und Dokumentstatus/Roadmap fortschreiben.
- [x] Git-Liefercommit4862e97 erstellt: Quellen0adcfb4,535 native PRT und Pruefnachweise versioniert.

## Review-Fokus

Unbestaetigte Liefermasse/Preisvarianten; Werkzeughalter-Kopf-Kollisionen bei Zustellung;
Parkraum gegen vollen Tischhub; KSS-Randanschluss und Tankwartung; veraltete Tabellen
oder konstante560-Teile-Pruefung. Native Erzeugung ist keine Maschinenfreigabe.

## Fortschrittsprotokoll

01.11: Audit und Baseline abgeschlossen. AliExpress-Direktzugriff blockiert; keine Umgehung.
Nutzer hat Eigenbau zugelassen und Spannpaket als zwingend benannt. KSS-Gegenbeispiele
sind reproduziert; zuerst diese eindeutig begrenzten Korrekturen, waehrend Artikelidentitaet geklaert wird.

## Ergebnis01.11.2026

163 Tests +91 Untertests bestanden. Native Matrix: siebenmal Exit0;511 Einzelteile,
20 Unterbaugruppen,19 native Blechkonvertierungen; alle511 Parts frisch geoeffnet.
Vier Reviewfehler mit Gegenbeispielen korrigiert. Vollstaendige Rohdaten unter
ergebnisse/entwicklung/20261101_teller/, native Nachweise im Lieferordner.

KSS-Offlinecheck bleibt Exit1 wegen6 unmontierter Sensorreferenzen; Achsstichproben
und Korbauszug0 Kollisionen.552 begrenzte Teller-Endpunktchecks0 Kollisionen.
Keine Freigabe der ganzen Wechselbahn. Bekannte6 Maschinenanschluss-Konflikte,
35 Istmasse, Tankauszug, Tuerdetails und auskonstruiertes Spannpaket bleiben offen.
HTML erzeugt; eingebetteter Browser blockiert lokale Datei-URL, Sichtpruefung offen.
Nutzerartikel nicht identifiziert, kein bestaetigter Preis-Leistungs-Sieger.

Die erledigten Kaestchen betreffen das begrenzte Entwurfs-/Softwarepaket; sie
bezeichnen weder einen betriebsfaehigen ATC noch ein fertiges Spannpaket.
