# -*- coding: utf-8 -*-
"""Native regression: expression provenance belongs to the owning Part.

Run with NX 2406 run_journal or Play Journal. Creates only a new test part.
No existing CAD file is opened or overwritten.
"""
import os
import sys
from datetime import datetime
from uuid import uuid4

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import NXOpen
import cnc_ansichtsmodell as model
from nx_native import NativeModelBuilder, RunLog
from nx_files import NativePartFiles, prepare_output_directory


def main():
    session = NXOpen.Session.GetSession()
    log = RunLog(session)
    run_id = uuid4().hex[:12]
    out = prepare_output_directory(
        HERE, 'SX35Z_METADATA_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + run_id, log)
    log.set_output_directory(out)
    files = NativePartFiles(session, out, run_id, log)
    path = files.filename(out, 'Metadatenprobe')
    part = files.create(path, lambda target: session.Parts.NewDisplay(target, NXOpen.Part.Units.Millimeters))
    parameters = model.load_parameters(os.path.join(HERE, 'Parameter.json'))
    builder = NativeModelBuilder(session, part, parameters, log)
    builder.expression_factory.mode = 'CreateNumberExpression'
    spec = next(s for s in model.SPECS if s['name'] == 'sheet_t')
    builder.create_expressions({'sheet_t'})
    builder.write_expression_metadata()
    assert not builder.warnings, 'Metadaten verursachen NX-Fehler: ' + repr(builder.warnings)
    for suffix, value in [('STATUS', spec['status']), ('BESCHREIBUNG', spec['note']),
                          ('QUELLE', spec['source']), ('EINHEIT', 'mm')]:
        actual = part.GetUserAttributeAsString('SX_EXPR_sheet_t_' + suffix, NXOpen.NXObject.AttributeType.String, -1)
        assert actual == value, (suffix, actual, value)
    assert part.Expressions.FindObject('sx_sheet_t').Value == parameters['sheet_t']
    files.save(part, path)
    log('METADATEN_REGRESSION_BESTANDEN: Herkunft am Part, Ausdruckswert unveraendert.')
    log.save()


if __name__ == '__main__':
    main()
