"""Single-source procurement, model mapping and release status. No NX dependency."""
import csv, hashlib, json
from pathlib import Path

def catalog(root=None):
    return json.loads((Path(root or Path(__file__).parent)/'Einkauf/Kaufteile_08.json').read_text(encoding='utf8'))

def release_report(root=None):
    root=Path(root or Path(__file__).parent)
    gates=json.loads((root/'Pruefung_08/Freigaben.json').read_text(encoding='utf8'))['gates']
    measures=json.loads((root/'Aufmass/Messwerte_08.json').read_text(encoding='utf8'))['measurements']
    missing=[m['id'] for m in measures if m['measured_value'] is None or not m['measured_by'] or not m['measurement_date']]
    open_gates=[g['id'] for g in gates if not(g['complete'] is True and g['evidence_file'] and g['checked_by'])]
    return {'schema':'SX35Z_RELEASE_08','build_ready':False,'purchase_release':False,'native_nx_run_this_revision':False,
            'note':'Dieser Export ist ein Planungsnachweis, keine externe Freigabeautomatik. Selbst ausgefüllte Checkboxen sind keine Sicherheitsvalidierung.',
            'missing_measurement_count':len(missing),'missing_measurements':missing,'open_gates':open_gates}

def bom_rows(parts,root=None):
    cat=catalog(root)['items'];by={}
    for p in parts:
        if p['supply_kind']!='BUY':continue
        x=by.setdefault(p['item_id'],{'instances':set(),'parts':[]})
        x['instances'].add(p['purchase_instance']);x['parts'].append(p['id']+':'+p['name'])
    rows=[]
    for id,it in cat.items():
        mod=by.get(id,{'instances':set(),'parts':[]})
        rows.append(dict(item_id=id,description=it['description'],manufacturer=it['manufacturer'],article=it['article'],
            quantity=it['planned_quantity'],unit=it['unit'],model_quantity=len(mod['instances']),model_bodies=len(mod['parts']),
            model_refs=' | '.join(mod['parts']),source_ids=' '.join(it['source_ids']),gates=' '.join(it['gates']),
            status=it['release'],model_scope=it['model_scope'],note=it['note'],unit_price_eur=it['unit_price_eur'],type=it['type']))
    return rows

def model_map(parts):
    return [dict(part_id=d['id'],name=d['name'],group=d['group'],kind=d['supply_kind'],item_id=d['item_id'],instance=d['purchase_instance'],
         source=d['source'],note=d['note'],manufacturing_released=False) for d in parts]

def manufacturing_rows(parts,p,model):
    rows={};v=model.all_values(p)
    for d in parts:
        if d['supply_kind']!='MAKE':continue
        x=rows.setdefault(d['item_id'],dict(item_id=d['item_id'],name=d['name'],quantity=0,model_refs=[],process='',material='',gates='G02 G05 G08',note=d['note'],blank_mm=''))
        x['quantity']+=1;x['model_refs'].append(d['id'])
        first=d['ops'][0]
        if d['material']=='glass':
            x.update(process='Schutzscheibe: fachgerecht konfektionieren und Halterung prüfen',material='Werkstoff, Aufbau und Dicke nach Schutz-/KSS-Auslegung; Modell keine Freigabe',gates='G05 G08')
        elif 'sheetmetal' in d:
            x.update(process='Lasern + Abkanten; Abwicklung/Zeichnung fehlen',material='Stahlblech2mm als Entwurf',gates='G05 G08')
        elif any(t in d['name'] for t in ('Leitblech','Trichter','Wanne','Spaenekorb','Deckblech','Schuerze','Dach','Seitenwand')):
            x.update(process='Blechzuschnitt / ggf.Kanten / Schweißen / Dichten',material='Blech; Werkstoff nachKSS und Korrosionsschutz wählen',gates='G05 G08')
        elif 'Staender_' in d['name']:
            x.update(process='Profil sägen / Bohren / Schweißen / Auflagen ausrichten',material='S235-Profil als Entwurf',gates='G03 G05 G08')
        elif 'Distanzsaeule' in d['name']:
            a=d['name'][4].lower();x.update(process='Drehen / Planen / Durchgang bohren',material='Stahl, Sorte/Zustand freizugeben',blank_mm=f"Ø12; Bohrung6.6; Fertiglänge {v['cnc_'+a+'_spacer_l']:g}")
        else:x.update(process='Fräsen / Bohren / ggf.Gewindeschneiden; Einzelzeichnung fehlt',material='S355 als Halterentwurf, sonst noch festlegen')
        if first['kind']=='box' and not x['blank_mm']:
            x['blank_mm']=' × '.join(f'{model.evaluate(q,v):g}' for q in first['size'])+' (Modell-Grundkörper, KEIN Zuschnittaufmaß)'
    return [dict(x,model_refs=' '.join(x['model_refs'])) for x in rows.values()]

def write_csv(path,rows):
    if not rows:return
    with open(path,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)

def export(root=None):
    root=Path(root or Path(__file__).parent)
    import cnc_ansichtsmodell as model
    p=model.load_parameters(root/'Parameter.json');parts=model.recipe();model.check_recipe(p)
    b=bom_rows(parts,root);mapping=model_map(parts);fab=manufacturing_rows(parts,p,model)
    write_csv(root/'Einkauf/Einkaufsliste_08.csv',b)
    write_csv(root/'Einkauf/Modellzuordnung_08.csv',mapping)
    write_csv(root/'Einkauf/Fertigungsteile_08.csv',fab)
    (root/'Pruefung_08/Freigabestatus_08.json').write_text(json.dumps(release_report(root),indent=2,ensure_ascii=False))
    report={'version':model.VERSION,'parts':len(parts),'operations':sum(len(d['ops']) for d in parts),'catalog_rows':len(b),
            'catalog_instances_in_model':sum(x['model_quantity'] for x in b),'manufactured_item_rows':len(fab),'model_map_rows':len(mapping),
            'parameter_sha256':hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'recipe_sha256':hashlib.sha256(json.dumps(parts,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'catalog_sha256':hashlib.sha256((root/'Einkauf/Kaufteile_08.json').read_bytes()).hexdigest(),
            'native_nx_executed':False,'all_released':False,'spindles':model.length_report(p)}
    (root/'Pruefung_08/Modell_Stuecklistenabgleich.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    return report
if __name__=='__main__': print(json.dumps(export(),indent=2,ensure_ascii=False))
