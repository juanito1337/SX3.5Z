# Konzept13: unabhaengige Reviews und Korrekturen,01.11.2026

Basis e8a0029, anschliessend neue13er Arbeitsdateien. Mechanikreview sowie
frischer Gesamt-/Codereview durch getrennte Agenten. Nur Offline-Geometrie,
keine native NX-Erfolgsbehauptung aus den Reviews.

Behoben: Greiferbacken oeffnen22mm je Seite; Werkzeugzustand Magazin/Arm/
Spindel getrennt; zusaetzliche28mm Anzugsbolzenhuelle. Radialzylinder seitlich
neben Fuehrung/Schlitten, sichtbare Konsolen/Anlenkung; Indexverriegelung und
Magazinmotor aus Scheibe/Werkzeug/Lagerplatte herausverlegt. Tropfboden mit
Stuetzausschnitt. Unmontierte Anschlagbloecke entfernt, Endverriegelung bleibt
auszuarbeiten. Radialfuehrung bekommt80mm breite Deckauflage.

Frischer Abschlussreview fand zwei wichtige Befunde:

1. Hubplatte gegen festen Hubmotor bei90mm Hub:32000mm3. Motor auch gegen
   Mast:17760mm3. Motor nachZ585 auf Montageplatte am Mastkopf versetzt,
   Fuehrungen/Spindel/Kupplung verlaengert; unteres Lager ergaenzt.
2. Eingezogenes Greifergehaeuse gegen beide Radialschienen:7040mm3 jeSchiene.
   Fuehrungen und Deckauflage50mm zurueckgesetzt; verbleibende Auflage im
   ausgefahrenen Zustand80mm im Entwurf.

Beide Befunde vor Korrektur mit `test_lift_motor_and_radial_rails_do_not_block_motion`
reproduziert:2 fehlgeschlagene Tests, Rohlog review_red.log. Danach Regression
und Gesamtsuite sowie erweiterte Bewegungspruefung. Die betreffenden Paarungen
sind jetzt auch ueber die Bewegungsstichproben im Checker enthalten.

Noch offen: reale Greifer-/Taschenretention und Drehlagenfuehrung, feste
Endlagenverriegelung/Bremse, konkrete Antriebe/Lager/Fuehrungen, mechanische
Passungen/Schrauben/Schweissdetails, volle kontinuierliche Bahn, reale
Spindel-/Werkzeugdaten. Keine beliebig hohe Bestueckung im Wechselraum.

Weitere Korrektur01.11.2026: konservative Hoehe unter Wechselbahn140 auf125mm
reduziert. Arm-Unterkante Z320 liegt unter Werkzeugspitze Z335. Regression
workspace_limit_red.log reproduziert140!=125, danach Gesamtsuite201/99 gruen.

Erster Vollaufbau NX: Exit1, OSError22 beim erneuten Schreiben Erzeugte_Teile.json.
Pfad/Datei vorhanden, ausreichender Speicherplatz. 1000 Ueberschreibungen einer
separaten Probe im selben Ordner in NX erfolgreich (io_probe.log Exit0).
Ursache nicht reproduziert; keine spekulative Modell-/API-Aenderung.
Erneuter Vollaufbau in neuem Verzeichnis. Kein fremder Prozess beendet.
