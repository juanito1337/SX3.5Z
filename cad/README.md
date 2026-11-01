# Native NX-Dateien im Git-Projekt

## Aktueller Lieferstand10 vom01.11.2026

Neu aus dem aktiven Git-Projekt erzeugt, keine alten CAD-Eingaben.
Teller seitlich auf Gestellstuetze; Spannpaket nur Bauraum, nicht funktionsfaehig.

Lieferverzeichnis: `nx/SX35Z_CNC_UMSETZUNG_10_TELLER_20261101_024515_031838_13e8dd801b5f/`

Hauptbaugruppe: `FRAESMASCHINE_CNC_TELLER_SPANNPAKET_10_NICHT_FREIGEGEBEN__13e8dd801b5f.prt`

Ordner mit `Teile/`, `Unterbaugruppen/` und Hauptbaugruppe zusammenhalten.
511 Einzelteile,20 Unterbaugruppen,1 Hauptbaugruppe und3 API-Pruefteile.
Alle511 Einzelteile in frischer NX2406-Sitzung voll geladen, jeweils ein Koerper.
19 native Blechkonvertierungen beim Aufbau im Modus required nachgewiesen;
Blechvorformen und Abwicklungen sind hiervon getrennte Nachweise.
Sieben Journale Exit0. Quellen, Befehle und Rohprotokolle unter `Pruefnachweise/`.
`PRUEFSTATUS.json` und `PRT_SHA256.json` beschreiben den konkreten Lieferlauf.

Aktuelles Wiedereroeffnen aus dem Repository-Stamm:

```powershell
$env:SX35Z_VERIFY_RUN = "$PWD/cad/nx/SX35Z_CNC_UMSETZUNG_10_TELLER_20261101_024515_031838_13e8dd801b5f"
& 'C:/Siemens/nx2406/NXBIN/run_journal.exe' "$PWD/projekt/NX_Git_Lieferstand_Pruefen.py"
```

`projekt/NX_CNC_Gesamtansicht.py` erzeugt weitere neue Laeufe. Kein PRT wird
ueberschrieben. Die aktuelle Pruefung verlangt `Rezept_beim_Aufbau.json` und
passende aktive Quellen; fuer09 das zugehoerige historische Journal verwenden.
Ein verschobener Checkout wurde fuer10 noch nicht gesondert nativ geprueft.

Aktuelle Offline-Vorschau: `projekt/Ansicht_Teller_10.html` (im Browser noch nicht
visuell geprueft). Aktuelle Anleitung und Grenzen:
`projekt/Dokumentation/Entwicklungsstand_Teller_10.md`.
Keine reale Spindelspannung, volle Wechselbahn oder Fertigungs-/Betriebsfreigabe.
Die folgenden Abschnitte beschreiben ausschliesslich den unveraendert erhaltenen09-Lauf.

## Historischer Lieferstand09

Am 31.10.2026 neu aus den aktuellen Stand09-Rezepten erzeugt. Keine alten CAD-
Dateien vom Rechner importiert. Status: Konstruktionsentwurf, nicht freigegeben.

## Oeffnen

Lieferverzeichnis:
`nx/SX35Z_CNC_UMSETZUNG_09_20261031_131548_912329_ecb147c4fdab/`

Hauptbaugruppe:
`FRAESMASCHINE_CNC_UMBAUSTAND_09_NICHT_FREIGEGEBEN__ecb147c4fdab.prt`

Den kompletten Lieferordner mit `Teile/` und `Unterbaugruppen/` zusammenhalten.
Es gibt 560 Einzelteile, 20 Unterbaugruppen und eine Hauptbaugruppe; die drei
weiteren PRT unter `_API_Test/` sind Pruefteile. `HAUPTBAUGRUPPE.txt` benennt
den Einstieg. Fuer einen verschobenen Checkout in NX die Komponentensuche auf
Lieferordner, `Teile/` und `Unterbaugruppen/` richten und alle Komponenten laden.
Das Pruefjournal unten setzt diese Suchpfade explizit.
Eine Kopie des neuen Lieferordners an einem anderen Pfad wurde in einer weiteren
frischen NX-Sitzung erfolgreich geladen (Exitcode 0); alle geladenen Parts kamen
ausschliesslich aus dieser Kopie. Nachweis: `Pruefnachweise/NX_Portabilitaet.json`.

## Neu erzeugen und pruefen

`projekt/NX_Ausgabe.json` muss auf den absoluten `cad/nx`-Pfad dieses Checkouts
zeigen. Blechmodus `required` bleibt unveraendert. Aus dem Repository-Stamm:

```powershell
& 'C:/Siemens/nx2406/NXBIN/run_journal.exe' "$PWD/projekt/NX_Metadaten_Pruefen.py"
& 'C:/Siemens/nx2406/NXBIN/run_journal.exe' "$PWD/projekt/NX_Blech_Pruefen.py"
& 'C:/Siemens/nx2406/NXBIN/run_journal.exe' "$PWD/projekt/NX_KSS_Pruefen.py"
& 'C:/Siemens/nx2406/NXBIN/run_journal.exe' "$PWD/projekt/NX_CNC_Gesamtansicht.py"
$env:SX35Z_VERIFY_RUN = "$PWD/cad/nx/SX35Z_CNC_UMSETZUNG_09_20261031_131548_912329_ecb147c4fdab"
& 'C:/Siemens/nx2406/NXBIN/run_journal.exe' "$PWD/projekt/NX_Git_Lieferstand_Pruefen.py"
```

Nach einem neuen Aufbau im letzten Befehl dessen neuen Laufordner einsetzen.
Das Pruefjournal verlangt eine frische NX-Sitzung und schreibt keine PRT.
Keine Originale oder frueheren Laeufe ueberschreiben. Nur einen vollstaendigen,
geprueften Lieferlauf gezielt in Git aufnehmen. PRT sind binaer; Git speichert
Revisionen, liefert aber keine geometrischen Text-Diffs.

## Nachweis und Grenzen

Gesamtaufbau und frisches Oeffnen wurden in NX 2406 / Python 3.10.15 mit
Exitcode 0 ausgefuehrt. Alle 560 Einzelteile enthalten nach erneutem Laden je
einen Koerper; alle 20 Unterbaugruppen sind vorhanden. Ausdrucks-Herkunft bleibt
als Part-Attribut `SX_EXPR_<Parameter>_*` gespeichert. 21 Teile besitzen beim
Aufbau gepruefte native Blechkonvertierungen; die geneigten KSS-Blechvorformen
sind getrennt davon zu betrachten. Keine vollstaendigen Abwicklungen behauptet.

Parameter-Snapshot, Teilemanifest, Kaufteil-/Stuecklistenbindung, Blech-Nachweis,
Geometrieprotokolle und Wiedereroeffnungsbericht liegen im Lieferverzeichnis.
`Pruefnachweise/` enthaelt Befehle, Rohprotokolle und Quellhashes.

Der historische Rezept-Hash weicht ab; der historische OpenCascade-
Referenzvergleich ist deshalb im Generator nicht aktiv. Native Einzeloperationen
werden weiterhin geprueft. Ursache offen; historische Berichte unveraendert.
Offline-pytest konnte wegen fehlendem Standard-Python nicht starten (9009).
35 fehlende Istmasse, sechs bekannte Anschlusskonflikte sowie fehlende
Spindelspannung/ATC-Wechselbahn bleiben offen. Kein Bau-, Bestell-, Betriebs-
oder ATC-Funktionsnachweis. Geometrie und bestehende Stuecklisten wurden durch
diesen Lauf nicht konstruktiv veraendert.
