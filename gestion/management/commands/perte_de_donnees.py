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
import math
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import encodings    
    
import codecs
from gestion.management.commands import init    
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
    #    parser.add_argument(
    #        '-r', '--rain', action='store', dest='rain', default=0,
    #        type=int
    #    )




    def handle(self, *args, **options):
       
      
        
        #Recherche des données manquantes
        postes = POSTE.objects.all()
        for i in range(0,postes.count()): 
            if postes[i].TYPE != 'SPIEA':
                codeposte = POSTE.objects.get(CODE_POSTE=postes[i].CODE_POSTE)
                now = datetime.datetime.now()
                #CONTROLE : période sur laquelle les données sont controlées
                #avant la date d'aujourd'hui
                CONTROLE = 100
                #TIMEDELTA : Temps habituel entre 2 relevés
                TIMEDELTA = 300
                datecontrole = now-datetime.timedelta(days=CONTROLE)
                ins = INSTAN.objects.filter(POSTE=codeposte,
                                            DATJ__gte=datecontrole) \
                                            .order_by('DATJ')
                
                Creneau_deb =[]
                Creneau_fin = []
                PERTE = False
                for i in range(0,ins.count()):
                    #On vérifie le pas de temps entre 2 données consécutives
                    timedelta = (ins[i+1].DATJ - ins[i].DATJ).seconds
                    
                    if timedelta != 300:
                        PERTE=True
                        #On rajoute le crenéau de perte dans les listes
                        Creneau_deb+=[ins[i].DATJ]
                        Creneau_fin+=[ins[i+1].DATJ]
            
                    
            #2 possibilités de traitement de ces créneaux :
            #Soit on traite toutes les données entre le 1er élèment de Creneau_deb
            #et le dernier élément de Creneau_fin
            #Soit on traite les données entre Creneau_deb[i] et Creneau_fin[i]
            
            #1er cas choisi
                if PERTE:
                    Deb = Creneau_deb[0] 
                    Fin = Creneau_fin[-1] 
                    delta_hour = math.floor(((Fin-Deb).days)*24)
                    delta_hour += math.floor(((Fin-Deb).seconds)/3600)+1 
                    
                    for i in range(0,delta_hour+1):
                         
                    
                    #daily_20180803_1100.json
                    #Chargement des fichiers json entre ces 2 dates
                        Date_chargement = (Deb+datetime.timedelta(hours=1)) \
                                .strftime('%Y%m%d_%H')
                        
                        #CETTE PARTIE DEPENDRA DE LA STRUCTURE DU JSON
                        #AJOUTER UNE VERIFICATION DU RETOUR DES FICHIERS DE 
                        #SAUVEGARDE
                        with codecs.open('data/sauvegarde/'+postes[i].CODE_POSTE+
                                         '/daily_'+Date_chargement+'00.json',
                                         encoding='utf-8') as json_data: 
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
                                #rain = data['rain'].replace(',','.')
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
                                
                                INSTAN.objects.get_or_create(POSTE=codeposte,
                                DATJ=datetime.datetime(int(annee)
                                ,int(mois),int(jour),int(heure),int(minn)),
                                PMER=barometer,IC=heatIndex,WINDCHILL=windchill,ETP=ET,
                                RAD=solarRadiation,RRI=rainRate*10,FF=windSpeed,DD=windDir,
                                FXI=windGust,DXI=windGustDir,T=outTemp,TD=dewpoint,
                                U=humidity)
                            
                    #On réinitialise la table H
                        
                    init.initH(nom_poste=postes[i].CODE_POSTE,datedeb = Deb,
                               datefin = Fin,perte=1)
                    init.initQ(nom_poste=postes[i].CODE_POSTE,datedeb = Deb,
                               datefin = Fin,perte=1)
                    init.initMensQ(nom_poste=postes[i].CODE_POSTE,datedeb = Deb,
                               datefin = Fin,perte=1)