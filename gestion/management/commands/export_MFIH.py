#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.core.management.base import BaseCommand

from gestion.models import POSTE,INSTAN


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
            types = postes[i].TYPE 

                
    #             
            if types != 'SPIEA':
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
                
               
                
                
                # /!\ RR dépend de la station
                
             
           
                ligneEntete = ";".join(entetes) + "\n"
                if not os.path.exists('exportMFIH'+nomposte+'.csv'):
                    f = open('exportMFIH'+nomposte+'.csv', 'w')
                    f.write(ligneEntete)
                else : 
                    f = open('exportMFIH'+nomposte+'.csv', 'a')
                    
                
                
                #comparer donnee à inserer à la derniere donnee presente
                h = open('exportMFIH'+nomposte+'.csv', 'r')
                test = h.readlines()
                lenline = len(test)
                
                try:
                    lastdatefichier = str((test[lenline-1].split(';'))[0])
                    
                except:
                    lastdatefichier = 'aucun'
                    
                if lastdatefichier == date:
                    res = 'yes'
                else: 
                    res = 'no'
                    
                if res == 'no':
                    valeurs = [date,str(last.RR)]
                    ligne = ";".join(valeurs) + "\n"
              
                    f.write(ligne)
             
                
                f.close()