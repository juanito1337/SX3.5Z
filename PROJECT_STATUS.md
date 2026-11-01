# Projektstatus zum Codex-Übergabestand

## Entwicklung12: BT30 auf rechter Saeulenkonsole,01.11.2026

Nutzer priorisiert sinnvolle Magazinbefestigung; Spindeltausch/Spannpaket folgen
separat.461 Modellkoerper,17 Gruppen. Grundplatte330x175x22/Scheibe280x16 nach
Bild,200mm Hub und180mm Werkzeugradius als unbestaetigte Arbeitsannahmen.
Feste Konsole mit oberen Rippen; alte Gestellstuetze/Kragen/Wannenoeffnung
entfallen. Vier Fangbleche bleiben. Offline190 Tests/99 Untertests sowie17
Stellungen/540 BRep-Pruefungen bestanden; native12-Lieferung separat nachweisen.
[Anleitung12](projekt/Dokumentation/Entwicklungsstand_12.md).


## Produktauswahl fortgeschrieben01.11.2026 – CAD weiterhin Stand11

AliExpress1005009887984460 vom Nutzer vorerst ausgewaehlt, sechs Original-
Screenshots jetzt im Repository gesichert. Direkte Maschinenbefestigung erlaubt,
Parkseite rechts bleibt. Grundplatte330x175x22mm und Scheibe280x16mm aus
Bildbeschriftung; AngebotsvarianteBT30 inzwischen vom Nutzer bestaetigt.
Greiferteilkreis, Bildzuordnung zur Lieferausfuehrung und nutzbarer Hub offen. SU32X200-S legt200mm nahe, bestaetigt aber keinen nutzbaren Magazinweg.

KatalogpositionO10-TELLER und Einkaufsliste11 verweisen auf den gewaehlten
Artikel (ein Paket) und weisen die abweichende Eigenentwurfsgeometrie klar aus.
Kein neuer nativer NX-Lauf, keine neue Maschinenrevision; alle bisherigen
NX-Nachweise gelten nur fuer ihre unveraenderten Lieferstaende.
[Auswertung und Integrationsbedarf](projekt/Werkzeugwechsler/RATTM_1005009887984460_Bildauswertung.md).

## Aktuell11: Nutzerkorrekturen01.11.2026

Rechte Parkseite ausdruecklich bestaetigt. Getrennte native PARK-/WECHSEL-
Baugruppen, jeweils454 Einzelteile/17 Unterbaugruppen. Vier neue Fangbleche
links/rechts;61 Originalanbauten entfernt, Demontageliste mit Funktionshinweisen.
Spindelmotor/Guss/Fuehrungsbaelge/CNC-Elektrik erhalten. Neue Zustellung389,33mm;
groessere Parkhaube mit11,1mm nominalem Gabeleckenabstand.

Neun native Journallaeufe Exit0, beide Gesamtstellungen gespeichert und in
frischen NX2406-Prozessen vollstaendig geoeffnet. Je19 native Blechkonvertierungen;
vier neue Fangbleche sind getrennt ausgewiesene geneigte Vorformen.
Native Halterkegelmessung in Wechselstellung stimmt innerhalb0,00001mm mit
nomineller Spindelachse/-hoehe ueberein. Keine reale SK30/BT30-Passungsfreigabe.
Offline173 Tests +99 Untertests,9 Wegstichproben/87 Schnittpruefungen und552
Endpunktchecks ohne Kollision. KSS Exit1 nur6 bekannte IFS206-Referenzkonflikte;
acht Achsecken und Korbauszug ohne Kollision, verformbare Baelge ausgeschlossen.

Spannpaket, Retention, volle Bahn, Festigkeit, elektrische Ersatzfunktionen,
35 Istmasse,6 Maschinenanschluss-Konflikte und Tankauszug weiter offen.
Anleitung: projekt/Dokumentation/Entwicklungsstand_11.md. Native Nachweise:
cad/README.md; Rohdaten: ergebnisse/entwicklung/20261101_revision11/.
Nachfolgende Staende10/09 sind historisch.

