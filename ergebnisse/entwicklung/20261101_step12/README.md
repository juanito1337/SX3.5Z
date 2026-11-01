# STEP-Export Stand12, 01.11.2026

Quelle: Git346934ac2d1be35b0ba68bb5fde998e00d3d3431, gespeicherte native
WECHSEL-Baugruppe fdd87de5a7ba. Keine geometrischen Aenderungen.

Aus Paketstamm ausgefuehrt:

- `C:/Siemens/nx2406/NXBIN/run_journal.exe ergebnisse/entwicklung/20261101_step12/export_step.py`
  NX2406/Python3.10.15, Exit0. Rohprotokoll `nx_export.log`,
  Uebersetzerprotokoll `../../../cad/step/SX35Z_12_Wechselstellung.log`.
  SHA256, Datum und Groesse stehen in `export_result.json`.
  Alle482 Quell-PRT-Dateien per SHA256 unveraendert.
- `.venv/Scripts/python.exe ergebnisse/entwicklung/20261101_step12/verify_step.py`
  Separate CadQuery/OCP-Umgebung, Exit0; `readback.log` und `readback_result.json`.
  STEP wieder eingelesen:461 Volumenkoerper, alle gueltig. Dies ist eine
  unabhaengige Offline-Pruefung, kein nativer NX-Reimport.

Erstversuch Exit1: Standardauswahl erfasste nur die koerperlose Hauptbaugruppe;
Uebersetzer meldete "No parts in current input file". Auswahl explizit auf
EntireAssembly und Eingabepfad gesetzt, danach erfolgreicher Export.
Erstversuchjournal/-protokolle separat erhalten.

Die STEP-Datei enthaelt die vollstaendige Maschine samt Einhausung und
Wechsler in Wechselstellung. Vereinfachte Kaufteile und alle offenen
Konstruktionspunkte von Stand12 bleiben bestehen. Keine Fertigungs- oder
Betriebsfreigabe. Native parametrische PRT-Dateien bleiben die CAD-Quelle.
