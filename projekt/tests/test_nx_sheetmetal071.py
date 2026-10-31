"""Regression of the reported UF namespace failure. Simulated NX, not an NX run."""
import unittest
from types import SimpleNamespace as NS
import nx_sheetmetal06 as sm


def plane(tag):
    """AskFaceData(face) -> (type, point, dir, box, radius, radData, normDir)."""
    return (22, [0., 0., 0.], [0., 1., 0.], [0., 0., 0., 10., 0., 10.], 0., 0., 1)


def fixture(groups=None, query=plane):
    calls = []
    face = NS(Tag=101)
    body = NS(GetFaces=lambda: [face])
    feature = NS(SetName=lambda value: calls.append(('name', value)), GetBodies=lambda: [body])
    builder = NS(CommitFeature=lambda: feature, Destroy=lambda: calls.append(('destroy',)))
    manager = NS(CreateConvertToSheetmetalFeatureBuilder=lambda null: builder,
                 IsSheetmetalBody=lambda item: True, GetBodyThickness=lambda item: 2.)
    pref = NS(SetThickness=lambda *args: calls.append(('thickness', args)),
              SetBendRadius=lambda *args: calls.append(('radius', args)),
              SetNeutralFactor=lambda *args: calls.append(('factor', args)),
              Commit=lambda: calls.append(('preferences',)))
    part = NS(Features=NS(SheetmetalManager=manager), Preferences=NS(PartSheetmetal=pref))
    uf = groups if groups is not None else NS(Modl=NS(), Modeling=NS(AskFaceData=query))
    nx = NS(Features=NS(Feature=NS(Null=None)), UF=NS(UFSession=NS(GetUFSession=lambda: uf)))
    meta = dict(plane_axis=1, plane_coordinate='0', thickness='2', bend_radius='3', neutral_factor='.4')
    return part, body, meta, nx, calls, builder


def run_case(groups=None, query=plane):
    part, body, meta, nx, calls, builder = fixture(groups, query)
    logs = []
    result = sm.convert(part, body, meta, float, str, 'required', log=logs.append, nx=nx)
    return result, calls, logs, builder


class NamespaceRegression(unittest.TestCase):
    def test_reported_missing_modl_method_can_use_modeling(self):
        error = None
        result = None
        try:
            result, calls, logs, builder = run_case()
        except Exception as exc:
            error = exc
        self.assertIsNone(error, 'Reported namespace defect reproduced: %r' % error)
        self.assertTrue(result[1]['sheetmetal_verified'])

    def test_modeling_available_without_modl_object(self):
        result, _, _, _ = run_case(NS(Modeling=NS(AskFaceData=plane)))
        self.assertTrue(result[1]['sheetmetal_verified'])

    def test_legacy_modl_binding_still_supported(self):
        result, _, _, _ = run_case(NS(Modl=NS(AskFaceData=plane)))
        self.assertTrue(result[1]['sheetmetal_verified'])

    def test_modlgeneral_accepted_only_if_callable_present(self):
        result, _, _, _ = run_case(NS(Modl=NS(), ModlGeneral=NS(AskFaceData=plane)))
        self.assertTrue(result[1]['sheetmetal_verified'])

    def test_prefer_modeling_and_never_call_other_group_after_selection(self):
        def forbidden(*args):
            self.fail('Wrong namespace was invoked')
        result, _, _, _ = run_case(NS(Modeling=NS(AskFaceData=plane), Modl=NS(AskFaceData=forbidden)))
        self.assertTrue(result[1]['sheetmetal_verified'])

    def test_missing_queries_report_capabilities_without_preferences_change(self):
        p, b, m, nx, calls, _ = fixture(NS(Modl=NS(), Modeling=NS(), ModlGeneral=NS()))
        with self.assertRaisesRegex(RuntimeError, 'AskFaceData.*fehlt'):
            sm.convert(p, b, m, float, str, 'required', nx=nx)
        self.assertEqual(calls, [])

    def test_noncallable_modeling_attribute_does_not_mask_legacy_method(self):
        result, _, _, _ = run_case(NS(Modeling=NS(AskFaceData=17), Modl=NS(AskFaceData=plane)))
        self.assertTrue(result[1]['sheetmetal_verified'])

    def test_query_exception_is_not_retried_in_other_namespace(self):
        seen = []
        def failed(tag):
            seen.append('failed')
            raise RuntimeError('Native face read failed')
        def fallback(tag):
            seen.append('forbidden_fallback')
            return plane(tag)
        p,b,m,nx,calls,_=fixture(NS(Modeling=NS(AskFaceData=failed),Modl=NS(AskFaceData=fallback)))
        with self.assertRaisesRegex(RuntimeError, 'Native face read failed'):
            sm.convert(p,b,m,float,str,'required',nx=nx)
        self.assertEqual(seen, ['failed'])
        self.assertEqual(calls, [])

    def test_raw_query_attributeerror_is_not_misread_as_missing_namespace(self):
        def failed(tag):
            raise AttributeError('Inside actual query')
        p,b,m,nx,_,_=fixture(query=failed)
        with self.assertRaisesRegex(AttributeError,'Inside actual query'):
            sm.convert(p,b,m,float,str,'required',nx=nx)

    def test_success_record_names_resolved_binding_and_patch(self):
        result, _, logs, _ = run_case()
        self.assertEqual(result[1]['face_query'], 'UF.Modeling.AskFaceData')
        self.assertEqual(result[1]['adapter_version'], sm.ADAPTER_VERSION)
        self.assertTrue(any('UF.Modeling.AskFaceData' in text for text in logs))
        self.assertTrue(any('AskFaceData(face)' in text for text in logs))

    def test_later_builder_error_records_stage_and_destroys_builder(self):
        p,b,m,nx,calls,builder=fixture()
        def fail():
            raise RuntimeError('Missing sheetmetal license')
        builder.CommitFeature=fail
        logs=[]
        with self.assertRaisesRegex(RuntimeError, 'Missing sheetmetal license'):
            sm.convert(p,b,m,float,str,'required',logs.append,nx=nx)
        self.assertIn(('destroy',),calls)
        self.assertTrue(any('CommitFeature' in msg and 'fehlgeschlagen' in msg for msg in logs))

    def test_wrong_tuple_not_treated_as_planar_face(self):
        p,b,m,nx,calls,_=fixture(query=lambda tag:(22,[0,0,0]))
        with self.assertRaisesRegex(RuntimeError,'AskFaceData'):
            sm.convert(p,b,m,float,str,'required',nx=nx)
        self.assertEqual(calls, [])

    def test_ambiguous_plane_never_selects_first_face(self):
        p,b,m,nx,calls,_=fixture()
        b.GetFaces=lambda:[NS(Tag=101),NS(Tag=102)]
        with self.assertRaisesRegex(RuntimeError,'nicht eindeutig: 2'):
            sm.convert(p,b,m,float,str,'required',nx=nx)
        self.assertEqual(calls, [])

    def test_no_plane_match_is_not_ignored(self):
        p,b,m,nx,calls,_=fixture()
        m['plane_coordinate']='3'
        with self.assertRaisesRegex(RuntimeError,'nicht eindeutig: 0'):
            sm.convert(p,b,m,float,str,'required',nx=nx)
        self.assertEqual(calls, [])