## Aktueller Entwicklungsstand10, 01.11.2026

Ausgangsrevision e87f522, neue Quellen durch native_source_hashes.json im
Prueflauf erfasst. Nutzer fordert Teller ausserhalb des Tisches und Spannpaket;
Eigenbau zulaessig, kein Budget gesetzt. Aktuell8er-Teller mit Gestellstuetze,
radialer Zustellreserve und Spritzschirm; kein ausgewaehltes Lieferantenprodukt.
Spannpaket ist nur als Raumreserve vorhanden, Originalspindel bleibt SK30/M12.

Nachgewiesen: sieben NX2406-Journale Exit0; Gesamtaufbau511 Einzelteile,
20 Unterbaugruppen,19 native Blechkonvertierungen im Modus required und frisches
Wiedereroeffnen aller Einzelteile. Offline163 Tests +91 Untertests bestanden.
552 begrenzte Teller-Endpunktpruefungen ohne Schnittvolumen; keine volle Wechselbahn.
KSS-Test Exit1: sechs Kollisionen unmontierter IFS206-Referenzen mit Leitblech;
Achsstichproben und Korbauszug ohne Kollision. Originale sechs Maschinenanschluss-
Konflikte und35 Istmasse weiterhin offen. Tankauszug nach hinten blockiert.

Behoben: KSS-Seitenluecke, Ruecklaufparametergrenzen, Serviceklappen-Demontagegruppe,
Blech-Fertigungsmetadaten sowie vier Reviewfehler (kanonischer Rezeptvergleich,
Haubenhoehe, Dichtkragenhoehe, veraltete Dokumentgeneratoren). Neue10-Tabellen
und Anleitung synchronisiert; alte09-Unterlagen erhalten. Lieferstand und
Pruefgrenzen: `cad/README.md` und `projekt/Dokumentation/Entwicklungsstand_Teller_10.md`.

Nutzerartikel AliExpress1005009887984460 noch nicht identifiziert, kein bestaetigter
Preis-Leistungs-Sieger. Lieferantenzeichnung und Kopfaufmass fehlen. Alle Bau-,
Bestell-, Betriebs- und ATC-Freigaben false. Folgende Abschnitte sind Historie.

## Entwicklungspruefung 31.10.2026, nach Revision 6631f8b

Alle sieben aktiven NX-Journale erneut in frischen NX-2406-Prozessen verarbeitet:
Exitcode jeweils 0, einschliesslich Gesamtaufbau und Wiedereroeffnung. Separate
lokale `.venv` eingerichtet: 112 Offline-Tests und 91 Untertests bestanden.
Hilfstests: 9 bestanden, 1 wegen nicht verfuegbarer Windows-Symlinks uebersprungen.

Die Rezept-Hashabweichung ist jetzt diagnostiziert: letzte Floatstellen von
sin/cos unterscheiden sich nach Rechenpfad. Echter NX-Hash und historischer
Hash sind aus identischem Code reproduziert; 49 Zahlenabweichungen in fuenf
Teilen, maximal 2,84e-14 mm bei ausgewerteten Laengen. Der historische
Referenzvergleich bleibt bis zu einer belegten Migration gesperrt.

Detailaudit: 105 von 148 Fertigungspositionen nennen fehlende Zeichnungen,
26 von 69 Einkaufspositionen sind offene Beschaffungen. Maschinenbefestigungen,
Sensorhalter, Spindelenden, Zeichnungs-/Abwicklungs-Export und Elektrik/ATC
brauchen weitere Ausarbeitung. 35 Istmasse und sechs Anschlusskonflikte offen.
Keine neue Produktionscode-Aenderung oder mechanische Freigabe in diesem Audit.

Verbindlicher Fortsetzungsindex mit Entwicklungsprompts:
`docs/superpowers/plans/2026-10-31-entwicklungsroadmap.md`.
Pruefergebnisse/Umfang: `docs/superpowers/plans/2026-10-31-journalpruefbericht.md`.
Die folgenden Abschnitte dokumentieren die vorangegangenen Arbeitsstaende.

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
