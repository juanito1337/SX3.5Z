# Normteile und ATC-Vorbereitung – Implementation Plan

> Ausführung inline mit executing-plans; keine Subagenten verfügbar.

**Goal:** Nachvollziehbarer Modell-/Beschaffungszuwachs ohne falsche ATC-Freigabe.
**Architecture:** Unveränderte 08-Basis, 09-Erweiterungsmodul, gemeinsamer Artikelkatalog und Berichtexport.
**Tech Stack:** NXOpen Python 3.10 auf Anwenderrechner; Python-Test/Geometrieprüfung separat.
**Spec:** docs/superpowers/specs/2026-10-30-normteile-atc.md

## Global Constraints
Native NX-Journale weiterverwenden. Originaldateien nicht verändern. Keine Fertigungsfreigabe.
## Review Focus
Kaufteilrevision, Schraubenmaßkette, Tischbewegung, falsche Taper-Kompatibilität, Vollständigkeit von Artikelzuordnung.

- [x] Test zuerst: Originalguss/Tür unverändert; eindeutige Artikellinks; ATC blockiert; sechs Plätze erreichbar.
- [x] Neues Modul normteile09.py und Modellwrapper implementieren, Katalog/Parameter zentral ergänzen.
- [x] Neue und geänderte Geometrie unabhängig auf gültige Einzelkörper / wirkende Schnitte prüfen.
- [x] NX-Gesamtjournal sowie Kurzlauftest anschließen; keine neuen ungeprüften NX-APIs.
- [x] Einkaufsdaten, Quellen, Montageergänzung und ATC-Lieferantenanfrage erzeugen.
- [x] Tests, Dokumentrendering, Stücklistenabgleich, ZIP-Integrität ausführen und Grenzen berichten.

Die Aufgaben gelten nur im dokumentierten Umfang als ausgeführt. Native NX-Abnahme, vollständige ATC-Spindelumrüstung und reale Betriebs-/Fertigungsfreigabe sind ausdrücklich NICHT erreicht. ZIP-Prüfung siehe externen Paketbericht.
