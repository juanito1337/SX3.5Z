"""K07 sheet-metal chip collection. Design dimensions, not selected hardware.
Slopes / openings are real recipe geometry. No hydraulic, leak, automatic chip
transport or fine filtration performance is inferred from these bodies.
"""
import math
import modell_v4 as base
from blech06 import u_profile

SOURCE='K07 Eigenentwurf nach Nutzerauftrag: Spaeneabgang unten/hinten, Korb vor KSS-Tank. Keine Kaufteil- oder Fertigungsfreigabe.'
NOTE=('Duenne Blechvorform zum Schweissen/Abdichten; Nennmasse Entwurf. '
      'Spanart, Spuelstrom, Feinfilter, Ueberlauf und Wartung noch auszulegen.')

def add_return_parts(part,box,cyl,ring):
    g='17_KSS'
    def flat(name,points,sx,sy):
        d=part(name,g,'sheet',points[0],note=NOTE,source=SOURCE)
        # vertical extrusion h=t*sqrt(1+sx^2+sy^2) has NORMAL thickness t.
        h=f'sheet_t*sqrt(1+({sx})*({sx})+({sy})*({sy}))'
        base.prism(d,points,h,(0,0,1),label='Geneigtes_Blech_Normaldicke')
        d['plate_normal_thickness']='sheet_t'
        d['slope_x']=str(sx);d['slope_y']=str(sy)
        if name=='KSS_Leitblech_links_hinten':
            base.box(d,('enc_left+sheet_t-1','enc_back-26',-30),('sheet_t+1',30,240),'cut','Freistellung_Rueckwand_Rueckkantung')
        if name=='KSS_Leitblech_rechts_hinten':
            base.box(d,('enc_right-2*sheet_t','enc_back-26',-30),('sheet_t+1',30,240),'cut','Freistellung_Rueckwand_Rueckkantung')
        return d
    def fold(name,o,w,depth,length,axes):
        d=part(name,g,'sheet',o,note=NOTE,source=SOURCE)
        return u_profile(d,o,w,depth,length,axes)
    # Raised machine island remains x +/-225, y -220..380, no load on drain sheets.
    # Inner edge of tray x +/-227 is outside the 2 mm seal/curb strip.
    for side,inner,outer,sx in [('links','-227','enc_left+sheet_t','-0.14'),('rechts','227','enc_right-sheet_t','0.14')]:
        for suffix,y0,y1,sy in [('vorn','enc_front+30','382','-0.025'),('hinten','382','enc_back-2*sheet_t','0')]:
            def zz(x,y):return f'-8+({sx})*(({x})-({inner}))+({sy})*(({y})-382)'
            pts=[(inner,y0,zz(inner,y0)),(outer,y0,zz(outer,y0)),(outer,y1,zz(outer,y1)),(inner,y1,zz(inner,y1))]
            flat('KSS_Leitblech_'+side+'_'+suffix,pts,sx,sy)
    # Front central panels shed to either side of the machine island, not into it.
    for suffix,x0,x1,sx in [('links','-227','0','5/227'),('rechts','0','227','-5/227')]:
        def z(x,y):return f'-3+({sx})*({x})-0.025*(({y})-382)'
        y0='enc_front+30';y1='-222'
        flat('KSS_Leitblech_Front_'+suffix,[(x0,y0,z(x0,y0)),(x1,y0,z(x1,y0)),(x1,y1,z(x1,y1)),(x0,y1,z(x0,y1))],sx,'-0.025')
    # Four coplanar trapezoids meet around the W x D aperture, no invisible cut.
    xl='-chip_outlet_w/2';xr='chip_outlet_w/2'
    yf='chip_outlet_y-chip_outlet_d/2';yb='chip_outlet_y+chip_outlet_d/2'
    flat('KSS_Trichter_links',[(-227,382,-8),(-227,'enc_back-2*sheet_t',-8),(xl,yb,-16),(xl,yf,-16)],'-8/(227-chip_outlet_w/2)','0')
    flat('KSS_Trichter_rechts',[(227,382,-8),(xr,yf,-16),(xr,yb,-16),(227,'enc_back-2*sheet_t',-8)],'8/(227-chip_outlet_w/2)','0')
    flat('KSS_Trichter_vorn',[(-227,382,-8),(xl,yf,-16),(xr,yf,-16),(227,382,-8)],'0','-8/(chip_outlet_y-chip_outlet_d/2-382)')
    flat('KSS_Trichter_hinten',[(-227,'enc_back-2*sheet_t',-8),(227,'enc_back-2*sheet_t',-8),(xr,yb,-16),(xl,yb,-16)],'0','8/(enc_back-2*sheet_t-chip_outlet_y-chip_outlet_d/2)')
    # Sheet island curbs, separate from load-bearing plate.
    for side,x in [('links',-227),('rechts',225)]:
        box('KSS_Innenaufkantung_'+side,g,(x,-222,-20),(2,604,40),'sheet',note=NOTE)
    for side,y in [('vorn',-222),('hinten',380)]:
        box('KSS_Innenaufkantung_'+side,g,(-225,y,-20),(450,2,40),'sheet',note=NOTE)
    # Centre rear lip bridges the small below-zero portion of the back wall.
    box('KSS_Rueckwand_Aufkantung',g,(-227,'enc_back-2*sheet_t',-8),(454,'sheet_t',38),'sheet',note=NOTE)
    # Rectangular chip chute fits BETWEEN machine support and rear frame beam.
    fold('KSS_Spaeneschacht_U',(xl,yf,-175),'chip_outlet_w','chip_outlet_d',159,((1,0,0),(0,1,0),(0,0,1)))
    box('KSS_Spaeneschacht_Rueckwand',g,('-chip_outlet_w/2+sheet_t','chip_outlet_y+chip_outlet_d/2-sheet_t',-175),('chip_outlet_w-2*sheet_t','sheet_t',159),'sheet',note=NOTE)
    # Catch housing below chute, open towards rear for service behind the machine.
    d=fold('KSS_Ruecklaufkasten_U',(-220,385,-280),440,110,180,((1,0,0),(0,0,1),(0,1,0)))
    base.cyl(d,(0,'chip_outlet_y',-281),50,'sheet_t+2',(0,0,1),'cut','Nur_KSS_Ablauf_nach_Korb')
    box('KSS_Ruecklaufkasten_Stirnwand',g,('-220+sheet_t',385,'-280+sheet_t'),('440-2*sheet_t','sheet_t','110-sheet_t'),'sheet',note=NOTE)
    box('KSS_Serviceklappe_hinten',g,(-220,565,-280),(440,2,110),'sheet',note='Abnehmbare hintere Wartungsklappe, Dichtprofil und Verschluesse noch zu spezifizieren. Vor Korbauszug abnehmen.')
    # Dedicated hangers bear on rear stand beam, not on thin tray sheets.
    for side,x in [('links',-224),('rechts',220)]:
        box('KSS_Kastenhalter_'+side,g,(x,480,-280),(4,45,200),'steel',note='Traglasche am hinteren Gestellholm. Verschraubung/Schweissanschluss und Tragfaehigkeit noch auslegen.')
    # Removable 420 x 160 x 70 mm coarse chip basket; genuine open floor slots.
    d=fold('KSS_Spaenekorb_U',(-210,390,-258),420,70,160,((1,0,0),(0,0,1),(0,1,0)))
    for ix in range(10):
        for iy in range(5):
            base.box(d,(-193+ix*39,399+iy*28,-259),(28,3,'sheet_t+2'),'cut','Grobsieb_Schlitz_KEIN_FEINFILTER')
    d['service_translation']=[0,220,0]
    for side,y in [('vorn',390),('hinten','550-sheet_t')]:
        d=box('KSS_Spaenekorb_Stirnwand_'+side,g,('-210+sheet_t',y,'-258+sheet_t'),('420-2*sheet_t','sheet_t','70-sheet_t'),'sheet',note=NOTE)
        d['service_translation']=[0,220,0]
    d=box('KSS_Spaenekorb_Griff',g,(-55,550,-227),(110,12,12),'frame',note='Griffhuelle fuer Korbauszug NACH HINTEN bei Maschinenstillstand; keine tragfaehige Griffauslegung.')
    d['service_translation']=[0,220,0]
    # Support strips beneath basket; no rail floating in nominal filter aperture.
    for side,x in [('links',-218),('rechts',195)]:
        box('KSS_Korbauflage_'+side,g,(x,390,-262),(23,170,4),'steel',note='Schmale Auflageleisten; Korb liegt auf und wird manuell herausgezogen.')
    d=box('KSS_Feinsieb_Klemmrahmen_Reserve',g,(-190,395,-271),(380,140,2),'dark',note='Nur offener Halterahmen. Feinfiltergewebe NICHT modelliert/ausgewaehlt; Grobsieb allein schuetzt nicht vor Feinspaenen.')
    base.box(d,(-180,405,-272),(360,120,4),'cut','Offener_Filtereinsatz_KEINE_GESCHLOSSENE_PLATTE')
    ring('KSS_Ablaufstutzen_nach_Korb',g,(0,'chip_outlet_y','-stand_h+175+tank_h'),56,50,'stand_h-455-tank_h',mat='steel',note='50-mm-Lichtweite als Studienmass, kein hydraulischer Nachweis. Rohr ragt in Tank; Dichtung/Kupplung offen.')
    # Retain tank/pump envelope; enlarge only the service-compatible return opening.
    d=box('KSS_Tank_Entwurf',g,('-tank_w/2','enc_back-260-tank_d/2','-stand_h+200'),('tank_w','tank_d','tank_h'),'sheet',note=NOTE)
    base.box(d,('-tank_w/2+3','enc_back-257-tank_d/2','-stand_h+203'),('tank_w-6','tank_d-6','tank_h'),'cut','Tankinnenraum')
    d=box('KSS_Tankdeckel',g,('-tank_w/2','enc_back-260-tank_d/2','-stand_h+200+tank_h'),('tank_w','tank_d',3),'sheet',note=NOTE)
    base.cyl(d,(0,'chip_outlet_y','-stand_h+199+tank_h'),58,5,(0,0,1),'cut','Ruecklaufdurchgang_Entwurf')
    cyl('KSS_Pumpe_Bauraum',g,(-165,'enc_back-250','-stand_h+203+tank_h'),70,100,mat='reserviert',note='Unveraenderter Pumpenbauraum. Foerderstrom, Ruecklaufleistung und Feinfiltration nicht ausgelegt.')

