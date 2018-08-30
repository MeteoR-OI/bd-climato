#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import sys
from gestion.models import PAYS,COMMUNE,POSTE,PANNE,INSTRUMENT,MAINTENANCE,INSTAN,H,Q,DECADQ,MENSQ,RECMENS,HISTMAINT,HISTPOST
import datetime
import json
import csv
import math
import urllib.request, json 
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
       
        nomposte = 'NDLP1520'
            
        with urllib.request.urlopen("http://stations.meteor-oi.re/"+nomposte+"/json/daily.json") as url:
            datas = json.loads(url.read().decode())

               
            data = datas['stats']
            data = data['current']
            outTemp = data['outTemp'].replace('"','').replace(',','.')
            windchill = data['windchill'].replace('"','').replace(',','.')
            heatIndex = data['heatIndex'].replace('"','').replace(',','.')
            dewpoint = data['dewpoint'].replace('"','').replace(',','.')
            humidity = data['humidity'].replace('"','').replace(',','.')
            barometer = data['barometer'].replace('"','').replace(',','.')
            windSpeed = data['windSpeed'].replace('"','').replace(',','.')
            windDir = data['windDir'].replace('"','').replace(',','.')
            windGust = data['windGust'].replace('"','').replace(',','.')
            windGustDir = data['windGustDir'].replace('"','').replace(',','.')
            rainRate = data['rainRate'].replace('"','').replace(',','.')
            rain = data['rainSum'].replace('"','').replace(',','.')
            try :            
                ET = data['ET'].replace('"','').replace(',','.')
                solarRadiation = data['solarRadiation'].replace('"','').replace(',','.')
            except:
                ET = None
                solarRadiation = None
            jour = datas['time'][0:2]
            mois = datas['time'][3:5]
            annee = datas['time'][6:10]
            heure = datas['time'][-5:-3]
            minn = datas['time'][-2:]
            print(outTemp)
            
            
            poste = POSTE.objects.get(CODE_POSTE=nomposte)
            recu,created = INSTAN.objects.get_or_create(POSTE=poste,
                    DATJ=datetime.datetime(int(annee)
                            ,int(mois),int(jour),int(heure),int(minn)))
            INSTAN.objects.filter(POSTE=poste,DATJ=datetime.datetime(int(annee)
                            ,int(mois),int(jour),int(heure),int(minn))).update(
                            PMER=float(barometer),IC=float(heatIndex),
                            WINDCHILL=float(windchill),ETP=float(ET),
                            RAD=float(solarRadiation),RRI=float(rainRate)*10,
                            FF=float(windSpeed),DD=float(windDir),
                            FXI=float(windGust),DXI=float(windGustDir),
                            T=float(outTemp),TD=float(dewpoint),
                            U=float(humidity),RR=float(rain)*10)
        #----------------------------------------------------------------------   
        #------------LISTING DES DIFFERENTS POSTES DANS LA BDD-----------------
        #----------------------------------------------------------------------
        
        
          
#         postes = POSTE.objects.all()
#          
#         for i in range(0,postes.count()):
#             poste = postes[i].CODE_POSTE
#             type = postes[i].TYPE 
            
#             
#             if type != 'SPIEA':  
#            
#                 with codecs.open('data/'+poste+'.json',encoding='utf-8') as json_data: #PARTIE A SUPPRIMER 
#                     datas = json.load(json_data)  
#                     data = datas['stats']
#                     data = data['current']
#                               
                    
#                          
#                
#                                                       

#                       
#                      

                
    
        #Ajouter les capteurs SOL
  
  
        


     
     
     
        
            