class PlaneValidation(unittest.TestCase):
    def select(self, record=None, axis=1, coordinate=0., tol=1e-5):
        body=NS(GetFaces=lambda:[NS(Tag=101)])
        query=NS(AskFaceData=lambda tag:plane(tag) if record is None else record)
        return sm.select_base_face(body,query,axis,coordinate,tol)

    def test_negative_normal_has_same_plane(self):
        r=list(plane(0));r[2]=[0,-1,0]
        self.assertEqual(self.select(tuple(r)).Tag,101)

    def test_nonunit_normal_is_normalized(self):
        r=list(plane(0));r[2]=[0,3,0]
        self.assertEqual(self.select(tuple(r)).Tag,101)

    def test_nonplanar_surface_is_not_used(self):
        r=list(plane(0));r[0]=16
        with self.assertRaisesRegex(RuntimeError,'nicht eindeutig: 0'):self.select(tuple(r))

    def test_invalid_axis_is_rejected(self):
        for axis in (-1,3,1.2,True,None):
            with self.subTest(axis=axis),self.assertRaises(ValueError):self.select(axis=axis)

    def test_nonfinite_plane_is_rejected(self):
        for value in (float('nan'),float('inf'),float('-inf'),True):
            with self.subTest(value=value),self.assertRaises(ValueError):self.select(coordinate=value)

    def test_bad_tolerance_rejected(self):
        for value in (0.,-1.,float('nan'),float('inf'),True):
            with self.subTest(value=value),self.assertRaises(ValueError):self.select(tol=value)

    def test_nonfinite_point_never_silently_skipped(self):
        for value in (float('nan'),float('inf')):
            r=list(plane(0));r[1]=[0,value,0]
            with self.subTest(value=value),self.assertRaisesRegex(RuntimeError,'AskFaceData.*Punkt'):
                self.select(tuple(r))

    def test_malformed_vectors_are_reported(self):
        for index, value in ((1,[0,0]),(2,[0,1]),(2,[0,True,0]),(2,[0,'bad',0])):
            r=list(plane(0));r[index]=value
            with self.subTest(index=index,value=value),self.assertRaisesRegex(RuntimeError,'AskFaceData'):
                self.select(tuple(r))

    def test_no_namespace_selection_needed_in_explicit_solid_mode(self):
        body=object();logs=[]
        result,record=sm.convert(None,body,{},float,str,'solid',logs.append,nx=NS())
        self.assertIs(body,result)
        self.assertFalse(record['sheetmetal_verified'])
        self.assertEqual(record['status'],'SOLID_PRECURSOR_ONLY')

if __name__=='__main__':unittest.main()
