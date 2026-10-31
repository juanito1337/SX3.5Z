# Projektstatus zum Codex-Übergabestand

## Fortschreibung 31.10.2026: Stand09 erstmals hier vollstaendig nativ erzeugt

Nach Nutzerentscheidung wurden neue Dateien ausschliesslich aus `projekt/`
erzeugt, ohne alte CAD-Dateien des Rechners zu verwenden. Unter `cad/nx/` liegt
Lauf `SX35Z_CNC_UMSETZUNG_09_20261031_131548_912329_ecb147c4fdab` mit 560
Einzelteilen, 20 Unterbaugruppen und einer Hauptbaugruppe sowie drei API-Pruefteilen.
NX-2406-Gesamtaufbau und anschliessendes Oeffnen in frischer NX-Sitzung endeten
mit Exitcode 0. Alle 560 Einzelteile wurden mit je einem Koerper voll geladen;
21 Teile wurden beim Aufbau als native Blechkoerper bestaetigt (`required`).

Fuer den Lauf wurde ein nativer Metadatenfehler korrigiert: NX-Ausdruecke
unterstuetzen keine Benutzerattribute (OM 580023). Herkunftsangaben liegen jetzt
am Part unter `SX_EXPR_<Parameter>_*`; Wert und Persistenz wurden nativ geprueft.
Keine Rezeptgeometrie oder Modellparameter wurden dazu geaendert.

Der historische Rezept-Hash stimmt trotz unveraenderter Rezeptquelldateien nicht
mit dem aktuellen Lauf ueberein. Der vorhandene Generator aktiviert deshalb
keinen historischen OpenCascade-Referenzvergleich. Seine nativen Werkzeuglagen-,
Volumen- und Boolean-Pruefungen bleiben aktiv. Ursache der Hashabweichung offen.
Offline-pytest wurde versucht, konnte mangels Standard-Python nicht starten
(Exitcode 9009). Die folgenden Angaben zur alten Uebergabe bleiben historisch.
35 Istmasse, sechs Anschlusskonflikte und alle mechanischen Freigabegrenzen
bleiben offen. Details und Befehle: `cad/README.md` und Lieferstand-Nachweise.

**31.10.2026.** Quelle für den Code: `SX35Z_CNC_Umsetzung_09.zip`, unverändert unter `projekt/`.
Dies ist eine Bestandsübernahme, kein neuer Funktionsstand10.

## Ziel und tatsächlicher Nutzerkontext

Die SX3.5Z ist beim Nutzer vorhanden und zerlegt; Istmaße können aufgenommen werden.
Ziel: eine praktisch umsetzbare reine CNC-Fräse, passende reale Kaufteile, native parametrische
NX-Konstruktion, vollständige Fertigungs-/Montageunterlagen und LinuxCNC/Mesa 7i95T.
Die ursprüngliche Anforderung verlangt Einbindung der realen NX-Ausgangsbaugruppe und
Originalschutz. Der jetzige Gesamtansichtsgenerator rekonstruiert dagegen aus Rezepten auf
v4.8-Modellkoordinaten. Diese Differenz ist noch zu schließen und darf nicht verschwiegen werden.

## Mitgeliefert und überprüfbar

- 335 unveränderte Dateien der Umsetzung09, darunter Python-Journale, Parameter, Tests,
  Kaufteil-/Modellzuordnung, Excel, PDF/Word, HTML-Ansicht, Quellen und historische Prüfberichte.
- 72 Original-Fotodateien und sieben ältere NX-Screenshots; außerdem drei klar getrennte
  generierte Konzeptbilder. Quellen sind in `referenzen/QUELLENINDEX.json` erfasst.
- Originalanforderungen, gescanntes Maschinenhandbuch, OCR-Fassung/Text, BF20-alt/neu-Archive.
- Historische NX-Fehlerprotokolle und die getrennten Quellzweige Bestandsmodell v4.8 und Entwicklung10.
- KEINE tatsächlich auf dem Nutzerrechner erzeugten oder manuell geänderten nativen `.prt`-Dateien.
  Der ältere STEP-Bestand ist nur eine Foto-Rekonstruktion, kein Ersatz für die fehlenden Original-PRT.

