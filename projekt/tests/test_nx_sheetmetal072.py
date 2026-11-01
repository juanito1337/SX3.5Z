"""07.2 regression: documented PartSheetmetal access. No Siemens NX runtime.

Strict property/method shapes are based on the Siemens reference, not copied
from the implementation. This still cannot establish NX2406 execution.
"""
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
import nx_sheetmetal06 as sm


class PartSheetmetalFixture:
    __slots__ = ('calls', 'fail_on')

    def __init__(self, calls):
        self.calls = calls
        self.fail_on = None

    def _set(self, name, updateModel, text):
        if type(updateModel) is not bool or not isinstance(text, str):
            raise TypeError('Expected (bool, str)')
        self.calls.append((name, updateModel, text))
        if self.fail_on == name:
            raise RuntimeError('Native setter failed: ' + name)

    def SetThickness(self, updateModel, thickness):
        """SetThickness(updateModel, thickness): bool, str."""
        self._set('SetThickness', updateModel, thickness)

    def SetBendRadius(self, updateModel, bendRadius):
        """SetBendRadius(updateModel, bendRadius): bool, str."""
        self._set('SetBendRadius', updateModel, bendRadius)

    def SetNeutralFactor(self, updateModel, neutralFactor):
        """SetNeutralFactor(updateModel, neutralFactor): bool, str."""
        self._set('SetNeutralFactor', updateModel, neutralFactor)

    def Commit(self):
        """Commit(): apply preference settings."""
        self.calls.append(('Commit',))
        if self.fail_on == 'Commit':
            raise RuntimeError('Native commit failed')


class PartPreferencesFixture:
    __slots__ = ('PartSheetmetal',)

    def __init__(self, value):
        self.PartSheetmetal = value


def case(preferences=None):
    calls = []
    face = NS(Tag=7)
    body = NS(GetFaces=lambda: [face])
    feature = NS(SetName=lambda text: calls.append(('name', text)), GetBodies=lambda: [body])
    builder = NS(CommitFeature=lambda: (calls.append(('feature_commit',)), feature)[1],
                 Destroy=lambda: calls.append(('destroy',)))
    def create(null):
        calls.append(('create', null))
        return builder
    manager = NS(CreateConvertToSheetmetalFeatureBuilder=create,
                 IsSheetmetalBody=lambda item: True, GetBodyThickness=lambda item: 2.)
    pref = PartSheetmetalFixture(calls)
    part = NS(Features=NS(SheetmetalManager=manager),
              Preferences=PartPreferencesFixture(pref) if preferences is None else preferences)
    def query(tag):
        return (22, [0., 0., 0.], [0., 1., 0.], [0., 0., 0., 80., 0., 50.], 0., 0., 1)
    uf = NS(Modl=NS(), Modeling=NS(AskFaceData=query))
    nx = NS(Features=NS(Feature=NS(Null=None)), UF=NS(UFSession=NS(GetUFSession=lambda: uf)))
    meta = dict(plane_axis=1, plane_coordinate='0', thickness='sheet_t',
                bend_radius='bend_r', neutral_factor='bend_k')
    values = {'0': 0., 'sheet_t': 2., 'bend_r': 3., 'bend_k': .4}
    return part, body, meta, nx, pref, calls, values, builder


def invoke(data, logs=None):
    part, body, meta, nx, pref, calls, values, builder = data
    return sm.convert(part, body, meta, values.__getitem__, lambda s: 'sx_' + s,
                      'required', (logs if logs is not None else []).append, nx=nx)


