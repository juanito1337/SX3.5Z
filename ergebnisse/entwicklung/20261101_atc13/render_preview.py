from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'projekt'));sys.path.insert(0,str(ROOT/'projekt/tools'))
import atc13_modell as m
from atc13_pruefen import world_body
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig=plt.figure(figsize=(18,9),facecolor='#f4f6f8');cache={};defs=m.recipe();p=m.load_parameters()
for i,pose in enumerate(('park','wechsel'),1):
    ax=fig.add_subplot(1,2,i,projection='3d'); all_faces=[]; all_colors=[]
    q=m.assembly_pose(p,pose);v=m.all_values(q)
    for d in defs:
        if not (int(d['group'][:2])<=14 or d['group']=='20_ATC_Option' or d['name'].startswith('KSS_Fangblech')):continue
        if d['name'].startswith('Faltenbalg'):continue
        key=(d['name'],tuple((n,v[n]) for n in sorted(m.used_parameters(d))))
        if key not in cache:
            shape=world_body(d,q);pts,tris=shape.tessellate(2.,.55);verts=[(t.x,t.y,t.z) for t in pts]
            cache[key]=[[verts[j] for j in tri] for tri in tris]
        col='#b55249';alpha=1.
        if d['group']=='14_Untergestell':col='#66818c'
        if d['group']=='20_ATC_Option':
            col='#387caf' if d['supply_kind']=='MAKE' else '#83919b'
            if d['name'].startswith('ATC13_BT30'):col='#333e48'
            if 'Greiferbacke' in d['name']:col='#f6b64e'
            if 'Magazingabel' in d['name']:col='#d9dfe0'
            if d['name'].startswith('Spannpaket'):col='#eab05b';alpha=.4
        if d['name'].startswith('KSS_Fangblech'):col='#7eaaa8';alpha=.55
        all_faces.extend(cache[key]); all_colors.extend([col]*len(cache[key]))
    poly=Poly3DCollection(all_faces,facecolors=all_colors,edgecolors=all_colors,linewidth=0,alpha=1.,zsort='average',shade=True,lightsource=matplotlib.colors.LightSource(azdeg=300,altdeg=50))
    ax.add_collection3d(poly)
    ax.set(xlim=(-750,1500),ylim=(-650,1120),zlim=(-750,1050));ax.set_box_aspect((2250,1770,1800))
    ax.view_init(elev=31,azim=-63);ax.set_axis_off()
    ax.set_title('PARK · Tischraum frei, Greifer zurückgezogen' if pose=='park' else 'WECHSEL · Einzelgreifer an der Spindel',fontweight='bold')
fig.suptitle('SX3.5Z · Konzept 13 · Seitenmagazin mit 12 Plätzen',fontsize=20,fontweight='bold',y=.96)
fig.text(.5,.075,'Blau: Zusatzrahmen / Mechanik   ·   Dunkelgrau: Werkzeughalter   ·   Gelb: Greiferbacken',ha='center')
fig.text(.5,.035,'CAD-Rezeptvorschau · Verkleidung und Schaltschrank für freie Sicht ausgeblendet · Konzept, keine Fertigungsfreigabe',ha='center',fontsize=11,color='#685b42')
fig.subplots_adjust(left=0,right=1,top=.9,bottom=.1,wspace=-.08)
out=ROOT/'cad/vorschau/SX35Z_13_Seitenmagazin_Park_Wechsel.png';fig.savefig(out,dpi=150,facecolor=fig.get_facecolor());print(out)

