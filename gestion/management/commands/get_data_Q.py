#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pytz

from django.core.management.base import BaseCommand

from gestion.models import POSTE,H
from gestion import init_data


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
#                 jr_pre = datetime.datetime.now() - datetime.timedelta(days=1)
#                 jr_pre = datetime.datetime(jr_pre.year,jr_pre.month,jr_pre.day,
#                                            0,0)
#                 deb = jr_pre - datetime.timedelta(seconds=300)
#                 fin = jr_pre + datetime.timedelta(seconds=300)
#                 
#                 
#                 init.initQ(nom_poste=postes[i].CODE_POSTE,datedeb=deb,datefin=fin)
                
        postes = POSTE.objects.all()
          
        for i in range(0,postes.count()):
            nomposte = postes[i].CODE_POSTE
            types = postes[i].TYPE 
#             init = postes[i].INIT
            
#             
            if types != 'SPIEA': 
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
                        init_data.initQ(nom_poste=nomposte,datedeb=deb,datefin=fin)
                        break
                
                
                print(jr_pre)  
       