# -*- coding: utf-8 -*-
"""Native NXOpen feature adapter, reused & extended from v3 diagnostics.
No STEP import and no faceted bodies. Must run in NX Python.
"""
import os,sys,re,traceback,math
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__))
if HERE in sys.path:sys.path.remove(HERE)
sys.path.insert(0,HERE)
import cnc_ansichtsmodell as model
import nx_formeln073
FORMULA_PATCH_VERSION = nx_formeln073.VERSION
import NXOpen, NXOpen.Features, NXOpen.GeometricUtilities, NXOpen.Assemblies
from nx_geometry import (BodyInspector, primitive_contract, assert_contract,
                         assert_boolean_change)
JOURNAL_VERSION='4.8'
class RunLog:
    """Listing Window plus lokales Laufprotokoll; keine externen Zugriffe."""
    def __init__(self, session):
        self.session = session
        self.lines = []
        self.path = None
        self.output_directory = None
        self.session.ListingWindow.Open()

    def __call__(self, text):
        text = str(text)
        self.lines.append(text)
        self.session.ListingWindow.WriteLine(text)

    def set_output_directory(self, directory):
        """Keep diagnostics with the exact chosen output, not on script drive W:."""
        if not os.path.isabs(directory):
            raise ValueError('Protokollordner muss absolut sein.')
        self.output_directory = os.path.abspath(directory)
        self.path = None

    def save(self, failed=False):
        text = "\n".join(self.lines) + "\n"
        try:
            from nx_files import default_output_root
            # When destination setup failed, diagnostics still go to a local
            # default log folder; this does not relocate .prt output silently.
            directory = self.output_directory or os.path.join(default_output_root(), '_Protokolle')
            os.makedirs(directory, exist_ok=True)
            if self.path is None:
                stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                self.path = os.path.join(directory, 'NX_Laufprotokoll_' + stamp + '.txt')
            with open(self.path, 'w', encoding='utf-8') as stream:
                stream.write(text)
            if failed:
                with open(os.path.join(directory, 'NX_Fehlerprotokoll.txt'), 'w', encoding='utf-8') as stream:
                    stream.write(text)
            self.session.ListingWindow.WriteLine('Protokoll: ' + self.path)
        except Exception as exc:
            self.session.ListingWindow.WriteLine('Lokales Protokoll nicht geschrieben; Listing Window bleibt erhalten: ' + str(exc))
        if failed:
            # Convenience copy at the familiar location; failure must neither
            # hide the original error nor invalidate an already saved local log.
            try:
                with open(os.path.join(HERE, 'NX_Fehlerprotokoll.txt'), 'w', encoding='utf-8') as stream:
                    stream.write(text)
            except Exception as exc:
                self.session.ListingWindow.WriteLine('Optionale Protokollkopie im Journalordner nicht geschrieben: ' + str(exc))


def log_environment(log):
    log("Journal-Version: " + JOURNAL_VERSION)
    log("Python: " + sys.version.replace("\n", " "))
    log("NXOpen-Modul: " + str(getattr(NXOpen, "__file__", "nicht ausgewiesen")))
    for name in ("UGII_VERSION", "UGII_FULL_VERSION"):
        value = os.environ.get(name)
        if value:
            log(name + ": " + value)
    log("Adapterdatei: " + os.path.abspath(__file__))
    log("Geometriedatei: " + os.path.abspath(model.__file__))
    log("Geometriestand: " + str(model.VERSION) + "; Journal-Patch: " + JOURNAL_VERSION)


def require_millimeter_part(part, log=None):
    """Validate part units without changing or rescaling the part.

    IMPORTANT: NewDisplay takes NXOpen.Part.Units, whereas PartUnits returns
    NXOpen.BasePart.Units. These are separate enum types. Do not compare one
    against the other and do not replace them by hard-coded integer values.

    The named BasePart enum is authoritative. Where the binding provides it,
    the conversion of one native length unit to mm is checked independently.
    Failure to read the enum, an unknown enum or a contradictory conversion
    stops the build; there is no implicit conversion of inch parts.
    """
    emit = log if log is not None else (lambda text: None)
    try:
        actual = part.PartUnits
        expected = NXOpen.BasePart.Units.Millimeters
        inches = NXOpen.BasePart.Units.Inches
    except Exception as exc:
        raise RuntimeError("NX-Teileinheit nicht sicher lesbar (BasePart.Units): "
                           + str(exc)) from exc
    actual_type = type(actual)
    expected_type = type(expected)
    emit("Einheitenpruefung: PartUnits=%r; Typ=%s.%s" %
         (actual, actual_type.__module__, actual_type.__name__))
    emit("Erwartet: NXOpen.BasePart.Units.Millimeters=%r; Typ=%s.%s" %
         (expected, expected_type.__module__, expected_type.__name__))
    if actual == inches:
        raise RuntimeError("Zollteil erkannt. Der SX35Z-Aufbau verlangt ein "
                           "Millimeterteil. Keine automatische Umrechnung.")
    if actual != expected:
        raise RuntimeError("Millimeterteil nicht bestaetigt: PartUnits=%r, "
                           "erwartet BasePart.Units.Millimeters=%r. "
                           "Keine Geometrie erzeugt." % (actual, expected))

    # Additional independent diagnostic: do not require guessed enum numbers,
    # locale-dependent text or undocumented Unit-object members.
    try:
        units = part.UnitCollection
        base = units.GetBase("Length")
        mm = units.FindObject("MilliMeter")
        factor = float(units.Convert(base, mm, 1.0))
    except Exception as exc:
        # The documented enum already identifies the part units correctly.
        # Older bindings may not provide this optional second check.
        emit("Zusatzpruefung Laengeneinheit nicht verfuegbar: %s: %s" %
             (type(exc).__name__, exc))
        emit("Einheitenpruefung OK: Millimeter per BasePart.Units bestaetigt.")
        return
    emit("Laengenpruefung: 1 native Laengeneinheit = %.12g mm" % factor)
    if not math.isfinite(factor) or abs(factor - 1.0) > 1.0e-9:
        raise RuntimeError("Widerspruechliche Laengeneinheit: Enum meldet mm, "
                           "aber 1 native Einheit entspricht %r mm. "
                           "Abbruch ohne Umrechnung." % factor)
    emit("Einheitenpruefung OK: Millimeter per BasePart.Units und Umrechnung bestaetigt.")


