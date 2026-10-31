# SX3.5Z – Blechadapter-Korrektur 07.2

## Befund aus deinem NX-Lauf

`NX_Fehlerprotokoll(7).txt` bestätigt den Patchstand 07.1. Der allgemeine
API-Vortest besteht; `UF.Modeling.AskFaceData` ist verfügbar, wird verwendet und
findet die Blechbasisfläche eindeutig. Danach bricht der Adapter bei
`part.Preferences.Sheetmetal` ab. Dieses Attribut gibt es an dem abgefragten
`NXOpen.Preferences.PartPreferences`-Objekt nicht. Der Blech-Builder wurde noch
nicht aufgerufen. Die Meldung belegt keinen Lizenzfehler und keine fehlgeschlagene
geometrische Konvertierung.

## Korrektur

Der Zugriff lautet jetzt:

```python
pref = part.Preferences.PartSheetmetal
```

Vor einer Änderung prüft das Journal alle vier weiterhin verwendeten Methoden:
`SetThickness`, `SetBendRadius`, `SetNeutralFactor` und `Commit`.
Die eingebettete lokale Methodendokumentation wird protokolliert. Fehlt der
Zugriff, werden die verfügbaren Sheet-bezogenen Eigenschaftsnamen ohne
Ersatzaufrufe aufgelistet. Tatsächliche Getter-, Setter-, Lizenz- oder
Builderfehler bleiben Fehler; es gibt weder eine geraten benannte Alternative
noch einen stillen Wechsel zu einem Volumenmodell.

Die drei Einstellwerte bleiben Formeln (beispielsweise `sx_sheet_t`) mit
unverändertem `updateModel=False`. Die vorhandene native Konvertierung,
Blechkörpererkennung und Dickenprüfung bleiben aktiv. Der Ergebnisbericht
vermerkt zusätzlich den verwendeten Präferenzzugriff.

## Installation in den vorhandenen Ordner 07 oder 07.1

Aus dem kleinen Fix-ZIP diese ZWEI Dateien direkt neben `Parameter.json` kopieren
und ersetzen:

```text
nx_sheetmetal06.py
NX_CNC_Gesamtansicht.py
```

Beide gehören zusammen. **Keine Parameterdateien ersetzen.** Das kleine Paket
enthält bewusst keine. Vorhandene PRT-Dateien und Ausgabeordner nicht löschen.
`NX_Blech_Pruefen.py` bleibt unverändert im bisherigen Ordner.

Alternativ das vollständige Paket 07.2 in einen neuen lokalen Ordner entpacken.
Das Gesamtpaket enthält Standardparameter; eigene Parameter zuvor sichern und
gezielt übernehmen. Kein Mischen einzelner älterer Python-Module.

## Zuerst der kleine NX-Test

In Siemens NX 2406, Journal wiedergeben / Play Journal:

```text
NX_Blech_Pruefen.py
```

Dieser Einstieg führt die allgemeinen Tests aus und baut anschließend nur den
oberen breiten Türrahmen auf. Im Ausgabefenster muss zuerst stehen:

```text
Blechadapter-Patch: 07.2
```

Bei erfolgreichem Zugriff folgt:

```text
Blechpraeferenzen ausgewaehlt: Preferences.PartSheetmetal
```

Diese Zeile ist NUR die erfolgreiche Auflösung des Präferenzobjekts. Für einen
bestandenen Blechtest müssen danach Konvertierung, Prüfung und Speichern
vollständig durchlaufen. Bei Standardparametern sind unter anderem zu erwarten:

```text
Blechkonvertierung OK: NX-Blechkoerper, Dicke 2 mm
FERTIG: 1 native Einzelteile.
```

Ein API-Vortest oder die Erzeugung der scharfkantigen Vorform allein reicht nicht.
Die Zeile `Journal-Version: 4.8` bezeichnet weiterhin den unveränderten
Grundadapter und ist neben dem Blechpatch 07.2 korrekt.

