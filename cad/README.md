# Native NX-Dateien im Git-Projekt

## Aktuelles Konzept13:12er Seitenmagazin,01.11.2026

- **NX PARK:** [Gesamtbaugruppe](nx/SX35Z_CNC_KONZEPT_13_SEITENMAGAZIN_PARK_20261101_200424_768031_719cf9cafd04/fraesmaschine_konzept13_park_nicht_freigegeben__719cf9cafd04.prt)
- **NX WECHSEL:** [Gesamtbaugruppe](nx/SX35Z_CNC_KONZEPT_13_SEITENMAGAZIN_WECHSEL_20261101_200858_763146_bf31b7c655a7/fraesmaschine_konzept13_wechsel_nicht_freigegeben__bf31b7c655a7.prt)
- **STEP PARK:** [3D-Modell](step/SX35Z_13_Park.step)
- **STEP WECHSEL:** [3D-Modell](step/SX35Z_13_Wechsel.step)
- [Park-/Wechselvorschau](vorschau/SX35Z_13_Seitenmagazin_Park_Wechsel.png),
  Verkleidung/Schaltschrank zur Einsicht ausgeblendet; offline aus CAD-Rezept.

Festes12er Eigenbau-Magazin rechts/hinten; Einzelarm mit90mm Hub und60mm
Radialzustellung. Gemeinsamer Zusatzrahmen, kein Aufbau auf dem Maschinentisch.
Nominale Einhausung1950x1575mm, Schaltschrank steht zusaetzlich aussen.
Originalmaschine und Achswege erhalten. Parkstellung ausserhalb modellierter
Tischhuelle. Fuer den Wechsel Bahnraum freihalten: konservativ125mm maximale
Werkstueck-/Spannmittelhoehe ueber Tisch im betroffenen Raum. Keine Aussage
ueber beliebig grosse Werkstuecke oder vollstaendige kontinuierliche Bahn.

Beide Baugruppen in NX2406 neu erzeugt, gespeichert und in frischen Prozessen
vollstaendig geoeffnet: je532 Einzelteile,17 Gruppen,24 native Blechkoerper
im Pflichtmodus required. AP214 direkt aus NX exportiert; beide STEP-Dateien
separat offline eingelesen, je532 gueltige Koerper. Native Quelle feaf3950c142590da45f353dc60b65c70ee527ed.
Komplette Laufordner zusammenhalten, nicht nur Haupt-PRT kopieren.

[Anleitung, Auslegung und offene Punkte13](../projekt/Dokumentation/ATC_Konzept13.md),
[Pruefbericht mit Grenzen](../ergebnisse/entwicklung/20261101_atc13/README.md).
SK30-Bestand bleibt Referenz, BT30-Spindel/Spannpaket und Greifer-/Taschenretention
noch nicht betriebsbereit. R13-Kaufteile sind unbestaetigte Bauraumreserven.
Historische12/11/10-Lieferstaende unveraendert erhalten; untenstehende
Aktuell-Angaben gelten jeweils fuer die damalige Revision.


**STEP-Ansicht Stand12:** [Gesamtbaugruppe in Wechselstellung](step/SX35Z_12_Wechselstellung.step),
direkt aus dem gespeicherten NX-Stand exportiert;461 Koerper nach erneutem
STEP-Einlesen gueltig. [Exportnachweis](../ergebnisse/entwicklung/20261101_step12/README.md).

## Aktuell12: BT30 auf fester rechter Saeulenkonsole,01.11.2026

- **PARK**: [fraesmaschine_cnc_12_park_nicht_freigegeben__e0b0be78f60d.prt](nx/SX35Z_CNC_UMSETZUNG_12_BT30_KONSOLE_PARK_20261101_125654_005752_e0b0be78f60d/fraesmaschine_cnc_12_park_nicht_freigegeben__e0b0be78f60d.prt)
- **WECHSEL**: [fraesmaschine_cnc_12_wechsel_nicht_freigegeben__fdd87de5a7ba.prt](nx/SX35Z_CNC_UMSETZUNG_12_BT30_KONSOLE_WECHSEL_20261101_130001_853869_fdd87de5a7ba/fraesmaschine_cnc_12_wechsel_nicht_freigegeben__fdd87de5a7ba.prt)