class ExpressionFactory:
    """Select one tested expression API for a complete new mm part.

    Four-argument overloads are documented by the user's NX2406 runtime.
    Unit objects are resolved from THIS part for EVERY creation; they are
    never trusted across undo, updates, metadata operations or part changes.
    All model expressions must pass the optional validation callback before
    a mode is selected. There is no per-expression fallback during a build.
    """
    def __init__(self, session, part, log):
        self.session = session
        self.part = part
        self.log = log
        self.unit = None
        self.mode = None
        self.last_equation = None
        self.attempts = []
        self.created_calls = 0  # Includes test expressions that were undone.
        self.last_unit_tag = None

    def _fresh_length_unit(self):
        errors = []
        for method, argument in (("GetBase", "Length"), ("FindObject", "MilliMeter")):
            try:
                unit = getattr(self.part.UnitCollection, method)(argument)
                if unit is None:
                    raise RuntimeError("Kein Unit-Objekt geliefert")
                # Store for diagnostics only, never reuse it in another call.
                self.unit = unit
                self.last_unit_tag = getattr(unit, "Tag", None)
                return unit
            except Exception as exc:
                errors.append("%s: %s: %s" % (method, type(exc).__name__, exc))
        self.unit = None
        self.last_unit_tag = None
        raise RuntimeError("Laengeneinheit fuer dieses Teil nicht verfuegbar: "
                           + "; ".join(errors))

    @staticmethod
    def _split_equation(equation):
        if not isinstance(equation, str):
            raise TypeError("NX-Gleichung muss Text bleiben, kein int oder Tag.")
        name, separator, formula = equation.partition("=")
        name, formula = name.strip(), formula.strip()
        if not separator or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) or not formula:
            raise ValueError("Ungueltige benannte Gleichung: " + repr(equation))
        return name, formula

    def _make(self, mode, equation):
        name, formula = self._split_equation(equation)
        self.last_equation = equation
        if mode == "Number_mm":
            self.unit = None
            self.last_unit_tag = None
            result = self.part.Expressions.CreateExpression("Number", equation)
        else:
            # NX2406 exposes both (equation, Unit) and
            # (name, formula, isUserLocked, Unit). Do not pass a Unit.Tag.
            unit = self._fresh_length_unit()
            if mode == "CreateNumberExpression4":
                result = self.part.Expressions.CreateNumberExpression(name, formula, False, unit)
            elif mode == "CreateNumberExpression":
                result = self.part.Expressions.CreateNumberExpression(equation, unit)
            elif mode == "CreateWithUnits4":
                result = self.part.Expressions.CreateWithUnits(name, formula, False, unit)
            elif mode == "CreateWithUnits":
                result = self.part.Expressions.CreateWithUnits(equation, unit)
            else:
                raise RuntimeError("Unbekannter Ausdrucksmodus: " + str(mode))
        if result is None:
            raise RuntimeError("NX lieferte keinen Ausdruck: " + equation)
        self.created_calls += 1
        return result

    @staticmethod
    def _close(actual, expected, description):
        actual, expected = float(actual), float(expected)
        tolerance = max(1.0e-7, abs(expected)*1.0e-10)
        if not math.isfinite(actual) or not math.isfinite(expected) or abs(actual-expected) > tolerance:
            raise RuntimeError("API-Vortest " + description + ": %r statt %r" % (actual, expected))

    def _rollback(self, mark):
        # If rollback fails, ABORT instead of trying another mode on dirty data.
        self.session.UndoToMark(mark, None)
        self.unit = None
        self.last_unit_tag = None
        try:
            self.session.DeleteUndoMark(mark, None)
        except Exception as exc:
            self.log("Undo-Markierung konnte nicht entfernt werden: " + str(exc))

    def _record_failure(self, mode, stage, exc):
        detail = "%s / %s: %s: %s" % (mode, stage, type(exc).__name__, exc)
        self.attempts.append(detail)
        self.log("API-Kandidat nicht bestanden: " + detail)
        self.log("Letzte Gleichung: " + repr(self.last_equation))
        code = getattr(exc, "ErrorCode", None)
        if code is not None:
            self.log("NX-Fehlercode: " + str(code))

    def _probe(self, mode):
        mark = self.session.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible,
                                        "SX35Z Ausdrucks-API pruefen")
        stage = "Ausdruckserzeugung"
        success = False
        try:
            a = self._make(mode, "sxprobe_a = 10.25")
            b = self._make(mode, "sxprobe_b = 2*sxprobe_a+1")
            self._close(a.Value, 10.25, "Zahlenwert")
            self._close(b.Value, 21.5, "abhaengiger Ausdruck")
            stage = "Assoziative Koordinatenskalare und Punkt"
            update = NXOpen.SmartObject.UpdateOption.WithinModeling
            dimensionality = NXOpen.Scalar.DimensionalityType.Length
            sa = self.part.Scalars.CreateScalarExpression(a, dimensionality, update)
            sb = self.part.Scalars.CreateScalarExpression(b, dimensionality, update)
            point = self.part.Points.CreatePoint(sa, sb, sa, update)
            point.Evaluate()
            xyz = point.Coordinates
            self._close(xyz.X, 10.25, "Punkt X")
            self._close(xyz.Y, 21.5, "Punkt Y")
            self._close(xyz.Z, 10.25, "Punkt Z")
            stage = "Aktualisierung nach Parameteraenderung"
            a.RightHandSide = "12.5"
            errors = self.session.UpdateManager.DoUpdate(mark)
            if errors:
                raise RuntimeError("%d Aktualisierungsfehler" % errors)
            point.Evaluate()
            xyz = point.Coordinates
            self._close(a.Value, 12.5, "geaenderter Zahlenwert")
            self._close(b.Value, 26.0, "geaenderter abhaengiger Ausdruck")
            self._close(xyz.X, 12.5, "geaenderter Punkt X")
            self._close(xyz.Y, 26.0, "geaenderter Punkt Y")
            self._close(xyz.Z, 12.5, "geaenderter Punkt Z")
            success = True
        except Exception as exc:
            self._record_failure(mode, stage, exc)
        finally:
            self._rollback(mark)
        return success

    def _probe_complete_model(self, mode, validate_model):
        """Run AFTER the small probe's rollback; roll back the ENTIRE candidate.

        A successful two-expression test is not enough: the supplied log showed
        that actual sx_table_y failed afterward. Validate all original input
        and derived expressions with the same path that the real model uses.
        """
        mark = self.session.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible,
                                        "SX35Z vollstaendiger Ausdruckstest")
        success = False
        self.mode = mode
        try:
            validate_model()
            errors = self.session.UpdateManager.DoUpdate(mark)
            if errors:
                raise RuntimeError("%d Updatefehler im vollstaendigen Ausdruckstest" % errors)
            # One more dependent expression AFTER an update, with a fresh Unit.
            extra = self._make(mode, "sxprobe_after_update = sx_table_x+1")
            base = self.part.Expressions.FindObject("sx_table_x")
            self._close(extra.Value, base.Value+1, "Ausdruck nach Update")
            success = True
        except Exception as exc:
            self._record_failure(mode, "Vollstaendiger Modell-Ausdruckstest", exc)
        finally:
            self._rollback(mark)
            if not success:
                self.mode = None
        return success

    def candidate_modes(self):
        modes = []
        for method in ("CreateNumberExpression", "CreateWithUnits"):
            if callable(getattr(self.part.Expressions, method, None)):
                modes.extend((method+"4", method))
        if callable(getattr(self.part.Expressions, "CreateExpression", None)):
            modes.append("Number_mm")
        return modes

    def select(self, validate_model=None):
        require_millimeter_part(self.part, self.log)
        for mode in self.candidate_modes():
            self.log("Pruefe Ausdrucks-API-Kandidat: " + mode)
            if not self._probe(mode):
                continue
            if validate_model is not None and not self._probe_complete_model(mode, validate_model):
                continue
            self.mode = mode
            self.log("Ausdrucks-API ausgewaehlt: " + mode)
            if validate_model is not None:
                self.log("Vollstaendiger Modell-Ausdruckstest nach Undo bestanden.")
            if mode == "Number_mm":
                self.log("KOMPATIBILITAETSMODUS: SX-Ausdruecke sind einheitenlose Number-Ausdruecke.")
                self.log("Alle SX-Laengenwerte bedeuten mm. Keine automatische Einheitenumrechnung.")
            return
        self.mode = None
        self.diagnostics()
        raise RuntimeError("Kein Ausdrucks-API-Weg bestand die erforderlichen Tests. "
                           "Bitte das neue NX_Fehlerprotokoll.txt bereitstellen.")

    def create(self, equation):
        if self.mode is None:
            raise RuntimeError("Ausdrucks-API wurde noch nicht ausgewaehlt.")
        try:
            return self._make(self.mode, equation)
        except Exception as exc:
            self._record_failure(self.mode, "Erzeugung", exc)
            # Never retry with another unit mode in a partially built part.
            raise

    def diagnostics(self):
        self.log("--- Ausdrucks-API-Diagnose ---")
        self.log("Ausgewaehlter Modus: " + str(self.mode))
        self.log("Letzter Ausdruck: " + str(self.last_equation))
        self.log("Erfolgreiche Create-Aufrufe inkl. zurueckgenommener Tests: " + str(self.created_calls))
        self.log("Expressions-Typ: " + type(self.part.Expressions).__name__)
        self.log("Letzter Unit-Typ: " + type(self.unit).__name__)
        self.log("Letzter Unit-Tag (nur Diagnose): " + repr(self.last_unit_tag))
        for name in ("CreateNumberExpression", "CreateWithUnits", "CreateExpression"):
            method = getattr(self.part.Expressions, name, None)
            doc = getattr(method, "__doc__", None) if method is not None else None
            self.log("%s vorhanden: %s" % (name, method is not None))
            if doc:
                self.log(str(doc)[:8000])


