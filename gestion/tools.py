'''
Created on 10 déc. 2018

@author: mhoareau
'''

def fonction_direction(DD):
    liste_dir_inf = [11.25,33.75,65.25,78.75,101.25,123.75,146.25,168.75,191.25,
                     213.75,236.25,258.75,281.25,303.75,326.25]
    liste_dir_sup = [33.75,65.25,78.75,101.25,123.75,146.25,168.75,191.25,
                     213.75,236.25,258.75,281.25,303.75,326.25,348.75]
    dirs = ['NNE','NE','ENE','E','ESE','SE','SSE','S','SSO','SO','OSO','O','ONO'
           ,'NO','NNO']
    try:
        if DD >= 348.75 or DD <= 11.25:
            Dir = 'N'
        else:
            for i in range(0,len(liste_dir_inf)):
                if DD >= liste_dir_inf[i] and DD <= liste_dir_sup[i]:
                    Dir = dirs[i]
    except:
        Dir = 'None'
    
    return(Dir)

def format_date(delta,ax):
    import matplotlib.dates as dates

    if delta >= 90:
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=31))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m/%Y'))
    elif delta >= 62:
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=15))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m')) 
    elif delta >= 31:
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=5))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m')) 
    elif delta >= 20 : 
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=2))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m')) 
    elif delta >= 10 : 
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m'))  
        
    elif delta >= 5 : 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=12))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%d'))   
    elif delta >= 3 : 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=6))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%d'))     
    elif delta >= 1 : 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=3))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%d')) 
    else: 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=1))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))    

    return


class ParamatersList(object):
    _parameters = {
        'T'         : 'Température (T)',
        'TD'        : 'Point de rosée (TD)',
        'U'         : 'Humidité relative (U)',
        'PMER'      : 'Pression mer (PMER)',
        'RR'        : 'Précipitations (RR)',
        'RRI'       : 'Intensité pluviométrique (RRI)',
        'FF'        : 'Vent moyen (FF)',
        'DD'        : 'Direction du vent moyen (DD)',
        'FXI'       : 'Rafale max (FXI)',
        'DXI'       : 'Direction de la rafale (DXI)',
        'IC'        : 'Indice de chaleur',
        'WINDCHILL' : 'Refroidissement éolien (WINDCHILL)',
        'UV'        : 'Indice UV',
        'RAD'       : 'Rayonnement (RAD)'
    }

    _unit_label = {
        'T'         : '°C',
        'TD'        : '°C',
        'U'         : '%',
        'PMER'      : 'hPa',
        'RR'        : 'mm',
        'RRI'       : 'mm/h',
        'FF'        : 'km/h',
        'DD'        : '°',
        'FXI'       : 'km/h',
        'DXI'       : '°',
        'IC'        : '°C',
        'WINDCHILL' : '°C',
        'UV'        : '',
        'RAD'       : 'W/m²',
        'RDV'       : ''
    }

    @staticmethod
    def get_choices(with_rdv=False, with_none=False):
        choices = list(ParamatersList._parameters.items())
        if with_rdv:
            choices.append(('RDV', 'Rose des vents'))
        if with_none:
            choices.insert(0, ('', 'Aucun'))
        return choices

    @staticmethod
    def get_list(with_rdv=False):
        keys = list(ParamatersList._parameters.keys())
        if with_rdv:
            keys.append('RDV')
        return keys

    @staticmethod
    def get_unit_label(parameter):
        return ParamatersList._unit_label[parameter]

    @staticmethod
    def get_parameter_label(parameter):
        if parameter not in ParamatersList._parameters.keys():
            return "Aucun"
        return ParamatersList._parameters[parameter]
