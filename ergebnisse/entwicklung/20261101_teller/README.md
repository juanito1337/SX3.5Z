# Prueflauf01.11.2026: Teller10 und KSS

Basis: e87f522. Exakter nativer Quellstand: `native_source_hashes.json`;
Quellcommit und Lieferumfang siehe `cad/nx/...13e8dd801b5f/PRUEFSTATUS.json`.
Keine Hardware, Lieferantenanfrage oder Bestellung ausgefuehrt. Historische
Quellen,09-Nachweise und urspruengliches Paketmanifest bleiben erhalten.

## Frische Abschlusspruefungen

| Pruefung | Umgebung | Ergebnis | Befehl/Datum/Rohprotokoll |
|---|---|---|---|
| Aktive pytest-Suite | Windows CPython3.12.14, pytest9.0.2, CQ2.8/OCP7.9.3.1.1 | Exit0;163 Tests +91 Untertests | verification_final.meta.json; pytest_final.stdout.txt |
| Handoff-Hilfstests | gleiche Standard-Python-Laufzeit | Exit0;9 bestanden,1 Symlinktest uebersprungen | verification_final.meta.json; handoff_final.stdout.txt |
| Original-Paketmanifest | gleiche Standard-Python-Laufzeit | Exit1;451/477 bytegleich,26 geaendert | verification_final.meta.json; package_original_final.stdout.txt |
| Sieben NX-Journale | NX2406/Python3.10.15 Windows | jeweils Exit0 | native_matrix.json; final_NX_*.stdout.txt |
| Vollstaendiger NX-Lauf | wie oben, Blech required |511 Einzelteile,20 Unterbaugruppen,19 native Blechkonvertierungen | final_NX_CNC_Gesamtansicht.stdout.txt |
| Frisches natives Oeffnen | wie oben |511 Einzelteile voll geladen, je1 Koerper, Metadaten persistent | final_NX_Git_Lieferstand_Pruefen.stdout.txt; Bericht im Lieferordner |
| KSS-Geometrie | Offline CadQuery/OCP | Exit1;6 Sensorreferenz-Kollisionen, Achsen/Korb0 | offline_geometry.meta.json; kss_geometrie_final.stdout.txt/json |
| Teller-Endpunkte | Offline CadQuery/OCP | Exit0;552 Checks ohne Schnittvolumen | offline_geometry.meta.json; teller_endpunkte_final.stdout.txt/json |

Die26 Manifestabweichungen stammen aus bewusst versionierten Weiterentwicklungen
seit der urspruenglichen Uebergabe; das alte Manifest wurde nicht ersetzt.
Dies ist kein gruener Identitaetsnachweis des Originalpakets. Neue Quellen und
native Dateien sind separat gehasht. Zusagen ueber Nicht-Pruefgegenstaende sind
ausgeschlossen: volle ATC-Bahn, Spindelspannung, Fertigungs-/Betriebssicherheit,
reale Maschinenpassungen, Tankauszug, Abwicklungen und Herstellerkonformitaet.

Der KSS-Check enthaelt6 unmontierte IFS206-Prueffeldreferenzen; nicht mit den
6 bekannten realen Maschinenanschluss-Konflikten verwechseln.35 Istmasse fehlen.

## Review und lokale Sicherungen

Gegenbeispiele und RED/GREEN-Protokolle liegen hier. Ein unabhaengiges Review
fand vier reproduzierbare Fehler: Rezept-Tupel/Listenserialisierung, statisches
Haubendach bei veraenderter Tellerhoehe, zu niedriger Dichtkragen und alte
Dokumentgeneratoren. Alle vier korrigiert, anschliessend Gesamtsuite und alle
sieben nativen Journale ausgefuehrt. Dokument-/Tabellenexport auf Arbeitskopie.

Nur der vollstaendige native Lieferlauf ist in cad/nx versioniert. Die sechs
neu erzeugten Teil-/API-Testlaeufe wurden nach Abschluss lokal in
`NX_Prueflaeufe/` verschoben; ihre urspruenglichen Erzeugungspfade stehen
unveraendert in native_matrix.json. Sicherungs-ZIP, Arbeitskopien, Cache und
Teil-PRT bleiben lokale Auditdaten und werden nicht erneut in Git dupliziert.

Die neue HTML-Vorschau wurde aus einer separaten Arbeitskopie erzeugt. Der
eingebettete Browser hat das Oeffnen lokaler file-URLs blockiert; keine Umgehung,
keine behauptete visuelle Abnahme. Der native Speichern-/Oeffnen-Nachweis ist
davon unabhaengig. Originale Geometrie_Referenz_Ansicht.json blieb unveraendert.
