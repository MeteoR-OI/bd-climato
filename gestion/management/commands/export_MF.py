#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os

from django.core.management.base import BaseCommand

from gestion.models import POSTE,H

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
                h = H.objects.filter(POSTE = poste).order_by('-DATJ')
                last = h[1].DATJ - datetime.timedelta(hours=1)
                last = datetime.datetime(last.year,last.month,last.day,last.hour,
                                         0,0)
                h = h.filter(DATJ=last)[0]
           
                entetes = [
                     u'H',
                     u'RR1', # /!\ sur l'heure passée
                     u'TN',
                     u'HTN',
                     u'TX',
                     u'HTX',
                     u'T',
                     u'DD',
                     u'FF',
                     u'DXI',
                     u'FXI',
                     u'HXI',
                     u'DXY',
                     u'FXY',
                     u'RAD',
                     u'PMER',
                     u'PMERMIN',
                     u'HPMERMIN',
                     u'HU',
                     u'HUX',
                     u'HUN'
                     
                ]
                date= str(h.DATJ.day)+'/'+str(h.DATJ.month)+'/'+str(h.DATJ.year)+ \
                                ' '+str(h.DATJ.hour)+'-'+str(h.DATJ.minute)
                HTN = str(h.HTN.hour)+'h'+str(h.HTN.minute)
                HTX = str(h.HTX.hour)+'h'+str(h.HTX.minute)
                HXI = str(h.HXI.hour)+'h'+str(h.HXI.minute)
                HPERMIN = str(h.HPERMIN.hour)+'h'+str(h.HPERMIN.minute)
                valeurs = [date,str(h.RR1),str(h.TN),str(HTN),str(h.TX),str(HTX)
                           ,str(h.T),str(h.DD)
                           ,str(h.FF),str(h.DXI),str(h.FXI),str(
                            HXI),str(h.DXY),str(h.FXY),str(h.RAD),str(h.PMER),
                           str(h.PMERMIN),
                           str(HPERMIN),str(h.U),str(h.UX),str(h.UN)]
                
                # /!\ RR dépend de la station
                
             
           
                ligneEntete = ";".join(entetes) + "\n"
                if not os.path.exists('exportMF'+nomposte+'.csv'):
                    f = open('exportMF'+nomposte+'.csv', 'w')
                    f.write(ligneEntete)
                else : 
                    f = open('exportMF'+nomposte+'.csv', 'a')
                    
                
                
              
                ligne = ";".join(valeurs) + "\n"
                f.write(ligne)
                
                f.close()