## Konstruktionsstand09 – aus mitgeliefertem Prüfbericht übernommen

| Bereich | Stand / Nachweisgrenze |
|---|---|
| Gesamtmodell | 560 Körper, 20 Gruppen, 1.829 Operationen laut Bericht09; hier keine vollständige Geometrie-Neuberechnung |
| Einkauf | 69 Positionen, teils konkrete Artikel, teils offene Systempakete; nicht pauschal bestellfreigegeben |
| Fertigung | 148 Positionen; noch nicht alle mit fertigen tolerierten Zeichnungen |
| Istaufmaß | 35 fehlende Einträge laut Bericht09; Standardparameter sind keine Messbestätigung |
| Verkleidung | Kompakter Blechentwurf, breite zweiteilige Senktür, äußerer anliegender Schrank, Späne/KSS-Rücklauf |
| ATC | Sechsplatz-Magazinoption; automatische Spann-/Löseeinheit und vollständiger Wechselablauf fehlen |
| Originalspindel | Weiter als SK30/M12 DIN2080 modelliert; BT30-Halter sind Raumreferenzen |
| Maschinenanschlüsse | Sechs statische Konflikte weiter offen; siehe `uebergabe/BEKANNTE_PROBLEME.json` |

Datenquelle: `projekt/Pruefung_09/Pruefbericht_09.json`.

## Was neu bei dieser Übergabe geprüft wurde

Die bestehende Suite wurde am unveränderten Code erneut ausgeführt: **112 Tests und 91 Untertests
bestanden**, Linux/Python 3.13.5, pytest 9.0.2, CadQuery 2.8.0 / OCP 7.9.3.1.1.
Das ist keine Windows-/NX-2406-Ausführung und kein neuer Vollnachweis aller 560 Körper.
Weitere Paketprüfungen einschließlich Hashes und ZIP-Wiederentpacken stehen unter `uebergabe/pruefung/`.

## Was echte Nutzer-NX-Protokolle belegen

`referenzen/nx_protokolle/NX_Fehlerprotokoll(8).txt` dokumentiert einen Lauf07.2:
allgemeiner API-Test und native Blechprobe erfolgreich, Teile bis406 gespeichert,
Abbruch bei407 `A407_KSS_Trichter_links` durch Dimensionskonflikt. Das ist KEIN vollständiger
Lauf09. Frühere Logs dokumentieren die zuvor korrigierten Namespace-/Preferences-Probleme.
Der aktuelle Quellcode enthält den späteren Formelpatch07.3. Ein erfolgreicher vollständiger
09-NX-Lauf ist durch die vorhandenen Protokolle nicht belegt.

## Verbleibende wesentliche Hindernisse

Maschinengenaue Anschlüsse und Wandstärken, sechs Konflikte, fertige Spindelenden,
Antriebs-/Bremsauslegung, Versorgung/Rückspeisung, vollständiger Stromlaufplan,
Blechabwicklungen und Toleranzzeichnungen, Türgleichlauf/Fangmechanik/Dichtheit,
KSS-Leistung/Filterung und automatische Spindelspannung/Orientierung/Sensorik.
Diese offenen Punkte verhindern Fertigungs-, Bestell- und Inbetriebnahmefreigaben.

## Entscheidungsgrenze beim Spannpaket

Zuletzt wurde die Untersuchung einer vollständigen BT30-ATC-Spindelpatrone als bevorzugte
Richtung empfohlen. Der Nutzer hat nach dem Einbauprinzip gefragt, aber keinen konkreten Artikel,
keine Abmessungen und keinen irreversiblen Kopfumbau freigegeben. Details in `uebergabe/SPANNPAKET_ATC.md`.
