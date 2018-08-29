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
       
       #-----------------------------------------------------------------------------
       #------------------EXECUTION HORAIRE------------------------------------------
       #-----------------------------------------------------------------------------
       postes = POSTE.objects.all()
        
       for i in range(0,postes.count()): #On parcourt tous les postes de la BDD
            
            poste = POSTE.objects.get(CODE_POSTE=postes[i].CODE_POSTE) #On sélectionne un poste
            mensq = MENSQ.objects.filter(POSTE=poste).order_by('DATJ') #on ordonne les données selon DATJ
    
            for mois in range(1,13):
                TX = -30
                TXDAT = None
                TN = 50
                TNDAT = None
                for i in range(0,mensq.count()):  #on parcourt les données 
        
                        
                    if mensq[i].DATJ.month == mois: 
                                
                            if mensq[i].TXAB > TX:
                                TX=mensq[i].TXAB
                                TXDAT=mensq[i].TXABDAT
                            if mensq[i].TNAB > TN:
                                TN=mensq[i].TNAB
                                TNDAT=mensq[i].TNDAT
                        #PMERM = PMERM/filtre.count()
                       
                RECMENS(POSTE=poste,PARAM='TX',NUM_MOIS=mensq[i].DATJ.month,RECORD=TX,DATERECORD=TXDAT)
                RECMENS(POSTE=poste,PARAM='TN',NUM_MOIS=mensq[i].DATJ.month,RECORD=TN,DATERECORD=TNDAT)
            