**`Blech_Optionen.json` bleibt auf `"mode": "required"`.** Der ausdrücklich
wählbare Modus `solid` würde nur Vorformen liefern und ist KEINE Behebung des
Blechfehlers.

## Danach der Gesamtaufbau

Nach vollständig bestandenem kleinen Test starten:

```text
NX_CNC_Gesamtansicht.py
```

Standardausgabe:

```text
%LOCALAPPDATA%\SX35Z\NX_Output\
  SX35Z_CNC_ANSICHT_07_2_<Zeitstempel>_<Kennung>\
    Teile\
    Unterbaugruppen\
    FRAESMASCHINE_CNC_BLECHENTWURF_07_2__<Kennung>.prt
    HAUPTBAUGRUPPE.txt
    Blech_Nachweis.json
```

Ein eigener Ausgabeort aus `NX_Ausgabe.json` bleibt gültig. Die komplette
Ausgabe mit allen Teilen und Unterbaugruppen zusammenhalten. Erst nach einem
vollständigen Gesamtaufbau die in `HAUPTBAUGRUPPE.txt` genannte Datei öffnen.

## Was unverändert bleibt

Modellstand `CNC_ANSICHT_07`, Maschinenmaße, Tür, Schaltschrank, Späne-/KSS-Rücklauf,
Farben, Referenzdatei und sämtliche Eingabekonfigurationen bleiben unverändert.
Die bisherigen Berichte und Vorschauen im Vollpaket sind historische Nachweise
zum Geometriestand 07, kein neuer NX-Konvertierungsnachweis für 07.2.

Die vorhandene Rezept-Fingerprint-Abweichung und optionale OM-Attributwarnungen
werden von diesem Patch nicht behoben. Sie sind nicht die neue Tracebackstelle.

## Tests und Grenzen

180 Offline-Tests bestehen (164 bisherige und 16 neue). In den beiden bisherigen
Adaptertests hatten die Testobjekte ebenfalls die falsche Eigenschaft
`Sheetmetal` angeboten. Diese falsche Annahme wurde entfernt. Der neue
Regressionstest wurde zuerst mit dem alten Adapter ausgeführt und reproduzierte
den fehlenden Eigenschaftszugriff. Die neuen Objekte bieten ausdrücklich nur
`PartSheetmetal` an; strenge Setter verlangen `(bool, str)`.

Ein bestehender Rezeptvergleich erzeugte das ganze Modell unnötigerweise in
jeder inneren Schleifeniteration neu. Der Test liest dieses unveränderte Rezept
jetzt einmal; seine Vergleiche bleiben gleich. Keine Geometrieänderung.

**Hier kein Siemens NX und kein nativer .prt-Aufbau.** Die Tests simulieren die
Schnittstellen und prüfen den Programmablauf. Ein tatsächlich erfolgreicher Lauf
in NX 2406, insbesondere das Commit des Blechfeatures, muss weiterhin auf deinem
Rechner nachgewiesen werden. Die abschließende Codeprüfung war eine
Autoren-Selbstprüfung, keine unabhängige Prüfung.

Die direkt angesprochene Siemens-Onlinedokumentation war nicht abrufbar. Als
Namens-/Signaturabgleich wurde deshalb eine gespiegelte, von Siemens verfasste
C++-API-Referenz verwendet. Sie nennt `PartSheetmetal`, ist aber weder die aktuelle
NX-2406-Pythonreferenz noch ein Beweis für deine konkrete Laufzeitbindung.
Fundstellen und verbleibende Unsicherheiten: `Dokumentation/API_BLECH_FIX_07_2.md`.

Bei erneutem Abbruch das NEUE `NX_Fehlerprotokoll.txt` mit
`Blechadapter-Patch: 07.2` aus dem tatsächlichen Ausgabeordner verwenden. Sofern
vorhanden die dortige `NX_Geometriediagnose.json` beilegen.
