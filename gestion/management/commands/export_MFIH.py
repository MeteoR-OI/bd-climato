#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import sys
import os
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
       
      
        postes = POSTE.objects.all()
         
        for i in range(0,postes.count()):
            nomposte = postes[i].CODE_POSTE
            poste = POSTE.objects.get(CODE_POSTE = nomposte)
            ins = INSTAN.objects.filter(POSTE = poste).order_by('-DATJ')
            last = ins[0]
            
       
            entetes = [
                 u'H',
                 u'RR', # /!\ sur l'heure passée
                
                 
            ]
            date= str(last.DATJ.day)+'/'+str(last.DATJ.month)+'/'+str(last.DATJ.year)+ \
                            ' '+str(last.DATJ.hour)+'-'+str(last.DATJ.minute)
            
           
            valeurs = [date,str(last.RR)]
            
            # /!\ RR dépend de la station
            
         
       
            ligneEntete = ";".join(entetes) + "\n"
            if not os.path.exists('exportMFIH'+nomposte+'.csv'):
                f = open('exportMFIH'+nomposte+'.csv', 'w')
                f.write(ligneEntete)
            else : 
                f = open('exportMFIH'+nomposte+'.csv', 'a')
                
            
            
          
            ligne = ";".join(valeurs) + "\n"
            f.write(ligne)
            
            f.close()