class NativeModelBuilder:
    def __init__(self,session,part,parameters,log=None,mode="gesamt"):
        self.session=session
        self.part=part
        self.mode=mode
        self.parameters=parameters
        self.values=model.all_values(parameters)
        self.runlog=log if log is not None else RunLog(session)
        self.expression_factory=ExpressionFactory(session,part,self.log)
        self.current_feature=None
        self.update=NXOpen.SmartObject.UpdateOption.WithinModeling
        self.scalars={}
        self.known=set(parameters)|set(model.DERIVED)
        self.aux_id=0
        self.feature_count=0
        self.warnings=[]
        self._expression_metadata=[]
        self.expression_names=[]
        self.last_builder_api=None
        self.last_builder_null_type=None
        self.last_primitive=None
        self.inspector=None
        self.geometry_trace=[]
        self.last_measurement=None
        self.last_geometry_context=None

    def log(self,text):
        self.runlog(str(text))

    def attr(self,obj,key,text):
        try:
            obj.SetUserAttribute(key,-1,str(text),NXOpen.Update.Option.Now)
        except Exception as exc:
            self.warnings.append('Attribut '+key+': '+str(exc))

    def expr_text(self,text):
        text=str(text)
        def replace(match):
            name=match.group(0)
            if name == 'sqrt': return 'sqrt'  # NX numeric expression; not a user variable.
            if name not in self.known:
                raise ValueError('Unbekannter Variablenname in Rezept: '+name)
            return 'sx_'+name
        return re.sub(r'\b[A-Za-z_]\w*\b',replace,text)

    def extrusion_height_text(self, rhs):
        """Keep normal-thickness grades unitless without freezing parameters.

        Recipes use millimetre numbers for rises/runs. A length-bearing NX
        parameter under sqrt must therefore be expressed as a number of mm.
        Allocate a fresh 1-mm helper per formula (no stale handles after undo).
        Only the explicitly supported thickness*sqrt(...) form is translated.
        All other extrusion formulas retain the existing code path.
        """
        text = str(rhs)
        if not re.search(r'\bsqrt\s*\(', text):
            return self.expr_text(text)
        unitless = {s['name'] for s in model.SPECS if s.get('unit') == 'unitless'}
        needs_ref = nx_formeln073.needs_length_reference(text, self.known, unitless)
        mode = self.expression_factory.mode
        if mode not in ('CreateNumberExpression', 'CreateNumberExpression4',
                        'CreateWithUnits', 'CreateWithUnits4', 'Number_mm'):
            raise RuntimeError('Normaldickenformel ohne geprueften Ausdrucksmodus.')
        reference = None
        if needs_ref and mode != 'Number_mm':
            self.aux_id += 1
            reference = 'sx_aux_%04d' % self.aux_id
            exp = self.expression_factory.create(reference+' = 1')
            self.expression_factory._close(exp.Value, 1.0, '1-mm-Formelreferenz')
        result = nx_formeln073.normal_thickness_rhs(text, self.known, unitless, reference)
        self.last_normal_thickness_formula = dict(recipe=text, native_rhs=result,
            millimeter_reference=reference, expression_mode=mode)
        self.log('KSS-Normaldickenformel 07.3: '+result)
        if reference:
            self.log('KSS-Laengennormierung: '+reference+' = 1 mm; sqrt-Argument einheitenlos.')
        return result

    def create_expressions(self, needed=None):
        """Geometry first: NO SetUserAttribute between expression creations.

        Optional metadata is stored by NAME only (never by a live NX object)
        and written after the complete solid has been built. This also avoids
        retaining expression handles from rolled-back candidate tests.
        """
        self._expression_metadata=[]
        self.expression_names=[]
        specs=[s for s in model.SPECS if needed is None or s['name'] in needed]
        derived=[(n,r) for n,r in model.DERIVED.items() if needed is None or n in needed]
        total=len(specs)+len(derived)
        self.log('Erzeuge %d Eingabe- und %d abgeleitete Ausdruecke; Attribute erst nach Geometrie.' %
                 (len(specs),len(derived)))
        for index,spec in enumerate(specs,1):
            name=spec['name']
            if index <= 3:
                self.log('  Ausdruck %d/%d: sx_%s' % (index,total,name))
            equation='sx_%s = %.12g'%(name,self.parameters[name])
            # K03 door_open is a ratio. Multiplying two length units would
            # invalidate door_open * door_travel in native NX expressions.
            if spec.get('unit')=='unitless':
                self.expression_factory._make('Number_mm',equation)
            else:
                self.expression_factory.create(equation)
            self.expression_names.append(name)
            self._expression_metadata.append((name,spec))
        for name,rhs in derived:
            self.expression_factory.create('sx_%s = %s'%(name,self.expr_text(rhs)))
            self.expression_names.append(name)
        self.verify_expression_values()
        self.log('Ausdruecke vollstaendig erzeugt und numerisch geprueft: %d/%d.' %
                 (len(self.expression_names),total))

    def verify_expression_values(self):
        for name in self.expression_names:
            exp=self.part.Expressions.FindObject('sx_'+name)
            self.expression_factory._close(exp.Value,self.values[name],'Modellwert sx_'+name)

    def write_expression_metadata(self):
        """Optional provenance AFTER all primitives; no geometry is created here."""
        for name,spec in self._expression_metadata:
            try:
                exp=self.part.Expressions.FindObject('sx_'+name)
                self.attr(exp,'SX_STATUS',spec['status'])
                self.attr(exp,'SX_BESCHREIBUNG',spec['note'])
                self.attr(exp,'SX_QUELLE',spec['source'])
                self.attr(exp,'SX_EINHEIT','einheitenlos (Verhaeltnis)' if spec.get('unit')=='unitless' else
                          ('mm' if self.expression_factory.mode!='Number_mm' else 'Zahlenwert in mm; NX-Ausdruck einheitenlos'))
            except Exception as exc:
                self.warnings.append('Ausdrucksattribute sx_'+name+': '+str(exc))
        self._expression_metadata=[]

    def scalar(self,rhs):
        # Gemeinsame Skalarobjekte erhalten die vollstaendige Expressionskette.
        text=self.expr_text(rhs)
        if text not in self.scalars:
            self.aux_id+=1
            exp=self.expression_factory.create('sx_aux_%04d = %s'%(self.aux_id,text))
            self.scalars[text]=self.part.Scalars.CreateScalarExpression(
                exp,NXOpen.Scalar.DimensionalityType.Length,self.update)
        return self.scalars[text]

    def point(self,origin):
        scalars=[self.scalar(c) for c in origin]
        point=self.part.Points.CreatePoint(scalars[0],scalars[1],scalars[2],self.update)
        # Check every actual NX smart point against the recipe before use.
        point.Evaluate()
        got=point.Coordinates
        expected=[model.evaluate(c,self.values) for c in origin]
        if any(abs(a-b)>1e-6 for a,b in zip((got.X,got.Y,got.Z),expected)):
            raise RuntimeError('Assoziativer Punkt falsch: IST %r SOLL %r' %
                               ((got.X,got.Y,got.Z),expected))
        # Hilfspunkte bleiben erhalten, werden aber nicht angezeigt.
        point.Blank()
        return point

    def boolean(self,builder,target,operation):
        bo=NXOpen.GeometricUtilities.BooleanOperation.BooleanType
        # Primitive verwenden BooleanOption, ExtrudeBuilder BooleanOperation.
        option = (builder.BooleanOperation if isinstance(builder, NXOpen.Features.ExtrudeBuilder)
                  else builder.BooleanOption)
        option.Type=bo.Create if target is None else (bo.Subtract if operation=='cut' else bo.Unite)
        if target is not None: option.SetTargetBodies([target])

    def direction(self, vector):
        return self.part.Directions.CreateDirection(NXOpen.Point3d(0.0,0.0,0.0),
                    NXOpen.Vector3d(*[float(c) for c in vector]), self.update)

    def new_feature_builder(self, collection, method_name, null_object):
        """Create a new native builder with the API's declared null type.

        Cone requires Cone.Null, NOT Feature.Null. Blocks, cylinders and
        extrusions take Feature.Null. Associative lines use their own type.
        Do not substitute None, integer tags or a different primitive on error.
        """
        self.last_builder_api = method_name
        typ = type(null_object)
        self.last_builder_null_type = typ.__module__ + "." + typ.__name__
        method = getattr(collection, method_name)
        builder = method(null_object)
        if builder is None:
            raise RuntimeError(method_name + " lieferte keinen Builder.")
        return builder

    def feature_diagnostics(self):
        """Report the actual modeling call, separate from expression diagnosis."""
        self.log("--- Feature-API-Diagnose ---")
        self.log("Feature: " + str(self.current_feature))
        self.log("Letzter Builder-Aufruf: " + str(self.last_builder_api))
        self.log("Uebergebener Nullobjekt-Typ: " + str(self.last_builder_null_type))
        self.log("Letzte Geometrieoperation: " + repr(self.last_primitive))
        self.log("Letzter Geometrievergleich: " + repr(self.last_geometry_context))
        for row in self.geometry_trace[-3:]:
            self.log("Geometrieschritt: " + repr(row))
        if self.inspector is not None:
            self.inspector.diagnostics()
        contracts = (("Features", "CreateBlockFeatureBuilder", "Feature"),
                     ("Features", "CreateCylinderBuilder", "Feature"),
                     ("Features", "CreateConeBuilder", "Cone"),
                     ("Features", "CreateExtrudeBuilder", "Feature"),
                     ("Features", "CreateBooleanBuilder", "BooleanFeature"),
                     ("BaseFeatures", "CreateAssociativeLineBuilder", "AssociativeLine"))
        for owner, name, null_name in contracts:
            try:
                collection = getattr(self.part, owner)
                method = getattr(collection, name, None)
                self.log("%s.%s: erwartet NXOpen.Features.%s.Null; vorhanden=%s" %
                         (owner, name, null_name, callable(method)))
                if name == self.last_builder_api:
                    doc = getattr(method, "__doc__", None)
                    if doc:
                        self.log(str(doc)[:8000])
            except Exception as exc:
                self.log("Optionale API-Diagnose %s: %s" % (name, exc))

    def profile_curve(self, start, end, name):
        """Native assoziative Linie zwischen zwei expressionsgesteuerten Punkten."""
        b=self.new_feature_builder(self.part.BaseFeatures, "CreateAssociativeLineBuilder",
                                   NXOpen.Features.AssociativeLine.Null)
        try:
            b.Associative=True
            b.StartPointOptions=NXOpen.Features.AssociativeLineBuilder.StartOption.Point
            b.EndPointOptions=NXOpen.Features.AssociativeLineBuilder.EndOption.Point
            b.StartPoint.Value=start
            b.EndPoint.Value=end
            f=b.CommitFeature()
            f.SetName(name)
            curves=[entity for entity in f.GetEntities() if isinstance(entity,NXOpen.Line)]
            if len(curves)!=1:
                raise RuntimeError("Assoziative Profillinie liefert nicht genau eine Linie: "+name)
            self.feature_count+=1
            return curves[0]
        finally:
            b.Destroy()

    def profile_extrude(self, op, target, name):
        points=[self.point(vertex) for vertex in op['points']]
        curves=[]
        for index,start in enumerate(points):
            self.current_feature=name+"_Profil_%03d"%(index+1)
            curves.append(self.profile_curve(start,points[(index+1)%len(points)],self.current_feature))
        self.current_feature=name
        section=self.part.Sections.CreateSection(0.001,0.01,0.5)
        section.SetAllowedEntityTypes(NXOpen.Section.AllowTypes.OnlyCurves)
        rule=self.part.ScRuleFactory.CreateRuleCurveDumb(curves)
        help_point=NXOpen.Point3d(*[model.evaluate(c,self.values) for c in op['points'][0]])
        section.AddToSection([rule],curves[0],NXOpen.NXObject.Null,NXOpen.NXObject.Null,
                             help_point,NXOpen.Section.Mode.Create,False)
        b=self.new_feature_builder(self.part.Features, "CreateExtrudeBuilder",
                                   NXOpen.Features.Feature.Null)
        try:
            b.Section=section
            b.Direction=self.direction(op['direction'])
            b.Limits.StartExtend.Value.RightHandSide="0"
            b.Limits.EndExtend.Value.RightHandSide=self.extrusion_height_text(op['height'])
            self.boolean(b,target,op['op'])
            feature=b.CommitFeature()
        finally:
            b.Destroy()
        # Konturen bleiben Eltern der Extrusion, werden nicht geloescht.
        for curve in curves:
            curve.Layer=190
            curve.Blank()
        return feature

    def primitive(self,op,target,feature_name):
        """v4.5: raw native tool first, measure, then a separate native Boolean.

        No primitive receives an integrated subtract/unite option. This avoids
        ambiguity between its own position and the target body construction.
        Every measured tool must match its recipe; every Boolean must change
        the target volume in the intended direction. Never skip failed cuts.
        """
        self.current_feature=feature_name
        self.last_primitive=dict(op)
        expected=primitive_contract(op,self.values,model.evaluate)
        self.last_geometry_context={'feature':feature_name,'operation':op['op'],'tool_expected':expected}
        if self.inspector is None:self.inspector=BodyInspector(self.part,self.log)
        before=self.inspector.measure(target) if target is not None else None
        self.last_geometry_context['target_before']=before
        raw_name=feature_name+'_Werkzeug' if target is not None else feature_name
        raw_feature,tool=self._raw_primitive(op,None,raw_name)
        self.current_feature=feature_name
        actual=self.inspector.measure(tool)
        self.last_geometry_context['tool_actual']=actual
        assert_contract(actual,expected,feature_name+' Werkzeug')
        if target is None:
            if op['op']!='add':raise RuntimeError('Erstes Feature darf kein Abzug sein: '+feature_name)
            feature=raw_feature;result=tool;after=actual
        else:
            if target.Tag==tool.Tag:raise RuntimeError('Werkzeug und Ziel identisch: '+feature_name)
            # Native Boolean retains the primitive as an associative parent.
            b=self.new_feature_builder(self.part.Features,'CreateBooleanBuilder',
                                       NXOpen.Features.BooleanFeature.Null)
            try:
                b.Operation=(NXOpen.Features.Feature.BooleanType.Subtract if op['op']=='cut'
                             else NXOpen.Features.Feature.BooleanType.Unite)
                b.Target=target
                b.Tools.Add(tool)
                b.RetainTarget=False;b.RetainTool=False
                b.CopyTargets=False;b.CopyTools=False
                b.Tolerance=0.001
                feature=b.CommitFeature()
            except Exception:
                self.log('Boolean fehlgeschlagen; Werkzeug bleibt nicht als fertiges Teil gewertet.')
                self.log('Geometrievergleich vor Fehler: '+repr(self.last_geometry_context))
                raise
            finally:b.Destroy()
            feature.SetName(feature_name)
            self.feature_count+=1
            bodies=feature.GetBodies()
            if len(bodies)!=1:raise RuntimeError('Boolean liefert nicht genau einen Koerper: '+feature_name)
            result=bodies[0]
            after=self.inspector.measure(result)
            assert_boolean_change(op['op'],before['volume_mm3'],after['volume_mm3'],actual['volume_mm3'],feature_name)
        self.last_measurement=after
        self.last_geometry_context['result']=after
        self.geometry_trace.append(dict(self.last_geometry_context))
        self.log('Geometrie OK: %s; Volumen %.9g mm^3; Aenderung %.9g mm^3' %
                 (feature_name,after['volume_mm3'],after['volume_mm3']-(before['volume_mm3'] if before else 0)))
        return feature,result

    def _raw_primitive(self,op,target,feature_name):
        self.current_feature=feature_name
        self.last_primitive=dict(op)
        origin=self.point(op['origin']) if op['kind'] != 'prism' else None
        if op['kind']=='box':
            b=self.new_feature_builder(self.part.Features, "CreateBlockFeatureBuilder",
                                       NXOpen.Features.Feature.Null)
            try:
                b.Type=NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths
                xyz=[model.evaluate(c,self.values) for c in op['origin']]
                b.SetOriginAndLengths(NXOpen.Point3d(*xyz),*[self.expr_text(s) for s in op['size']])
                b.SetOrientation(NXOpen.Vector3d(1.0,0.0,0.0),NXOpen.Vector3d(0.0,1.0,0.0))
                # NACH initialen Laengen setzen: OriginPoint nicht wieder numerisch ueberschreiben.
                b.OriginPoint=origin
                b.ParentAssociativity=True
                self.boolean(b,target,op['op'])
                feature=b.CommitFeature()
            finally:
                b.Destroy()
        elif op['kind']=='cylinder':
            b=self.new_feature_builder(self.part.Features, "CreateCylinderBuilder",
                                       NXOpen.Features.Feature.Null)
            try:
                b.Type=NXOpen.Features.CylinderBuilder.Types.AxisDiameterAndHeight
                b.Diameter.RightHandSide=self.expr_text(op['diameter'])
                b.Height.RightHandSide=self.expr_text(op['height'])
                # Fresh axis per feature; never mutate/reuse a builder-owned axis.
                # Explicit numeric initialization precedes (not follows) binding.
                b.Origin=NXOpen.Point3d(*[model.evaluate(c,self.values) for c in op['origin']])
                b.Direction=NXOpen.Vector3d(*[float(c) for c in op['direction']])
                b.ReverseDirection=False
                direction=self.direction(op['direction'])
                axis=self.part.Axes.CreateAxis(origin,direction,self.update)
                axis.Evaluate()
                b.Axis=axis
                b.ParentAssociativity=True
                self.boolean(b,target,op['op'])
                feature=b.CommitFeature()
            finally:
                b.Destroy()
        elif op['kind']=='cone':
            # NX2406 rejects Feature.Null here: this factory takes a Cone.
            b=self.new_feature_builder(self.part.Features, "CreateConeBuilder",
                                       NXOpen.Features.Cone.Null)
            try:
                b.Type=NXOpen.Features.ConeBuilder.Types.DiametersAndHeight
                b.BaseDiameter.RightHandSide=self.expr_text(op['diameter'])
                b.TopDiameter.RightHandSide=self.expr_text(op['top_diameter'])
                b.Height.RightHandSide=self.expr_text(op['height'])
                axis=self.part.Axes.CreateAxis(origin,self.direction(op['direction']),self.update)
                axis.Evaluate()
                b.Axis=axis
                b.ParentAssociativity=True
                self.boolean(b,target,op['op'])
                feature=b.CommitFeature()
            finally:
                b.Destroy()
        elif op['kind']=='prism':
            feature=self.profile_extrude(op,target,feature_name)
        else:
            raise ValueError('Unbekannter Featuretyp: '+op['kind'])
        feature.SetName(feature_name)
        self.feature_count+=1
        bodies=feature.GetBodies()
        if len(bodies)!=1:
            raise RuntimeError('Erwartet wurde genau ein Koerper in '+feature_name)
        return feature,bodies[0]

    def style(self,body,definition):
        body.SetName(definition['name'])
        body.Layer=model.LAYERS[definition['group']]
        self.attr(body,'SX_BAUGRUPPE',definition['group'])
        self.attr(body,'SX_GEOMETRIE','CNC-GESAMTANSICHT; ALLE ANSCHLUSSMASSE UNBESTAETIGT')
        self.attr(body,'SX_KLASSE','FOTOGRAFIERTES_GUSSTEIL' if definition.get('status')=='FOTO_REKONSTRUKTION' else 'RESTANNAHME_ODER_SICHTDETAIL')
        self.attr(body,'SX_HINWEIS',definition['note'])
        self.attr(body,'SX_QUELLE',definition.get('source','Quellen siehe Paket'))
        # Prefer named colours from NX's own displayed-part table. Explicit
        # configurable palette indices are the documented fallback; never abort
        # valid geometry merely because an optional colour enum is unavailable.
        import json
        color_names={'cast':'RedName','machine_red':'RedName','dark':'CharcoalGrayName',
            'steel':'SilverGrayName','panel':'LightGrayName','black':'BlackName',
            'red':'RedName','yellow':'YellowName','green':'GreenName','glass':'PaleCyanName',
            'silver':'SilverGrayName','aluminum':'LightGrayName','lcd':'GreenName',
            'copper':'BrownName','bronze':'BrownName','pcb':'GreenName','orange':'OrangeName',
            'grey':'GrayName','castiron':'GrayName','core':'GrayName','white':'WhiteName',
            'cabinet':'GrayName','design_blue':'BlueName','frame':'CharcoalGrayName','sheet':'SilverGrayName','reserviert':'OrangeName'}
        palette=dict(model.DEFAULT_COLORS)
        cfg=os.path.join(HERE,'NX_Farben.json')
        if os.path.isfile(cfg):
            with open(cfg,encoding='utf-8-sig') as stream:palette.update(json.load(stream))
        dm=None
        try:
            import NXOpen.UF
            uf=NXOpen.UF.UFSession.GetUFSession()
            idx=None
            types=[type(uf.Disp),getattr(NXOpen.UF,'Disp',None),getattr(NXOpen.UF,'UFDisp',None)]
            for typ in types:
                enum_type=getattr(typ,'ColorName',None)
                named=getattr(enum_type,color_names[definition['material']],None)
                if named is not None:
                    idx=uf.Disp.AskClosestColorInDisplayedPart(named)
                    break
            if idx is None:
                idx=int(palette[definition['material']])
                self.warnings.append('Konfigurierbarer Farbindex statt benannter NX-Farbe: '+definition['material']+'='+str(idx))
            dm=self.session.DisplayManager.NewDisplayModification()
            dm.ApplyToAllFaces=True
            dm.NewColor=int(idx)
            dm.NewTranslucency=75 if definition['material']=='glass' else 0
            dm.Apply([body])
        except Exception as exc:
            self.warnings.append('Darstellung '+definition['name']+': '+str(exc))
        finally:
            if dm is not None:dm.Dispose()

    def _probe_primitive(self, op, target, name):
        self.log("Featureprobe START: " + name)
        result = self.primitive(op, target, name)
        self.log("Featureprobe OK: " + name)
        return result

    def native_probe(self):
        """Echter Laufzeittest in NX, kein hier behaupteter Testlauf.

        Testet Block, Zylinderabzug, Kegel, Kegelabzug entlang -X,
        assoziative Linien und Extrusion.
        Prueft nach Ausdrucksaenderung Position UND Abmessung des Blockkoerpers.
        Saemtliche Probegeometrie und Probeaenderungen werden zurueckgenommen.
        """
        import NXOpen.UF
        uf=NXOpen.UF.UFSession.GetUFSession()
        mark=self.session.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible,'SX35Z native API-Probe')
        old_scalars=dict(self.scalars);old_aux=self.aux_id;old_count=self.feature_count
        success=False
        try:
            op=dict(kind='box',op='add',origin=['pos_x','0','0'],size=['table_x/100','10','10'])
            _,body=self._probe_primitive(op,None,'SXPROBE_Block')
            op=dict(kind='cylinder',op='cut',origin=['pos_x+table_x/200','5','-1'],diameter='2',height='12',direction=(0,0,1))
            _,body=self._probe_primitive(op,body,'SXPROBE_Bohrung')
            op=dict(kind='cone',op='add',origin=['30','0','0'],diameter='8',top_diameter='4',height='10',direction=(0,0,1))
            self._probe_primitive(op,None,'SXPROBE_Kegel')
            # Explicitly exercise the same cone subtraction used by the wheels
            # and spindle taper, including a direction other than +Z.
            op=dict(kind='box',op='add',origin=['80','0','0'],size=['20','20','20'])
            _,cut_body=self._probe_primitive(op,None,'SXPROBE_Kegelabzug_Rohteil')
            op=dict(kind='cone',op='cut',origin=['101','10','10'],diameter='6',top_diameter='10',height='22',direction=(-1,0,0))
            self._probe_primitive(op,cut_body,'SXPROBE_Kegelabzug_minusX')
            op=dict(kind='prism',op='add',origin=['50','0','0'],points=[['50','0','0'],['56','0','0'],['50','6','0']],height='10',direction=(0,0,1))
            self._probe_primitive(op,None,'SXPROBE_Profil')
            op=dict(kind='cylinder',op='add',origin=['140','12','18'],diameter='10',height='16',direction=(0,-1,0))
            _,axis_body=self._probe_primitive(op,None,'SXPROBE_Zylinder_minusY')
            op=dict(kind='box',op='add',origin=['138','-6','16'],size=['4','4','4'])
            self._probe_primitive(op,axis_body,'SXPROBE_Vereinigung')
            exp_x=self.part.Expressions.FindObject('sx_pos_x')
            exp_l=self.part.Expressions.FindObject('sx_table_x')
            exp_x.RightHandSide='%.12g'%(self.parameters['pos_x']+1)
            exp_l.RightHandSide='%.12g'%(self.parameters['table_x']+10)
            errors=self.session.UpdateManager.DoUpdate(mark)
            if errors: raise RuntimeError('API-Probe: %d Updatefehler'%errors)
            modl=getattr(uf,'ModlGeneral',None) or getattr(uf,'Modl',None)
            if modl is None or not hasattr(modl,'AskBoundingBox'):
                raise RuntimeError('NX UF: weder ModlGeneral.AskBoundingBox noch Modl.AskBoundingBox verfuegbar')
            bounds=modl.AskBoundingBox(body.Tag)
            if len(bounds)!=6: raise RuntimeError('API-Probe: ungueltige BoundingBox-Rueckgabe')
            expected_x=self.parameters['pos_x']+1
            expected_l=(self.parameters['table_x']+10)/100
            if abs(bounds[0]-expected_x)>1e-4 or abs((bounds[3]-bounds[0])-expected_l)>1e-4:
                raise RuntimeError('API-Probe: Featureposition/Laenge aktualisiert sich nicht assoziativ: '+str(bounds))
            self.log('Native API-Probe bestanden: getrennte Werkzeuge/Booleans, Soll-Ist-Geometrie, Richtungen und Ausdrucksaenderung.')
            success=True
        finally:
            self.session.UndoToMark(mark,None)
            self.expression_factory.unit=None
            self.expression_factory.last_unit_tag=None
            try:self.session.DeleteUndoMark(mark,None)
            except Exception:pass
            self.scalars=old_scalars;self.aux_id=old_aux;self.feature_count=old_count
            if success: self.current_feature=None

