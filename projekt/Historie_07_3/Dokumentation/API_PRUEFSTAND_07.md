# NX API-Prüfstand 07

Keine native NX-Ausführung in dieser Umgebung. Vorhandene Modellierungs-,
Speicher- und Blechkonvertierungspfade bleiben erhalten.
`nx_native.py::expr_text` lässt zusätzlich das Funktionswort `sqrt` unverändert
durch; die Python-Rezeptauswertung akzeptiert ausschließlich sichere Arithmetik
und diese eine Funktion. Das ist kein Aufruf eines erfundenen NX-API-Builders.
Im realen Vortest wird jetzt `API_Schraegblech07_Normaldicke` aufgebaut und
vermessen; dies prüft vor dem Gesamtaufbau die neue Ausdrucksverwendung.
Die konkrete Bindung und Lizenzverfügbarkeit muss in NX 2406 bestehen.
Der Modus `required` bleibt Pflicht für markierte Kantprofile, kein stiller Ersatz.
Unabhängige Geometrieprüfungen prüfen scharfkantige Vorformen; Kollisionen nach
der NX-Blechkonvertierung und fertige Abwicklungen sind nicht nachgewiesen.
