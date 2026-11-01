# BT30-Saeulenkonsole12 – Entwurf und Arbeitsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sinnvolle rechte Maschinenbefestigung und Zustellung des ausgewaehlten BT30-Tellers im neuen nativen CAD-Stand darstellen und pruefen.

**Architecture:** `teller12.py` ersetzt die aktive Gestellstuetze und Eigenbautellerscheibe, nutzt bestehende Primitive und bewahrt Kopf/Spindel als Referenz. Bildmasse330x175x22 und280x16 werden uebernommen; Hub200, Werkzeugradius180 und nicht belegte Antriebs-/Greifergeometrie bleiben gekennzeichnete Einbaustudie. Vier Fangbleche bleiben; die alte KSS-Durchdringung entfaellt.

**Tech Stack:** bestehendes NX2406/NXOpen-Python, CadQuery/OCP nur fuer ergaenzende Offline-Pruefungen; Git.

**Spec:** Nutzerpriorisierung01.11.2026: sinnvolle Wechslerbefestigung zuerst; moeglicher BT30-Spindeltausch darf spaeter erfolgen und blockiert das Layout nicht. Rechte Parkseite, kein Tischmagazin, beidseitiger Spaenefang bleiben verbindlich.

## Global Constraints / Entwurfsentscheidung

- Feste Saeulenkonsole rechts als Bearbeiterentwurf: vertikale Z-Relativbewegung zum Magazin bleibt moeglich. Eine mitfahrende Kopfmontage braeuchte eine zusaetzliche Relativachse. Gestellmontage waere eine Alternative, beansprucht hier aber laengere Auskragung und die bisherige Wannenoeffnung.
- Konsole mit Anschlussplatte, Tragplatte und Rippen darstellen; keine neuen Bohrungen/Freistellungen im Originalguss. Lasten, echte Anschlussflaechen und Schrauben bleiben offen.
- Arbeitsannahme200mm Hub, radial schraeg von rechts vorn zur Achse. Parkmittelpunkt aus Werkzeugradius plus Hub ableiten; kein zufaelliger separater Stellwert.
- Grundplatte/Scheibe Bildangabe; fehlende Abstaende/Antriebsvolumina/Greifer als Entwurf. Keine Hersteller-CAD-Identitaet oder Freigabe behaupten.
- Originalspindel weiterSK30-Referenz; BT30 ist Ziel-Schnittstelle. Kein Spindeltausch im Modell aus dem Gedaechtnis. Spannpaket bleibt sichtbar als Reserve.
- Neue NX-Laufordner; Blechmodus required. Gemeinsame NX-Oberflaeche nicht anfassen, nur eigene run_journal-Prozesse.
- Keine Hardwareausfuehrung. Alle Freigabeflags false.

## Review Focus

1.Nominales Erreichen der Achse muss aus real erzeugter Werkzeuggeometrie folgen.
2.Werkzeugradius ist keine aus280mm abgeleitete Herstellerangabe; Unsicherheit sichtbar halten.
3.Konsole/Wechsler duerfen Tisch-/Kopfbewegungen nicht schneiden; beabsichtigte Kaufteil-Innenkontakte getrennt behandeln.
4.Wannenoeffnung und Dichtkragen gemeinsam entfernen, Spaenefang erhalten.
5.Alte11-Nachweise nicht mit neuer12-Quelle pruefen oder ueberschreiben.

## Task1: Modell und verknuepfte Unterlagen

- [ ] Tests fuer200mm-Zustellung, Bildmasse, feste Maschinenkonsole, geschlossene Wanne und falsche Herstellerfreigaben zuerst schreiben; Rotlauf dokumentieren.
- [ ] `projekt/teller12.py`, `Layout_Parameter_12.json` und aktive Modellverdrahtung erstellen. Legacy10/11-Dateien erhalten.
- [ ] Anordnung mit begrenzten Kollisionspruefungen verbessern; echte Fehler reproduzieren und vor Fix diagnostizieren.
- [ ] Bestehende Tests an die ersetzte Stuetzenausfuehrung anpassen; Anforderungen erhalten. Gesamte Offline-Suite ausfuehren.
- [ ] Katalog/12-Stuecklisten/Anleitung/Entscheidungen und Parameterherkunft gemeinsam aktualisieren. Export nur in Arbeitskopie.

## Task2: Native Ausfuehrung und Lieferung

- [ ] Journalversion/Reload/Teilauswahl und Werkzeuglagen-Nachweis auf12 fortschreiben.
- [ ] Neue Park- und Wechselbaugruppe in NX2406 erzeugen; beide in frischen Prozessen vollstaendig oeffnen. Native Blechkonvertierungen getrennt pruefen.
- [ ] Frischer abschliessender Review; Befunde beheben. Rohprotokolle, Quellrevision, Hashes, Befehle/Exitcodes und Grenzen mitliefern.
- [ ] Neue CAD-Dateien und Unterlagen im bestehenden Git-Repository versionieren/pushen; Arbeitsstand und Remote vergleichen.

## Ausfuehrungsnotizen

- Spindelpassung ist nach neuester Nutzerentscheidung kein Layout-Blocker. Sie bleibt ein Blocker fuer Fertigung/Betrieb.
- Bestehender Git-Ordner auf eigenem codex-Branch; Ausgangsarchiv gesichert. Keine alten Fremd-CAD-Dateien.
