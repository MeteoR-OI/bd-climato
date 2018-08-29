#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import sys
from gestion.models import PAYS,COMMUNE,POSTE,PANNE,INSTRUMENT,MAINTENANCE,INSTAN,H,Q,DECADQ,MENSQ,RECMENS,HISTMAINT,HISTPOST
import datetime
import json
import csv
import math
import urllib
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import encodings    
    
import codecs
    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
    #    parser.add_argument(
    #        '-r', '--rain', action='store', dest='rain', default=0,
    #        type=int
    #    )




    def handle(self, *args, **options):
       
      
        
        
            
        #-----------------------------------------------------------------------   
        #------------A AJOUTER -----------------------------
        #----------------------------------------------------------------------
          
        #with urllib.request.urlopen("http://stations.meteor-oi.re/NDLP1520/json/daily.json") as url:
        #    data_json = url.read().decode('utf-8') 
        #    datas = json.load(data_json)
             
        #    data = datas['stats']
        #    data = data['current']
        #    outTemp = data['outTemp'].replace('°C','').replace(',','.')
        #    print(outTemp)
        #----------------------------------------------------------------------   
        #------------LISTING DES DIFFERENTS POSTES DANS LA BDD-----------------
        #----------------------------------------------------------------------
        
        
          
        postes = POSTE.objects.all()
         
        for i in range(0,postes.count()):
            poste = postes[i].CODE_POSTE
            type = postes[i].TYPE 
            
            if type != 'SPIEA':  
           
                with codecs.open('data/'+poste+'.json',encoding='utf-8') as json_data: #PARTIE A SUPPRIMER 
                    datas = json.load(json_data)  
                    data = datas['stats']
                    data = data['current']
                              
                    outTemp = data['outTemp'].replace(',','.')
                    windchill = data['windchill'].replace(',','.')
                    heatIndex = data['heatIndex'].replace(',','.')
                    dewpoint = data['dewpoint'].replace(',','.')
                    humidity = data['humidity'].replace(',','.')
                    barometer = data['barometer'].replace(',','.')
                    windSpeed = data['windSpeed'].replace(',','.')
                    windDir = data['windDir'].replace(',','.')
                    windGust = data['windGust'].replace(',','.') 
                    windGustDir = data['windGustDir'].replace(',','.')
                    rainRate = data['rainRate'].replace(',','.')
                    #rain = data['rain'].replace(',','.')*10
                    try :            
                        ET = data['ET'].replace(',','.')
                        solarRadiation = data['solarRadiation'].replace(',','.')
                    except:
                        ET = None
                        solarRadiation = None
                         
               
                                                      
                    jour = datas['time'][0:2]
                    mois = datas['time'][3:5]
                    annee = datas['time'][6:10]
                    heure = datas['time'][-5:-3]
                    minn = datas['time'][-2:]
                      
                     
                    codeposte = POSTE.objects.get(CODE_POSTE=postes[i].CODE_POSTE)
                    INSTAN(POSTE=codeposte,DATJ=datetime.datetime(int(annee)
                            ,int(mois),int(jour),int(heure),int(minn)),
                            PMER=barometer,IC=heatIndex,WINDCHILL=windchill,ETP=ET,
                            RAD=solarRadiation,RRI=rainRate*10,FF=windSpeed,DD=windDir,
                            FXI=windGust,DXI=windGustDir,T=outTemp,TD=dewpoint,
                            U=humidity).save()
                
        #MANQUE RR5MIN
        #Ajouter les capteurs SOL
  
  
        


     
     
     
        
            