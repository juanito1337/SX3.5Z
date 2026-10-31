"""Regression tests of the design/data contract, NOT tests in Siemens NX."""
import json, math, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import cnc_ansichtsmodell08 as model
import cnc_ansichtsmodell07 as original

class Contract08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=model.load_parameters(ROOT/'Parameter.json')
        cls.parts=model.recipe()
    def test_revision(self): self.assertEqual(model.VERSION,'CNC_UMSETZUNG_08')
    def test_catalog_present(self): self.assertTrue((ROOT/'Einkauf/Kaufteile_08.json').is_file())
    def test_z_pilot_real_family_not_old_73(self): self.assertEqual(self.p['cnc_z_pilot_d'],60)
    def test_z_ff15_bearing_journal(self): self.assertEqual(self.p['cnc_z_free_journal_d'],15)
    def test_motor_b_revision_conflict_retained(self):
        self.assertEqual(self.p['cnc_z_motor_l'],144)
        self.assertIn('REVISION',next(d for d in self.parts if d['name']=='CNC_Z_Motor_Gehaeuse')['note'])
    def test_no_fictitious_supports(self):
        names={x['name'] for x in self.parts}
        for a in 'XYZ':
            self.assertIn('CNC_'+a+'_THK_Festlager',names)
            self.assertIn('CNC_'+a+'_THK_Loslager',names)
    def test_originals_unchanged(self):
        new={x['name']:x for x in self.parts}
        for d in original.recipe():
            if d['name'] in ('Basis_Guss_Foto','Saeule_Guss_Foto','Arbeitstisch_Foto','Kreuzschlitten_Guss_Detail','Spindelkopf_Guss_Detail') or d.get('door_leaf'):
                self.assertEqual(d['ops'],new[d['name']]['ops'],d['name'])
                self.assertEqual(d['datum'],new[d['name']]['datum'],d['name'])
    def test_every_model_body_classified(self):
        for d in self.parts:
            self.assertIn(d.get('supply_kind'),('BUY','MAKE','EXISTING','RESERVE'),d['name'])
            self.assertTrue(d.get('item_id'),d['name'])
            self.assertFalse(d['manufacturing_released'])
    def test_purchase_instances_not_body_count(self):
        instances={d['purchase_instance'] for d in self.parts if d.get('item_id')=='K-MOT-XY'}
        self.assertEqual(len(instances),2)
    def test_dimensions_parametric(self):
        vals=model.check_recipe(self.p)
        self.assertEqual(vals['cnc_x_motor_front'],84)
        self.assertEqual(vals['cnc_z_motor_front'],125)
        self.assertEqual(vals['cnc_x_spacer_l'],57)
        self.assertEqual(vals['cnc_z_spacer_l'],98)
    def test_axial_shaft_gaps(self):
        v=model.all_values(self.p)
        for a in 'xyz':
            front=v['cnc_'+a+'_motor_front'];shaft=v['cnc_'+a+'_shaft_l']
            end=80 if a=='z' else 60
            self.assertGreaterEqual(front-shaft-end,3)
    def test_catalog_controls_mapped_dimensions(self):
        if not hasattr(model,'CATALOG_PARAMETER_MAP'):self.fail('catalog mapping missing')
        catalog=json.loads((ROOT/'Einkauf/Kaufteile_08.json').read_text())['items']
        for par,item,key in model.CATALOG_PARAMETER_MAP:
            self.assertEqual(self.p[par],catalog[item]['dims'][key])
    def test_release_gate_unmeasured(self):
        import umbau_daten08
        report=umbau_daten08.release_report(ROOT)
        self.assertFalse(report['build_ready'])
        self.assertGreater(report['missing_measurement_count'],0)
    def test_unknowns_cannot_become_zero(self):
        data=json.loads((ROOT/'Aufmass/Messwerte_08.json').read_text())
        self.assertTrue(all(x['measured_value'] is None for x in data['measurements']))
    def test_catalog_entities_traceable(self):
        import umbau_daten08
        cat=umbau_daten08.catalog(ROOT)
        for d in self.parts:
            if d['supply_kind']=='BUY':self.assertIn(d['item_id'],cat['items'])
    def test_bom_vs_model_counts(self):
        import umbau_daten08
        bom=umbau_daten08.bom_rows(self.parts,ROOT)
        byid={b['item_id']:b for b in bom}
        self.assertEqual(byid['K-FK12']['model_quantity'],2)
        self.assertEqual(byid['K-FF15']['model_quantity'],1)
        self.assertEqual(byid['K-MOT-XY']['model_quantity'],2)
        self.assertEqual(byid['K-DRV-XY']['model_quantity'],2)
    def test_existing_castings_never_purchase(self):
        for d in self.parts:
            if d['name'] in ['Basis_Guss_Foto','Saeule_Guss_Foto','Arbeitstisch_Foto']:
                self.assertEqual(d['supply_kind'],'EXISTING')
    def test_positive_operations(self):
        v=model.all_values(self.p)
        for d in self.parts:
            for o in d['ops']:
                for x in o.get('size',[]):self.assertGreater(model.evaluate(x,v),0)
                for k in ('height','diameter'):
                    if k in o:self.assertGreater(model.evaluate(o[k],v),0)
    def test_unique_identifiers(self):
        self.assertEqual(len(self.parts),len({d['id'] for d in self.parts}))
        self.assertEqual(len(self.parts),len({d['name'] for d in self.parts}))
    def test_readonly_catalog_override_guard(self):
        if not hasattr(model,'assert_catalog_dimensions'):self.fail('catalog guard missing')
        p=dict(self.p);p['cnc_z_pilot_d']=73
        with self.assertRaises(ValueError):model.assert_catalog_dimensions(p)

if __name__=='__main__': unittest.main()
