# Gesamtansicht 03 — kompakte Einhausung, horizontale Schiebetüren

## Umfang / Auslegung
Nutzerwunsch: kleinere Einhausung und horizontale Tür. Arbeitshypothese:
seitlich schiebende, mittig öffnende Doppeltür, nicht horizontal geteilte Klappe.
Unverändert: Maschinengeometrie, 500/200/240 mm Zielhübe, 750 mm Aufstellebene,
Schaltschrankbauraum und die ausdrücklich noch ungeprüften Anschlussstellen.
Reine Entwurfsänderung; keine Fertigungs-, Schutz- oder Dichtheitsfreigabe.

## Entwurfsentscheidung
Aus Stand 02: formkonstante Teile über Zielhub ungefähr x=-690..814,
y=-382..427,z=0..1111 mm. Neue Hülle 1650 x 1000 x 1200 mm,
Mitte x=62/y=25; Sockelhöhe 750 mm bleibt erhalten. Kein einfaches Skalieren.
760 x 1000 mm lichte Frontöffnung, Türflügel auf zwei versetzten horizontalen
Führungsebenen. Beide Blätter parken hinter/vor seitlichen Festfeldern innerhalb
der Gehäusebreite. Türstellung zentral über door_open (0..1). Linien-/Flächen-
und Dichtkonzept muss am realen Aufbau weiter ausgelegt werden.

## Architektur
Bestehenden NX-Adapter weiterverwenden; einzige Erweiterung: einheitenlose Verhältnisausdrücke für door_open. cnc_ansichtsmodell.py liefert
neue parametrische Türkörper und verkleinerten Rahmen/Wanne. Ein unabhängiges
Modul enclosure_checks03.py berechnet konservative additive Körperhüllen bei
acht Verfahrweg-Eckstellungen. Browseransicht verwendet das gleiche Rezept
und nur die zugehörigen Türtranslationen. Keine erfundenen NX-API-Aufrufe.

## Aufgaben
- [x] Tests für Parameter, Öffnung, Blätter und Platzbedarf zuerst (ROT).
- [x] Parametrische Tür- und Hüllgeometrie plus analytische Hüllprüfung (GRÜN).
- [x] Browser-Schiebebewegung, neue Geometrie und Vorschauen erstellen.
- [x] Gesamte Testsuite, unabhängiger Körperaufbau, Selbstprüfung, ZIP-Rückprüfung.

## Prüffokus
Verfahrwege nicht verkürzen; Türparken bei voller Öffnung innerhalb Hüllenbreite;
Glas und Rollen bewegen sich mit Rahmen; kein alter Mittelpfosten blockiert den
Eingriff; hinterlegte Prüfungen/Ansichtsnetze aktualisieren; offene Tür darf nie
als geschlossene Betriebs-Schutzeinhausung bezeichnet werden. Änderung von
anderen Maschinenparametern wird neu geprüft. Keine originalen Dateien ändern.

## Durchgefuehrte Selbstpruefung
TDD: erwartete Fehler und gruene Laeufe in Arbeitsnachweis03. Bei der unabhaengigen
CAD-Probe gefundene Mittelueberdeckungs-/Unterfuehrungsdurchdringungen korrigiert;
keine Fehler uebersprungen. Rollengeometrie und Ueberwachungskoerper sind weiterhin
Entwuerfe. Browser file:-URL im Container gesperrt; HTML via set_content ohne
externes Netz gerendert. Kein Agent/keine unabhaengige Zweitpruefung. Kein NX.

## Durchgefuehrte Selbstpruefung
TDD: erwartete Fehler und gruene Laeufe in Arbeitsnachweis03. Bei der unabhaengigen
CAD-Probe gefundene Mittelueberdeckungs-/Unterfuehrungsdurchdringungen korrigiert;
keine Fehler uebersprungen. Rollengeometrie und Ueberwachungskoerper sind weiterhin
Entwuerfe. Browser file:-URL im Container gesperrt; HTML via set_content ohne
externes Netz gerendert. Kein Agent/keine unabhaengige Zweitpruefung. Kein NX.
