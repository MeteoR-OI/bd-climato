#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import urllib.request

from django.core.management.base import BaseCommand

from gestion.models import POSTE,INSTAN

# si la valeur n'existe pas --> none 
def convert(value):
    try: 
        return value.replace('"','')
    except:
        return value
    try:
        return value.replace(',','.')
    except: 
        return value
    try:
        return float(value)
    except:
        return None 
        
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
    #    parser.add_argument(
    #        '-r', '--rain', action='store', dest='rain', default=0,
    #        type=int
    #    )


    def handle(self, *args, **options):
        
        
        postes = POSTE.objects.all()
          
        for i in range(0,postes.count()):
            nomposte = postes[i].CODE_POSTE
            types = postes[i].TYPE 
#             init = postes[i].INIT
            
#             
            if types != 'SPIEA':  
#         nomposte = 'GDC030'
            
                with urllib.request.urlopen("http://stations.meteor-oi.re/"+nomposte+"/json/daily.json") as url:
                    datas = json.loads(url.read().decode())
        
                       
                    data = datas['stats']
                    data = data['current']
                    outTemp = convert(data['outTemp'])
                    windchill = convert(data['windchill'])
                    heatIndex = convert(data['heatIndex'])
                    dewpoint = convert(data['dewpoint'])
                    humidity = convert(data['humidity'])
                    barometer = convert(data['barometer'])
                    windSpeed = convert(data['windSpeed'])
                    windDir = convert(data['windDir'])
                    windGust = convert(data['windGust'])
                    windGustDir = convert(['windGustDir'])
                    rainRate = convert(data['rainRate'])
                    rain = convert(data['rainSum'])
                    ET = convert(data['ET'])
                    solarRadiation = convert(data['solarRadiation'])
#                     outTemp = data['outTemp'].replace('"','').replace(',','.')
#                     windchill = data['windchill'].replace('"','').replace(',','.')
#                     heatIndex = data['heatIndex'].replace('"','').replace(',','.')
#                     dewpoint = data['dewpoint'].replace('"','').replace(',','.')
#                     humidity = data['humidity'].replace('"','').replace(',','.')
#                     barometer = data['barometer'].replace('"','').replace(',','.')
#                     windSpeed = data['windSpeed'].replace('"','').replace(',','.')
#                     windDir = data['windDir'].replace('"','').replace(',','.')
#                     windGust = data['windGust'].replace('"','').replace(',','.')
#                     windGustDir = data['windGustDir'].replace('"','').replace(',','.')
#                     rainRate = data['rainRate'].replace('"','').replace(',','.')
#                     rain = data['rainSum'].replace('"','').replace(',','.')

#                     try :            
#                         ET = data['ET'].replace('"','').replace(',','.')
#                         solarRadiation = data['solarRadiation'].replace('"','').replace(',','.')
#                     except:
#                         ET = None
#                         solarRadiation = None
                    jour = datas['time'][0:2]
                    mois = datas['time'][3:5]
                    annee = datas['time'][6:10]
                    heure = datas['time'][-5:-3]
                    minn = datas['time'][-2:]
                    print(outTemp)
                    
                    dateTime = datetime.datetime(int(annee),int(mois),int(jour),int(heure),int(minn))
                    
                    
                    poste = POSTE.objects.get(CODE_POSTE=nomposte)
                    recu,created = INSTAN.objects.get_or_create(POSTE=poste,
                            DATJ=dateTime)
                    INSTAN.objects.filter(POSTE=poste,DATJ=dateTime).update(
                                    PMER=barometer,IC=heatIndex,
                                    WINDCHILL=windchill,ETP=ET,
                                    RAD=solarRadiation,RRI=rainRate,
                                    FF=windSpeed,DD=windDir,
                                    FXI=windGust,DXI=windGustDir,
                                    T=outTemp,TD=dewpoint,
                                    U=humidity,RR=rain)

#                          
#                
#                                                       

#                       
#                      

                
    
        #Ajouter les capteurs SOL 
  
  
        


     
     
     
        
            