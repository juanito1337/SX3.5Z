# -*- coding: utf-8 -*-
"""Umsetzung09: extra source-linked enclosure details + explicitly non-operational ATC study.
All previous original-machine features and native APIs remain in the retained08 module.
"""
import copy,json,math,re
from pathlib import Path
from collections import OrderedDict
import cnc_ansichtsmodell08 as prev
import normteile09
import teller10
base=prev.base
evaluate=prev.evaluate
local_definition=prev.local_definition
ROOT=Path(__file__).resolve().parent
VERSION='CNC_UMSETZUNG_10_TELLER'
CAT=json.loads((ROOT/'Einkauf/Kaufteile_09.json').read_text(encoding='utf8'))['items']
SPECS=copy.deepcopy(prev.SPECS)
DERIVED=copy.deepcopy(prev.DERIVED)
GROUPS=OrderedDict(prev.GROUPS)
GROUPS.update([('19_Normdetails','09 – Servicegriffe / Kabeleinführungen / Normteile'),('20_ATC_Option','09 – Werkzeugmagazin OPTION; Spindelumrüstung fehlt')])
GROUPS['20_ATC_Option']='10 – Teller und Spannpaket; unbestaetigte Einbaustudie'
LAYERS={g:(i+1)*10 for i,g in enumerate(GROUPS)}
PALETTE=dict(prev.PALETTE)
DEFAULT_COLORS=dict(prev.DEFAULT_COLORS)
NEW_DEFAULTS=dict(prev.NEW_DEFAULTS)
DEFAULTS09=dict(normteile09.CUSTOM_DEFAULTS)
for n,(item,key) in normteile09.CATALOG_PARAMETERS.items():DEFAULTS09[n]=float(CAT[item]['dims'][key])
for n,value in DEFAULTS09.items():
    NEW_DEFAULTS[n]=value
    item=normteile09.CATALOG_PARAMETERS.get(n)
    SPECS.append(dict(name=n,value=value,unit='unitless' if n=='atc_pocket_count' else 'mm',status='KATALOG_HAUPTMASS' if item else 'ENTWURF_09',source=item[0] if item else 'Entwurf09',note='Siehe Quellen09 und ATC-Konzept; keine Freigabe.',limits=None))
DERIVED.update(teller10.DERIVED)
for n,value in teller10.DEFAULTS.items():
    SPECS.append(dict(name=n,value=value,unit='unitless' if n in teller10.UNITLESS else 'mm',
        status='ENTWURF_10_UNBESTAETIGT',source='E10 Layoutstudie01.11.2026',
        note='Kein Hersteller- oder Istmass; Magazin/Spannpaket ohne Betriebsfreigabe.',limits=None))

def load_parameters(path=None):
    p=OrderedDict(prev.load_parameters(path));p.update(DEFAULTS09)
    fp=(Path(path).resolve().parent if path else ROOT)/'Detail_Parameter_09.json'
    if fp.exists():
        q=json.loads(fp.read_text(encoding='utf-8-sig'))
        for n,val in q.items():
            if n.startswith('_'):continue
            if n not in DEFAULTS09:raise ValueError('Unbekannter Detailparameter09: '+n)
            if isinstance(val,bool) or not isinstance(val,(float,int)) or not math.isfinite(val):raise ValueError('Ungültiger Detailparameter09: '+n)
            p[n]=float(val)
    p.update(teller10.DEFAULTS)
    fp=(Path(path).resolve().parent if path else ROOT)/'Teller_Parameter_10.json'
    if fp.exists():
        q=json.loads(fp.read_text(encoding='utf-8-sig'))
        for n,val in q.items():
            if n.startswith('_'):continue
            if n not in teller10.DEFAULTS:raise ValueError('Unbekannter Tellerparameter: '+n)
            if isinstance(val,bool) or not isinstance(val,(float,int)) or not math.isfinite(val):
                raise ValueError('Ungueltiger Tellerparameter: '+n)
            p[n]=float(val)
    validate(p);return p

def all_values(p):
    v=OrderedDict(p)
    for n,e in DERIVED.items():v[n]=evaluate(e,v)
    return v

def validate(p):
    prev.validate(p)
    for n,default in DEFAULTS09.items():
        if n not in p or not math.isfinite(p[n]):raise ValueError('Parameter09 fehlt/ungültig: '+n)
        if n!='atc_y' and p[n]<=0:raise ValueError('Nichtpositive Länge: '+n)
    for n,(item,key) in normteile09.CATALOG_PARAMETERS.items():
        if not math.isclose(p[n],CAT[item]['dims'][key],rel_tol=0,abs_tol=1e-9):
            raise ValueError('Katalogmaß09 darf ohne geänderte Lieferrevision nicht überschrieben werden: '+n)
    if p['sheet_t']!=2 or p['cable_plate_t']!=2 or p['cable_plate_seal_t']!=.5:
        raise ValueError('09-Schraubenmaßketten gelten nur für 2mm-Bleche und0.5mm-Kabelplattendichtung.')
    if p['atc_locator_bore']<=p['n09_tool_nut_d']:
        raise ValueError('Halterdurchgang der Gabelraumreserve zu klein')
    teller10.validate(p,all_values(p))
    return True

def used_parameters(d):
    known={s['name'] for s in SPECS}|set(DERIVED);out=set()
    def scan(x):
        if isinstance(x,str):out.update(set(re.findall(r'\b[A-Za-z_]\w*\b',x))&known)
        elif isinstance(x,dict):
            for k,val in x.items():
                if k not in ('label','name','note','source'):scan(val)
        elif isinstance(x,(tuple,list)):
            for v in x:scan(v)
    scan(d['ops']);scan(d['datum']);scan(d.get('sheetmetal',{}))
    while True:
        old=set(out)
        for n in list(out):
            if n in DERIVED:scan(DERIVED[n])
        if old==out:return out

def recipe():return teller10.extend(normteile09.extend(copy.deepcopy(prev.recipe()),base,CAT),base,CAT)

def check_recipe(p,parts=None):
    validate(p);v=all_values(p);ds=parts if parts is not None else recipe();seen=set()
    for d in ds:
        if d['name'] in seen:raise ValueError('Doppelter Teilname: '+d['name'])
        seen.add(d['name'])
        if d['group'] not in GROUPS or d['material'] not in PALETTE:raise ValueError('Gruppe/Farbe fehlt: '+d['name'])
        for op in d['ops']:
            for x in op['origin']:evaluate(x,v)
            for x in op.get('size',[]):
                if evaluate(x,v)<=0:raise ValueError('Nichtpositive Größe: '+d['name'])
            for key in ('height','diameter','top_diameter'):
                if key in op and evaluate(op[key],v)<=0:raise ValueError('Nichtpositive Abmessung: '+d['name'])
            for pt in op.get('points',[]):
                for x in pt:evaluate(x,v)
    # Retain existing drive/enclosure gates, do NOT relabel them as full ATC collision validation.
    prev.check_recipe(p,prev.recipe())
    return v

def atc_report(p):return teller10.report(p,all_values(p))
length_report=prev.length_report
door_layout=prev.door_layout
spring_report=prev.spring_report
drain_report=prev.drain_report
axis_frame=prev.axis_frame
assert_catalog_dimensions=prev.assert_catalog_dimensions
CATALOG_PARAMETER_MAP=prev.CATALOG_PARAMETER_MAP

def enclosure_report(p,definitions=None):
    return prev.enclosure_report(p,prev.recipe() if definitions is None else definitions)
