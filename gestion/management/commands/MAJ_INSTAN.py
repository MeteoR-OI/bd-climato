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
        value= float(value)
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
                    outTemp = data['outTemp']
                    windchill = data['windchill']
                    heatIndex = data['heatIndex']
                    dewpoint = data['dewpoint']
                    humidity = data['humidity']
                    barometer = data['barometer']
                    windSpeed = data['windSpeed']
                    windDir = data['windDir']
                    windGust = data['windGust']
                    windGustDir = ['windGustDir']
                    rainRate = data['rainRate']
                    rain = data['rainSum']
                    try:
                        ET = convert(data['ET'])
                    except: 
                        ET = None
                    try : 
                        solarRadiation = convert(data['solarRadiation'])
                    except:
                        solarRadiation = None 
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
                                    PMER=convert(barometer),IC=convert(heatIndex),
                                    WINDCHILL=convert(windchill),ETP=ET,
                                    RAD=solarRadiation,RRI=convert(rainRate),
                                    FF=convert(windSpeed),DD=convert(windDir),
                                    FXI=convert(windGust),DXI=convert(windGustDir),
                                    T=convert(outTemp),TD=convert(dewpoint),
                                    U=convert(humidity),RR=convert(rain))

#                          
#                
#                                                       

#                       
#                      

                
    
        #Ajouter les capteurs SOL 
  
  
        


     
     
     
        
            