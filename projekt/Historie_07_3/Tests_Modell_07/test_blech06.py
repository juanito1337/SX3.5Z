import math,unittest
from pathlib import Path
import cnc_ansichtsmodell as m
from enclosure_checks03 import body_bounds
R=Path(__file__).resolve().parents[1]
class SheetDoor06Tests(unittest.TestCase):
 def p(self):return m.load_parameters(R/'Parameter.json')
 def test_full_width(self):
  self.assertEqual(self.p()['door_clear_w'],1420)
  self.assertGreater(self.p()['door_clear_w']/self.p()['stand_w'],.85)
 def test_sheet_frame_not_30mm_solid(self):
  d=next(d for d in m.recipe() if d['name']=='Senktuer_UPPER_Rahmen')
  self.assertIn('sheetmetal',d)
  self.assertEqual(d['ops'][0]['kind'],'prism')
  self.assertEqual(d['sheetmetal']['thickness'],'sheet_t')
 def test_width_limits_explicit(self):
  with self.assertRaises(ValueError):m.validate(dict(self.p(),door_clear_w=1650))
 def test_new_parts_unique_and_valid(self):
  p=self.p();v=m.check_recipe(p);ds=m.recipe()
  self.assertEqual(len(ds),len({d['name'] for d in ds}))
  self.assertGreaterEqual(len([d for d in ds if 'sheetmetal' in d]),15)
 def test_no_negative_fixed_field(self):
  v=m.all_values(self.p())
  for d in m.recipe():
   for o in d['ops']:
    for s in o.get('size',[]):self.assertGreater(m.evaluate(s,v),0,d['name'])
 def test_door_contained_x_and_z(self):
  p=self.p()
  for f in (0,.25,.5,.75,1):
   v=m.all_values(dict(p,door_open=f))
   for d in m.recipe():
    if d.get('door_leaf'):
     b=body_bounds(d,v,m.evaluate)
     self.assertGreaterEqual(b[0],v['enc_left']);self.assertLessEqual(b[3],v['enc_right'])
     self.assertGreater(b[2]+p['stand_h'],100);self.assertLessEqual(b[5],v['enclosure_h'])
 def test_gas_springs_are_not_claimed_catalog_parts(self):
  ds=[d for d in m.recipe() if 'Gasfeder06' in d['name']]
  self.assertGreaterEqual(len(ds),8)
  for d in ds:self.assertIn('KEIN KAUFTEIL',d['note'])
 def test_independent_spring_stroke_515mm(self):
  self.assertTrue(hasattr(m,'spring_report'))
  r=m.spring_report(self.p())
  self.assertFalse(r['released']);self.assertAlmostEqual(r['stroke_each_mm'],515)
  self.assertEqual(r['spring_count'],4)
 def test_gas_force_opposes_gravity(self):
  self.assertTrue(hasattr(m,'spring_report'))
  r=m.spring_report(self.p());self.assertGreater(r['opening_hand_force_N'][0],r['opening_hand_force_N'][-1])
  self.assertLess(r['maximum_balance_fraction'],1)
 def test_native_sheetmetal_adapter_exists(self):
  self.assertTrue((R/'nx_sheetmetal06.py').exists())
 def test_default_requires_conversion(self):
  import json
  self.assertTrue((R/'Blech_Optionen.json').exists())
  q=json.loads((R/'Blech_Optionen.json').read_text());self.assertEqual(q['mode'],'required')
 def test_build_does_not_read_generated_picture(self):
  t=(R/'NX_CNC_Gesamtansicht.py').read_text()
  self.assertNotIn('imagegen',t);self.assertIn('nx_sheetmetal06',t)
