# -*- coding: utf-8 -*-
"""SX3.5Z integrated CNC view -- create parts, 20 subassemblies and a root .prt.
Not a final CNC conversion: layout study with explicit unverified adapters.
Run with Siemens NX > Journal > Play. No external Python packages required.
Always writes a new timestamped directory; existing parts remain unmodified.
The STEP files are not read by this script.
"""
import os, sys, json, re, traceback, importlib.util
from uuid import uuid4
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__))
if HERE in sys.path:sys.path.remove(HERE)
sys.path.insert(0,HERE)
# NX retains modules between journal runs: explicitly reload this package only.
for _n in ('cnc_ansichtsmodell','teller10','normteile09','cnc_ansichtsmodell08','umbau_daten09','cnc_ansichtsmodell07','umbau_daten08','cnc_ansichtsmodell01','modell_v4','v3_geometriebasis','nx_native','nx_files','nx_geometry','enclosure_checks03','blech06','nx_sheetmetal06','formeln07','ruecklauf07','nx_formeln073'):
    if _n in sys.modules:del sys.modules[_n]
import cnc_ansichtsmodell as model
import nx_sheetmetal06
with open(os.path.join(HERE,"Blech_Optionen.json"),encoding="utf-8-sig") as _stream:
    SHEETMETAL_MODE=nx_sheetmetal06.validate_options(json.load(_stream))
import NXOpen, NXOpen.Features, NXOpen.Assemblies
from nx_native import (NativeModelBuilder, ExpressionFactory, RunLog,
                       log_environment, require_millimeter_part, JOURNAL_VERSION, FORMULA_PATCH_VERSION)
from nx_files import NativePartFiles, FILES_VERSION, prepare_output_directory
from nx_geometry import ReferenceCheck, GEOMETRY_VERSION


_metadata_warnings=[]
def attr(obj,key,value):
    # Provenance metadata is optional. Geometry/file/assembly errors remain fatal.
    try:obj.SetUserAttribute(key,-1,str(value),NXOpen.Update.Option.Now)
    except Exception as exc:_metadata_warnings.append('%s: %s'%(key,exc))

def ident():
    m=NXOpen.Matrix3x3()
    m.Xx=1.;m.Xy=0.;m.Xz=0.;m.Yx=0.;m.Yy=1.;m.Yz=0.;m.Zx=0.;m.Zy=0.;m.Zz=1.
    return m

def newpart(session,name,log=None):
    # NewDisplay explicitly requires Part.Units (NOT BasePart.Units).
    part=session.Parts.NewDisplay(name,NXOpen.Part.Units.Millimeters)
    # PartUnits, in contrast, returns BasePart.Units. Check every new part,
    # including assembly containers, before creating any features.
    require_millimeter_part(part,log)
    part.WCS.SetOriginAndMatrix(NXOpen.Point3d(0.0,0.0,0.0),ident())
    if not part.Preferences.Modeling.GetHistoryMode():
        raise RuntimeError('NX muss im History-Modus arbeiten. Kein historienfreier Aufbau.')
    return part

def add_component(parent,filename,name,xyz,layer=1):
    result=parent.ComponentAssembly.AddComponent(filename,'Entire Part',name,
                        NXOpen.Point3d(*[float(x) for x in xyz]),ident(),int(layer))
    if isinstance(result,tuple):
        component=result[0]
        for item in result[1:]:
            if hasattr(item,'NumberUnloadedParts') and item.NumberUnloadedParts:
                messages=[]
                for i in range(item.NumberUnloadedParts):
                    try:messages.append(item.GetStatusDescription(i))
                    except Exception:pass
                item.Dispose()
                raise RuntimeError('Komponente nicht voll geladen: '+str(messages))
            if hasattr(item,'Dispose'):item.Dispose()
    else:component=result
    if component is None:raise RuntimeError('AddComponent lieferte keine Komponente: '+name)
    return component

