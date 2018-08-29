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
            q = Q.objects.filter(POSTE=poste).order_by('-DATJ') 
    
            for ind in range(0,q.count()): 
                INST = 0
                cumulRR = 0
                RRAB = 0
                NBJRR1 = 0
                NBJRR5 = 0
                NBJRR10 =0
                NBJRR30 = 0
                NBJRR50 =0
                NBJRR100 =0
                PMERM= 0
                PMERMINAB= 2000
                NBJTX0 = 0 
                NBJTX25 = 0
                NBJTX30 = 0
                NBJTX35 = 0
                NBJTXI20 = 0
                NBJTXI27 = 0
                NBJTX32 = 0
                TNAB = 100
                TNDAT = None
                TNMAX = -20
                TNMAXDAT = None
                PMERMINABDAT = None
                RRABDAT = None
                TXAB = -30
                TXABDAT = None
                TXMIN = 100
                TXMINDAT = None
                NBJTN5= 0
                NBJTNI10=0
                NBJTNI15=0
                TN=0
                TX=0
                NBJTNI20=0
                NBJTNS20=0
                NBJTNS25=0
                NBJGELEE = 0
                UNAB = 100
                UNABDAT = None
                UXAB = 100
                UMM=0
                UXABDAT = None
                FXIAB = -1
                DXIAB =0
                HXIAB = 0
                NBJFF10 = 0
                NBJFF16 =  0
                NBJFF28 = 0
                NBJFXY8 = 0
                NBJFXY10 =  0
                NBJFXY15 = 0
                FXYAB = -1
                DXYAB = 0
                FXYABDAT = None
                if q[ind].DATJ.month == 12:
                    date_fin_du_mois = datetime.datetime(q[ind].DATJ.year+1,1,1)-datetime.timedelta(days=1)
                else :
                    date_fin_du_mois = datetime.datetime(q[ind].DATJ.year,q[ind].DATJ.month+1,1)-datetime.timedelta(days=1)
                if (q[ind].DATJ.day == 10 or q[ind].DATJ.day == 20 or  q[ind].DATJ.day == date_fin_du_mois.day ):
                    
                    if date_fin_du_mois.day == 28 and q[ind].DATJ.day != 10 and q[ind].DATJ.day != 20 :
                        delta = 7
                    elif date_fin_du_mois.day == 29 and q[ind].DATJ.day != 10 and q[ind].DATJ.day != 20:
                        delta = 8
                    elif date_fin_du_mois.day == 30 and q[ind].DATJ.day != 10 and q[ind].DATJ.day != 20:
                        delta = 9
                    elif date_fin_du_mois.day == 31 and q[ind].DATJ.day != 10 and q[ind].DATJ.day != 20:
                        delta = 10
                    else:
                        delta = 9
                            
                    filtre = q.filter(DATJ__lte = q[ind].DATJ,DATJ__gte=q[ind].DATJ-datetime.timedelta(days=delta)) #..on filtre les données sur cette journée
                    
                    if q[ind].DATJ.day > 20 :
                        NUM_DECADE = 3
                    elif q[ind].DATJ.day > 10 :
                        NUM_DECADE = 2
                    elif q[ind].DATJ.day >= 1 :
                        NUM_DECADE = 1    
                        
                    for j in range(0,filtre.count()):
                        cumulRR+=filtre[j].RR
                        PMERM+=filtre[j].PMER
                        TN+=filtre[j].TN
                        TX+=filtre[j].TX
                        UMM+=filtre[j].UM
                        if filtre[j].INST != None:
                                INST+=filtre[j].INST
                        if filtre[j].UN < UNAB:
                            UNAB = filtre[j].UN
                            UNABDAT = filtre[j].DATJ
                        if filtre[j].UX > UXAB:
                            UXAB = filtre[j].UX
                            UXABDAT = filtre[j].DATJ
                        if filtre[j].TN <= 0:
                            NBJGELEE += 1
                        if filtre[j].TN <= -5:
                            NBJTN5 += 1
                        if filtre[j].TN <= 10:
                            NBJTNI10 += 1
                        if filtre[j].TN <= 15:
                            NBJTNI15 += 1
                        if filtre[j].TN <= 20:
                            NBJTNI20 += 1
                        if filtre[j].TN > 20:
                            NBJTNS20 += 1
                        if filtre[j].TN >+ 25:
                            NBJTNS25 += 1
                        if filtre[j].TN <= TNAB:
                            TNAB=filtre[j].TN
                            TNDAT = filtre[j].DATJ
                        if filtre[j].TN >= TNMAX:
                            TNMAX=filtre[j].TN
                            TNMAXDAT = filtre[j].DATJ
                        if filtre[j].PMER <= PMERMINAB:
                            PMERMINAB = filtre[j].PMER
                            PMERMINABDAT= filtre[j].DATJ
                        if filtre[j].RR >= RRAB:
                            RRAB=filtre[j].RR
                            RRABDAT = filtre[j].DATJ
                        if filtre[j].RR >= 1:
                            NBJRR1 += 1
                        if filtre[j].RR >= 5:
                            NBJRR5 += 1    
                        if filtre[j].RR >= 10:
                            NBJRR10 += 1
                        if filtre[j].RR >= 30:
                            NBJRR30 += 1
                        if filtre[j].RR >= 50:
                            NBJRR50 += 1
                        if filtre[j].RR >= 100:
                            NBJRR100 += 1   
                        if filtre[j].TX >= TXAB:
                            TXAB = filtre[j].TX
                            TXABDAT = filtre[j].DATJ 
                        if filtre[j].TX <= TXMIN:
                            TXMIN = filtre[j].TX
                            TXMINDAT = filtre[j].DATJ 
                        if filtre[j].TX < 0:
                            NBJTX0 += 1
                        if filtre[j].TX > 25:
                            NBJTX25 += 1
                        if filtre[j].TX > 30:
                            NBJTX30 += 1
                        if filtre[j].TX > 32:
                            NBJTX32 += 1
                        if filtre[j].TX > 35:
                            NBJTX35 += 1
                        if filtre[j].TX < 20:
                            NBJTXI20 += 1
                        if filtre[j].TX < 27:
                            NBJTXI27 += 1   
                        if filtre[j].FXI > FXIAB:
                            FXIAB = filtre[j].FXI   
                            DXIAB = filtre[j].DXI
                            HXIAB = filtre[j].HXI
                        if filtre[j].FXY > FXYAB:
                            FXYAB = filtre[j].FXY   
                            DXYAB = filtre[j].DXY
                            FXYABDAT = filtre[j].HXY
                        if filtre[j].FXI >= 36: #10m/s = 36km/h
                            NBJFF10 += 1
                        if filtre[j].FXI >= 57.6:
                            NBJFF16 += 1
                        if filtre[j].FXI >= 100.8:
                            NBJFF28 += 1
                        if filtre[j].FXY >= 28.8: 
                            NBJFXY8 += 1
                        if filtre[j].FXY >= 36:
                            NBJFXY10 += 1
                        if filtre[j].FXY >= 54:
                            NBJFXY15 += 1
                        if q[0].TSM != None:
                            TSM= 0
                            TSX = -30
                            TSN = 100
                        else : 
                            TSM = None
                            TSX= None
                            TSN =None
                    PMERM = PMERM/filtre.count()
                    TN = TN/filtre.count()
                    TX = TX/filtre.count()
                    UMM = UMM/filtre.count()
                    DECADQ(POSTE=poste,DATJ=q[ind].DATJ,NUM_DECADE = NUM_DECADE,RR=cumulRR,STATUS_DRR=2,RRAB=RRAB,RRABDAT=RRABDAT,NBJRR1=NBJRR1,NBJRR5=NBJRR5,NBJRR10=NBJRR10,NBJRR30=NBJRR30,NBJRR50=NBJRR50,NBJRR100=NBJRR100,PMERM=PMERM,PMERMINAB=PMERMINAB,PMERMINABDAT=PMERMINABDAT,TX=TX,TXAB=TXAB,TXABDAT=TXABDAT,TXMIN=TXMIN,TXMINDAT=TXMINDAT,NBJTX0=NBJTX0,NBJTX25=NBJTX25,NBJTX30=NBJTX30,NBJTX32=NBJTX32,NBJTX35=NBJTX35,NBJTXI20=NBJTXI20,NBJTXI27=NBJTXI27,TN=TN,TNAB=TNAB,TNDAT=TNDAT,TNMAX=TNMAX,TNMAXDAT=TNMAXDAT,NBJTN5=NBJTN5,NBJTNI10=NBJTNI10,NBJTNI15=NBJTNI15,NBJTNI20=NBJTNI20,NBJTNS20=NBJTNS20,NBJTNS25=NBJTNS25,NBJGELEE=NBJGELEE,UNAB=UNAB,UNABDAT=UNABDAT,UXAB=UXAB,UXABDAT=UXABDAT,FXIAB=FXIAB,DXIAB=DXIAB,FXIDAT=HXIAB,NBJFF10=NBJFF10,NBJFF16=NBJFF16,NBJFF28=NBJFF28,FXYAB=FXYAB,DXYAB=DXYAB,FXYABDAT=FXYABDAT,NBJFXY8=NBJFXY8,NBJFXY10=NBJFXY10,NBJFXY15=NBJFXY15,INST=INST).save()
                    break