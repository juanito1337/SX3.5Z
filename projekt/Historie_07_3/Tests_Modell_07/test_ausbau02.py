import unittest,sys,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell as m
class AusbauTests(unittest.TestCase):
 def test_no_manual_quill_drive(self):
  names={d['name'] for d in m.recipe()}
  self.assertFalse(any(n.startswith('Sternhebel_') for n in names))
  self.assertNotIn('Feinvorschub_Pinole',names)
  self.assertIn('Pinole_Huelse_Detail',names)
 def test_mounting_chain_exists(self):
  names={d['name'] for d in m.recipe()}
  for a in 'XYZ':
   for tail in ['Motorbefestigung_1','Festlager_Befestigung_1','Festlager_Deckel','Festlager_Sicherungsmutter','Loslager_Anschlussbruecke']:
    self.assertIn('CNC_'+a+'_'+tail,names)
 def test_enclosure_stand_cabinet(self):
  groups={d['group'] for d in m.recipe()}
  for g in ['14_Untergestell','15_Einhausung','16_Schaltschrank','17_KSS']:
   self.assertIn(g,groups)
 def test_length_report_all_target_ends(self):
  self.assertTrue(hasattr(m,'length_report'))
  rows=m.length_report(m.load_parameters(ROOT/'Parameter.json'))
  self.assertEqual({r['axis'] for r in rows},set('XYZ'))
  for r in rows:self.assertGreaterEqual(r['minimum_reserve_mm']+1e-6,r['required_reserve_mm'])
 def test_floor_table_height(self):
  p=m.load_parameters(ROOT/'Parameter.json');v=m.all_values(p)
  self.assertIn('stand_h',v);self.assertEqual(v['stand_h']+v['table_top_z'],930)
 def test_originals_retained_except_handdrive(self):
  names={d['name'] for d in m.recipe()}
  for n in ['Basis_Guss_Foto','Saeule_Guss_Foto','Arbeitstisch_Foto','Spindelkopf_Guss_Detail']:
   self.assertIn(n,names)
 def test_every_part_has_source_status_palette_and_unique_name(self):
  ds=m.recipe();self.assertEqual(len(ds),len({d['name'] for d in ds}))
  for d in ds:
   self.assertIn(d['material'],m.PALETTE);self.assertTrue(d['status']);self.assertTrue(d['source']);self.assertTrue(d['note'])
 def test_no_nx_execution_claim_in_model(self):
  for d in m.recipe():self.assertFalse(d.get('manufacturing_released',False))
if __name__=='__main__':unittest.main()

class JointAccessTests(unittest.TestCase):
 def test_motor_screw_heads_have_own_clearance(self):
  p=m.load_parameters(ROOT/'Parameter.json');v=m.all_values(p)
  for a in 'XYZ':
   d=next(d for d in m.recipe() if d['name']=='CNC_'+a+'_Motorbefestigung_1')
   self.assertIn('Motorbefestigung_Kopf_hinter_Flansch',[o['label'] for o in d['ops']])
 def test_machine_heads_clear_fixed_housing(self):
  ds=m.recipe();v=m.all_values(m.load_parameters(ROOT/'Parameter.json'))
  for a in 'XYZ':
   d=next(d for d in ds if d['name']=='CNC_'+a+'_Maschinenanschluss_1')
   xyz=[m.evaluate(q,v) for q in d['ops'][0]['origin']]
   if a=='X':u=xyz[1]-v['pos_y']
   else:u=xyz[0]
   self.assertGreater(abs(u)-4.8,30)

class ViewerContractTests(unittest.TestCase):
 def test_modes_include_machine_and_cabinet(self):
  html=(ROOT/'tools/viewer_template.html').read_text()
  self.assertIn('bschrank',html)
  self.assertIn('bmaschine',html)
 def test_no_stale_part_count(self):
  html=(ROOT/'tools/viewer_template.html').read_text()
  self.assertNotIn('229 Einzelkörper',html)
 def test_motor_heads_are_outside_flange_and_body_is_reliefed(self):
  v=m.all_values(m.load_parameters(ROOT/'Parameter.json'))
  for a in 'XYZ':
   d=next(d for d in m.recipe() if d['name']=='CNC_'+a+'_Motorbefestigung_1')
   head=next(o for o in d['ops'] if o['label']=='Motorbefestigung_Kopf_hinter_Flansch')
   xyz=[m.evaluate(q,v) for q in head['origin']];n='cnc_'+a.lower()+'_'
   local=xyz[0]-(v['pos_x']+v['table_x']/2) if a=='X' else (v['base_front_y']-xyz[1] if a=='Y' else xyz[2]-v['column_top_z']-v['column_cap_h'])
   self.assertAlmostEqual(local,v[n+'motor_front']+5)
   body=next(d for d in m.recipe() if d['name']=='CNC_'+a+'_Motor_Gehaeuse')
   self.assertEqual(sum(o.get('label')=='Kopfzugang_nur_Huellendarstellung' for o in body['ops']),4)

class SourceFlangeTests(unittest.TestCase):
 def test_xy_motor_flange_retains_catalog_through_holes(self):
  for a in 'XY':
   d=next(d for d in m.recipe() if d['name']=='CNC_'+a+'_Motor_Frontflansch')
   holes=[o for o in d['ops'] if o.get('label')=='Motorloch']
   self.assertEqual(len(holes),4)
   self.assertTrue(all(float(o['diameter'])==5.0 for o in holes))

class BearingClearanceTests(unittest.TestCase):
 def test_rotating_shoulder_clears_stationary_housing_entry(self):
  v=m.all_values(m.load_parameters(ROOT/'Parameter.json'))
  for a in 'XYZ':
   d=next(d for d in m.recipe() if d['name']=='CNC_'+a+'_Festlager_Entwurf')
   bore=next(o for o in d['ops'] if o.get('label')=='Zapfenfreiraum')
   self.assertGreater(m.evaluate(bore['diameter'],v),v['cnc_'+a.lower()+'_journal_d']+6)
