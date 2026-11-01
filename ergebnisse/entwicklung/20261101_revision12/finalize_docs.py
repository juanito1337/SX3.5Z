from pathlib import Path
import json,datetime
ROOT=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
matrix=read(A/'native_matrix.json');assert len(matrix)==5 and all(x['exitcode']==0 for x in matrix)
runs=read(A/'lieferlaeufe.json');source=matrix[0]['source_base']
def put(p,s):p.write_bytes(s.encode('utf8'))
def top(rel,s):
    p=ROOT/rel;old=p.read_text(encoding='utf8');h,b=old.split('\n',1);put(p,h+'\n\n'+s.strip()+'\n'+b)
def replace(rel,a,b):
    p=ROOT/rel;s=p.read_text(encoding='utf8');assert a in s,(rel,a);put(p,s.replace(a,b,1))
links=[]
for pose in ('park','wechsel'):
    folder=Path(runs[pose]);opened=read(next(folder.glob('NX_Wiederoeffnung_*.json')))
    assert opened['saved_parts_reopened'] and len(opened['components'])==461
    main=next(folder.glob('fraesmaschine*.prt'))
    links.append('- **'+pose.upper()+'**: ['+main.name+']('+main.relative_to(ROOT/'cad').as_posix()+')')
top('cad/README.md','''## Aktuell12: BT30 auf fester rechter Saeulenkonsole,01.11.2026

'''+ '\n'.join(links)+'''

Beide Gesamtbaugruppen in NX2406 neu erzeugt, gespeichert und in frischen
Prozessen vollstaendig geoeffnet: je461 Einzelteile,17 Unterbaugruppen und
19 native Blechkonvertierungen im Pflichtmodus required. Vier Fangbleche
sind geneigte Vorformen.482PRT pro Lauf inklusive3 API-Pruefteilen.
Native Halterkegellage in WECHSEL:0/0/400mm, Toleranz0.00001mm. Dies prueft
die nominale Ausrichtung, nicht SK30/BT30-Passung oder automatisches Spannen.

Die Laufordner mit Teile/ und Unterbaugruppen/ vollstaendig zusammenhalten.
PRUEFSTATUS.json, PRT_SHA256.json und Pruefnachweise/ gehoeren zum Lieferstand.
Quellrevision '''+source+'''. Bei Wiederoeffnungspruefungen passende Quellen
verwenden. Alte11/10/09-Lieferstaende nicht ueberschreiben.

[Park-/Wechselvorschau](vorschau/SX35Z_12_Park_Wechsel.png) aus dem Modellrezept,
offline gerendert. [Anleitung und Grenzen12](../projekt/Dokumentation/Entwicklungsstand_12.md).
Grundplatte/Scheibe nach Bild;200mm Hub, Werkzeugteilkreis und Antriebs-/
Greiferhuellen bleiben Entwurf. Konsole braucht Istaufmass, Befestigung und
Festigkeitsnachweis. Die folgenden Eintraege beschreiben historische Staende.
''')
replace('README_START.md','**Aktive Entwicklung12,01.11.2026:** BT30-Wechsler auf fester rechter\nSaeulenkonsole, angenommene200mm Zustellung. [Anleitung12](projekt/Dokumentation/Entwicklungsstand_12.md).\nSpindelwahl folgt separat. Alte11-Dateien bleiben historisch; neue native\nLaufpfade stehen nach Erzeugung in [cad/README.md](cad/README.md).',
'''**Aktuell12,01.11.2026:** BT30-Wechsler auf fester rechter Saeulenkonsole,
angenommene200mm Zustellung. Beide nativen NX-Stellungen neu erzeugt und
frisch geoeffnet: je461 Einzelteile/17 Gruppen. [CAD-Dateien und Vorschau](cad/README.md),
[Anleitung12](projekt/Dokumentation/Entwicklungsstand_12.md). Spindelwahl folgt
separat. Kaufteil-/Konsolendetails bleiben unbestaetigt; alte Staende historisch.''')
replace('PROJECT_STATUS.md','Stellungen/540 BRep-Pruefungen bestanden; native12-Lieferung separat nachweisen.',
'''Stellungen/540 BRep-Pruefungen bestanden. Fuenf native Journallaeufe Exit0,
beide Gesamtstellungen gespeichert/frisch geoeffnet, je19 native Blech-
konvertierungen. Native Werkzeugachse0/0/400mm nachgewiesen; keine Passung.
KSS weiterhin6 IFS206-Referenzkonflikte, keine neuen Achs-/Korbbefunde.
Native Lieferpfade/Quellrevision: cad/README.md.''')
replace('NEXT_STEPS.md','Native Park-/Wechsel-Erzeugung und Wiedereroeffnung laufen im neuen12-Paket.',
        'Native Park-/Wechsel-Erzeugung und Wiedereroeffnung sind im12-Paket nachgewiesen.')
