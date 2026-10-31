"""Dimensional regression for NX_Fehlerprotokoll(8), no NX runtime.

The quantity evaluator below is deliberately separate from the compiler. It
rejects dimensionally incompatible addition and dimensioned sqrt arguments.
It is NOT a full NX expression parser and is not a geometric kernel test.
"""
import ast
import importlib
import math
from pathlib import Path
import re
from types import SimpleNamespace as NS
import unittest
import cnc_ansichtsmodell as model

ROOT = Path(__file__).resolve().parents[1]


class Quantity:
    def __init__(self, value, dimension=0):
        self.value, self.dimension = float(value), dimension


def quantity_eval(text, values):
    def walk(n):
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            return Quantity(n.value)
        if isinstance(n, ast.Name):
            return values[n.id]
        if isinstance(n, ast.UnaryOp):
            a = walk(n.operand)
            return Quantity((-1 if isinstance(n.op, ast.USub) else 1)*a.value, a.dimension)
        if isinstance(n, ast.BinOp):
            a, b = walk(n.left), walk(n.right)
            if isinstance(n.op, (ast.Add, ast.Sub)):
                if a.dimension != b.dimension:
                    raise ValueError('Dimension mismatch (binary operation)')
                return Quantity(a.value + (1 if isinstance(n.op, ast.Add) else -1)*b.value, a.dimension)
            if isinstance(n.op, ast.Mult):
                return Quantity(a.value*b.value, a.dimension+b.dimension)
            if isinstance(n.op, ast.Div):
                return Quantity(a.value/b.value, a.dimension-b.dimension)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'sqrt':
            a = walk(n.args[0])
            if a.dimension != 0:
                raise ValueError('Grade factor in sqrt must be dimensionless')
            return Quantity(math.sqrt(a.value))
        raise ValueError('Unsupported test expression: '+ast.dump(n))
    return walk(ast.parse(text, mode='eval').body)


def adapter_class():
    """Execute actual adapter methods, not reimplemented replacement logic."""
    tree = ast.parse((ROOT/'nx_native.py').read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'NativeModelBuilder')
    wanted = {'expr_text', 'extrusion_height_text', 'profile_extrude', 'log'}
    cls.body = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    fake_nx = NS(Section=NS(AllowTypes=NS(OnlyCurves=1), Mode=NS(Create=2)),
                 NXObject=NS(Null=None), Features=NS(Feature=NS(Null=None)),
                 Point3d=lambda *x: x)
    ns = {'re': re, 'math': math, 'model': model, 'NXOpen': fake_nx}
    if (ROOT/'nx_formeln073.py').exists():
        ns['nx_formeln073'] = importlib.import_module('nx_formeln073')
    exec(compile(ast.Module(body=[cls], type_ignores=[]), '<actual adapter methods>', 'exec'), ns)
    return ns['NativeModelBuilder']


class HeightFixture:
    """Fake EndExtend.Value enforces unit algebra at the actual failing setter."""
    def __init__(self, values, expected_dimension):
        self.values, self.expected_dimension = values, expected_dimension
        self.text, self.result = None, None

    @property
    def RightHandSide(self):
        return self.text

    @RightHandSide.setter
    def RightHandSide(self, text):
        result = quantity_eval(text, self.values)
        if result.dimension != self.expected_dimension:
            raise ValueError('Extrusion end limit has wrong dimension')
        self.text, self.result = text, result


def run_profile(definition, params, mode='CreateNumberExpression'):
    builder = adapter_class()()
    numeric = model.all_values(params)
    unitless = {s['name'] for s in model.SPECS if s.get('unit') == 'unitless'}
    quantities = {'sx_'+k: Quantity(v, 0 if mode == 'Number_mm' or k in unitless else 1)
                  for k, v in numeric.items()}
    helper_equations, logs = [], []
    def create(equation):
        name, rhs = [s.strip() for s in equation.split('=', 1)]
        # A constant created via the factory is a native length expression.
        value = float(rhs)
        quantities[name] = Quantity(value, 0 if mode == 'Number_mm' else 1)
        helper_equations.append(equation)
        return NS(Value=value)
    def close(actual, expected, label):
        if abs(actual-expected) > 1e-9:
            raise ValueError(label)
    builder.expression_factory = NS(mode=mode, create=create, _close=close)
    builder.known = set(numeric)
    builder.values = numeric
    builder.aux_id = 0
    builder.runlog = logs.append
    builder.point = lambda vertex: vertex
    builder.profile_curve = lambda *args: NS(Blank=lambda: None)
    builder.direction = lambda v: v
    builder.boolean = lambda *args: None
    section = NS(SetAllowedEntityTypes=lambda *args: None, AddToSection=lambda *args: None)
    builder.part = NS(Sections=NS(CreateSection=lambda *args: section),
                      ScRuleFactory=NS(CreateRuleCurveDumb=lambda *args: None), Features=NS())
    end = HeightFixture(quantities, 0 if mode == 'Number_mm' else 1)
    feature = object()
    extrude = NS(Limits=NS(StartExtend=NS(Value=NS()), EndExtend=NS(Value=end)),
                 CommitFeature=lambda: feature, Destroy=lambda: None)
    builder.new_feature_builder = lambda *args: extrude
    op = model.local_definition(definition)['ops'][0]
    builder.profile_extrude(op, None, '001_Geneigtes_Blech_Normaldicke')
    return end, helper_equations, quantities, logs