class PartBuilder(NativeModelBuilder):
    def __init__(self,session,part,parameters,definition,log,reference=None):
        super().__init__(session,part,parameters,log)
        self.definition=model.local_definition(definition)
        self.source_definition=definition
        self.reference=reference
        self.needed=model.used_parameters(self.definition)
        self.sheetmetal_result=None
        if 'sheetmetal' in definition:self.needed.update({'sheet_t','bend_r','bend_k'})
        self.known=set(parameters)|set(model.DERIVED)
    def create_expressions(self):
        super().create_expressions(needed=self.needed)
    def build_one(self,mode=None):
        # Mode was tested in a separate API part. Unit objects are resolved
        # freshly from this actual part for every expression creation.
        if mode is None:
            self.expression_factory.select()
        else:
            require_millimeter_part(self.part)
            self.expression_factory.mode=mode
            self.expression_factory.unit=None
        self.create_expressions();target=None
        for i,op in enumerate(self.definition['ops'],1):
            self.current_feature='%03d_%s'%(i,op['label'])
            _,target=self.primitive(op,target,self.current_feature)
            if self.reference is not None:self.reference.check(self.definition['id'],i,self.last_measurement)
        if 'sheetmetal' in self.source_definition:
            self.current_feature='K06_Native_Blechkonvertierung'
            target,self.sheetmetal_result=nx_sheetmetal06.convert(self.part,target,
                self.source_definition['sheetmetal'],lambda x:model.evaluate(x,self.values),
                self.expr_text,SHEETMETAL_MODE,self.log)
            self.last_measurement=self.inspector.measure(target)
            if self.sheetmetal_result['sheetmetal_verified']:self.feature_count+=1
        # All primitives exist before optional provenance metadata is attached.
        self.verify_expression_values()
        self.write_expression_metadata()
        self.style(target,self.source_definition)
        for key,value in {'SX_VERSION':model.VERSION,'SX_JOURNAL_VERSION':JOURNAL_VERSION,'SX_PART_ID':self.definition['id'],'SX_TEILNAME':self.definition['name'],'SX_ARTIKEL_ID':self.source_definition.get('item_id',''),'SX_BESCHAFFUNGSART':self.source_definition.get('supply_kind',''),'SX_KAUFINSTANZ':self.source_definition.get('purchase_instance',''),
                          'SX_GRUPPE':self.definition['group'],'SX_QUELLE':self.definition['source'],
                          'SX_STATUS':self.definition['status'],'SX_GRENZEN':self.definition['note'],
                          'SX_DATUM_FORMEL':json.dumps(self.definition['datum']),
                          'SX_EINHEIT':'mm','SX_NX_TEST':'Lokaler Lauf erforderlich; keine Fertigungsfreigabe'}.items():attr(self.part,key,value)
        # Explicit MODEL reference set avoids exposing construction objects on import.
        try:
            rs=self.part.CreateReferenceSet();rs.SetName('MODEL');rs.AddObjectsToReferenceSet([target])
        except Exception as exc:self.log('Optionales MODEL-Referenzset nicht erzeugt: '+str(exc))
        return target

