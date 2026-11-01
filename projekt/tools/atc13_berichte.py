"""Offline concept13 reports. No CAD, hardware, purchases or legacy CSV writes.

Default output: projekt/Konzept13. Existing target files are never overwritten;
use --output-dir for a new report revision. Standard Python3.10+ only.
"""
import argparse
from collections import Counter, defaultdict
import copy
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import atc13_modell as model

RELEASE = dict(build_ready=False, manufacturing_released=False,
    purchase_released=False, machine_operation_enabled=False, atc_operational=False)
KINDS = ('EXISTING', 'MAKE', 'BUY', 'RESERVE')
FILENAMES = ('Stueckliste_13.csv', 'Kaufteile_13.json',
             'Parameter_Herkunft_13.json', 'Bewegungsfolge_13.json')


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(',', ':')).encode('utf8')).hexdigest()


def bom_rows(definitions):
    """Group by item ID; distinguish physical purchase instances from bodies."""
    groups = defaultdict(list)
    seen = set()
    for definition in definitions:
        if definition['id'] in seen:
            raise ValueError('Doppelte Teilkennung: ' + definition['id'])
        seen.add(definition['id'])
        if not definition.get('item_id') or not definition.get('purchase_instance'):
            raise ValueError('Artikel-/Instanzzuordnung fehlt: ' + definition['id'])
        if definition.get('supply_kind') not in KINDS:
            raise ValueError('Unbekannte Beschaffungsart: ' + definition['id'])
        groups[definition['item_id']].append(definition)
    rows = []
    for item_id, members in groups.items():
        kinds = {d['supply_kind'] for d in members}
        if len(kinds) != 1:
            raise ValueError('Widerspruechliche Beschaffungsart: ' + item_id)
        kind = next(iter(kinds))
        catalog = model.CAT.get(item_id, {})
        if item_id.startswith('R13-') and kind != 'RESERVE':
            raise ValueError('R13 muss unselektierte Reserve bleiben: ' + item_id)
        status = ('UNSELECTED' if kind == 'RESERVE' else
                  'FERTIGUNGSENTWURF' if kind == 'MAKE' else
                  'BESTAND' if kind == 'EXISTING' else 'KATALOGREFERENZ_NICHT_BESTELLFREIGEGEBEN')
        rows.append(dict(Artikel_ID=item_id, Beschaffungsart=kind,
            Bezeichnung=catalog.get('description',catalog.get('name',members[0]['name'])),
            Menge=len({d['purchase_instance'] for d in members}), Einheit='Stk',
            Modellkoerper=len(members), Auswahlstatus=status,
            Hersteller='' if kind in ('MAKE','RESERVE','EXISTING') else catalog.get('manufacturer',''),
            Herstellerartikel='' if kind in ('MAKE','RESERVE','EXISTING') else catalog.get('article',''),
            Quellen=' | '.join(sorted(set(catalog.get('source_ids',[])) | {d.get('source','') for d in members})),
            Teilkennungen=' | '.join(d['id'] for d in members),
            Teile=' | '.join(d['name'] for d in members),
            Instanzen=' | '.join(sorted({d['purchase_instance'] for d in members})),
            Fertigungsfreigabe=False, Bestellfreigabe=False))
    return sorted(rows,key=lambda r:(KINDS.index(r['Beschaffungsart']),r['Artikel_ID']))