class NormalThicknessRegression073(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params = model.load_parameters(ROOT/'Parameter.json')
        cls.parts = {d['name']: d for d in model.recipe()}
        cls.slopes = [d for d in cls.parts.values() if 'plate_normal_thickness' in d]

    def test_reported_left_funnel_passes_actual_extrude_rhs_path(self):
        failure = None
        try:
            end, equations, _, _ = run_profile(self.parts['KSS_Trichter_links'], self.params)
        except Exception as exc:
            failure = exc
        self.assertIsNone(failure, 'Reported failure at EndExtend.Value.RightHandSide: %r' % failure)
        self.assertAlmostEqual(end.result.value, 2.0235302212255237)
        self.assertEqual(end.result.dimension, 1)
        self.assertEqual(len(equations), 1)

    def test_original_formula_has_dimension_conflict(self):
        op = self.parts['KSS_Trichter_links']['ops'][0]
        b = adapter_class()(); b.known = set(model.all_values(self.params))
        original = b.expr_text(op['height'])
        values = {'sx_'+k: Quantity(v, 1) for k, v in model.all_values(self.params).items()}
        with self.assertRaisesRegex(ValueError, 'Dimension mismatch'):
            quantity_eval(original, values)

    def test_all_ten_sloped_panels_have_length_result_and_same_values(self):
        self.assertEqual(len(self.slopes), 10)
        for d in self.slopes:
            with self.subTest(part=d['name']):
                end, _, _, _ = run_profile(d, self.params)
                expected = model.evaluate(d['ops'][0]['height'], model.all_values(self.params))
                self.assertAlmostEqual(end.result.value, expected)
                self.assertEqual(end.result.dimension, 1)

    def test_all_funnels_stay_associative_after_dimension_changes(self):
        for d in self.slopes:
            if not d['name'].startswith('KSS_Trichter_'): continue
            end, _, quantities, _ = run_profile(d, self.params)
            for changes in ({'chip_outlet_w': 320}, {'chip_outlet_d': 50}, {'chip_outlet_y': 450},
                            {'sheet_t': 2.5}, {'stand_d': 1020}):
                with self.subTest(part=d['name'], change=changes):
                    p = dict(self.params, **changes)
                    v = model.all_values(p)
                    updated = dict(quantities)
                    for k, val in v.items():
                        updated['sx_'+k] = Quantity(val, quantities['sx_'+k].dimension)
                    actual = quantity_eval(end.text, updated)
                    expected = model.evaluate(d['ops'][0]['height'], v)
                    self.assertAlmostEqual(actual.value, expected)
                    self.assertEqual(actual.dimension, 1)

    def test_number_mm_compatibility_mode_not_normalized_twice(self):
        for d in self.slopes:
            with self.subTest(part=d['name']):
                end, equations, _, _ = run_profile(d, self.params, 'Number_mm')
                self.assertEqual(equations, [])
                self.assertEqual(end.result.dimension, 0)
                expected = model.evaluate(d['ops'][0]['height'], model.all_values(self.params))
                self.assertAlmostEqual(end.result.value, expected)

    def test_constant_grade_requires_no_mm_reference(self):
        end, equations, _, _ = run_profile(self.parts['KSS_Leitblech_links_vorn'], self.params)
        self.assertEqual(equations, [])
        self.assertEqual(end.result.dimension, 1)

    def test_both_documented_typed_factory_modes(self):
        for mode in ('CreateNumberExpression', 'CreateNumberExpression4', 'CreateWithUnits', 'CreateWithUnits4'):
            with self.subTest(mode=mode):
                end, _, _, _ = run_profile(self.parts['KSS_Trichter_hinten'], self.params, mode)
                self.assertEqual(end.result.dimension, 1)

    def test_no_new_nx_api_called_by_formula_helper(self):
        self.assertTrue((ROOT/'nx_formeln073.py').exists())
        text = (ROOT/'nx_formeln073.py').read_text()
        self.assertNotIn('import NXOpen', text)
        self.assertNotIn('eval(', text)

    def test_runtime_probe_includes_real_funnels(self):
        text = (ROOT/'NX_CNC_Gesamtansicht.py').read_text()
        self.assertIn('KSS_Formelprobe073', text)
        self.assertIn("startswith('KSS_Trichter_')", text)

    def test_short_test_exists_and_filters_sloped_panels(self):
        path = ROOT/'NX_KSS_Pruefen.py'
        self.assertTrue(path.exists())
        text = path.read_text()
        self.assertIn('plate_normal_thickness', text)
        self.assertIn('parts_only=True', text)


if __name__ == '__main__':
    unittest.main()

class FormulaScope073(unittest.TestCase):
    def test_unitless_input_in_grade_remains_unitless(self):
        from nx_formeln073 import normal_thickness_rhs, needs_length_reference
        text = 'sheet_t*sqrt(1+door_open*door_open)'
        self.assertFalse(needs_length_reference(text, {'sheet_t', 'door_open'}, {'door_open'}))
        out = normal_thickness_rhs(text, {'sheet_t', 'door_open'}, {'door_open'})
        q = quantity_eval(out, {'sx_sheet_t': Quantity(2, 1), 'sx_door_open': Quantity(.5)})
        self.assertEqual(q.dimension, 1)
        self.assertAlmostEqual(q.value, math.sqrt(5))

    def test_ordinary_extrusion_path_unchanged(self):
        params = model.load_parameters(ROOT/'Parameter.json')
        d = next(d for d in model.recipe() if d['name'] == 'KSS_Trichter_links')
        import copy
        d = copy.deepcopy(d); d['ops'][0]['height'] = 'sheet_t'
        end, helpers, _, _ = run_profile(d, params)
        self.assertEqual(end.text, 'sx_sheet_t')
        self.assertEqual(helpers, [])

    def test_only_documented_formula_shape_is_translated(self):
        from nx_formeln073 import normal_thickness_rhs
        for text in ('sqrt(sheet_t)', '2*sqrt(1+1)', 'sheet_t+sqrt(1)', 'sheet_t*sqrt(1,2)',
                     'sheet_t*sqrt(x=1)', 'door_open*sqrt(1)'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                normal_thickness_rhs(text, {'sheet_t', 'door_open'}, {'door_open'})

    def test_unknown_names_attributes_calls_and_powers_rejected(self):
        from nx_formeln073 import needs_length_reference
        for arg in ('missing', 'sheet_t.real', 'float(1)', 'sqrt(1)', 'sheet_t**2',
                    '__import__("os")', '[1][0]', 'True', '1e309'):
            with self.subTest(arg=arg), self.assertRaises((ValueError, SyntaxError)):
                needs_length_reference('sheet_t*sqrt('+arg+')', {'sheet_t'})

    def test_reference_name_is_not_arbitrary_code(self):
        from nx_formeln073 import normal_thickness_rhs
        for reference in ('1', 'sx_aux_1+0', 'os.path', '__import__', 'sx_sheet_t'):
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                normal_thickness_rhs('sheet_t*sqrt(1+sheet_t)', {'sheet_t'}, (), reference)

    def test_unknown_factory_mode_not_silently_changed(self):
        params = model.load_parameters(ROOT/'Parameter.json')
        d = next(d for d in model.recipe() if d['name'] == 'KSS_Trichter_links')
        with self.assertRaisesRegex(RuntimeError, 'Ausdrucksmodus'):
            run_profile(d, params, 'UnknownMode')

    def test_root_parameters_not_frozen_to_current_values(self):
        params = model.load_parameters(ROOT/'Parameter.json')
        d = next(d for d in model.recipe() if d['name'] == 'KSS_Trichter_links')
        end, helpers, _, _ = run_profile(d, params)
        self.assertIn('sx_chip_outlet_w', end.text)
        self.assertIn('sx_sheet_t', end.text)
        self.assertNotIn('350', end.text)
        self.assertEqual(helpers[0].split('=')[1].strip(), '1')

    def test_diagnostics_record_native_formula(self):
        params = model.load_parameters(ROOT/'Parameter.json')
        d = next(d for d in model.recipe() if d['name'] == 'KSS_Trichter_links')
        end, _, _, logs = run_profile(d, params)
        self.assertTrue(any(end.text in line for line in logs))
        self.assertTrue(any('1 mm' in line for line in logs))
