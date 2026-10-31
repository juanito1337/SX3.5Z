from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'],headless=True)
 page=b.new_page(viewport={'width':1480,'height':1080})
 page.set_content((R/'Ansicht_3D.html').read_text(),wait_until='load');page.wait_for_function('window.modelReady===true')
 page.evaluate("document.getElementById('legend').style.display='none';document.getElementById('hint').style.display='none';window.originalVisible=visible;void 0;")
 for prefix,name,az,el in [("s.name.startsWith('Kabelplatte_')||s.name.startsWith('LAPP_5311')",'Kabeleinfuehrung_09',-.8,-.4),("s.name==='Servicegriff_KSS'||s.name==='Griff_Hinterlegung_KSS'||s.name.startsWith('Griffscheibe_KSS')||s.name.startsWith('Griffschraube_KSS')",'Servicegriff_09',1.2,.35)]:
  page.evaluate(f"visible=s=>({prefix});az={az};el={el};zoom=1;schedule();")
  page.wait_for_function('window.modelReady===true');page.locator('#stage').screenshot(path=str(R/'Vorschau'/f'{name}.png'))
 b.close()
