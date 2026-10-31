import json, sys, tempfile, unittest, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell08 as m
import umbau_daten08 as u
class Review08(unittest.TestCase):
 def test_all_sources_nonempty(self):
  for d in m.recipe(): self.assertTrue(d.get('source'), d['name'])
 def test_too_long_table_is_rejected(self):
  p=m.load_parameters(ROOT/'Parameter.json');p['table_x']+=600
  with self.assertRaises(ValueError):m.check_recipe(p)
 def test_too_short_screw_is_rejected(self):
  p=m.load_parameters(ROOT/'Parameter.json');p['cnc_x_extra_l']=-200
  with self.assertRaises(ValueError):m.check_recipe(p)
 def test_mapped_purchase_quantities(self):
  for d in u.bom_rows(m.recipe(),ROOT):
   if d['type']!='Offene Beschaffung':self.assertEqual(d['quantity'],d['model_quantity'],d['item_id'])
 def test_all_checkboxes_do_not_grant_safety_release(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'Pruefung_08').mkdir();(root/'Aufmass').mkdir()
   a=json.loads((ROOT/'Pruefung_08/Freigaben.json').read_text());b=json.loads((ROOT/'Aufmass/Messwerte_08.json').read_text())
   for g in a['gates']:g.update(complete=True,evidence_file='unverified.pdf',checked_by='test')
   for r in b['measurements']:r.update(measured_value=1,measured_by='test',measurement_date='2026-10-30')
   (root/'Pruefung_08/Freigaben.json').write_text(json.dumps(a));(root/'Aufmass/Messwerte_08.json').write_text(json.dumps(b))
   self.assertFalse(u.release_report(root)['build_ready'])
 def test_purchase_units_and_sources(self):
  cat=u.catalog(ROOT)['items'];src=json.loads((ROOT/'Quellen/Quellen_08.json').read_text())['sources']
  for id,it in cat.items():
   for s in it['source_ids']:self.assertIn(s,src,id)
   self.assertIsNone(it['unit_price_eur'])
 def test_order_lengths_unknown(self):
  for r in m.length_report(m.load_parameters(ROOT/'Parameter.json')):self.assertIsNone(r['order_length_mm'])

class ManufacturingReview08(unittest.TestCase):
 def test_glazing_is_not_a_steel_machining_order(self):
  rows=u.manufacturing_rows(m.recipe(),m.load_parameters(ROOT/'Parameter.json'),m)
  windows=[r for r in rows if r['name'].endswith('Scheibe') or r['name']=='Einhausung_Seitenscheibe_links']
  self.assertEqual(len(windows),3)
  for r in windows:
   self.assertNotIn('S355',r['material'])
   self.assertIn('Schutzscheibe',r['process'])