def probe(session,params,log,out,files):
    """Actual runtime test on user's NX, including file save + component insertion.
    The numeric part shape is checked via the existing associative probe.
    Files are retained in _API_Test for diagnostics and are NOT in final assembly.
    """
    os.makedirs(out,exist_ok=True)
    path=files.filename(out,'API_Testteil')
    p=files.create(path,lambda target:newpart(session,target,log))
    b=NativeModelBuilder(session,p,params,log)
    try:
        log('API-Testphase 1: API-Auswahl mit Punktprobe UND allen Modell-Ausdruecken')
        b.expression_factory.select(validate_model=b.create_expressions)
        log('API-Testphase 2: Alle Modell-Ausdruecke nach Test-Ruecknahme erneut erzeugen')
        b.create_expressions()
        log('API-Testphase 3: Native Featuretypen und Parameteraktualisierung')
        b.native_probe()
    except Exception:
        log('API-Testteil: '+str(getattr(p,'Name','unbekannt')))
        log('API-Testfeature: '+str(b.current_feature))
        b.feature_diagnostics()
        b.expression_factory.diagnostics()
        raise
    log('API-Testphase 4: Speichern und Einfuegen einer Testkomponente')
    # Build and save a small native solid so the actual assembly API is tested too.
    op=dict(kind='box',op='add',origin=['0','0','0'],size=['10','10','10'])
    b.primitive(op,None,'API_Testwuerfel')
    # Actual local NX test for the new sqrt expression in a sloped sheet precursor.
    b.current_feature='API_Schraegblech07_Normaldicke'
    op=dict(kind='prism',op='add',origin=['200','0','0'],
            points=[['200','0','0'],['210','0','1.4'],['210','20','1.4'],['200','20','0']],
            height='sheet_t*sqrt(1+0.14*0.14)',direction=(0,0,1))
    b.primitive(op,None,b.current_feature)
    # 07.3: reproduce the actual FOUR parameter-dependent funnel formulas
    # before starting hundreds of machine parts. The former constant-grade
    # coupon did not exercise a dimensioned parameter inside sqrt.
    funnel_rows=[]
    try:
        funnels=[d for d in model.recipe() if d['name'].startswith('KSS_Trichter_')]
        if len(funnels)!=4:
            raise RuntimeError('KSS_Formelprobe073 erwartet genau vier Trichterbleche.')
        for definition in funnels:
            for op in model.local_definition(definition)['ops']:
                b.current_feature='KSS_Formelprobe073_'+definition['name']
                b.primitive(op,None,b.current_feature)
                funnel_rows.append(dict(part=definition['name'],
                    formula=b.last_normal_thickness_formula, measured=b.last_measurement))
    except Exception:
        log('KSS-Formelvortest fehlgeschlagen: '+str(b.current_feature))
        b.feature_diagnostics()
        b.expression_factory.diagnostics()
        raise
    errors=session.UpdateManager.DoUpdate(session.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible,'API update'))
    if errors:raise RuntimeError('API-Test Updatefehler: '+str(errors))
    b.verify_expression_values()
    with open(os.path.join(out,'NX_KSS_Formelprobe_073.json'),'w',encoding='utf8') as f:
        json.dump(dict(patch=FORMULA_PATCH_VERSION,scope='Vier lokale Trichter-Vorformen; keine Fertigungsfreigabe',
                       parts=funnel_rows),f,indent=2)
    log('KSS-Formelvortest 07.3 bestanden: 4 echte Trichterrezepte; Lage und Volumen geprueft.')
    # The last cube tests expression creation after native_probe's rollback.
    # Optional attributes are not interleaved with geometric operations.
    b.write_expression_metadata()
    for warning in b.warnings[:10]:log('Metadatenhinweis: '+warning)
    files.save(p,path)
    assembly_path=files.filename(out,'API_Testbaugruppe')
    a=files.create(assembly_path,lambda target:newpart(session,target,log))
    c=add_component(a,path,'API_Testkomponente',(13,0,0))
    result=c.GetPosition()
    if not isinstance(result,tuple) or abs(result[0].X-13)>1e-6:raise RuntimeError('AddComponent/GetPosition API-Test nicht bestanden')
    files.save(a,assembly_path)
    log('API-Vortest bestanden: Ausdruecke, Parameteraenderung, Features, Save und AddComponent.')
    return b.expression_factory.mode

