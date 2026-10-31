# SX3.5Z CNC-Gesamtansicht 07.1 – Korrektur der NX-Blechabfrage

## Ursache im hochgeladenen NX-Protokoll

Der allgemeine API-Vortest besteht: Ausdruecke, native Grundfeatures, Aktualisierung,
Speichern und Komponenteneinfuegung. Die erste Blechvorform entsteht mit 13.600 mm³.
Danach bricht `nx_sheetmetal06.py` bei `uf.Modl.AskFaceData(...)` ab, weil diese
Methode am dortigen `NXOpen.UF.Modl`-Objekt nicht vorhanden ist. Der eigentliche
Konvertierungs-Builder wurde in diesem Lauf noch nicht erreicht. Das ist ein
Adapterfehler; aus diesem Protokoll ergibt sich kein Nachweis einer fehlenden
Sheet-Metal-Lizenz oder einer ungueltigen Blechgeometrie.

## Aenderung

`nx_sheetmetal06.py` erhaelt Patchstand **07.1**. Vor der ersten Flaechenabfrage
wird die aufrufbare Methode `AskFaceData` an der tatsächlichen UF-Sitzung gesucht:
bevorzugt `UF.Modeling`, danach bei tatsaechlicher Verfuegbarkeit `UF.Modl` und
`UF.ModlGeneral`. Es werden keine aehnlich benannten Abfragefunktionen geraten.
Die Auswahl selbst ruft keine Geometriefunktion auf. Die gewaehlte Methode bleibt
fuer diese Konvertierung festgelegt; ein Fehler beim eigentlichen Lesen wird
nicht durch einen Wechsel zu einer anderen Methode verdeckt.

Der Lauf protokolliert Gruppenverfuegbarkeit, ausgewaehlte Funktion und deren
lokale Methodendokumentation. Ein eindeutiges, planares Flaechenergebnis auf der
vorgegebenen lokalen Ebene bleibt erforderlich. Ungueltige Ebenenparameter und
nicht endliche Punkte/Normalen werden explizit abgewiesen. Der weitere
Konvertierungsablauf bleibt fachlich unveraendert; seine Fehlerstufe wird genauer
protokolliert. Typ- und Dickenpruefung bleiben aktiv.

Keine Aenderung an Geometrie, Farben, Bewegungsparametern, Tuer, Schaltschrank oder
Spaene-/KSS-Ruecklauf. Grundadapter **4.8**, Dateiverwaltung **4.8**,
Geometriepruefung **4.6** und Modellstand **CNC_ANSICHT_07** bleiben bestehen.
Das neue Merkmal ist **Blechadapter-Patch: 07.1**. Die alte Zeile
`Journal-Version: 4.8` ist deshalb weiterhin korrekt.

## Installation – bestehendes Paket 07

Aus dem kleinen Fix-ZIP nur diese beiden Python-Dateien direkt in den bisherigen
Ordner neben `Parameter.json` kopieren und dort ersetzen:

- `nx_sheetmetal06.py`
- `NX_CNC_Gesamtansicht.py`

Beide zusammen verwenden. **Keine Parameterdatei ersetzen.** Das Fix-ZIP enthaelt
bewusst keine Parameterdateien. Vorhandene PRTs und Ausgaben nicht loeschen.

Alternativ das Gesamtpaket 07.1 in einen neuen lokalen Ordner entpacken. Es enthält
Standardparameter. Eigene Massänderungen aus dem alten Ordner gesondert sichern
und uebernehmen, nicht mit einer Standard-Parameterdatei ueberschreiben.

## Kurzer Test vor dem Gesamtaufbau

In NX 2406, Journal wiedergeben / Play Journal:

```
NX_Blech_Pruefen.py
```

Dieses bereits vorhandene Testjournal fuehrt den allgemeinen API-Test aus und
baut dann nur den oberen breiten Tuerrahmen als Einzelteil auf. Der erfolgreiche
allgemeine Vortest alleine genuegt NICHT. Pruefen:

```
Blechadapter-Patch: 07.1
Blech-Flaechenabfrage ausgewaehlt: UF.<tatsaechliche Gruppe>.AskFaceData
Blechkonvertierung OK: NX-Blechkoerper, Dicke 2 mm
FERTIG: 1 native Einzelteile.
```

Die 2 mm gelten fuer die unveraenderten Standardparameter. Nach einem Fehler
nicht mit dem Maschinenaufbau fortfahren. `Blech_Optionen.json` bleibt auf
`"mode": "required"`. Eine ausdrueckliche Vorformansicht mit `"solid"` waere
weiterhin kein erfolgreicher Blechtest und ist NICHT die Fehlerkorrektur.

## Gesamte Maschine erzeugen

Nach vollstaendig bestandenem Einzelteiltest:

```
NX_CNC_Gesamtansicht.py
```

Die Ausgabe wird neu angelegt:

```
%LOCALAPPDATA%\SX35Z\NX_Output\
  SX35Z_CNC_ANSICHT_07_1_<Zeitstempel>_<Kennung>\
    Teile\
    Unterbaugruppen\
    FRAESMASCHINE_CNC_BLECHENTWURF_07_1__<Kennung>.prt
    HAUPTBAUGRUPPE.txt
    Blech_Nachweis.json
```

Ein in `NX_Ausgabe.json` konfiguriertes Ziel bleibt erhalten. Nach vollstaendigem
Erfolg die in `HAUPTBAUGRUPPE.txt` genannte Datei oeffnen und den gesamten
Ausgabeordner zusammenhalten.

## Aussagekraft und Grenzen

Der Namespacefehler wurde mit nachgebildeten NX-Objekten vor der Korrektur
reproduziert. 164 Offline-Tests (141 vorhandene plus 23 neue) bestehen. Alle
29 Python-Dateien bestehen die Python-3.10-Grammatikpruefung. Die geaenderten
NX-Aufrufe wurden NICHT hier in NX ausgefuehrt. Es gibt keine neue native PRT
und keine behauptete Blechkonvertierung in Siemens NX durch den Autor.

Die konkreten verfuegbaren UF-Methoden und ihre Rueckgabe werden beim Nutzer
geprueft. Die aktuelle offizielle NX-2406-Online-Pythonreferenz war beim
Zugriffsversuch nicht abrufbar; eine alte .NET-Referenz wird nicht als Beweis
fuer die Python-Gruppierung verwendet. Die lokale eingebettete API-Dokumentation
und das Ergebnis der echten Flaechenabfrage werden deshalb mitprotokolliert.

Die Meldung zum Rezept-Referenzfingerprint aus Version 07 und die optionalen
OM-Attributwarnungen sind von diesem Patch nicht behoben. Sie waren nicht die
Traceback-Abbruchstelle. Der Parameter- und Geometrieinhalt des Pakets ist
bytegleich geblieben; es wurde kein neuer Geometrienachweis vorgetaeuscht.
Vorhandene Geometrie-/Kollisionsberichte im Paket bleiben Nachweise der Revision07,
nicht eines hier ausgefuehrten nativen NX-Blech-Endzustands.

Bei erneutem Abbruch das NEUE `NX_Fehlerprotokoll.txt` aus dem Ausgabeordner
verwenden; sofern erzeugt auch `NX_Geometriediagnose.json`. Die letzte
`NX-Blech-Pflichtmodus fehlgeschlagen [<Stufe>]`-Zeile nennt nun die genaue
Stelle. Ein Zwischenstand ist keine fertige Baugruppe.
