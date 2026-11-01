from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'projekt'))
sys.path.insert(0,str(ROOT/'projekt/tools'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import cnc_ansichtsmodell as m
from atc_anschlusspruefung09 import world_body

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
p=m.load_parameters();defs=m.recipe();cache={}
fig=plt.figure(figsize=(16,8),facecolor='#f5f7fa')
for i,pose in enumerate(('park','wechsel'),1):
    ax=fig.add_subplot(1,2,i,projection='3d',computed_zorder=False)
    q=m.assembly_pose(p,pose);v=m.all_values(q)
    selected=[d for d in defs if int(d['group'][:2])<=13 or d['group']=='20_ATC_Option' or d['name'].startswith('KSS_Fangblech_')]
    for d in selected:
        if 'Faltenbalg' in d['name']:continue
        key=(d['name'],tuple((n,v[n]) for n in sorted(m.used_parameters(d))))
        if key not in cache:
            body=world_body(d,q);pts,tris=body.tessellate(1.5,.55)
            vs=[(t.x,t.y,t.z) for t in pts]
            cache[key]=[[vs[j] for j in t] for t in tris]
        col='#bd524b';alpha=1
        if d['group']=='20_ATC_Option':
            col='#2c75b2' if d['supply_kind']=='MAKE' else '#929eaa'
            if d['name'].startswith('Spannpaket_'):col='#eba340';alpha=.45
            if d['name'].startswith('ATC_Parkhaube_'):col='#71adc5';alpha=.15
            if 'BT30_ER20' in d['name']:col='#424c5b'
        elif d['name'].startswith('KSS_Fangblech_'):col='#74abb0';alpha=.65
        elif d['name'].startswith('CNC_'):col='#637b91'
        elif 'Arbeitstisch' in d['name']:col='#b5bbc0'
        poly=Poly3DCollection(cache[key],facecolors=col,edgecolors='#42505b' if d['supply_kind']=='MAKE' and d['group']=='20_ATC_Option' else col,linewidth=.15,alpha=alpha,shade=True,lightsource=matplotlib.colors.LightSource(azdeg=300,altdeg=50))
        ax.add_collection3d(poly)
    ax.set(xlim=(-430,760),ylim=(-450,370),zlim=(0,950))
    ax.set_box_aspect((1190,820,950));ax.view_init(elev=24,azim=-63)
    ax.set_axis_off();ax.set_title('PARK — rechts an der Säule' if pose=='park' else 'WECHSEL — Werkzeug auf Spindelachse',fontweight='bold',pad=0)
fig.suptitle('SX3.5Z · BT30-Wechsler auf fester Säulenkonsole · Entwurf 12',fontsize=18,fontweight='bold',y=.96)
fig.text(.5,.07,'Blau: Konsole / eigene Teile    Grau: Kaufteil-Hüllen    Türkis: Spänefang / Spritzschirm',ha='center')
fig.text(.5,.035,'Rezeptvorschau (Offline) · 200 mm Hub und Greifer-Teilkreis angenommen · Spindel/Spannpaket noch offen',ha='center',color='#725022',fontsize=10)
fig.subplots_adjust(left=0,right=1,bottom=.09,top=.89,wspace=-.1)
out=ROOT/'cad/vorschau/SX35Z_12_Park_Wechsel.png';out.parent.mkdir(exist_ok=True)
fig.savefig(out,dpi=150,facecolor=fig.get_facecolor());print(out)
