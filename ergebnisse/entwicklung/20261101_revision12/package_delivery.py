from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
matrix=read(A/'native_matrix.json');runs=read(A/'lieferlaeufe.json')
assert len(matrix)==5 and all(x['exitcode']==0 for x in matrix)
source=matrix[0]['source_base'];assert all(x['source_base']==source for x in matrix)
for row in read(A/'native_source_hashes.json'):
    assert sha(ROOT/row['path']).upper()==row['sha256'].upper(),row['path']
motion=read(A/'motion_final.json');end=read(A/'endpoints_final.json')
kss=read(A/'arbeitskopie/projekt/Dokumentation/K07_Kollisionen.json')
assert not motion['collisions'] and len(motion['checks'])==540 and motion['sampled_poses']==17
assert not end['collisions']
assert len(kss['static_conflicts'])==6 and not kss['axis_pose_conflicts'] and not kss['basket_conflicts']
assert all('IFS206' in x['a'] or 'IFS206' in x['b'] for x in kss['static_conflicts'])
write(A/'kss_final.json',kss)
assert '190 passed, 99 subtests passed' in (A/'offline_final.log').read_text(encoding='utf-8-sig')
for pose,path in runs.items():
    folder=Path(path);assert folder.resolve().is_relative_to((ROOT/'cad/nx').resolve())
    opened=read(next(folder.glob('NX_Wiederoeffnung_*.json')))
    assert opened['saved_parts_reopened'] and len(opened['components'])==461
    assert opened['group_count']==17 and not opened['errors'] and not opened['unloaded']
    prts=sorted(folder.rglob('*.prt'));assert len(prts)==482
    sheet=read(folder/'Blech_Nachweis.json')
    assert sheet['mode']=='required' and len(sheet['parts'])==19
    assert all(x['sheetmetal']['sheetmetal_verified'] for x in sheet['parts'])
    if pose=='wechsel':
        position=read(folder/'NX_Werkzeuglage_12.json')
        assert position['nominal_alignment_verified']
        assert all(abs(x-y)<1e-5 for x,y in zip(position['measured_holder_cone_axis_and_gauge_mm'],[0,0,400]))
    proof=folder/'Pruefnachweise';proof.mkdir(exist_ok=False)
    names=['native_matrix.json','native_source_hashes.json','run_native.ps1','offline_final.log',
           'motion_final.json','endpoints_final.json','kss_final.json','kss_final.log',
           'review.md','README.md','verification.meta.json','package.log','handoff_tests.log']
    names += [x.name for x in A.glob('native_*.stdout.txt')]
    for name in names:shutil.copy2(A/name,proof/name)
    write(folder/'PRT_SHA256.json',dict(date=datetime.datetime.now().astimezone().isoformat(),
        code_commit=source,scope='482 saved native PRT; byte identity only',
        files={p.relative_to(folder).as_posix():sha(p) for p in prts}))
    write(folder/'PRUEFSTATUS.json',dict(date=datetime.datetime.now().astimezone().isoformat(),
        code_commit=source,source_base='8204471',model_version='CNC_UMSETZUNG_12_BT30_KONSOLE',pose=pose,
        native_nx_executed=True,saved_parts_reopened=True,part_count=461,group_count=17,prt_files=482,
        native_sheetmetal_parts=19,new_sloped_chip_catch_precursors=4,removed_original_parts=61,
        environment='NX2406 Python3.10.15 Windows',native_journals=5,native_exitcodes=[x['exitcode'] for x in matrix],
        commands_and_raw_logs='Pruefnachweise/native_matrix.json',source_hashes='Pruefnachweise/native_source_hashes.json',
        offline_tests=190,offline_subtests=99,offline_exitcode=0,sampled_poses=17,
        sampled_path_brep_checks=540,sampled_path_collisions=0,indexed_endpoint_checks=len(end['checks']),
        indexed_endpoint_collisions=0,offline_kss_exitcode=1,unmounted_sensor_reference_conflicts=6,
        known_machine_interface_conflicts=6,missing_measurements=35,
        nominal_alignment_verified_native=(pose=='wechsel'),
        supplier_geometry_verified=False,spindle_interface_verified=False,spindle_clamping_verified=False,
        trajectory_verified=False,build_ready=False,purchase_released=False,machine_operation_enabled=False,atc_operational=False,
        notes='Fixed column console and200mm placement study. Real casting attachment/fasteners/loads, actual product datums/pitch/stroke, spindle/clamping, guards and complete path remain open.'))
    cmd=[str(ROOT/'.venv/Scripts/python.exe'),str(ROOT/'tools_handoff/verify_package.py'),'--root',str(folder),'--manifest','PRT_SHA256.json']
    check=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (proof/'hash_verification.log').write_bytes(check.stdout)
    write(proof/'hash_verification.meta.json',dict(command=cmd,exitcode=check.returncode,code_commit=source,
        date=datetime.datetime.now().astimezone().isoformat(),scope='File byte identity only; separate NX reopening proof required'))
    assert check.returncode==0,check.stdout
    subprocess.run(['git','add','--',str(folder.relative_to(ROOT))],cwd=ROOT,check=True)
print('Two native deliveries verified and staged:964PRT, source '+source)
