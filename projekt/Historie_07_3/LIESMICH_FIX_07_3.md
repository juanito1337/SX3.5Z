# Korrekturstand 07.3 – Einheitenfehler am KSS-Trichter

## Befund aus deinem NX-Protokoll (8)

Der Lauf mit Blechadapter 07.2 hat den nativen Blechvortest bestanden. Im
Protokoll stehen 406 erfolgreiche Speichereinträge für Maschinen-Einzelteile.
Es gibt 17 Meldungen zur erfolgreichen Blechkonvertierung (Probe plus 16 Teile).
Der Abbruch erfolgt bei **A407_KSS_Trichter_links**, Feature
`001_Geneigtes_Blech_Normaldicke`, beim Setzen von
`Limits.EndExtend.Value.RightHandSide`:

`NXOpen.NXException: Bemaßung stimmt nicht überein (Binär-Operation)`

Dies ist kein erneuter Fehler am Blechzugriff. Die vorherige Korrektur bleibt
unverändert erhalten. Eine fertige Gesamtbaugruppe belegt dieser Lauf nicht.

## Ursache und gezielte Korrektur

Die Rezeptformel für die vertikale Extrusionslänge des schrägen Blechs lautet:

`sheet_t*sqrt(1+(-8/(227-chip_outlet_w/2))*(-8/(227-chip_outlet_w/2))+(0)*(0))`

In der numerischen Rezeptrechnung stehen alle Längen als Millimeterzahlen.
Im nativen NX-Modell sind `sx_chip_outlet_w` und `sx_sheet_t` dagegen echte
Längenausdrücke. Unter der Wurzel muss der Steigungsfaktor einheitenlos sein.
Die alte reine Namensübersetzung sicherte diese Unterscheidung nicht ab.

07.3 erzeugt bei Bedarf einen eigenen nativen **1-mm-Längenausdruck** über die
bereits verwendete ExpressionFactory. Längenparameter innerhalb des
Wurzelarguments werden durch diese Referenz geteilt. Die führende Blechdicke
bleibt ein Längenausdruck. Der vollständige Ausdruck bleibt von den ursprünglichen
Parametern abhängig; er wird nicht durch einen fest eingetragenen Zahlenwert ersetzt.

Beispielprinzip (Hilfsname je Teil unterschiedlich):

```
sx_aux_XXXX = 1                         # native Länge, Millimeter
sx_sheet_t * sqrt(1 + (-8/(227-(sx_chip_outlet_w/sx_aux_XXXX)/2))
                       * (-8/(227-(sx_chip_outlet_w/sx_aux_XXXX)/2)))
```

Mit Standardwerten bleibt die Extrusionslänge des linken Trichterblechs
2,0235302212255237 mm. Die **Normaldicke bleibt 2 mm**. Blechdicke oder
Auslassbreite müssen zur Fehlerbehebung nicht verändert werden.

Die Korrektur ist auf die vorhandene Form `dicke*sqrt(...)` für die Normaldicke
beschränkt. Andere Extrusionsformeln bleiben auf dem bisherigen Pfad.
Unbekannte Ausdrücke werden abgewiesen, nicht geraten. Der bestehende explizite
`Number_mm`-Kompatibilitätsmodus wird nicht doppelt normiert und nicht als
Fehlerumgehung automatisch eingeschaltet.

## Kleines Patchpaket installieren – nur für Gesamtansicht 07.2

Im vorhandenen Journalordner **zwei Dateien ersetzen**:

- `nx_native.py`
- `NX_CNC_Gesamtansicht.py`

**Zwei neue Dateien daneben ablegen**:

- `nx_formeln073.py`
- `NX_KSS_Pruefen.py`

Alle vier müssen direkt bei `Parameter.json` liegen, nicht in einem zusätzlichen
Unterordner. Nicht die Dateien innerhalb eines ZIPs ausführen.
Das kleine Patchpaket enthält keine Parameterdateien und keinen Austausch des
Blechadapters. `nx_sheetmetal06.py` bleibt auf **07.2**. Für ältere/geänderte
Adapterbestände ist das vollständige Paket 07.3 der eindeutigere Ausgangspunkt.
Vorhandene eigene Skriptänderungen vor dem Ersetzen separat sichern.

`Parameter.json`, `CNC_Parameter.json`, `Ausbau_Parameter.json`, `NX_Farben.json`,
`NX_Ausgabe.json` und `Blech_Optionen.json` beibehalten. Der Blechmodus bleibt
`"required"`; die native Blechkonvertierung wird nicht ausgeschaltet.

