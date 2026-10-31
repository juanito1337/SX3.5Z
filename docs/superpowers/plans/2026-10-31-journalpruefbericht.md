# Journalpruefung und Entwicklungsdiagnose

Datum: 31.10.2026, Europe/Berlin. Gepruefte Quellrevision:
`6631f8b65e7a1188d24391d8b10ce84c1cd7b114`.
Aktive Produktionsskripte und Modellparameter wurden in diesem Pruefauftrag
nicht geaendert. Ergebnisse: `ergebnisse/entwicklung/20261031_134859/`.

## Native Siemens-NX-Pruefung

Umgebung: Windows, Siemens NX 2406, NX-Python 3.10.15. Je Journal ein frischer
Prozess. Befehl jeweils:
`C:/Siemens/nx2406/NXBIN/run_journal.exe <absoluter Journalpfad>`.
Beim Wiedereroeffnen verweist `SX35Z_VERIFY_RUN` auf den gerade neu erzeugten
Gesamtlauf. Vollstaendige Befehle, Startzeit, Dauer, Ausgabe und Exitcode stehen
in `journal_matrix.json`, Rohprotokolle in `<Journalname>.stdout.txt`.

| Journal unter projekt/ | Umfang | Ergebnis |
|---|---|---|
| NX_Metadaten_Pruefen.py | Herkunft am Part, unveraenderter Ausdruck, Speichern | Exitcode 0 |
| NX_Blech_Pruefen.py | 1 neuer Tuerrahmen, native Blechkonvertierung | Exitcode 0 |
| NX_KSS_Pruefen.py | 10 geneigte KSS-Vorformen samt Formelvortest | Exitcode 0 |
| NX_Umbau_Kern_Pruefen.py | 154 neue Kern-/Schrank-/Prueffeldteile | Exitcode 0 |
| NX_Normteile_ATC_Pruefen.py | 129 neue09/geaenderte Teile | Exitcode 0 |
| NX_CNC_Gesamtansicht.py | 560 Einzelteile, 20 Unterbaugruppen, Hauptbaugruppe | Exitcode 0 |
| NX_Git_Lieferstand_Pruefen.py | neuen Gesamtlauf vollstaendig frisch laden | Exitcode 0 |

Beim Gesamtaufbau wurden 21 native Blechkonvertierungen im Modus `required`
protokolliert. Bei frischem Oeffnen: 560 vollstaendig geladene Einzelteile mit
je einem Koerper, 20 Gruppen, keine Ladefehler, persistente sheet_t-Herkunft und
Werte in 142 Teilen. Keine alten CAD-Dateien vom Rechner verwendet.

Der neue Test-Gesamtlauf heisst
`SX35Z_CNC_UMSETZUNG_09_20261031_135314_122605_c81c49e3187f`.
Alle in diesem Auftrag erzeugten Testlaeufe wurden nach Abschluss unter
`ergebnisse/entwicklung/20261031_134859/NX_Laeufe/` archiviert. Die originalen
Ausfuehrungspfade bleiben unveraendert in den Rohprotokollen; die Zuordnung
steht in `lokales_laufarchiv.json`. Dies ist keine Wiedereroeffnungsbehauptung
fuer die nachtraeglich verschobenen Archivpfade. Der bereits versionierte
CAD-Lieferstand `...131548_912329_ecb147c4fdab` bleibt unveraendert; keine neue
Geometrieversion durch einen reinen Wiederholungstest.

## Offline-Pruefungen

Separate lokale `.venv`, erstellt mit der vorhandenen gebuendelten CPython-
Laufzeit. Keine globale oder NX-Python-Installation geaendert. Installiert aus
`requirements-offline.txt`; genaue Versionen in `offline_freeze.txt`:
Python 3.12.14, pytest 9.0.2, CadQuery 2.8.0, OCP-Paket 7.9.3.1.1.

| Befehl | Umfang | Ergebnis |
|---|---|---|
| `../.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider` (cwd projekt) | gesamte aktive Suite | 112 passed, 91 subtests passed, Exitcode 0 |
| `.venv/Scripts/python.exe -m unittest discover -s tools_handoff -p "test_*.py" -v` | Paketpruefer-Hilfstests | 10 Tests: 9 bestanden, 1 skip, Exitcode 0 |
| `.venv/Scripts/python.exe tools_handoff/verify_package.py` | historische Paketidentitaet | 470/477 identisch, sieben Abweichungen, Exitcode 1 |