def main(probe_only=False,parts_only=False,part_filter=None,paths_only=False):
    session=NXOpen.Session.GetSession();log=RunLog(session)
    current=None;builder=None;out=None;mark=None;files=None
    try:
        log('SX3.5Z CNC-GESAMTANSICHT -- gesamte Maschine, XYZ-Antriebe und Baugruppen in einem Lauf.')
        log('UMSETZUNGSSTAND10: Teller-/Spannpaket-Entwurf; Maschinen-Aufmass und Lieferrevisionen offen. KEINE FERTIGUNGS-/BESTELLFREIGABE.')
        log_environment(log)
        log('Geometriestand: '+model.VERSION+'; Untergestell/Einhausung/Schaltschrank als ENTWURF.')
        log('Startjournal: '+os.path.abspath(__file__))
        log('KSS-Formelpatch: '+str(FORMULA_PATCH_VERSION))
        if FORMULA_PATCH_VERSION != '07.3':
            raise RuntimeError('Gemischter Formelpatch: Startjournal, nx_native.py und nx_formeln073.py aus 07.3 gemeinsam verwenden.')
        log('Blechadapter-Patch: '+str(getattr(nx_sheetmetal06,'ADAPTER_VERSION','nicht vorhanden')))
        log('Blechadapterdatei: '+str(getattr(nx_sheetmetal06,'__file__','unbekannt')))
        if getattr(nx_sheetmetal06,'ADAPTER_VERSION',None) != '07.2':
            raise RuntimeError('Gemischter Blechpatch: NX_CNC_Gesamtansicht.py und nx_sheetmetal06.py aus 07.2 gemeinsam verwenden.')
        if JOURNAL_VERSION != '4.8' or FILES_VERSION != '4.8' or GEOMETRY_VERSION != '4.6' or model.VERSION != 'CNC_UMSETZUNG_10_TELLER':
            raise RuntimeError('Gemischte Journalversionen. Alle Patchdateien im selben Ordner ablegen.')
        params=model.load_parameters(os.path.join(HERE,'Parameter.json'));values=model.check_recipe(params)
        stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        run_id=uuid4().hex[:12]
        out=prepare_output_directory(HERE,'SX35Z_'+model.VERSION+'_'+stamp+'_'+run_id,log)
        log.set_output_directory(out)
        if paths_only:
            log('Nur Pfadtest: keine NX-Testteile oder Maschinenbauteile erzeugt.')
            log.save();return
        files=NativePartFiles(session,out,run_id,log)
        log('Dateiverwaltung: '+os.path.join(HERE,'nx_files.py'))
        log('Geometriepruefung: '+os.path.join(HERE,'nx_geometry.py')+' / '+GEOMETRY_VERSION)
        log('Laufkennung fuer ALLE Dateinamen: '+run_id)
        log('Speicherweg: NewDisplay am endgueltigen Pfad, dann Save; kein SaveAs.')
        reference=ReferenceCheck(os.path.join(HERE,'Geometrie_Referenz_Ansicht.json'),params,model.recipe(),log)
        with open(os.path.join(out,'Parameter_beim_Aufbau.json'),'w',encoding='utf8') as f:json.dump(params,f,indent=2)
        with open(os.path.join(out,'Spaene_KSS_Entwurfsdaten.json'),'w',encoding='utf8') as f:json.dump(model.drain_report(params),f,indent=2,ensure_ascii=False)
        with open(os.path.join(out,'ATC_Schnittstellenstatus09.json'),'w',encoding='utf8') as stream:
            json.dump(model.atc_report(params),stream,indent=2,ensure_ascii=False)
        log('ATC-OPTION: SK30-Bestand unveraendert. Keine automatische Spann-/Loeseeinrichtung; kein M6-Betrieb freigegeben.')
        mode=probe(session,params,log,os.path.join(out,'_API_Test'),files)
        if probe_only:log.save();return
        definitions=model.recipe()
        with open(os.path.join(out,'Rezept_beim_Aufbau.json'),'w',encoding='utf8') as stream:
            json.dump(definitions,stream,sort_keys=True,separators=(',',':'))
        # Verify the new licensing/API path before building all machine parts.
        if not part_filter and SHEETMETAL_MODE=='required':
            coupon=dict(name='K06_Blechprobe',group='15_Einhausung',material='sheet',datum=['0','0','0'],ops=[],id='BLECHPROBE',filename='BLECHPROBE',source='K06',status='TEST',note='Native Blechprobe, keine Maschine')
            from blech06 import u_profile
            u_profile(coupon,(0,0,0),80,30,50)
            testpath=files.filename(os.path.join(out,'_API_Test'),'Blechprobe')
            testpart=files.create(testpath,lambda path:newpart(session,path,log))
            builder=PartBuilder(session,testpart,params,coupon,log)
            current='Blech_Vortest'
            builder.build_one(mode);files.save(testpart,testpath)
            current=None;builder=None
            log('Blech-Vortest bestanden; native Blechkoerpererkennung und Dicke geprueft.')
        if part_filter:definitions=[d for d in definitions if d['id'] in part_filter or d['name'] in part_filter]
        if not definitions:raise ValueError('Keine Teile im Filter')
        partsdir=os.path.join(out,'Teile');groupsdir=os.path.join(out,'Unterbaugruppen')
        os.makedirs(partsdir);os.makedirs(groupsdir)
        manifest=[]
        import umbau_daten09
        with open(os.path.join(out,'Einkauf_Modellbindung09.json'),'w',encoding='utf8') as stream:
            json.dump({'catalog':umbau_daten09.catalog(HERE),'bom':umbau_daten09.bom_rows(definitions,HERE),'mapping':umbau_daten09.model_map(definitions),'release':umbau_daten09.release_report(HERE)},stream,indent=2,ensure_ascii=False)
        for index,d in enumerate(definitions,1):
            current=d['filename'];log('[%03d/%03d] %s'%(index,len(definitions),current))
            path=files.filename(partsdir,d['filename'])
            p=files.create(path,lambda target:newpart(session,target,log))
            mark=session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible,'V4 '+d['name'])
            builder=PartBuilder(session,p,params,d,log,reference);body=builder.build_one(mode)
            errors=session.UpdateManager.DoUpdate(mark)
            if errors:raise RuntimeError('NX Update meldet %d Fehler'%errors)
            if len(list(p.Bodies))!=1:raise RuntimeError('Einzelteil enthaelt nicht genau einen Koerper: '+current)
            try:p.ModelingViews.WorkView.Orient(NXOpen.View.Canned.Isometric,NXOpen.View.ScaleAdjustment.Fit)
            except Exception:pass
            files.save(p,path)
            with open(path+'.geometrie.json','w',encoding='utf8') as f:json.dump(builder.geometry_trace,f,indent=2)
            item=dict(id=d['id'],name=d['name'],file=os.path.relpath(path,out),group=d['group'],datum=[model.evaluate(x,values) for x in d['datum']],datum_formula=d['datum'],native_feature_count=builder.feature_count,expression_mode=mode,journal_version=JOURNAL_VERSION)
            item['sheetmetal']=builder.sheetmetal_result
            item.update(item_id=d.get('item_id'),supply_kind=d.get('supply_kind'),purchase_instance=d.get('purchase_instance'),source=d.get('source'),release=False)
            manifest.append(item)
            with open(os.path.join(out,'Erzeugte_Teile.json'),'w',encoding='utf8') as f:json.dump(manifest,f,indent=2)
            for w in builder.warnings[:2]:log('Darstellungshinweis: '+w)
            # Do not close all parts or modify existing user documents.
            mark=None
        if not parts_only:
            subpaths=[]
            for group in model.GROUPS:
                members=[m for m in manifest if m['group']==group]
                if not members:continue
                current=group
                path=files.filename(groupsdir,group)
                p=files.create(path,lambda target:newpart(session,target,log))
                for m in members:
                    c=add_component(p,os.path.join(out,m['file']),m['id']+'_'+m['name'],m['datum'],model.LAYERS[group])
                    attr(c,'SX_PART_ID',m['id']);attr(c,'SX_ARTIKEL_ID',m.get('item_id',''));attr(c,'SX_BESCHAFFUNGSART',m.get('supply_kind',''));attr(c,'SX_PLATZIERUNG','Parameter.json; explizite Lage, keine Montagezwangsbedingungen')
                attr(p,'SX_VERSION',model.VERSION);attr(p,'SX_JOURNAL_VERSION',JOURNAL_VERSION);attr(p,'SX_BAUGRUPPE',model.GROUPS[group])
                files.save(p,path);subpaths.append((group,path))
                log('Unterbaugruppe gespeichert: '+group)
            current='FRAESMASCHINE_CNC_TELLER_SPANNPAKET_10_NICHT_FREIGEGEBEN'
            rootpath=files.filename(out,current)
            root=files.create(rootpath,lambda target:newpart(session,target,log))
            for g,path in subpaths:add_component(root,path,g,(0,0,0))
            attr(root,'CNC_ANSICHTSTATUS','ANSCHAUUNG; Anschlussgeometrie, Verfahrwege, Kaufteilauswahl nicht freigegeben')
            attr(root,'SX_VERSION',model.VERSION);attr(root,'SX_JOURNAL_VERSION',JOURNAL_VERSION);attr(root,'SX_MODELLTYP','Native Dateibaugruppe; parametrisierte Einzelteile, explizite Einbaupositionen')
            attr(root,'SX_GRENZEN','Zusammengebaute CNC-Ansicht mit ENTWURFSANSCHLUESSEN. Keine Montagezwangsbedingungen, keine freigegebenen Kollisionen oder Fertigungsmasse.')
            for n in ['pos_x','pos_y','head_down','quill_down']:attr(root,'SX_STELLUNG_'+n,params[n])
            try:root.ModelingViews.WorkView.Orient(NXOpen.View.Canned.Isometric,NXOpen.View.ScaleAdjustment.Fit)
            except Exception:pass
            files.save(root,rootpath)
            with open(os.path.join(out,'HAUPTBAUGRUPPE.txt'),'w',encoding='utf8') as f:
                f.write(os.path.basename(rootpath)+'\n')
            log('HAUPTBAUGRUPPE: '+rootpath)
        with open(os.path.join(out,'Parameter_beim_Aufbau.json'),'w',encoding='utf8') as f:json.dump(params,f,indent=2)
        if _metadata_warnings:log('Optionale Metadatenwarnungen: %d; Geometrie dadurch nicht uebersprungen.'%len(_metadata_warnings))
        with open(os.path.join(out,'Blech_Nachweis.json'),'w',encoding='utf8') as stream:
            json.dump(dict(adapter_version=nx_sheetmetal06.ADAPTER_VERSION,mode=SHEETMETAL_MODE,parts=[m for m in manifest if m.get('sheetmetal')],manufacturing_released=False),stream,indent=2)
        log('FERTIG: %d native Einzelteile. Ihre bereits offenen Dateien wurden nicht bearbeitet.'%len(manifest))
        log('Formaenderungen lokal: Ausdruecke sx_. Maschinenstellung: Parameter.json; CNC-Baugruppen: CNC_Parameter.json; Ausbau: Ausbau_Parameter.json. Gesamtansicht neu aufbauen.')
        log('Ausgabeordner komplett zusammenhalten: Teile + Unterbaugruppen + Hauptbaugruppe.')
        log.save()
    except Exception:
        log(traceback.format_exc());log('Betroffenes Teil: '+str(current))
        if builder is not None:
            if out:
                try:
                    with open(os.path.join(out,'NX_Geometriediagnose.json'),'w',encoding='utf8') as f:
                        json.dump(dict(part=current,parameters=params,completed=builder.geometry_trace,
                                       failed=builder.last_geometry_context),f,indent=2)
                except Exception as e:log('Geometriediagnose nicht geschrieben: '+str(e))
            log('Betroffenes Feature: '+str(builder.current_feature))
            try:
                builder.feature_diagnostics()
                builder.expression_factory.diagnostics()
            except Exception:pass
        if mark is not None:
            try:session.UndoToMark(mark,None)
            except Exception as e:log('Ruecknahme fehlgeschlagen: '+str(e))
        if out:
            if current is None:
                log('Abbruch im Vortest; in diesem Lauf wurden noch keine Maschinen-Einzelteile aufgebaut.')
            log('Ausgabeordner dieses Laufs (ggf. unvollstaendig): '+out)
        log.save(failed=True)
        try:NXOpen.UI.GetUI().NXMessageBox.Show('SX35Z CNC-Umbau 09',NXOpen.NXMessageBox.DialogType.Error,'Abbruch. Details im Listing Window und NX_Fehlerprotokoll.txt. Keine fertige Baugruppe behauptet.')
        except Exception:pass
        raise

def getUnloadOption(dummy):return NXOpen.Session.LibraryUnloadOption.Immediately
if __name__=='__main__':main()
