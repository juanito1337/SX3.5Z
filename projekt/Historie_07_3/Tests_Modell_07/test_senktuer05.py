import copy,json,unittest
from pathlib import Path
import cnc_ansichtsmodell as m
from enclosure_checks03 import body_bounds
from tools.laengen_und_huellraum import signature
ROOT=Path(__file__).resolve().parents[1]

class DownwardDoorTests(unittest.TestCase):
 def p(self):return m.load_parameters(ROOT/'Parameter.json')
 def test_revision(self):self.assertEqual(m.VERSION,'CNC_ANSICHT_07')
 def test_two_downward_segments(self):
  r=m.door_layout(self.p());self.assertEqual(r['direction'],[0,0,-1]);self.assertEqual(len(r['leaves']),2)
 def test_fully_open_both_below_opening(self):
  r=m.door_layout(dict(self.p(),door_open=1))
  for leaf in r['leaves']:self.assertLessEqual(leaf['zmax'],r['opening_zmin']-5+1e-7)
 def test_ground_clearance_throughout(self):
  p=self.p()
  for q in [i/8 for i in range(9)]:
   for leaf in m.door_layout(dict(p,door_open=q))['leaves']:self.assertGreaterEqual(leaf['zmin']+p['stand_h'],250)
 def test_closed_panels_cover_aperture_with_overlap(self):
  r=m.door_layout(self.p());ls=sorted(r['leaves'],key=lambda x:x['zmin'])
  self.assertEqual(len(ls),2)
  self.assertLessEqual(ls[0]['zmin'],r['opening_zmin']);self.assertGreaterEqual(ls[-1]['zmax'],r['opening_zmax'])
  self.assertGreaterEqual(ls[0]['zmax']-ls[1]['zmin'],20)
  for leaf in ls:
   self.assertLessEqual(leaf['xmin'],r['opening_xmin']);self.assertGreaterEqual(leaf['xmax'],r['opening_xmax'])
 def test_panels_use_different_depth_lanes(self):
  ls=m.door_layout(self.p())['leaves'];self.assertEqual(len(ls),2)
  self.assertGreaterEqual(abs(ls[0]['ymin']-ls[1]['ymin']),50)
 def test_outer_enclosure_and_heights_retained(self):
  p=self.p();v=m.all_values(p)
  self.assertEqual([p[k] for k in ('stand_w','stand_d','enclosure_h','travel_x','travel_y','z_travel_used')],[1650,1000,1200,500,200,240]);self.assertEqual(v['workheight'],930)
  self.assertAlmostEqual(m.door_layout(p)['fixed_total_height_mm'],1952)
 def test_rigid_motion_and_2to1_ratio(self):
  p=self.p();a=m.all_values(p);b=m.all_values(dict(p,door_open=1));seen={}
  for d in [d for d in m.recipe() if d.get('door_leaf')]:
   self.assertEqual(signature(d,a),signature(d,b),d['name'])
   x=[m.evaluate(q,a) for q in d['datum']];y=[m.evaluate(q,b) for q in d['datum']]
   self.assertEqual(x[:2],y[:2]);self.assertLess(y[2]-x[2],0)
   seen.setdefault(d['door_leaf'],round(y[2]-x[2],7));self.assertAlmostEqual(seen[d['door_leaf']],y[2]-x[2])
  self.assertEqual(set(seen),{'LOWER','UPPER'});self.assertAlmostEqual(seen['UPPER'],2*seen['LOWER'])
 def test_no_upward_names(self):
  self.assertFalse(any(d['name'].startswith('Hubtuer_') for d in m.recipe()))
 def test_each_leaf_has_position_switch_reserve(self):
  ds=m.recipe();self.assertEqual(len([d for d in ds if d['name'].startswith('Tuerueberwachung_')]),2)
 def test_ground_and_ceiling_bound_all_door_hardware(self):
  p=self.p()
  for q in (0,.5,1):
   v=m.all_values(dict(p,door_open=q))
   for d in m.recipe():
    if d['name'].startswith(('Senktuer_','Tuerueberwachung_')):
     b=body_bounds(d,v,m.evaluate);self.assertGreaterEqual(b[2]+p['stand_h'],50,d['name']);self.assertLessEqual(b[5],p['enclosure_h'],d['name'])
 def test_other_groups_unchanged(self):
  snapshot=json.loads((ROOT/'tests/fixtures/unveraendert03.json').read_text());v=m.all_values(self.p())
  recipe=m.recipe()
  ds=[d for d in recipe if int(d['group'][:2])<=14 and not d['name'].startswith('Schrank_')]
  eligible={a['name'] for a in recipe if int(a['group'][:2])<=14 and not a['name'].startswith('Schrank_')}
  self.assertEqual({d['name'] for d in ds},{n for n in snapshot if n in eligible})
  for d in ds:
   old=snapshot[d['name']];self.assertEqual(json.loads(json.dumps(signature(d,v))),old['signature'],d['name'])
   self.assertEqual([m.evaluate(x,v) for x in d['datum']],old['datum'],d['name']);self.assertEqual(d['material'],old['material'])
 def test_old_one_piece_downward_would_hit_floor(self):
  p=self.p();single_bottom=p['stand_h']+p['door_z']-p['door_overlap']-(p['door_clear_h']+p['door_overlap']+p['door_open_clearance'])
  self.assertEqual(single_bottom,-195)
 def test_invalid_low_stand_rejected(self):
  with self.assertRaises(ValueError):m.validate(dict(self.p(),stand_h=450))
 def test_clearance_cannot_be_negative(self):
  p=self.p();self.assertIn('door_panel_overlap',p)
  with self.assertRaises(ValueError):m.validate(dict(p,door_panel_overlap=1))
 def test_glass_not_too_thick_for_lane(self):
  with self.assertRaises(ValueError):m.validate(dict(self.p(),window_t=25))
 def test_guides_cover_all_carriages(self):
  ds=m.recipe();gs=[d for d in ds if d['name'].startswith('Senktuer_Fuehrung_')];self.assertEqual(len(gs),4)
  p=self.p()
  for q in (0,.25,.5,.75,1):
   v=m.all_values(dict(p,door_open=q));sl=[d for d in ds if d['name'].startswith('Senktuer_Schlitten_')];self.assertEqual(len(sl),8)
   for d in sl:
    a=body_bounds(d,v,m.evaluate);guides=[e for e in gs if d['door_leaf'] in e['name']]
    self.assertTrue(any((lambda b:b[0]<a[0] and b[3]>a[3] and b[2]<=a[2] and b[5]>=a[5])(body_bounds(e,v,m.evaluate)) for e in guides),d['name'])
 def test_no_manufacturing_release(self):
  for d in m.recipe():self.assertFalse(d.get('manufacturing_released',False))
 def test_model_motion_metadata_is_segment_specific(self):
  vals=m.all_values(self.p());ms=[d for d in m.recipe() if d.get('door_leaf')]
  self.assertGreater(len(ms),10)
  for d in ms:
   self.assertEqual(d.get('door_motion_vector'),[0,0,-1]);self.assertIn('door_shift_z',d)
   self.assertLess(m.evaluate(d['door_shift_z'],vals),0)
 def test_parameters_have_no_mixed_revision(self):
  self.assertIn("model.VERSION != 'CNC_ANSICHT_07'",(ROOT/'NX_CNC_Gesamtansicht.py').read_text())

if __name__=='__main__':unittest.main()

class DoorSamplingTests(unittest.TestCase):
 def test_motion_sampling_uses_each_segment(self):
  from tools import tuerbewegung_pruefen as tool
  self.assertTrue(hasattr(tool,'motion_delta'),'Sampler must use per-segment negative travel')
  p=m.load_parameters(ROOT/'Parameter.json');v=m.all_values(p)
  for d in [d for d in m.recipe() if d.get('door_leaf')]:
   delta=tool.motion_delta(d,v,.5)
   self.assertEqual(delta[:2],(0.,0.))
   self.assertAlmostEqual(delta[2],-.5*v['door_travel_'+d['door_leaf'].lower()])