top('NX_ENVIRONMENT.md','''## Nativer Nachweis12,01.11.2026

Quellrevision '''+source+'''. NX2406/Python3.10.15, separate eigene
run_journal-Prozesse; gemeinsame Oberflaeche nicht benutzt. Fuenf erfolgreiche
Journallaeufe: Normteil/ATC-Teilpruefung, PARK, frisches PARK-Oeffnen, WECHSEL,
frisches WECHSEL-Oeffnen. Je461 Einzelteile/17 Gruppen/19 native Blechteile.
Laufmatrix/Rohprotokolle: ergebnisse/entwicklung/20261101_revision12/.
Ein vorheriger Lauf wurde wegen Reviewbefund kontrolliert gestoppt; dessen
Zwischenstand ist als versuch01 erhalten und nicht ausgeliefert. Keine fremden
NX-Prozesse beendet. Aktuelle Pfade und Pruefgrenzen: cad/README.md.
''')
plan=ROOT/'docs/superpowers/plans/2026-11-01-bt30-saeulenkonsole12.md'
put(plan,plan.read_text(encoding='utf8').replace('- [ ]','- [x]')+'''

## Abschlussnachweis

Quelle92ce68f im Review korrigiert auf '''+source+'''. Erstkontakt zur
Saeulenwand und Gabelwurzel als Regression abgesichert.190 Tests/99 Untertests,
17 Stellungen/540 Schnitte,744 Endpunktvergleiche bestanden. Fuenf native
Journale Exit0,461 Teile je Stellung neu gespeichert/frisch geoeffnet.
Laufpfade in cad/README.md. Lieferstand bleibt nicht fertigungs-/betriebsfreigegeben.
''')
meta=dict(date=datetime.datetime.now().astimezone().isoformat(),source_revision=source,
    environment='Windows; CPython3.12.14/CadQuery2.8/OCP7.9.3.1.1; nativeNX2406/Python3.10.15 separately',
    checks=[
      dict(command='../.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider',cwd='projekt',exitcode=0,raw_log='offline_final.log',result='190passed99subtests'),
      dict(command='.venv/Scripts/python.exe projekt/tools/wechselweg12_pruefen.py --output ergebnisse/entwicklung/20261101_revision12/motion_final.json',cwd='repository root',exitcode=0,raw_log='motion_final.log',result='17poses540BRep0hits'),
      dict(command='.venv/Scripts/python.exe projekt/tools/teller_pruefung10.py --output ergebnisse/entwicklung/20261101_revision12/endpoints_final.json',cwd='repository root',exitcode=0,raw_log='endpoints_final.log',result='744checks0hits'),
      dict(command='.venv/Scripts/python.exe ergebnisse/entwicklung/20261101_revision12/arbeitskopie/projekt/tools/pruefen07.py',cwd='repository root',exitcode=1,raw_log='kss_final.log',result='6knownIFS206referencehits;0axis0basket'),
      dict(command='.venv/Scripts/python.exe tools_handoff/verify_package.py',cwd='repository root',exitcode=1,raw_log='package.log',result='449of477originalhashesmatch;28intentionalhistoricalchanges'),
      dict(command='.venv/Scripts/python.exe -m unittest discover -s tools_handoff -p test_*.py -v',cwd='repository root',exitcode=0,raw_log='handoff_tests.log',result='9pass1Windows-symlinkskip'),
      dict(command='ergebnisse/entwicklung/20261101_revision12/run_native.ps1',cwd='repository root',exitcode=0,raw_log='native_matrix.json',result='5journals;2completeassemblies;2freshreopens')],
    native_nx_executed=True,physical_fit_verified=False,machine_operation_enabled=False)
put(A/'verification.meta.json',json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
put(A/'README.md','''# Revision12 – Ausfuehrung und Pruefgrenzen

01.11.2026; Ausgang8204471, finale native Quelle '''+source+'''.
Rechte Saeulenkonsole, angenommener200mm-Einschub, Bildmasse fuer Grundplatte
und Scheibe, geschlossene Wanne ohne alte Gestellstuetze. Spindelwahl separat.

190 Offline-Tests/99 Untertests bestanden;17 Stellungen/540 BRep-Pruefungen
und744 begrenzte Endpunktvergleiche ohne Kollision. KSS-Pruefung Exit1 wegen
sechs bereits bekannter IFS206-Referenzkonflikte;8 Achsecken und Korbauszug
ohne Kollision. Die6 originalen Maschinenanschluss-Konflikte sind separat.
35 Istmasse weiterhin offen. Keine kontinuierliche Bahn oder reale Passung.

Fuenf finale NX2406/Python3.10.15-Journallaeufe Exit0; je461 Einzelteile,
17 Gruppen und19 native Blechteile gespeichert und frisch geoeffnet. Native
Werkzeugkegellage in WECHSEL0/0/400mm innerhalb0.00001mm nachgewiesen.
Vollstaendige Befehle, Umgebung, Revision, Datum, Exitcodes und Rohprotokolle:
[verification.meta.json](verification.meta.json),[native_matrix.json](native_matrix.json).
Datei-Hashes: native_source_hashes.json und PRT_SHA256.json in den Lieferordnern.

Historische Paketidentitaet:449/477 passend,28 absichtliche Git-Fortschreibungen;
Originalmanifest nicht umgeschrieben. Hilfstests9bestanden/1Windows-Symlinkskip.
Berichtsexport ausschliesslich in Arbeitskopie; Tabellen09/10/11 erhalten.

Review und Red/Green: [review.md](review.md),review_red.log,offline_final.log.
Urspruengliche Unterrippen kollidierten52mal; nach oben verlegt. Review fand
Anschluss an falscher Fusskontur; an Saeulenwand korrigiert und Kontakt
regressionsgeprueft. Vorheriger nativer Versuch gezielt gestoppt und in
versuch01 erhalten. Nur eigener SX3.5Z-Prozess beendet; gemeinsame NX-GUI und
fremde Prozesse unberuehrt. Finale Lieferung komplett neu erzeugt.

Native Laufpfade siehe ../../../cad/README.md. Kaufteilinnengeometrie,
Greifer/Retention, effektiver Hub, realer Gussanschluss/Schrauben/Festigkeit,
Spindel-/Spannpaket, Schutzverschluss und volle Bahn bleiben offen.
Keine Fertigungs-, Kauf- oder Betriebsfreigabe.
''')
print('Final native evidence documented; source '+source)
