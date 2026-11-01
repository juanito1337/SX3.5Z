"""User-requested stripped conversion and side chip-catch study; no hardware IO."""
import math

DEFAULTS = dict(catch_z=40., catch_rise=40., catch_slope=.04)
REMOVED_GROUPS = {'07_Bedienpanel','08_Blechsaeule','09_Elektrik'}
REMOVED_NAMES = {'Riemenabdeckung_Blech','Anzugspindel_Abdeckung','Riemendeckel_Schraubknopf',
    'Spindelschutz_oben','Spindelschutz_unten','Schutz_Halter','Schutz_Klemmschraube_-1',
    'Schutz_Klemmschraube_1','Lampenhalter','Arbeitslampe','Arbeitslampe_Linse',
    'Riemenhauben_Sicherheitsschalter'}


def removed(d):
    return d['group'] in REMOVED_GROUPS or d['name'] in REMOVED_NAMES


def removal_report(parts):
    return [dict(id=d['id'],name=d['name'],group=d['group'],reason='Nutzer01.11.2026: Originalanbau entfaellt im eingehausten CNC-Umbau; Funktion/Neuverkabelung separat auslegen.') for d in parts if removed(d)]


def validate(p,v):
    for key in DEFAULTS:
        value=p[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError('Ungueltiger Fangblechparameter: '+key)
    if not (30<=p['catch_z']<=50 and 30<=p['catch_rise']<=40 and .02<=p['catch_slope']<=.05):
        raise ValueError('Fangblechlage/Gefaelle ausserhalb gepruefter Entwurfsspanne')
    if p['catch_z']+1.25*p['catch_rise']+602*p['catch_slope']+3>125:
        raise ValueError('Fangblech zu hoch fuer nominalen Tisch-/Motorfreiraum')
    if v['enc_left']>=-510 or v['enc_right']<=510:
        raise ValueError('Seitlicher Fangblechraum fehlt')


def assembly_pose(p,name,values):
    q=dict(p)
    if name=='park':q['teller_feed']=0.
    elif name=='wechsel':
        q.update(teller_feed=1.,teller_index_cos=1.,teller_index_sin=0.,
                 head_down=values['spindle_face_z']+p['head_down']-p['teller_gauge_z'])
    else:raise ValueError('Unbekannte Baugruppenstellung: '+str(name))
    return q


def extend(parts,base):
    result=[d for d in parts if not removed(d)]
    for side,sign in [('links',-1),('rechts',1)]:
        for section,a,b,za,zb in [('innen',227,350,'catch_z+catch_rise','catch_z'),
                                  ('aussen',350,500,'catch_z','catch_z+1.25*catch_rise')]:
            name='KSS_Fangblech_'+side+'_'+section
            d=dict(id='E%03d'%(1+sum(x.get('revision_added')=='11' for x in result)),name=name,
                group='17_KSS',material='sheet',datum=['0','0','0'],ops=[],
                supply_kind='MAKE',item_id='F11-'+name,purchase_instance=name,
                source='Nutzerbild01.11.2026; E11 unbestaetigte Fangblechmasse',
                note='Abnehmbare geneigte 2mm-Blechvorform ueber bestehender Sammelwanne; offene hintere Abwurfkante. Halter, Fugen, Abwicklung und Durchsatz offen.',
                status='ENTWURF_11_UNBESTAETIGT',revision_added='11',manufacturing_released=False)
            d['filename']=d['id']+'_'+name
            slope=f'(({zb})-({za}))/({b-a})'
            points=[(sign*a,-220,f'({za})+catch_slope*602'),
                    (sign*b,-220,f'({zb})+catch_slope*602'),
                    (sign*b,382,zb),(sign*a,382,za)]
            base.prism(d,points,f'sheet_t*sqrt(1+({slope})*({slope})+catch_slope*catch_slope)',(0,0,1),label='Fangblech_Normaldicke_2mm')
            d.update(plate_normal_thickness='sheet_t',slope_x=f'({sign})*({slope})',slope_y='-catch_slope')
            result.append(d)
    return result
