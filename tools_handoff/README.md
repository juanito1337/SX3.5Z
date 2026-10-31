# Integritätsprüfung

Python3.10+, nur Standardbibliothek. Liest Dateien, schreibt und installiert nichts.
Vom Paketstamm:

```powershell
python tools_handoff/verify_package.py
python tools_handoff/verify_package.py --manifest uebergabe/BASIS09_SHA256.json
python -m unittest discover -s tools_handoff -p "test_*.py" -v
```

Exitcode0 bedeutet: alle im jeweiligen Manifest aufgeführten Dateien sind bytegleich.
Exitcode1 bedeutet: fehlende/veränderte Dateien oder ungültiges Manifest.
Zusätzliche neue Dateien sind nicht Teil dieser Hash-Prüfung. Nach bewussten Änderungen ist
ein Hashunterschied normal; die Ausgangsmanifeste sind historische Nachweise, keine Reparaturquelle.
Nicht zur Unterdrückung von Differenzen automatisch neu schreiben.

Die Prüfung führt KEIN NX-Journal und KEINEN Maschinenbefehl aus.
