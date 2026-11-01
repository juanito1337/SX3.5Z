# SX3.5Z CNC – verbindliche Projektregeln

## Vor jeder Arbeit lesen

`README_START.md`, `PROJECT_STATUS.md`, `NEXT_STEPS.md`, `NX_ENVIRONMENT.md`,
`uebergabe/ENTSCHEIDUNGEN.md`, `uebergabe/SPANNPAKET_ATC.md` und
`referenzen/anforderungen/Eingefügter Text(7).txt`.
Bei Widersprüchen zwischen Implementierung und älterem Bericht: Widerspruch dokumentieren,
Quelldatum/Revision nennen; niemals einen Bericht über das beobachtete Programmverhalten stellen.
Aus dem originalen Prompt stammen die verbindlichen NX-Anforderungen; spätere ausdrücklich
getroffene Nutzerentscheidungen ergänzen sie. Bearbeiterempfehlungen sind keine Nutzerfreigaben.

## Ziel

Vorhandene reale SIEG SX3.5Z zu einer reinen CNC-Fräse mit LinuxCNC/Mesa 7i95T entwickeln.
Native parametrische NX-Einzelteile und Gesamtbaugruppe, reale Kaufteile, passende Stückliste,
Fertigungsunterlagen und Bauanleitung müssen gemeinsam gepflegt werden. ATC ist ein zusätzliches
Ziel, derzeit nicht betriebsbereit. Keine vollständige Neukonstruktion aus dem Gedächtnis.

## Aktiver Stand und Originalschutz

- Ausschließlich `projekt/` ist der aktive Programmstand11 (rechte Teller-/Wechselstellung und Spaenefang auf Basis09/10). Historische ZIPs und
  `projekt/Historie_07_3/` nicht über aktive Dateien kopieren. Ältere nummerierte Module im
  aktiven Stamm sind teilweise importierte Abhängigkeiten, also nicht nach Dateinamen löschen.
- Die Dateien unter `referenzen/` sind Quellen; `eingaben/original_nx/` enthält künftig
  geschützte Nutzerkopien. Nicht überschreiben, nicht pauschal bereinigen, nicht destruktiv speichern.
- Vor Änderungen lokale Nutzerparameter/Dateien vergleichen und Ausgangsstand sichern.
  Neue NX-Ergebnisse in neue Laufverzeichnisse schreiben. Keine globale NX-/Python-Installation ändern.
- Keine Ausführung von Hardware, Maschinenbewegungen, Ventilen oder Spindelbefehlen als Seiteneffekt
  von Tests. Kein automatischer Einkauf, keine Lieferantenanfrage versenden, keine Veröffentlichung.

## Arbeitsweise und Superpowers

Verfügbare Superpowers-Skills verwenden: Kontext/Brainstorming vor neuen Entscheidungen,
writing-plans für umgrenzte Arbeitspakete, test-driven-development bei Codeänderungen,
systematic-debugging bei Fehlern, verification-before-completion vor Erfolgsbehauptungen,
requesting-code-review für größere Änderungen. Pläne unter `docs/superpowers/plans/` pflegen.
Ist ein Skill nicht verfügbar, dies melden; nicht behaupten, er sei aufgerufen worden.
Das ZIP installiert kein Plugin und setzt keine Freigabe-/Sandboxregeln außer Kraft.
Kleine, überprüfbare Änderungen; keine pauschale Umstrukturierung vor Reproduktion der Basis.

## Native NX-Anforderung

Siemens NX 2406 / NX Open Python ist das Ziel. Keine erfundenen API-Methoden oder Signaturen.
Lokale NX-Dokumentation, aufgezeichnete Journale und reale Laufprotokolle bevorzugen.
NX-spezifischer Code muss in der NX-Laufzeit geprüft werden. Mocks, CadQuery/OCP-Prüfungen,
Browseransichten, AST-Prüfungen oder grüne pytest-Läufe beweisen keine native NX-Ausführung.
Andere Kernel nur als ausdrücklich ergänzende Offline-Prüfung, nicht als Ersatz für native Parts.
Blech-Pflichtmodus `required` nicht zur Fehlerumgehung auf `solid` umstellen.
Versionen 4.8 (Basisadapter), 07.2 (Blechadapter), 07.3 (Formeln) und 11 (aktuelles Modell auf Basis09/10) sind absichtlich verschieden.

## Maße, Kaufteile und Freigaben

Gemessen / Herstellermaß / Entwurf / vereinfachte Geometrie / unbestätigt getrennt kennzeichnen.
Keine Bildgeneratorbilder oder perspektivischen Maßbandfotos zu freigegebenen Passungen erklären.
SK30/DIN2080/M12 der Originalspindel nicht als BT30-ATC-Schnittstelle umetikettieren.
Eine komplette BT30-Patrone wurde als bevorzugt zu untersuchende Option empfohlen, nicht bestellt
oder vom Nutzer endgültig ausgewählt. Quellen und Schnittstellen vor Anpassung am Kopf belegen.
Bewegungshüllen sind keine Bestellzeichnungen. Gussfreistellungen brauchen Istmaß, Wandstärke,
Bezugsflächen und Bearbeitungszeichnung. Keine Führungsflächen/Rippen auf Fotoannahmen abtragen.
AliExpress-Suchtreffer und historische Indexpreise sind keine bestätigten Angebote.

## Tests und eindeutige Befehle

Paketintegrität (ab Paketstamm, Standard-Python):
`python tools_handoff/verify_package.py`

Hilfstests (ab Paketstamm):
`python -m unittest discover -s tools_handoff -p "test_*.py" -v`

Bestehende Offline-Suite (Arbeitsverzeichnis `projekt/`):
`python -m pytest -q -p no:cacheprovider`

Die Suite verwendet CadQuery/OCP. Fehlende Pakete als fehlende Voraussetzung melden, Tests nicht
heimlich ausblenden. Tests für `Historie_07_3` sind nicht Teil des aktiven pytest.ini-Umfangs.
Für Berichte existiert `Projekt09_Berichte.py`; dieses Skript SCHREIBT CSV/JSON im Projekt.
Nur auf einer Arbeitskopie ausführen und die Änderungen prüfen. Dokumentgeneratoren unter `tools/`
haben zusätzliche Abhängigkeiten; nicht ungeprüft in NX installieren oder automatisch starten.

## Prüfaussagen

Jedes Ergebnis braucht Revision, Datum, Befehl, Umgebung, Umfang, Exitcode und Rohprotokoll.
Historische Nachweise unverändert erhalten; neue Ergebnisse unter `ergebnisse/` speichern.
"Nicht geprüft", "fehlgeschlagen", "nur offline geprüft" und "in NX nachgewiesen" unterscheiden.
Bekannte sechs Maschinenanschluss-Konflikte nicht mit Nullkollisionen einer Teilprüfung verwechseln.
`build_ready`, `purchase_released`, `machine_operation_enabled`, `atc_operational` nicht ohne
nachgewiesene sachliche Voraussetzungen auf true setzen. Softwaretests sind keine Sicherheitsfreigabe.

## Abschluss einer konstruktiven Änderung

Modell/Rezept + Parameter/Herkunft + Kaufteilkatalog + Stückliste/Mengen + Anleitung + Prüfungen
zusammen aktualisieren. Blechvorform und tatsächlich konvertiertes Blech separat prüfen.
Neue native Dateien erst nach realem Speichern/Öffnen als vorhanden melden.
Eigene Grenzen, unerledigte Konflikte und noch fehlende Istaufmaße ausdrücklich aufführen.
