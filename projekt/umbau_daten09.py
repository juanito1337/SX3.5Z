"""Revision09 source-linked BOM. Reuses08 serialisation; never releases a purchase."""
import json,hashlib
from pathlib import Path
import umbau_daten08 as old
ROOT=Path(__file__).resolve().parent

def catalog(root=None):
    return json.loads((Path(root or ROOT)/'Einkauf/Kaufteile_09.json').read_text(encoding='utf8'))

def sources(root=None):
    root=Path(root or ROOT)
    q=json.loads((root/'Quellen/Quellen_08.json').read_text(encoding='utf8'))
    #08 uses an object keyed by source id.
    result=dict(q['sources']) if 'sources' in q else dict(q)
    for s in json.loads((root/'Quellen/Quellen_09.json').read_text(encoding='utf8'))['sources']:
        result[s['id']]={'title':s['title'],'url':s['url'],'evidence':s['scope'],'checked_on':'2026-10-30','source_type':s['source_type']}
    for s in json.loads((root/'Quellen/Quellen_Teller_20261101.json').read_text(encoding='utf8'))['sources']:
        result[s['id']]={'title':s['title'],'url':s['url'],'evidence':s['scope'],'checked_on':'2026-11-01','source_type':s['source_type']}
    return result

def release_report(root=None):
    root=Path(root or ROOT);r=old.release_report(root)
    r.update(schema='SX35Z_RELEASE_12',atc_operational=False,native_nx_run_this_revision=False)
    r['open_gates']=list(r['open_gates'])+['A09']
    extra=json.loads((root/'Aufmass/Messwerte_09_Zusatz.json').read_text())['measurements']
    missing=[x['id'] for x in extra if x['measured_value'] is None or not x['measured_by'] or not x['measurement_date']]
    r['missing_measurements']+=missing;r['missing_measurement_count']=len(r['missing_measurements'])
    return r

def bom_rows(parts,root=None):
    cat=catalog(root)['items'];by={};rows=[]
    for p in parts:
        if p['supply_kind']!='BUY' and not (p['supply_kind']=='RESERVE' and p['item_id'] in cat):continue
        if p['item_id'] not in cat:raise ValueError('Unmapped purchased body: '+p['name'])
        x=by.setdefault(p['item_id'],{'instances':set(),'parts':[]})
        x['instances'].add(p['purchase_instance']);x['parts'].append(p['id']+':'+p['name'])
    for key,it in cat.items():
        mod=by.get(key,{'instances':set(),'parts':[]})
        rows.append(dict(item_id=key,description=it['description'],manufacturer=it['manufacturer'],article=it['article'],quantity=it['planned_quantity'],unit=it['unit'],model_quantity=len(mod['instances']),model_bodies=len(mod['parts']),model_refs=' | '.join(mod['parts']),source_ids=' '.join(it['source_ids']),gates=' '.join(it['gates']),status=it['release'],model_scope=it['model_scope'],note=it['note'],unit_price_eur=it['unit_price_eur'],type=it['type'],option='ATC-OPTION' if 'A09' in it['gates'] else 'GRUNDMASCHINE'))
    return rows

model_map=old.model_map
write_csv=old.write_csv

def manufacturing_rows(parts,p,model):
    rows=old.manufacturing_rows(parts,p,model)
    for x in rows:
        if x['name'] in {'KSS_Tank_Entwurf','KSS_Tankdeckel','KSS_Ruecklaufkasten_Stirnwand',
                          'KSS_Spaeneschacht_Rueckwand','KSS_Serviceklappe_hinten'}:
            x.update(process='Blechzuschnitt / Schweissen / Dichten; Einzelzeichnung fehlt',
                     material='Blech; Guete und KSS-Vertraeglichkeit unbestaetigt',gates='G05 G08')
        elif x['name'].startswith('KSS_Fangblech_'):
            x.update(process='2mm Blechzuschnitt; geneigte Vorform, Halter/Zeichnung/Abwicklung fehlen',
                     material='2mm Blech als Entwurf; Guete und KSS-Vertraeglichkeit offen',gates='G05 G08')
        elif x['name'].startswith(('ATC_KSS_','ATC_Parkhaube_')):
            x.update(process='Blechzuschnitt / Rollen / Schweissen / Dichten; Zeichnung fehlt',
                     material='2mm Blech als Entwurf; Guete und Dichtheit offen',gates='A09 G05 G08')
        elif x['name'].startswith('ATC_Lokator'):
            x.update(material='POM als Entwurfswahl; Eignung/Kriechen/KSS bestätigen',process='Fräsen/Bohren; Schwerkraftablage, Verdrehsicherung fehlt',gates='A09 G05 G08')
        elif x['name'].startswith('ATC_'):
            x['gates']='A09 G05 G08'
            if x['name']=='ATC_Magazintraeger_Kantblech':x['material']='4mm Stahlblech, Radius6 als Entwurf'
            if 'Grundplatte' in x['name']:x['material']='8mm Stahlplatte als Entwurf'
        elif 'Kabelplatte' in x['name']:x['gates']='G05 G06 G08'
    return rows

def export(root=None):
    import cnc_ansichtsmodell as model
    root=Path(root or ROOT);p=model.load_parameters(root/'Parameter.json');ds=model.recipe();model.check_recipe(p)
    b=bom_rows(ds,root);mp=model_map(ds);fab=manufacturing_rows(ds,p,model)
    (root/'Pruefung_12').mkdir(exist_ok=True)
    for fn,rows in [('Einkaufsliste_12',b),('Modellzuordnung_12',mp),('Fertigungsteile_12',fab)]:write_csv(root/'Einkauf'/f'{fn}.csv',rows)
    (root/'Pruefung_12/Freigabestatus_12.json').write_text(json.dumps(release_report(root),ensure_ascii=False,indent=2),encoding='utf8')
    (root/'Werkzeugwechsler/ATC_Schnittstellenstatus_12.json').write_text(json.dumps(model.atc_report(p),ensure_ascii=False,indent=2),encoding='utf8')
    r=dict(version=model.VERSION,model_bodies=len(ds),operations=sum(len(d['ops']) for d in ds),catalog_rows=len(b),manufactured_item_rows=len(fab),new_bodies=sum(d.get('revision_added')=='12' for d in ds),new_catalog_rows=sum(x['item_id'].startswith('O10') for x in b),purchase_instances=sum(x['model_quantity'] for x in b),native_nx_executed=False,purchase_released=False,atc_operational=False)
    for label,obj in [('parameter',p),('recipe',ds),('catalog',catalog(root))]:r[label+'_sha256']=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (root/'Pruefung_12/Modell_Stuecklistenabgleich_12.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
    (root/'Pruefung_12/Demontageliste_12.json').write_text(json.dumps(model.removal_report(),indent=2,ensure_ascii=False),encoding='utf8')
    return r
if __name__=='__main__':print(json.dumps(export(),indent=2))