## Zuerst nur die zehn geneigten KSS-Bleche testen

In **Siemens NX 2406 → Journal wiedergeben / Play Journal** starten:

```
NX_KSS_Pruefen.py
```

Nicht im gewöhnlichen Windows-Python starten. Keine zusätzlich installierten
Python-Bibliotheken sind für diese Journale nötig.

Die erwarteten Versionszeilen sind:

```
Journal-Version: 4.8
KSS-Formelpatch: 07.3
Blechadapter-Patch: 07.2
```

Diese drei unterschiedlichen Versionsstände sind beabsichtigt.
Der allgemeine API-Vortest enthält jetzt zusätzlich die **vier tatsächlichen
Trichterrezepte** – nicht nur das bisherige Muster mit konstanter Steigung.
Er prüft ihre erzeugten Körper mit den vorhandenen Lage-/Volumenmessungen.
Erst danach werden die zehn gefilterten KSS-Bleche als Einzelteile aufgebaut.

Bei vollständig erfolgreichem Lauf erscheinen:

```
KSS-Formelvortest 07.3 bestanden: 4 echte Trichterrezepte; Lage und Volumen geprueft.
FERTIG: 10 native Einzelteile. Ihre bereits offenen Dateien wurden nicht bearbeitet.
```

Der Kurztest erzeugt **keine Gesamtbaugruppe** und prüft an den ebenen,
geneigten KSS-Vorformen keine neue Blechkonvertierung oder Abwicklung.
Eine einzelne bestandene Vortestmeldung genügt nicht als Abschlussnachweis.

## Danach die gesamte Maschine aufbauen

Nach vollständig bestandenem Kurztest:

```
NX_CNC_Gesamtansicht.py
```

Die neue Standardausgabe liegt unter:

```
%LOCALAPPDATA%\SX35Z\NX_Output\
SX35Z_CNC_ANSICHT_07_3_<Zeitstempel>_<Kennung>\
```

Die Einstellung `output_root` in `NX_Ausgabe.json` wird weiterhin beachtet.
Nach vollständig erfolgreichem Gesamtaufbau nennt `HAUPTBAUGRUPPE.txt` die
Hauptdatei. Den gesamten Ausgabeordner mit Teilen und Unterbaugruppen zusammenhalten.

**Kein automatisches Fortsetzen:** Die bereits gespeicherten 406 Teile des
alten Laufs werden weder gelöscht noch überschrieben, aber auch nicht automatisch
wiederverwendet. Der Gesamtaufbau startet in einem neuen Ausgabeordner. Der Kurztest
verhindert, dass erst nach erneutem Aufbau von 406 Teilen die Formel geprüft wird.

## Diagnose bei erneutem Abbruch

Die neue `NX_Fehlerprotokoll.txt` mit der Zeile `KSS-Formelpatch: 07.3` ist der
maßgebliche Ausgangspunkt. Die übersetzte Formel und ihre 1-mm-Referenz werden
protokolliert. Nach erfolgreichem Formelvortest liegt unter `_api_test` zusätzlich
`NX_KSS_Formelprobe_073.json` mit den gemessenen Vorformkörpern.

Die vorhandenen optionalen Metadaten-/Reference-Set-Hinweise sind nicht der hier
behobene Abbruch. Der ältere Referenzhash-Hinweis wird nicht verdeckt oder durch
einen ungeprüften Sollwert ersetzt. Die Einzeloperationen behalten ihre
Geometrieprüfungen.

## Prüfgrenzen

Die lokalen Tests prüfen Übersetzung, Einheitenalgebra und unveränderte
Zahlenwerte. Einheitenkonflikte werden in einem separaten Rechenmodell nachgestellt;
NX-Objekte für den betroffenen Setter werden nachgebildet. Das ist **kein NX-Lauf**.
Der ursprüngliche Fehler wurde vor der Änderung im betroffenen Codepfad reproduziert.
Parameterabhängigkeit wurde unter anderem für Auslassbreite, -tiefe, -position,
Blechdicke und Gestelltiefe geprüft.

Dein Protokoll belegt reale NX-Ausführung des alten Standes bis Teil 406. **Der neue
Patch 07.3 wurde hier nicht in Siemens NX ausgeführt.** Eine vollständige native
Baugruppe oder Fehlerfreiheit der späteren Schritte wird damit nicht behauptet.
Es erfolgt keine neue Kollisions-, Dichtheits-, Festigkeits- oder Sicherheitsfreigabe.
Modellrezepte, Geometrieparameter und Vorschauen sind gegenüber 07.2 unverändert.
