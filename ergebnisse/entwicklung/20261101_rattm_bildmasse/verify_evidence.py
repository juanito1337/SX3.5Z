from pathlib import Path
import csv, hashlib, json, platform, subprocess, sys, datetime
ROOT=Path(__file__).resolve().parents[3]
AUDIT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))
ref=ROOT/'referenzen/kaufteile/rattm_1005009887984460'
manifest=read(ref/'provenienz.json')
assert len(manifest['images'])==6
for i in manifest['images']:
    assert sha(ROOT/i['file'])==i['sha256']==sha(Path(i['original_path']))
    assert (ROOT/i['file']).stat().st_size==i['bytes']
data=read(ROOT/'projekt/Werkzeugwechsler/Produktdaten_RATTM_1005009887984460.json')
sources={i['id'] for i in manifest['images']}
assert len(data['dimensions'])==21
assert all(d['source_id'] in sources for d in data['dimensions'])
assert all(not d['measured_on_physical_product'] and d['tolerance_mm'] is None for d in data['dimensions'])
assert not data['cylinder']['usable_magazine_travel_verified']
assert data['selected_tool_interface'] is None
assert not any(data[k] for k in ['cad_matches_selected_product','build_ready','purchase_released','machine_operation_enabled','atc_operational'])
sel=read(ROOT/'projekt/Werkzeugwechsler/Auswahl_AliExpress_1005009887984460.json')
assert sel['dimension_image_count']==6 and sel['dimension_images_retrieved']
assert not sel['selected_variant_verified'] and not sel['dimensions_verified']
before=read(AUDIT/'source_hashes_before.json')
allowed={'projekt/Einkauf/Kaufteile_09.json','projekt/Quellen/Quellen_Teller_20261101.json',
         'projekt/Werkzeugwechsler/Auswahl_AliExpress_1005009887984460.json',
         'projekt/Pruefung_11/Modell_Stuecklistenabgleich_11.json'}
changed=[path for path,h in before.items() if sha(ROOT/path)!=h]
assert set(changed)<=allowed,changed
diff=subprocess.check_output(['git','diff','--name-only','2b83f2c'],cwd=ROOT,text=True).splitlines()
assert not any(p.startswith('cad/nx/') for p in diff)
sys.path.insert(0,str(ROOT/'projekt'))
import cnc_ansichtsmodell as model
import umbau_daten09 as reports
p=model.load_parameters()
assert model.check_recipe(p)
old=json.loads(subprocess.check_output(['git','show','2b83f2c:projekt/Pruefung_11/Modell_Stuecklistenabgleich_11.json'],cwd=ROOT,text=True))
new=read(ROOT/'projekt/Pruefung_11/Modell_Stuecklistenabgleich_11.json')
for key in old:
    if key!='catalog_sha256':assert old[key]==new[key],key
cat=reports.catalog()
assert new['catalog_sha256']==hashlib.sha256(json.dumps(cat,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert new['recipe_sha256']==hashlib.sha256(json.dumps(model.recipe(),sort_keys=True,separators=(',',':')).encode()).hexdigest()
rows=reports.bom_rows(model.recipe())
item=next(r for r in rows if r['item_id']=='O10-TELLER')
assert item['quantity']==item['model_quantity']==1
assert 'KEIN Abbild' in item['model_scope']
assert all(s in reports.sources() for s in item['source_ids'].split())
raw=(ROOT/'projekt/Einkauf/Einkaufsliste_11.csv').read_text(encoding='utf-8-sig')
assert '1005009887984460' in raw and 'KEIN Abbild' in raw
result=dict(date=datetime.datetime.now().astimezone().isoformat(),source_base_revision='2b83f2c',
    environment=dict(python=sys.version,platform=platform.platform()),
    command='.venv/Scripts/python.exe ergebnisse/entwicklung/20261101_rattm_bildmasse/verify_evidence.py',
    exit_code=0,images_verified=6,dimension_labels=21,changed_existing_json=changed,
    production_python_unchanged=True,model_recipe_and_parameters_unchanged=True,native_files_unchanged=True,
    selected_package_quantity=item['quantity'],catalog_rows=len(rows),native_nx_executed=False,
    scope='Image copy hashes, provenance references, conservative flags, unchanged existing code/parameters/recipe, catalog and BOM consistency. No dimensional accuracy, native NX or physical fit test.')
(AUDIT/'verification.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
print(json.dumps(result,ensure_ascii=False,indent=2))
