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
from gestion.management.commands import init
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import encodings    
import pytz    
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
#             
#             if type != 'SPIEA':
#                 jr_pre = datetime.datetime.now() - datetime.timedelta(days=1)
#                 jr_pre = datetime.datetime(jr_pre.year,jr_pre.month,jr_pre.day,
#                                            0,0)
#                 deb = jr_pre - datetime.timedelta(seconds=300)
#                 fin = jr_pre + datetime.timedelta(seconds=300)
#                 
#                 
#                 init.initQ(nom_poste=postes[i].CODE_POSTE,datedeb=deb,datefin=fin)
                
        nomposte = 'NDLP1520'
        poste = POSTE.objects.get(CODE_POSTE=nomposte)
        
        h = H.objects.filter(POSTE=poste).order_by('-DATJ')
        
        jr_pre = 600
        
        for value_h in h:
            if value_h.DATJ.minute == 0 and value_h.DATJ.hour == 0:
                derniere_date = datetime.datetime(value_h.DATJ.year,
                            value_h.DATJ.month,value_h.DATJ.day,
                            0,0)
                jr_pre = derniere_date - datetime.timedelta(hours=24)
                deb = jr_pre - datetime.timedelta(seconds=300)
                fin = jr_pre + datetime.timedelta(seconds=300)
                deb = deb.replace(tzinfo=pytz.UTC)
                fin = fin.replace(tzinfo=pytz.UTC)
                init.initQ(nom_poste=nomposte,datedeb=deb,datefin=fin)
                break
        
        
        print(jr_pre)  
       