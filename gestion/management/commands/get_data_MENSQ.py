#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import sys
from gestion.models import PAYS,COMMUNE,POSTE,PANNE,INSTRUMENT,MAINTENANCE,INSTAN,H,Q,DECADQ,MENSQ,RECMENS,HISTMAINT,HISTPOST
import datetime
import json
import csv
import pytz
import math
import urllib
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
#        postes = POSTE.objects.all()
#         
#        for i in range(0,postes.count()): #On parcourt tous les postes de la BDD
#             type = postes[i].TYPE 
#             init = postes[i].INIT
#             
#             if type != 'SPIEA' and init == 1:
#                 mois_pre = datetime.datetime.now() - datetime.timedelta(days=1)
#                 mois_pre = datetime.datetime(mois_pre.year,mois_pre.month,1,
#                                            0,0)
#                 deb = mois_pre - datetime.timedelta(seconds=300)
#                 fin = mois_pre + datetime.timedelta(seconds=300)
#                 
#                 
#                 init.initMensQ(nom_poste=postes[i].CODE_POSTE,datedeb=deb,datefin=fin)
        nomposte = 'NDLP1520'
        poste = POSTE.objects.get(CODE_POSTE=nomposte)
        
        q = Q.objects.filter(POSTE=poste).order_by('-DATJ')
        
        mois_pre = 600
        
        for value_q in q:
            if value_q.DATJ.day == 1:
                derniere_date = datetime.datetime(value_q.DATJ.year,
                            value_q.DATJ.month,1,
                            0,0)
                
                if value_q.DATJ.month == 1:
                    moisavant = 12
                    anneeavant = value_q.DATJ.year-1
                else:
                    moisavant = value_q.DATJ.month - 1
                    anneeavant = value_q.DATJ.year
                mois_pre = datetime.datetime(anneeavant,moisavant,1,0,0)
                deb = mois_pre - datetime.timedelta(seconds=300)
                fin = mois_pre + datetime.timedelta(seconds=300)
                deb = deb.replace(tzinfo=pytz.UTC)
                fin = fin.replace(tzinfo=pytz.UTC)
                init.initMensQ(nom_poste=nomposte,datedeb=deb,datefin=fin)
                break
        
        
        print(mois_pre) 