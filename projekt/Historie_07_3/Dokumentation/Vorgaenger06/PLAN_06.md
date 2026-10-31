# Umsetzung 06 – breite Senktür als Blechbaugruppe

Ziel: den vom Nutzer bestätigten Bildentwurf in das vorhandene NX-Open-Paket übertragen.
Kein Ersatz der Maschinengeometrie durch Bildinterpretation. Grundfläche 1650 x 1000,
Tischhöhe 930, zwei nach unten teleskopierende Segmente bleiben erhalten.

Entscheidung: 1420 mm lichte Breite (86 %). 2-mm-Kantprofile statt massiver Türrahmen.
Native Features aus bestehendem Adapter; gesonderte NX-Sheet-Metal-Konvertierung
mit explizitem Pflichtmodus, kein stilles Ausweichen bei API-/Lizenzfehlern.
Gasdruckfedern als klar gekennzeichnete Einbaustudie: gegen die Absenkbewegung,
kein nachgebildetes Katalogteil und keine Auslegung aus einem Renderbild.

- [x] Tests für Breite, Raum, dünnwandige Profile und Bibliotheksstatus zuerst.
- [x] Geometrierezept und gekantete Blechteile, Fensterleisten, Kassette ergänzen.
- [x] Gasdruckfeder-Einbauräume und Kraftbilanz, Lagerpunkte/Richtung dokumentieren.
- [x] NXSM-Adapter mit Laufzeitprüfung sowie kurzer Blechteil-Vortest.
- [x] Gesamtes Modell unabhängig geometrisch prüfen; Darstellung aktualisieren.
- [x] Dokumentation, vollständiges ZIP und frisch entpackte Tests.

Grenzen: keine .prt-Laufzeit vorhanden. Renderbild dient nicht als Maßbeleg.
Keine Schutz-/KSS-Dichtheits-/Fertigungsfreigabe. Endgültige Synchronisierung,
Fangsicherung, Federprodukt und Abwicklungen bleiben gesonderte Nachweise.

Abschluss: Offline-Implementierung und Vorformprüfung. Native Ausführung weiterhin offen.

Entscheidung: Der neue Hauptdateiname bezeichnet den Blechentwurf explizit.
Der alte reine Namensvergleich wurde passend migriert; kein Geometrietest entfernt.