class PreferenceRegression(unittest.TestCase):
    def test_reported_missing_sheetmetal_uses_documented_part_sheetmetal(self):
        data = case()
        self.assertFalse(hasattr(data[0].Preferences, 'Sheetmetal'))
        error, result = None, None
        try:
            result = invoke(data)
        except Exception as exc:
            error = exc
        self.assertIsNone(error, 'Reported PartPreferences defect: %r' % error)
        self.assertTrue(result[1]['sheetmetal_verified'])

    def test_old_incorrect_member_is_never_accessed(self):
        data = case()
        pref = data[4]
        class Preferences:
            PartSheetmetal = pref
            @property
            def Sheetmetal(self):
                raise AssertionError('Undocumented property must not be queried')
        data[0].Preferences = Preferences()
        self.assertTrue(invoke(data)[1]['sheetmetal_verified'])

    def test_formulas_and_update_flags_are_preserved(self):
        data = case()
        invoke(data)
        self.assertEqual(data[5][:4], [
            ('SetThickness', False, 'sx_sheet_t'),
            ('SetBendRadius', False, 'sx_bend_r'),
            ('SetNeutralFactor', False, 'sx_bend_k'), ('Commit',)])
        self.assertEqual(data[5][4], ('create', None))

    def test_success_record_identifies_preference_path(self):
        record = invoke(case())[1]
        self.assertEqual(record['preferences_path'], 'Preferences.PartSheetmetal')
        self.assertEqual(record['adapter_version'], '07.2')
        self.assertFalse(record['flat_pattern_generated'])
        self.assertFalse(record['manufacturing_released'])

    def test_diagnostics_include_local_preference_signatures(self):
        logs = []
        invoke(case(), logs)
        self.assertTrue(any('Preferences.PartSheetmetal' in text for text in logs))
        self.assertTrue(any('SetThickness(updateModel, thickness)' in text for text in logs))
        self.assertTrue(any('SetNeutralFactor(updateModel, neutralFactor)' in text for text in logs))

    def test_missing_documented_property_does_not_use_wrong_member(self):
        wrong = NS(SetThickness=lambda *a: self.fail('Wrong property used'))
        data = case(NS(Sheetmetal=wrong))
        logs = []
        with self.assertRaises(AttributeError):
            invoke(data, logs)
        self.assertEqual(data[5], [])
        self.assertTrue(any('verfuegbare' in text.lower() and 'Sheetmetal' in text for text in logs))
        self.assertTrue(any('fehlgeschlagen [Preferences.PartSheetmetal]' in text for text in logs))

    def test_null_documented_preference_is_not_success(self):
        data = case(PartPreferencesFixture(None))
        with self.assertRaisesRegex(RuntimeError, 'PartSheetmetal'):
            invoke(data)
        self.assertEqual(data[5], [])

    def test_missing_method_fails_before_any_setting(self):
        for name in ('SetThickness', 'SetBendRadius', 'SetNeutralFactor', 'Commit'):
            with self.subTest(name=name):
                data = case()
                proxy = NS(**{n: getattr(data[4], n) for n in
                    ('SetThickness', 'SetBendRadius', 'SetNeutralFactor', 'Commit') if n != name})
                data[0].Preferences = PartPreferencesFixture(proxy)
                with self.assertRaisesRegex(RuntimeError, name):
                    invoke(data)
                self.assertEqual(data[5], [])

    def test_noncallable_method_fails_before_any_setting(self):
        data = case()
        proxy = NS(**{n: getattr(data[4], n) for n in
            ('SetThickness', 'SetBendRadius', 'SetNeutralFactor', 'Commit')})
        proxy.SetNeutralFactor = 0.4
        data[0].Preferences = PartPreferencesFixture(proxy)
        with self.assertRaisesRegex(RuntimeError, 'SetNeutralFactor'):
            invoke(data)
        self.assertEqual(data[5], [])

    def test_native_property_exception_is_preserved(self):
        failure = RuntimeError('Native access/license error')
        class Preferences:
            @property
            def PartSheetmetal(self):
                raise failure
        data = case(Preferences())
        with self.assertRaises(RuntimeError) as caught:
            invoke(data)
        self.assertIs(caught.exception, failure)
        self.assertEqual(data[5], [])

    def test_native_setter_failures_stop_before_feature_creation(self):
        for name in ('SetThickness', 'SetBendRadius', 'SetNeutralFactor'):
            with self.subTest(name=name):
                data = case()
                data[4].fail_on = name
                logs = []
                with self.assertRaisesRegex(RuntimeError, 'Native setter failed: ' + name):
                    invoke(data, logs)
                self.assertFalse(any(row[0] == 'create' for row in data[5]))
                self.assertTrue(any('Preferences.PartSheetmetal.' + name in text and
                                    'fehlgeschlagen' in text for text in logs))

    def test_native_commit_failure_is_not_ignored(self):
        data = case()
        data[4].fail_on = 'Commit'
        with self.assertRaisesRegex(RuntimeError, 'Native commit failed'):
            invoke(data)
        self.assertFalse(any(row[0] == 'create' for row in data[5]))

    def test_each_part_gets_its_own_preferences(self):
        a, b = case(), case()
        invoke(a)
        before = list(a[5])
        invoke(b)
        self.assertEqual(a[5], before)
        self.assertEqual(a[5], b[5])

    def test_builder_still_receives_selected_face_and_real_radius_option(self):
        data = case()
        invoke(data)
        self.assertEqual(data[7].BaseFace.Tag, 7)
        self.assertIs(data[7].MaintainZeroBendRadius, False)
        self.assertEqual(data[5].count(('destroy',)), 1)
        self.assertLess(data[5].index(('feature_commit',)), data[5].index(('destroy',)))

    def test_no_native_access_in_explicit_solid_mode(self):
        class Forbidden:
            def __getattribute__(self, name):
                raise AssertionError('Unexpected native access')
        body = object()
        result, record = sm.convert(Forbidden(), body, {}, float, str, 'solid', nx=Forbidden())
        self.assertIs(result, body)
        self.assertFalse(record['sheetmetal_verified'])

    def test_entrypoint_matches_new_adapter_patch(self):
        source = (Path(__file__).resolve().parents[1] / 'NX_CNC_Gesamtansicht.py').read_text()
        self.assertIn("!= '07.2'", source)
        # The sheet adapter stays 07.2; the formula patch uses its own 07.3 output.
        self.assertIn("'SX35Z_'+model.VERSION", source)  # output follows model revision; API patch remains07.2


if __name__ == '__main__':
    unittest.main()
