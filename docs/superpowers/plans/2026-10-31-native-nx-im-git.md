# Neue native NX-Dateien im Git-Projekt

Nutzerauftrag vom 31.10.2026: 3D-Dateien im Git-Ordner neu erzeugen und
versionieren; keine alten CAD-Dateien vom Rechner verwenden.

Basis: Commit 463497f, aktives Modell CNC_UMSETZUNG_09. Bestehende Rezepte,
Parameter und native NX-Journale verwenden. Die neue Nutzervorgabe ersetzt
fuer diesen Lauf die bisher geplante Uebernahme alter Nutzer-PRT. Die Geometrie
bleibt eine Rezeptrekonstruktion mit offenen Istmassen und Anschlusskonflikten.

## Vorgehen

- [x] Konfiguration und lokale NX-Startmoeglichkeit lesen; vorherige
  NX_Ausgabe.json unter ergebnisse/nx/ sichern.
- [x] Bestehende Ausgabekonfiguration auf cad/nx/ im Repository setzen.
  Neue eindeutige Laufordner beibehalten, nichts ueberschreiben.
- [x] Vorhandene Blech- und KSS-Journale mit lokalem NX run_journal ausfuehren.
  Rohprotokoll, Exitcode, Quellrevision und Umgebung festhalten. Blech required.
- [x] Bei erfolgreichen Proben den Gesamtgenerator ausfuehren; Teilemanifest,
  Unterbaugruppen und Hauptbaugruppe auf Vollstaendigkeit pruefen.
- [x] Neu gespeicherte Baugruppe in einer frischen NX-Sitzung oeffnen und
  Komponenten-Ladestatus pruefen. Nur neu erzeugte Dateien verwenden.
- [x] Erfolgreichen Lieferstand mit Parameter-/Quellnachweis und Pruefstatus
  in Git aufnehmen; fehlgeschlagene Teilstaende eindeutig kennzeichnen.
  Groesse und .gitignore vor Commit pruefen; abschliessend Remote vergleichen.

## Entscheidungen und Grenzen

Kein neuer Generator und keine neue Geometrie geplant. Vorhandenes absolutes
output_root-Feld nutzen, statt die Pfadlogik umzubauen. cad/nx/ wird nicht von
.gitignore ausgeschlossen. Laufprotokolle und Prueflinge unter ergebnisse/
bleiben lokal, sofern nicht ausdruecklich als Liefernachweis uebernommen.
Keine alten PRT importieren, keine Hardware ansteuern, keine globale Installation
aendern. Fehlende NX-Lizenz oder native Fehler als solche dokumentieren.
Software-/Dateipruefungen sind keine Fertigungs-, Bestell- oder Betriebsfreigabe.

## Laufnachweis und begrenzte Anpassung

Die ersten Blech-/KSS-Proben erzeugten 1 bzw. 10 Teile, endeten aber wegen
ununterstuetzter Benutzerattribute auf Expressions mit Exitcode 1.
Nativer Regressionstest NX_Metadaten_Pruefen.py reproduzierte dies (RED).
Korrektur in nx_native.py: Herkunft am Part unter SX_EXPR_<Parameter>_* ablegen.
GREEN in NX: Exitcode 0, Attribute und unveraenderter Ausdruckswert geprueft.
Keine Geometrieaenderung. Vorherige Datei lokal unter ergebnisse/nx/ gesichert.

Vollstaendiger Aufbau im Lauf ...131548_912329_ecb147c4fdab: Exitcode 0,
560 Einzelteile, 20 Gruppen, Hauptbaugruppe, 21 native Blechkonvertierungen.
Erneutes Oeffnen in frischem NX-Prozess: Exitcode 0, alle Teile geladen,
sheet_t-Metadaten und Wert in 142 Teilen persistent. Auch eine an einen anderen
Pfad kopierte Fassung bestand denselben Test; keine geladenen Teile ausserhalb
des neuen Kopieordners. Zwei unabhaengige Code-Review-Durchgaenge ohne
blockierende Befunde; anfangs offener Persistenznachweis ist geschlossen.

Offen: Historischer Rezept-Hash weicht ab; keine Aktivierung des alten
OpenCascade-Referenzvergleichs. Native Operationspruefungen bleiben aktiv.
Offline-pytest-Aufruf scheitert am fehlenden Standard-Python (9009), nicht an
ausgeblendeten Tests. Native Gesamtpruefung ersetzt die Offline-Suite nicht.
