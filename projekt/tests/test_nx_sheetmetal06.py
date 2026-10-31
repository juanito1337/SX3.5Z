"""API adapter contract tests; fake objects are NOT NX execution."""
import importlib.util,unittest
from types import SimpleNamespace as NS
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'nx_sheetmetal06.py'

def module():
 if not P.exists():return None
 s=importlib.util.spec_from_file_location('nx_sheetmetal06',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class AdapterTests(unittest.TestCase):
 def test_supported_modes_reject_unknown(self):
  m=module();self.assertIsNotNone(m,'new native sheetmetal adapter missing')
  for x in ['auto','fallback',True,None]:
   with self.assertRaises(ValueError):m.validate_options({'mode':x})
 def test_select_base_plane_unambiguous(self):
  m=module();self.assertIsNotNone(m)
  a=NS(Tag=1);b=NS(Tag=2);body=NS(GetFaces=lambda:[a,b])
  uf=NS(AskFaceData=lambda t:(22,[0,0 if t==1 else 2,0],[0,1,0],[0,0,0,10,0,10],0,0,1))
  self.assertIs(m.select_base_face(body,uf,1,0),a)
 def test_no_select_by_first_face(self):
  m=module();self.assertIsNotNone(m)
  body=NS(GetFaces=lambda:[NS(Tag=1),NS(Tag=2)])
  uf=NS(AskFaceData=lambda t:(22,[0,0,0],[0,1,0],[0,0,0,10,0,10],0,0,1))
  with self.assertRaises(RuntimeError):m.select_base_face(body,uf,1,0)
 def test_solid_mode_explicit_not_a_sheetmetal_success(self):
  m=module();self.assertIsNotNone(m)
  target=object();r,record=m.convert(None,target,{},lambda x:0,lambda x:x,'solid',nx=None)
  self.assertIs(r,target);self.assertEqual(record['status'],'SOLID_PRECURSOR_ONLY');self.assertFalse(record['sheetmetal_verified'])
 def test_missing_api_fails_required(self):
  m=module();self.assertIsNotNone(m)
  with self.assertRaises(RuntimeError):m.convert(NS(Features=NS()),object(),{},lambda x:0,lambda x:x,'required',nx=NS())

class ConvertContractTests(unittest.TestCase):
 def fixture(self,thickness=2.,is_sheet=True):
  body=NS(GetFaces=lambda:[NS(Tag=1)])
  uf=NS(AskFaceData=lambda t:(22,[0,0,0],[0,1,0],[0,0,0,10,0,10],0,0,1))
  feature=NS(SetName=lambda x:None,GetBodies=lambda:[body])
  b=NS(CommitFeature=lambda:feature,Destroy=lambda:None)
  mgr=NS(CreateConvertToSheetmetalFeatureBuilder=lambda null:b,IsSheetmetalBody=lambda x:is_sheet,GetBodyThickness=lambda x:thickness)
  calls=[]
  pref=NS(SetThickness=lambda *v:calls.append(('t',v)),SetBendRadius=lambda *v:calls.append(('r',v)),SetNeutralFactor=lambda *v:calls.append(('k',v)),Commit=lambda:None)
  part=NS(Features=NS(SheetmetalManager=mgr),Preferences=NS(PartSheetmetal=pref))
  nx=NS(Features=NS(Feature=NS(Null=None)),UF=NS(UFSession=NS(GetUFSession=lambda:NS(Modl=uf))))
  meta={'plane_axis':1,'plane_coordinate':'0','thickness':'2','bend_radius':'3','neutral_factor':'.4'}
  return part,body,meta,nx,calls
 def test_native_success_requires_type_and_thickness(self):
  m=module();p,b,d,n,c=self.fixture();result,r=m.convert(p,b,d,float,str,'required',nx=n)
  self.assertTrue(r['sheetmetal_verified']);self.assertEqual(len(c),3);self.assertFalse(r['flat_pattern_generated'])
 def test_wrong_thickness_is_not_success(self):
  m=module();p,b,d,n,c=self.fixture(thickness=3.)
  with self.assertRaises(RuntimeError):m.convert(p,b,d,float,str,'required',nx=n)
 def test_non_sheet_result_is_not_success(self):
  m=module();p,b,d,n,c=self.fixture(is_sheet=False)
  with self.assertRaises(RuntimeError):m.convert(p,b,d,float,str,'required',nx=n)
 def test_license_exception_is_not_swallowed(self):
  m=module();p,b,d,n,c=self.fixture()
  def failure(*args):raise RuntimeError('Missing license')
  p.Features.SheetmetalManager.CreateConvertToSheetmetalFeatureBuilder=failure
  with self.assertRaisesRegex(RuntimeError,'Missing license'):m.convert(p,b,d,float,str,'required',nx=n)
 def test_nonfinite_normal_cannot_be_matched(self):
  m=module();body=NS(GetFaces=lambda:[NS(Tag=1)])
  uf=NS(AskFaceData=lambda t:(22,[0,0,0],[0,float('nan'),0],[0,0,0,10,0,10],0,0,1))
  with self.assertRaises(RuntimeError):m.select_base_face(body,uf,1,0)