def sequence_report(parameters):
    """Human-readable functional sequence, deliberately not executable M6 code."""
    park = model.assembly_pose(parameters,'park')
    change = model.assembly_pose(parameters,'wechsel')
    steps = [
        ('Vorbereitung','Spindel und KSS stoppen; sicheren Wechselraum herstellen, Kopf in Wechselhoehe und Spindel orientieren.',
         'Werkstueck/Spannmittel unter der gesamten Bahn maximal125mm ueber Tisch; Raum und Endlagen bestaetigt.'),
        ('Altes Werkzeug greifen','Leeren Arm niedrig/eingezogen zur Spindelseite schwenken; am Endpunkt zustellen und anheben; Greifer schliessen.',
         'Spindel haelt bis formschluessiges Greifen, Werkzeugpraesenz und Verdrehsicherung bestaetigt sind.'),
        ('Ausspannen','Spindel loesen; Werkzeug am Spindelendpunkt axial90mm absenken.',
         'Spannpaket/Loesekraft/Auswurf/Spindellagerentlastung noch auszulegen; keine reale Loesefreigabe.'),
        ('Zum leeren Platz','60mm radial einziehen, niedrig zur Magazinseite schwenken; leeren Platz indexieren/verriegeln und60mm zustellen.',
         'Belegung des Zielplatzes, Indexlage, Greiferhalt und freie Bahn pruefen; kein Schwenken mit ausgefahrenem Schlitten.'),
        ('Altes Werkzeug ablegen','Taschenaufnahme/Retention schliessen und bestaetigen; Greifer je Backe22mm oeffnen und radial einziehen.',
         'Werkzeug niemals gleichzeitig von Tasche und Greifer ungesichert lassen.'),
        ('Neues Werkzeug holen','Gewuenschten Platz indexieren/verriegeln; Greifer zustellen und schliessen; Taschenretention erst danach freigeben.',
         'Belegung, Werkzeugidentitaet, Greiferhalt und Winkelorientierung bestaetigen.'),
        ('Zur Spindel','Mit Werkzeug60mm einziehen, niedrig zur Spindelseite schwenken, dort60mm zustellen und90mm axial anheben.',
         'Freier Wechselraum und passende Spindelorientierung; Einfuehrung/Passung noch nicht nachgewiesen.'),
        ('Einspannen','Spindel spannen und Spannzustand bestaetigen; erst danach Greifer oeffnen.',
         'Werkzeugzustand geht von1 getragen auf2 in Spindel ueber; keine alleinige Zeitsteuerung als Haltbeleg.'),
        ('Parken','Leeren geoeffneten Greifer radial abziehen, absenken und niedrig/eingezogen zum Magazin parken.',
         'Parklage/Arretierung und freie Maschinen-Verfahrhuelle bestaetigen, bevor Bearbeitung freigegeben wird.'),
    ]
    return dict(schema='ATC13_BEWEGUNGSFOLGE_ENTWURF', executable_machine_program=False,
        tool_states={'0':'in ausgewaehlter Magazintasche','1':'vom Greifer getragen','2':'in Spindel gehalten'},
        limits=dict(radial_feed_mm=60,vertical_lift_mm=90,jaw_opening_each_mm=22,
            total_jaw_separation_change_mm=44,workpiece_over_table_limit_mm=model.atc_report(park)['toolchange_workpiece_limit_mm']),
        modeled_poses={name:model.atc_report(model.assembly_pose(parameters,name)) for name in ('park','magazin','wechsel')},
        spindle_change_head_down_mm=change['head_down'],
        steps=[dict(number=i,phase=name,action=action,required_condition=condition) for i,(name,action,condition) in enumerate(steps,1)],
        limitations=['Konzept zeigt den Transferhalter und zwoelf Taschen; alle Index-/Belegungszustaende sind keine fertig ausgelegte Steuerung.',
            'Greifer-/Taschenverdrehsicherung, Spannpaket, Antriebe, feste Endlagenverriegelungen und Sensorik sind offen.',
            'Gesamte kontinuierliche Bahn samt realem Werkstueck, Schlaeuchen und Werkzeugen ist nicht freigegeben.'],
        **RELEASE)


