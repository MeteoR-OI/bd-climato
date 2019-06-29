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
import pytz
from gestion.management.commands import init
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

        #-----------------------------------------------------------------------------
        #------------------EXECUTION HORAIRE------------------------------------------
        #-----------------------------------------------------------------------------
#         postes = POSTE.objects.all()
#         #AVANT DE FAIRE L'INITIALISATION HORAIRE - VERIFIER LA PRESENCE DE TOUS LES INSTAN 
#         for i in range(0,postes.count()): 
#              type = postes[i].TYPE 
#              init = postes[i].INIT
#             
#             if type != 'SPIEA' and init == 1:
            
            
            #On définit l'heure à laquelle doit s'initialiser les tables
            
            #recherche du premier créneau horaire complet puis mise à jour

            postes = POSTE.objects.all()

            for poste in postes:
                nomposte = poste.CODE_POSTE
                types = poste.TYPE
                print("Poste %s" % nomposte)

                if types != 'SPIEA':
                    INSTANT_options = {
                        "POSTE" :   poste
                    }

                    if H.objects.filter(POSTE = poste).count() > 0:
                        last_h_data = H.objects.filter(POSTE = poste).order_by('-DATJ')[0]

                        INSTANT_options['DATJ__gte'] = last_h_data.DATJ - datetime.timedelta(hours=1)

                    instant_count = INSTAN.objects.filter(**INSTANT_options).count()
                    instant_per_page = 200
                    page_index = 1

                    INSTANT_options.update({
                        'DATJ__minute' : 0
                    })

                    while "Executer une fois puis les suivantes.":
                        first_inst = page_index*instant_per_page-instant_per_page
                        last_inst = page_index*instant_per_page-1
                        print("\t Index: %s, First: %s, Last: %s" % (nomposte, first_inst, last_inst))

                        ins = INSTAN.objects.filter(**INSTANT_options).order_by('DATJ')[first_inst:last_inst]

                        for value_ins in ins:
                            derniere_date = datetime.datetime(value_ins.DATJ.year,
                                                              value_ins.DATJ.month,
                                                              value_ins.DATJ.day,
                                                              value_ins.DATJ.hour,0)

                            hr_pre = derniere_date - datetime.timedelta(hours=1)
                            deb = hr_pre - datetime.timedelta(seconds=300)
                            fin = hr_pre + datetime.timedelta(seconds=300)
                            deb = deb.replace(tzinfo=pytz.UTC)
                            fin = fin.replace(tzinfo=pytz.UTC)
                            print(nomposte, deb, fin)
                            init.initH(nom_poste=nomposte,datedeb=deb,datefin=fin)

                        if page_index*instant_per_page-1 > instant_count:
                            break

                        page_index+=1
             
                
                
                
                
            
            
            