Der Skip ist `test_symlink_outside_root_fails`: Symlinks sind in dieser
Windows-Umgebung nicht verfuegbar. Kein Test wurde fuer diesen Lauf ausgeblendet.
Der Kurzpfad in `pytest_baseline_meta.txt` ist relativ zum Paketstamm notiert;
fuer die dort genannte cwd `projekt/` gilt der oben angegebene `../.venv/`-Pfad.
Die sieben Hashabweichungen sind die bereits in `6631f8b` absichtlich geaenderten
Dateien NEXT_STEPS.md, NX_ENVIRONMENT.md, PROJECT_STATUS.md, README_START.md,
projekt/NX_Ausgabe.json, projekt/nx_native.py und uebergabe/ENTSCHEIDUNGEN.md.
Das historische Manifest wurde nicht umgeschrieben. Der Paketcheck ist damit
weiterhin ein fehlgeschlagener Identitaetscheck gegen das Originalpaket,
kein fehlgeschlagener NX-Lauf.

## Debugging: historischer Rezept-Hash

Ursache nachgewiesen: plattformabhaengige letzte Floatstellen der sin/cos-
Berechnung werden in Rezept-Formelstrings serialisiert und exakt gehasht.
Ein Standard-Python-Diagnoseprozess reproduziert sowohl das echte NX-JSON
(`da8b4b...`) als auch exakt den historischen Hash (`6790b5...`), ohne
Produktionsdateien zu aendern. Zwei Decimal-Praezisionen liefern identische
historische Rekonstruktionen. Linux selbst wurde nicht erneut ausgefuehrt.

49 Zahlenunterschiede betreffen fuenf Teile, ausschliesslich Operationen;
Struktur, Parameter, 560 Teile und 1.829 Operationen bleiben identisch.
Maximale ausgewertete Laengendifferenz: 2,84e-14 mm. Das ist ein Nachweis zur
Serialisierung, kein neuer Volumen- oder Kollisionsnachweis.

Reproduktion und alle Einzeldifferenzen: `hashdiagnose/BEFUND.txt`,
`reproduce_recipe_hash.py`, `evidence.json`, `raw_stdout.txt`,
`recipe_historical_reconstructed.json` sowie der echte `recipe_nx310.json`.
Keine globale FMA-Einstellung geaendert. `ReferenceCheck` bleibt unveraendert:
historischer OpenCascade-Volumenvergleich wegen exaktem Hashunterschied nicht
aktiv; native Werkzeuglagen-/Volumen-/Boolean-Pruefungen bleiben aktiv.
Eine neue versionierte Referenzidentitaet ist Roadmap-Paket R01, noch nicht umgesetzt.

## Detailbefunde und naechste Arbeit

Roadmap: `2026-10-31-entwicklungsroadmap.md`, Pakete R00–R14 mit ausfuehrbaren
Prompts, Eingaben und Abnahmen. Jetzt belegte Luecken sind insbesondere fehlende
Maschinenbefestigungen/Loslager-Lastabtraege, Sensorhalter, Spindelenden,
105 ausdruecklich fehlende Zeichnungen, falsche KSS-Fertigungszuordnungen,
26 offene Beschaffungspakete und unvollstaendige Elektrik/Tuer/KSS/ATC-Auslegung.

Naechstes begrenztes Softwarepaket: R02 Fertigungsmetadaten und Nachweisregister.
Danach Messmatrix R03 und API-Pilot R08; massabhaengige Achs-/Spindelpakete erst
mit den benannten Eingaben. R00 ist abgearbeitet; R01-Diagnose abgeschlossen,
produktive Referenzmigration und konstruktive Pakete sind nicht erledigt.

## Nachweisgrenzen

Keine neue Journal-Laufzeitfehlfunktion in den sieben Prueflaeufen festgestellt;
daher keine spekulative Produktionscode-Korrektur. Der zuvor korrigierte
Metadatenfehler bleibt behoben. Kein neuer Nachweis fuer sechs bekannte
Anschlusskonflikte, fehlende 35 Istmasse, volle Bewegungsbahnen, Toleranzen,
Festigkeit, reale Passung, KSS-Dichtheit, elektrische Sicherheit oder ATC-Betrieb.
Keine Fertigungs-, Bestell- oder Betriebsfreigabe.
