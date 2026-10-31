import copy, math, unittest
from pathlib import Path
import cnc_ansichtsmodell as m
from enclosure_checks03 import body_bounds
ROOT=Path(__file__).resolve().parents[1]

class CabinetDrain07Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=m.load_parameters(ROOT/'Parameter.json');cls.v=m.all_values(cls.p)
  cls.ds={d['name']:d for d in m.recipe()}
 def test_version(self):self.assertEqual(m.VERSION,'CNC_ANSICHT_07')
 def test_right_side_has_no_window(self):
  self.assertNotIn('Einhausung_Seitenscheibe_rechts',self.ds)
  self.assertFalse(any(o['op']=='cut' and o.get('label')=='Fensterausschnitt' for o in self.ds['Einhausung_Seitenwand_rechts']['ops']))
 def test_left_side_and_door_glazing_retained(self):
  self.assertIn('Einhausung_Seitenscheibe_links',self.ds)
  self.assertEqual(sum('Scheibe' in n and n.startswith('Senktuer_') for n in self.ds),2)
 def test_cabinet_flush_with_outer_sheet(self):
  a=body_bounds(self.ds['Schaltschrank_Hohlschale'],self.v,m.evaluate)
  b=body_bounds(self.ds['Einhausung_Seitenwand_rechts'],self.v,m.evaluate)
  self.assertAlmostEqual(a[0],b[3]);self.assertEqual(self.p['cab_gap'],0)
 def test_zero_gap_valid_negative_rejected(self):
  m.validate(dict(self.p,cab_gap=0))
  with self.assertRaises(ValueError):m.validate(dict(self.p,cab_gap=-1))
 def test_drain_report_exists(self):self.assertTrue(callable(getattr(m,'drain_report',None)))
 def test_large_chip_throat(self):
  self.assertIn('KSS_Spaeneschacht_U',self.ds)
  self.assertIn('KSS_Spaenekorb_U',self.ds)
  self.assertIn('KSS_Ruecklaufkasten_U',self.ds)
 def test_coarse_basket_has_real_openings(self):
  d=self.ds.get('KSS_Spaenekorb_U',{})
  self.assertGreaterEqual(sum(o.get('label')=='Grobsieb_Schlitz_KEIN_FEINFILTER' for o in d.get('ops',[])),24)
 def test_old_closed_filter_and_small_inlet_removed(self):
  self.assertNotIn('KSS_Filterkorb',self.ds)
  self.assertNotIn('KSS_Wannenboden_hinten',self.ds)
 def test_unchanged_door_motion(self):
  r=m.door_layout(self.p)
  self.assertEqual(r['travels_mm'],{'LOWER':515.,'UPPER':1030.})
  self.assertEqual(r['clear_width_mm'],1420.)
 def test_sqrt_positive(self):self.assertAlmostEqual(m.evaluate('2*sqrt(1+3*3)',{}),2*math.sqrt(10))
 def test_unsafe_formula_rejected(self):
  for q in ['__import__("os")','sqrt(-1)','sin(0)','True','sqrt(1,2)']:
   with self.subTest(q=q),self.assertRaises((ValueError,TypeError)):m.evaluate(q,{})
 def test_slot_parameters_reject_colliding_frame(self):
  self.assertIn('chip_outlet_d',self.p)
  with self.assertRaises(ValueError):m.validate(dict(self.p,chip_outlet_d=180))
 def test_new_drain_parts_keep_no_release(self):
  for d in self.ds.values():
   if d['group']=='17_KSS':
    self.assertFalse(d.get('manufacturing_released',False))
    self.assertTrue(d['source']);self.assertTrue(d['note'])

if __name__=='__main__':unittest.main()

class ClearanceRegression07Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=m.load_parameters(ROOT/'Parameter.json');cls.v=m.all_values(cls.p)
  cls.ds={d['name']:d for d in m.recipe()}
 def test_tray_starts_behind_front_posts(self):
  for n,d in self.ds.items():
   if n.startswith('KSS_Leitblech_'):
    self.assertGreaterEqual(body_bounds(d,self.v,m.evaluate)[1],self.v['enc_front']+30)
 def test_ramp_grade_clears_x_motor_cover(self):
  d=self.ds['KSS_Leitblech_rechts_vorn']
  self.assertLessEqual(m.evaluate(d['slope_x'],self.v),.14)
 def test_front_ridge_under_y_drive(self):
  d=self.ds['KSS_Leitblech_Front_rechts']
  self.assertLessEqual(abs(m.evaluate(d['slope_x'],self.v)),5/227+.00001)
 def test_tank_ends_before_rear_lower_beam(self):
  a=body_bounds(self.ds['KSS_Tank_Entwurf'],self.v,m.evaluate)
  b=body_bounds(self.ds['Staender_Querholm_1_1'],self.v,m.evaluate)
  self.assertLessEqual(a[4],b[1])
 def test_sloped_panels_have_constant_normal_thickness(self):
  for d in self.ds.values():
   if 'plate_normal_thickness' not in d:continue
   sx=m.evaluate(d['slope_x'],self.v);sy=m.evaluate(d['slope_y'],self.v)
   h=m.evaluate(d['ops'][0]['height'],self.v)
   self.assertAlmostEqual(h/math.sqrt(1+sx*sx+sy*sy),self.p['sheet_t'])
 def test_back_upstand_only_touches_enclosure_web(self):
  a=body_bounds(self.ds['KSS_Rueckwand_Aufkantung'],self.v,m.evaluate)
  self.assertLessEqual(a[4],self.v['enc_back']-self.p['sheet_t'])

class NativeFormula07Tests(unittest.TestCase):
 def test_sqrt_kept_as_function_not_sx_parameter(self):
  import ast,re,types
  tree=ast.parse((ROOT/'nx_native.py').read_text())
  cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='NativeModelBuilder')
  fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='expr_text')
  ns={'re':re};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<isolated expression adapter>','exec'),ns)
  self.assertEqual(ns['expr_text'](types.SimpleNamespace(known={'sheet_t'}),'sheet_t*sqrt(1+0.14*0.14)'), 'sx_sheet_t*sqrt(1+0.14*0.14)')
 def test_runtime_contains_sloped_panel_probe(self):
  self.assertIn('API_Schraegblech07_Normaldicke',(ROOT/'NX_CNC_Gesamtansicht.py').read_text())

class DrainReportConsistency07Tests(unittest.TestCase):
 def test_reported_slope_angle_matches_reported_grade(self):
  p=m.load_parameters(ROOT/'Parameter.json');r=m.drain_report(p)
  self.assertAlmostEqual(r['side_slope_angle_deg'], math.degrees(math.atan(r['side_slope_percent']/100.)))
