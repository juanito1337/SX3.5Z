# API-Abgleich – Blechpatch 07.2

Stand: 2026-10-30. Kein Zugriff auf Siemens NX 2406 zur Ausführung.

## Primärer Laufzeitbefund

Benutzerdatei `NX_Fehlerprotokoll(7).txt`, Zeilen 120–165 des Originals:
- Blechvorform entsteht.
- `UF.Modeling.AskFaceData` ist aufrufbar; die Basisfläche wird eindeutig gefunden.
- `Preferences.Sheetmetal` löst einen AttributeError aus.
- Der native ConvertToSheetmetal-Builder wird in diesem Lauf nicht erreicht.

## Dokumentationsabgleich

1. Von Siemens verfasste NXOpen-C++-Referenz, gespiegelte Ausgabe:
   https://www.ugapi.com/doc/nxopen/a04630.html
   Klasse `NXOpen::Preferences::PartPreferences`, Member `PartSheetmetal`.
   Herkunftsdatei `Preferences_PartPreferences.hxx`, Copyright Siemens 2013.
2. Dieselbe Siemens-Referenz für das zurückgegebene Objekt:
   https://www.ugapi.com/doc/nxopen/a04631.html
   `SetThickness(bool, string)`, `SetBendRadius(bool, string)`,
   `SetNeutralFactor(bool, string)` und `Commit()`.
3. Vergeblicher direkter Zugriff auf Siemens-Dokumentationsportal:
   https://docs.sw.siemens.com/en-US/doc/209349590/PL20230622300201030.nxopen_prog_guide/en_US/nxopen_prog_guide.html
   Beim Abruf nicht zugänglich; keine Aussage aus diesem nicht gelesenen Inhalt.

Die Referenzen sind KEIN Beleg eines erfolgreichen NX-2406-Pythonlaufs. Der Patch
verwendet nur die dokumentierte Eigenschaft, prüft die tatsächlichen Methoden
vor dem Schreiben und protokolliert ihre lokalen Docstrings. Kein automatisches
Raten alternativer Namen; keine andere API nach einem tatsächlichen Setterfehler.

Die Struktur von SheetmetalManager/ConvertToSheetmetalBuilder wird hier nicht
neu entworfen. Native Körpererkennung und Dickenprüfung bleiben unverändert.
Ein weiterer Fehler beim Setter oder Commit würde einen weiteren Laufzeitbefund
liefern, nicht einen bestätigten Konvertierungserfolg.

## Testlücke aus 07.1

Die bisherigen nachgebildeten Preferences-Objekte exponierten ebenfalls
`Sheetmetal`. Damit konnten die Tests genau diesen Namensfehler nicht erkennen.
Beide Fixtures wurden korrigiert. Die neuen strengen Fixtures sind getrennt vom
Adapter definiert und erlauben den dokumentierten Zugriff; sie bleiben Mocks.

## Selbstprüfung

- Diff nur an zwei produktiven Dateien: Blechadapter und Startjournal-Version.
- Alle bestehenden Geometrie-/Parameterdateien mit Quellarchiv vergleichen.
- Kein Pfad zu gespeicherten Original-PRTs wird geändert.
- Kein automatischer Moduswechsel, kein unterdrückter Setter-/Lizenzfehler.
- Test- und Archivprüfung nach frischem Entpacken.
- Keine unabhängige Review-Instanz und keine lokale NX-Laufzeit vorhanden.
