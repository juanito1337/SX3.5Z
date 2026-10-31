from playwright.sync_api import sync_playwright
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];out=R/'Vorschau';out.mkdir(exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=__import__('os').environ.get('CHROMIUM_EXECUTABLE','/usr/bin/chromium'),args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1540,'height':1160},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((R/'Ansicht_3D.html').read_text(encoding='utf-8'),wait_until='load');page.wait_for_function('window.modelReady===true',timeout=60000)
 page.screenshot(path=str(out/'Browser_geschlossen.png'))
 # Generate image directly from the rendered geometry, with on-canvas legend hidden.
 page.evaluate("document.getElementById('legend').style.display='none';document.getElementById('hint').style.display='none';az=-1.35;el=.20;schedule()")
 page.wait_for_function('window.modelReady===true')
 page.locator('#stage').screenshot(path=str(out/'Gesamtansicht.png'))
 page.locator('#stage').screenshot(path=str(out/'Gesamtansicht_geschlossen.png'))
 closed=page.evaluate("canvas.toDataURL()")
 page.locator('#bdoors').click();page.wait_for_function('window.modelReady===true')
 assert page.locator('#doorStatus').inner_text()=='offen'
 assert page.evaluate('doorFraction')==1
 opened=page.evaluate("canvas.toDataURL()")
 assert opened!=closed
 page.locator('#stage').screenshot(path=str(out/'Gesamtansicht_offen.png'))
 page.screenshot(path=str(out/'Browser_offen.png'))
 for q in (.25,.5,.75):
  page.evaluate(f'setDoors({q})');page.wait_for_function('window.modelReady===true');assert page.evaluate('doorFraction')==q
 page.evaluate('az=-Math.PI/2;el=.06;setDoors(1)');page.wait_for_function('window.modelReady===true')
 page.locator('#stage').screenshot(path=str(out/'Front_offen.png'))
 page.evaluate('setDoors(0)');page.wait_for_function('window.modelReady===true')
 page.locator('#stage').screenshot(path=str(out/'Front_geschlossen.png'))
 for mode,name in [('maschine','Maschine_ohne_Einhausung'),('innen','Innenansicht'),('schrank','Schaltschrank_offen'),('cnc','Antriebe'),('kss','Spaene_KSS_Ruecklauf')]:
  page.evaluate(f"setMode('{mode}')");page.wait_for_function('window.modelReady===true')
  page.locator('#stage').screenshot(path=str(out/(name+'.png')))
 # Real rotate/zoom controls smoke checks.
 page.evaluate("setMode('gesamt')");page.wait_for_function('window.modelReady===true')
 angle=page.evaluate('az');page.mouse.move(950,550);page.mouse.down();page.mouse.move(1020,560,steps=4);page.mouse.up();page.wait_for_function('window.modelReady===true');assert page.evaluate('az')!=angle
 z=page.evaluate('zoom');page.mouse.wheel(0,-140);page.wait_for_timeout(300);page.wait_for_function('window.modelReady===true');assert page.evaluate('zoom')!=z
 assert not errors,errors
 r={'browser':'Chromium via Playwright set_content (file URLs blocked in host policy)','native_nx_executed':False,'door_states_checked':[0,.25,.5,.75,1],'door_motion':'two segments -Z, upper 1030 mm / lower 515 mm','render_changes_when_open':True,'rotation_control':True,'zoom_control':True,'modes_checked':7,'javascript_errors':errors}
 (R/'Pruefung_08/Browserpruefung.json').write_text(json.dumps(r,indent=2));print(r)
 b.close()
