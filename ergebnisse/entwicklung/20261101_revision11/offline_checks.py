from pathlib import Path
import subprocess,sys,json,shutil,datetime
root=Path(__file__).resolve().parents[3];audit=Path(__file__).resolve().parent
copy=audit/'arbeitskopie_final'
shutil.copytree(root/'projekt',copy,ignore=shutil.ignore_patterns('__pycache__','Historie_07_3','*.html'))
records=[]
for name,args,cwd in [
 ('wechselweg',['tools/wechselweg11_pruefen.py','--output',str(audit/'final_wechselweg.json')],root/'projekt'),
 ('endpunkte',['tools/teller_pruefung10.py','--output',str(audit/'final_endpunkte.json')],root/'projekt'),
 ('kss',['tools/pruefen07.py'],copy),
 ('berichte',['Projekt09_Berichte.py'],copy)]:
 start=datetime.datetime.now().astimezone().isoformat();command=[sys.executable,'-B']+args
 result=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (audit/('final_'+name+'.stdout.txt')).write_bytes(result.stdout)
 records.append(dict(date=start,source_base='7bffcd4',command=command,cwd=str(cwd),
    environment='Windows CPython3.12.14 CadQuery2.8 OCP7.9.3.1.1',scope=name,exitcode=result.returncode,raw_log='final_'+name+'.stdout.txt'))
 (audit/'final_offline.meta.json').write_text(json.dumps(records,indent=2),encoding='utf8')
 print(name,'exit',result.returncode,flush=True)
 if name=='kss' and (copy/'Dokumentation/K07_Kollisionen.json').exists():
  shutil.copy2(copy/'Dokumentation/K07_Kollisionen.json',audit/'final_kss.json')