def reports(parameters=None):
    parameters = model.load_parameters() if parameters is None else dict(parameters)
    definitions = model.recipe()  # Populates concept13 catalog entries.
    model.check_recipe(parameters,definitions)
    rows = bom_rows(definitions)
    revision = subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip()
    common = dict(version=model.VERSION,date=datetime.now().astimezone().isoformat(),
        source_revision=revision,environment=sys.version,
        recipe_sha256=fingerprint(definitions),parameter_sha256=fingerprint(parameters),
        source_sha256={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (Path(model.__file__),Path(__file__))},
        scope='Offline report generation from recipe; no native NX or release proof',
        native_nx_executed=False,**RELEASE)
    items = {}
    for row in rows:
        item_id = row['Artikel_ID']
        item = copy.deepcopy(model.CAT.get(item_id,{}))
        old_quantity = item.pop('planned_quantity',None)
        item.update(id=item_id,planned_quantity=row['Menge'],model_body_count=row['Modellkoerper'],
            supply_kind=row['Beschaffungsart'],selection_status=row['Auswahlstatus'],
            source_catalog_quantity=old_quantity,quantity_basis='Unique purchase_instance values in concept13 recipe',
            part_ids=row['Teilkennungen'].split(' | '),purchase_released=False,manufacturing_released=False)
        if item_id.startswith('R13-'):
            item.update(manufacturer=None,article=None,selection_status='UNSELECTED',
                model_scope='CUSTOM_RESERVE; unbestaetigter Funktions-/Bauraumentwurf, kein Hersteller-CAD',verified=False)
        if item_id == 'K09-BT30ER20':
            item['concept13_note']='12 Halter nach Modell13; K09-Hauptmasse beibehalten. Flanschnut/28mm Anzugsbolzen/35mm Fräserprojektion Entwurf; keine SK30-Passung.'
        items[item_id] = item
    catalog = dict(common,items=items,
        categories={kind:[r['Artikel_ID'] for r in rows if r['Beschaffungsart']==kind] for kind in KINDS},
        quantity_note='Eine Kaufbaugruppe kann mehrere Modellkoerper haben; Menge zaehlt physische Instanzen, Modellkoerper separat.')
    values = model.all_values(parameters)
    specs = {s['name']:s for s in model.SPECS}
    provenance = dict(common,parameters=[dict(name=name,value=value,
        unit=specs.get(name,{}).get('unit','unbekannt'),
        status=specs.get(name,{}).get('status','HERKUNFT_FEHLT'),
        source=specs.get(name,{}).get('source','HERKUNFT_FEHLT'),
        note=specs.get(name,{}).get('note','')) for name,value in parameters.items()],
        derived=[dict(name=name,formula=formula,value=values[name],
            provenance='Aus Parametern berechnet; keine zusaetzliche Messbestaetigung') for name,formula in model.DERIVED.items()])
    sequence = dict(common,**sequence_report(parameters))
    summary = dict(part_count=len(definitions),item_count=len(rows),
        model_bodies_by_kind=dict(Counter(d['supply_kind'] for d in definitions)),
        physical_instances_by_kind={kind:sum(r['Menge'] for r in rows if r['Beschaffungsart']==kind) for kind in KINDS},
        bt30_holder_quantity=items['K09-BT30ER20']['planned_quantity'])
    return rows,catalog,provenance,sequence,summary


def export(output_dir=None):
    out = Path(output_dir).resolve() if output_dir else PROJECT/'Konzept13'
    rows,catalog,provenance,sequence,summary = reports()
    if any((out/name).exists() for name in FILENAMES):
        raise FileExistsError('Berichtsdateien existieren bereits; neuen Ordner mit --output-dir waehlen: '+str(out))
    out.mkdir(parents=True,exist_ok=True)
    with (out/FILENAMES[0]).open('x',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter=';')
        writer.writeheader();writer.writerows(rows)
    for name,payload in zip(FILENAMES[1:],(catalog,provenance,sequence)):
        with (out/name).open('x',encoding='utf8') as stream:
            json.dump(payload,stream,indent=2,ensure_ascii=False)
    return dict(output_dir=str(out),files=list(FILENAMES),**summary)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    print(json.dumps(export(args.output_dir),indent=2,ensure_ascii=False))