Beide Gesamtbaugruppen in NX2406 neu erzeugt, gespeichert und in frischen
Prozessen vollstaendig geoeffnet: je461 Einzelteile,17 Unterbaugruppen und
19 native Blechkonvertierungen im Pflichtmodus required. Vier Fangbleche
sind geneigte Vorformen.482PRT pro Lauf inklusive3 API-Pruefteilen.
Native Halterkegellage in WECHSEL:0/0/400mm, Toleranz0.00001mm. Dies prueft
die nominale Ausrichtung, nicht SK30/BT30-Passung oder automatisches Spannen.

Die Laufordner mit Teile/ und Unterbaugruppen/ vollstaendig zusammenhalten.
PRUEFSTATUS.json, PRT_SHA256.json und Pruefnachweise/ gehoeren zum Lieferstand.
Quellrevision b6e4643d5558780936f7b622af0102ad64041215. Bei Wiederoeffnungspruefungen passende Quellen
verwenden. Alte11/10/09-Lieferstaende nicht ueberschreiben.

[Park-/Wechselvorschau](vorschau/SX35Z_12_Park_Wechsel.png) aus dem Modellrezept,
offline gerendert. [Anleitung und Grenzen12](../projekt/Dokumentation/Entwicklungsstand_12.md).
Grundplatte/Scheibe nach Bild;200mm Hub, Werkzeugteilkreis und Antriebs-/
Greiferhuellen bleiben Entwurf. Konsole braucht Istaufmass, Befestigung und
Festigkeitsnachweis. Die folgenden Eintraege beschreiben historische Staende.

**Abgrenzung zur neuen Produktauswahl01.11.2026:** Die nachfolgend verlinkten
NX-Dateien11 enthalten weiterhin den eigenen Tellerentwurf (Scheibe310x10mm,
Zustellung389,33mm). Sie sind **kein Modell des gewaehlten RATTM-Artikels**.
Die jetzt erhaltenen Lieferantenbilder zeigen unter anderem Scheibe280x16mm
und Grundplatte330x175x22mm. Ihre [Auswertung](../projekt/Werkzeugwechsler/RATTM_1005009887984460_Bildauswertung.md)
ist erfasst; Produktintegration und native Neuerzeugung sind noch offen.

## Aktuell11: Parkstellung und Wechselstellung, 01.11.2026

- **PARK**: [fraesmaschine_cnc_11_park_nicht_freigegeben__7aecac2684bf.prt](nx/SX35Z_CNC_UMSETZUNG_11_FANGBLECHE_PARK_20261101_111503_626609_7aecac2684bf/fraesmaschine_cnc_11_park_nicht_freigegeben__7aecac2684bf.prt)
- **WECHSEL**: [fraesmaschine_cnc_11_wechsel_nicht_freigegeben__5b021d005ea9.prt](nx/SX35Z_CNC_UMSETZUNG_11_FANGBLECHE_WECHSEL_20261101_111814_576079_5b021d005ea9/fraesmaschine_cnc_11_wechsel_nicht_freigegeben__5b021d005ea9.prt)

WECHSEL zeigt den rechten Teller bis zur nominellen Spindelachse, Kopf auf
Uebergabehoehe. PARK zeigt die eingefahrene Ablage. Jeweils den vollstaendigen
Laufordner mit Teile/ und Unterbaugruppen/ zusammenhalten.454 Einzelteile,
17 Unterbaugruppen,1 Hauptbaugruppe und3 API-Pruefteile pro Lauf (475 PRT).
Beide Stellungen gespeichert und in frischer NX2406-Sitzung voll geoeffnet.
19 native Blechkonvertierungen je Lauf; vier neue Fangbleche sind Vorformen.
PRUEFSTATUS.json, PRT_SHA256.json und Pruefnachweise/ begleiten jeden Lauf.
NX_Werkzeuglage_11.json im WECHSEL-Ordner dokumentiert die native Lagepruefung.

Erzeugung: projekt/NX_CNC_Gesamtansicht.py bzw. NX_CNC_Wechselstellung.py.
Wiedereroeffnen: SX35Z_VERIFY_RUN auf einen der obigen Laufordner setzen und
projekt/NX_Git_Lieferstand_Pruefen.py in frischer NX-Sitzung starten.
Nur mit passenden Quellen/Parametern pruefen; keine alten Parts ueberschreiben.

Spannpaket/BT30-Passung, volle Bahn und Betriebsfreigabe bleiben offen.
Aktuelle Anleitung: projekt/Dokumentation/Entwicklungsstand_11.md.
Historische10/09-Dateien und HTML-Ansichten bleiben erhalten; untenstehende
Angaben gelten nur fuer diese alten Lieferstaende.

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