def validate(p,v):
    if not 200<=p['chip_outlet_w']<=380:raise ValueError('Spaeneauslassbreite 200..380 mm erforderlich')
    if not 30<=p['chip_outlet_d']<=70:raise ValueError('Spaeneauslasstiefe 30..70 mm erforderlich')
    yf=p['chip_outlet_y']-p['chip_outlet_d']/2;yb=p['chip_outlet_y']+p['chip_outlet_d']/2
    if yf<390 or yb>v['enc_back']-p['tube_side']-4:raise ValueError('Spaeneschacht kollidiert mit Maschineninsel/hinterem Rahmen')
    if not 395<=yf and yb<=550:raise ValueError('Spaeneschacht nicht ueber dem Korb')
    if p['tank_w']<470:raise ValueError('Tank zu schmal fuer Ruecklaufstudie')
    if p['stand_h']-p['tank_h']<=465:raise ValueError('Tank zu hoch fuer Ruecklaufkasten und Stutzen')
    return True

def report(p,v):
    return dict(schema='K07_DRAIN_LAYOUT',native_nx_executed=False,manufacturing_released=False,
        cabinet=dict(gap_mm=p['cab_gap'],wall_outer_x_mm=v['enc_right']+p['sheet_t'],cabinet_back_x_mm=v['cab_x'],right_window=False,
                     note='Rueckseite gegen geschlossene Nassraumwand, Last auf eigenem Gestell. Keine Rueckseitenbelueftung vorgesehen; Kuehlung/Abdichtung offen.'),
        side_slope_percent=14.,side_slope_angle_deg=math.degrees(math.atan(.14)),longitudinal_slope_percent=2.5,
        outlet_outer_mm=[p['chip_outlet_w'],p['chip_outlet_d']],outlet_clear_mm=[p['chip_outlet_w']-2*p['sheet_t'],p['chip_outlet_d']-2*p['sheet_t']],
        outlet_y_limits_mm=[p['chip_outlet_y']-p['chip_outlet_d']/2,p['chip_outlet_y']+p['chip_outlet_d']/2],
        basket_outer_mm=[420,160,70],basket_gross_inner_litres=(420-2*p['sheet_t'])*(160-2*p['sheet_t'])*(70-p['sheet_t'])/1e6,
        basket_slots=dict(count=50,size_mm=[28,3],gross_open_area_mm2=50*28*3),
        rear_extraction_stroke_mm=220,rear_service_space_proposed_mm=500,
        flow_sequence=['Leitbleche um Maschineninsel','hinterer Trichter','rechteckiger Spaeneschacht','entnehmbarer Grobkorb','offene Feinfilterreserve','KSS-Stutzen','Tank'],
        limitations=['Keine garantierte selbsttaetige Spanfoerderung. Lange Spaene manuell entfernen.','Schweissnaehte, Dichtungen, Gewebe, Verstopfung/Notueberlauf und hydraulischer Durchsatz offen.','Korb nach hinten: Wartungsfreiraum erforderlich. Fronttuer/Tankzugang nicht ersetzt.'])
