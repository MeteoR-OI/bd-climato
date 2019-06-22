import datetime

from django.db.models import Sum,Avg

from gestion.models import POSTE,INSTAN,H,Q,MENSQ


        

# On initialise la table INSTAN
def initDonnees(nom, CODE_POSTE):
        # On récupère le fichier enregistré
        link =  nom
        #On l'ouvre, on le lit ligne par ligne et on injecte les données dans 
        #la table INSTAN
        with open(link, "r") as f:
            lignes = f.readlines()
            for ligne in lignes:
                #Récupération des données pour chaque ligne
                #ligne = ligne.replace('\\N', np.nan)
                #ligne = ligne.replace('NULL','\N')
                
                l = ligne.split(',')
                l = [None if element == '\\N' else element for element in l]
                
                dateTime = int(str(l[0]).replace('"',''))
                
                interval = str(l[2]).replace('"','')
                barometer = str(l[3]).replace('"','')
               
                barometer = convert(barometer)
                pressure = str(l[4]).replace('"','')
                altimeter = str(l[5]).replace('"','')
                outTemp = str(l[7]).replace('"','')
                outTemp = convert(outTemp)
                outHumidity = str(l[9]).replace('"','')
                outHumidity = convert(outHumidity)
                windSpeed = str(l[10]).replace('"','')
                windSpeed = convert(windSpeed)
                windDir = str(l[11]).replace('"','')
                windDir = convert(windDir)
                windGust = str(l[12]).replace('"','')
                windGust = convert(windGust)
                windGustDir = str(l[13]).replace('"','')
                windGustDir = convert(windGustDir)
                rainRate = str(l[14]).replace('"','')
                rainRate = convert(rainRate)
                rain = str(l[15]).replace('"','')
                rain = convert(rain)
                dewpoint = str(l[16]).replace('"','')
                dewpoint = convert(dewpoint)
                windchill = str(l[17]).replace('"','')
                windchill = convert(windchill)
                heatindex = str(l[18]).replace('"','')
                heatindex = convert(heatindex)
                
                try:
                    radiation = str(l[20]).replace('"','')
                    radiation = convert(radiation)
                    ET= str(l[19]).replace('"','')
                    ET = convert(ET)
                except:
                    radiation = None
                    ET = None
                
                try:
                    UV= str(l[21]).replace('"','')
                    UV = convert(UV)
                except: 
                    UV = None
                try:
                    soilTemp = str(l[25]).replace('"','')
                    soilTemp = convert(soilTemp)
                    leafTemp = str(l[29]).replace('"','')
                    leafTemp = convert(leafTemp)
                    leafWet =str(l[33]).replace('"','')
                    leafWet = convert(leafWet)
                except:
                    soilTemp = None
                    leafTemp = None
                    leafWet = None
                
                
                #Traitement des données
                dateTime = datetime.datetime.fromtimestamp(dateTime) #Conversion du temps unix
                dateTime = (dateTime + datetime.timedelta(hours=4)) \
                .strftime('%Y-%m-%d %H:%M:%S')

                # Injection de toutes les donnees dans la table INS
                postes = POSTE.objects.get(CODE_POSTE = CODE_POSTE)
                INSTAN.objects.get_or_create(POSTE = postes, 
                                             DATJ = dateTime, RR = rain*10,
                RRI = rainRate*10, FF = windSpeed, 
                DD = windDir, FXI = windGust, 
                DXI = windGustDir, T = outTemp, 
                TD = dewpoint, U = outHumidity, 
                PMER = barometer, UV = UV, RAD = radiation,
                IC = heatindex, WINDCHILL = windchill,
                ETP = ET, HF = leafWet, TS = soilTemp)
                  
        #On initialise les données horaires        
 
def convert(value):
    if value is None:
        return value
    try:
        return round(float(value),2)
    except:
        return None 
          
def initH(nom_poste, datedeb=0, datefin=0, perte=0):
    #code = 0 : initialisation / perte de donnees
    #code = 1 : MAJ automatique des dernieres donnees

    #Récupération des données 
    poste = POSTE.objects.get(CODE_POSTE = nom_poste)

    # Préparer les options pour la requête
    ins_query_options = {
        'POSTE'         : poste,
        'DATJ__minute'  : 0,
    }

    ins = INSTAN.objects.filter(**ins_query_options)

    # Datedeb est utilisée pour la récupération des données afin d'éviter
    #   le traitement de données non indispensables.
    if datedeb==0:
        # Par défaut, ce code est appelé pour l'initialisation
        fin = ins.order_by('-DATJ')[0].DATJ
        deb = ins.order_by('DATJ')[0].DATJ
        creneau = False
    else:
        deb = datedeb
        fin = datefin
        creneau = True

        ins_query_options.update({
            'DATJ__gte' : deb,
            'DATJ__lte' : fin
        })

    # Filter sur les heures fixes (1h00, 2h00, ....) et l'intervalle voulu
    ins = INSTAN.objects.filter(**ins_query_options).order_by('-DATJ')

    #On parcourt toutes les données instantanées
    for i in range(0,ins.count()):
        #Lorsqu'une nouvelle heure est rencontrée
        if ins[i].DATJ.time().minute == 0 and ins[i].DATJ <= fin \
            and ins[i].DATJ >= deb:

            filtre = ins.filter(DATJ__gte = ins[i].DATJ,
                                DATJ__lt =  ins[i].DATJ + datetime.timedelta(hours=1))
            filtreRR = ins.filter(DATJ__gt = ins[i].DATJ - datetime.timedelta(hours=1),
                                  DATJ__lte = ins[i].DATJ)
            filtreVent = ins.filter(DATJ__gte = ins[i].DATJ  + datetime.timedelta(seconds=600),
                                    DATJ__lte = ins[i].DATJ + datetime.timedelta(hours=1))

            #Pour les premieres données
            if i <= ins.count()-2:
                PDT = ((ins[i].DATJ-ins[i+1].DATJ).total_seconds())/60
#                 print(ins[i-1].DATJ,ins[i].DATJ,(ins[i-1].DATJ-ins[i].DATJ).total_seconds())
            else: 
                PDT = ((ins[ins.count()-2].DATJ - ins[ins.count()-1].DATJ).total_seconds())/60
            
            
            #On parcourt les données de l'heure voulue en les traitant  
            Ventmoyen = filtreVent.order_by('-FF')[0]
            FXY, DXY, HXY = Ventmoyen.FF, Ventmoyen.DD, Ventmoyen.DATJ
            Rafales = filtreVent.order_by('-FXI')[0]
            FXI, DXI, HXI  = Rafales.FXI, Rafales.DXI, Rafales.DATJ
            cumulRR = float(filtreRR.aggregate(Sum('RR'))['RR__sum'])
            DRR1 = (filtreRR.filter(RR__gt=0).count())*PDT
            INST = (filtre.filter(RAD__gt=0).count())*PDT
            PluieInstan = filtreRR.order_by('-RRI')[0]
            RRI, HRRI = PluieInstan.RRI, PluieInstan.DATJ
            Tempemini = filtre.order_by('T')[0]
            TN,HTN = Tempemini.T, Tempemini.DATJ
            Tempemaxi = filtre.order_by('-T')[0]
            TX, HTX = Tempemaxi.T, Tempemaxi.DATJ
            Humiditemini = filtre.order_by('U')[0]
            UN,HUN = Humiditemini.U,Humiditemini.DATJ
            Humiditemaxi = filtre.order_by('-U')[0]
            UX, HUX = Humiditemaxi.U,Humiditemaxi.DATJ
            Pmermini = filtre.order_by('PMER')[0]
            PMERMIN, HPMERMIN = Pmermini.PMER, Pmermini.DATJ
            ETPX = filtre.order_by('-ETP')[0].ETP
            ETPN = filtre.order_by('ETP')[0].ETP
            HFX = filtre.order_by('-HF')[0].HF
            HFN = filtre.order_by('HF')[0].HF
            HSX = filtre.order_by('-HS')[0].HS
            HSN = filtre.order_by('HS')[0].HS
            TSX = filtre.order_by('-TS')[0].TS
            TSN = filtre.order_by('TS')[0].TS
            
            
                        
            recu,created = H.objects.get_or_create(POSTE = poste, DATJ = ins[i].DATJ)
            #if created:                                       
            H.objects.filter(POSTE = poste, DATJ = ins[i].DATJ).update( 
                  STATUS_DRR1 = 2, 
                  RR1 = cumulRR, RRI = RRI, HRRI = HRRI, FF = ins[i].FF,
                  DD = ins[i].DD, FXY = FXY, DXY =DXY , HXY = HXY,
                  FXI = FXI, DXI = DXI, HXI = HXI, T = ins[i].T,
                  TD = ins[i].TD, TN = TN, HTN = HTN, TX = TX, HTX = HTX, 
                  U = ins[i].U, UN = UN, HUN = HUN, UX = UX, HUX = HUX,
                  PMER=ins[i].PMER, PMERMIN = PMERMIN, HPERMIN = HPMERMIN,
                  UV = ins[i].UV, RAD=ins[i].RAD, IC = ins[i].IC,
                  WINDCHILL = ins[i].WINDCHILL, ETP = ins[i].ETP,
                  ETPX = ETPX, ETPN = ETPN, HF = ins[i].HF, HFX = HFX, HFN = HFN,
                  HS = ins[i].HS, HSX = HSX, HSN = HSN, TS = ins[i].TS, TSX = TSX,
                  TSN = TSN, INST = INST, DRR1 = DRR1)
#             else: 
#             
#                 recu,____ = H.objects.get(POSTE = poste, DATJ = ins[i].DATJ)
#                 recu.STATUS_DRR1 = 2
#                 recu.RR1 =cumulRR
#                 recu.RRI=RRI
#                 recu.HRRI=HRRI
#                 recu.FF=ins[i].FF
#                 recu.DD=ins[i].DD
#                 recu.FXY=FXY
#                 recu.DXY=DXY
#                 recu.HXY=HXY
#                 recu.FXI=FXI
#                 recu.DXI=DXI
#                 recu.HXI=HXI
#                 recu.T= ins[i].T
#                 recu.TD=ins[i].TD
#                 recu.TN=TN
#                 recu.HTN=HTN
#                 recu.TX=TX
#                 recu.HTX=HTX
#                 recu.U=ins[i].U
#                 recu.UN=UN
#                 recu.HUN=HUN
#                 recu.UX=UX
#                 recu.HUX=HUX
#                 recu.PMER=ins[i].PMER
#                 recu.PMERMIN=PMERMIN
#                 recu.HPERMIN=HPMERMIN
#                 recu.UV=ins[i].UV
#                 recu.RAD=ins[i].RAD
#                 recu.IC=ins[i].IC
#                 recu.WINDCHILL=ins[i].WINDCHILL
#                 recu.ETP=ins[i].ETP
#                 recu.ETPX=ETPX
#                 recu.ETPN=ETPN
#                 recu.HF=ins[i].HF
#                 recu.HFX=HFX
#                 recu.HFN=HFN
#                 recu.HS=ins[i].HS
#                 recu.HSX=HSX
#                 recu.HSN=HSN
#                 recu.TS=ins[i].TS
#                 recu.TSX=TSX
#                 recu.TSN=TSN
#                 recu.INST=INST
#                 recu.DRR1=DRR1
#                  
#                 recu.save()
#                     

def initQ(nom_poste, datedeb=0, datefin=0,perte=0):

    #Récupération des données 
    poste = POSTE.objects.get(CODE_POSTE=nom_poste)
    ins = H.objects.filter(POSTE=poste).order_by('-DATJ') 
    if datedeb == 0:
        fin = ins[0].DATJ
        deb = ins[ins.count()-1].DATJ
        creneau = False
    else:
        deb = datedeb
        fin = datefin
        creneau = True
    
               
    for i in range(0, ins.count()): 
        if ins[i].DATJ.time().hour == 0 and \
         ins[i].DATJ.time().minute == 0 and ins[i].DATJ >= deb \
          and ins[i].DATJ <= fin:                    
            filtre = ins.filter(DATJ__gte = ins[i].DATJ, 
                                DATJ__lt = ins[i].DATJ + 
                                datetime.timedelta(days=1)) 
            filtreRR = ins.filter(DATJ__gt = ins[i].DATJ, 
                                DATJ__lte = ins[i].DATJ  + 
                                datetime.timedelta(days=1))
            
            #On parcourt les données de l'heure voulue en les traitant  
            
            
            
            cumulRR = float(filtreRR.aggregate(Sum('RR1'))['RR1__sum'])
            DRR = float(filtreRR.aggregate(Sum('DRR1'))['DRR1__sum'])
            TM = float(filtre.aggregate(Avg('T'))['T__avg'])
            PMERM = float(filtre.aggregate(Avg('PMER'))['PMER__avg'])
            UM = float(filtre.aggregate(Avg('U'))['U__avg'])
            try:
                INST = float(filtre.aggregate(Sum('INST'))['INST__sum'])
            except :
                INST = None
            try:            
                ETPM = float(filtre.aggregate(Avg('ETP'))['ETP__avg'])
                ETPX = filtre.order_by('-ETP')[0].ETP
                ETPN = filtre.order_by('ETP')[0].ETP
            except:
                ETPM = None
                ETPX = None
                ETPN = None
            try:
                HFM = float(filtre.aggregate(Avg('HF'))['HF__avg'])
                HFX = filtre.order_by('-HF')[0].HF
                HFN = filtre.order_by('HF')[0].HF
                HSM = float(filtre.aggregate(Avg('HS'))['HS__avg'])
                HSX = filtre.order_by('-HS')[0].HS
                HSN = filtre.order_by('HS')[0].HS
                TSM = float(filtre.aggregate(Avg('TS'))['TS__avg'])
                TSX = filtre.order_by('-TS')[0].TS
                TSN = filtre.order_by('TS')[0].TS
            except:
                HFM = None
                HFX = None
                HFN = None
                HSM = None
                HSX = None
                HSN = None
                TSM = None
                TSX = None
                TSN = None
            Tempemini = filtre.order_by('T')[0]
            TN,HTN = Tempemini.T, Tempemini.DATJ
            Tempemaxi = filtre.order_by('-T')[0]
            TX, HTX = Tempemaxi.T, Tempemaxi.DATJ
            Pmermini = filtre.order_by('PMER')[0]
            PMERMIN= Pmermini.PMER
            Humiditemini = filtre.order_by('U')[0]
            UN,HUN = Humiditemini.U,Humiditemini.DATJ
            Humiditemaxi = filtre.order_by('-U')[0]
            UX, HUX = Humiditemaxi.U,Humiditemaxi.DATJ
            Ventmoyen = filtre.order_by('-FF')[0]
            FXY, DXY, HXY = Ventmoyen.FF, Ventmoyen.DD, Ventmoyen.DATJ
            Rafales = filtre.order_by('-FXI')[0]
            FXI, DXI, HXI  = Rafales.FXI, Rafales.DXI, Rafales.DATJ
            DG = filtre.filter(T__lte=0).count()
             

            recu,created = Q.objects.get_or_create(POSTE = poste, DATJ = ins[i].DATJ)
#             if created: 
            Q.objects.filter(POSTE = poste, DATJ = ins[i].DATJ).update(RR = cumulRR, DRR = DRR,
              STATUS_DRR = 2, TN = TN, HTN = HTN, TX = TX, HTX = HTX, 
              TM = TM, DG = DG, PMERM = PMERM, 
              PMERMIN = PMERMIN, FXY = FXY, DXY = DXY, HXY = HXY, FXI = FXI,
              DXI = DXI, HXI = HXI, UM = UM, UN = UN, HUN = HUN, UX = UX,
              HUX = HUX, ETPM = ETPM, HFM = HFM, HFMX = HFX, HFMN = HFN,
              HSM = HSM, HSMN = HSN, HSMX = HSX, INST = INST, TS = TSM, 
              TSX = TSX, TSN = TSN)   
#             else:
#                 recu,____ = Q.objects.get_or_create(POSTE = poste, DATJ = ins[i].DATJ)
#                 recu.RR=cumulRR
#                 recu.DRR=DRR
#                 recu.STATUS_DRR=2
#                 recu.TN=TN
#                 recu.HTN=HTN
#                 recu.TX=TX
#                 recu.HTX=HTX
#                 recu.TM=TM
#                 recu.TAMPLI=TX-TN
#                 recu.DG=DG
#                 recu.PMERM=PMERM
#                 recu.PMERMIN=PMERMIN
#                 recu.FXY=FXY
#                 recu.DXY=DXY
#                 recu.HXY=HXY
#                 recu.FXI=FXI
#                 recu.DXI=DXI
#                 recu.HXI=HXI
#                 recu.UM=UM
#                 recu.UN=UN
#                 recu.HUN=HUN
#                 recu.UX=UX
#                 recu.HUX=HUX
#                 recu.ETPM=ETPM
#                 recu.HFM=HFM
#                 recu.HFMX=HFX
#                 recu.HFMN=HFN
#                 recu.HSM=HSM
#                 recu.HSMN=HSN
#                 recu.HSMX=HSX
#                 recu.INST=INST
#                 recu.TS=TSM
#                 recu.TSX=TSX
#                 recu.TSN = TSN  
#                 recu.save()
                 


        
def initMensQ(nom_poste, datedeb=0, datefin=0,perte=0):   
     #Récupération des données 
    
    poste = POSTE.objects.get(CODE_POSTE = nom_poste) 
    q = Q.objects.filter(POSTE = poste).order_by('-DATJ')
     
    if datedeb == 0:
        fin = q[0].DATJ
        deb = q[q.count()-1].DATJ
        creneau = False
    else:
        deb = datedeb
        fin = datefin
        creneau = True
    for i in range(0,q.count()): 
        
        
 
            
        if q[i].DATJ.day == 1 and q[i].DATJ >= deb \
          and q[i].DATJ <= fin:
            
            if q[i].DATJ.month == 12:
                annee = q[i].DATJ.year + 1
                mois = 1
            else : 
                annee = q[i].DATJ.year
                mois =  q[i].DATJ.month+1       
            filtre = q.filter(DATJ__lt = datetime.datetime(annee,mois,1),
                              DATJ__gte = q[i].DATJ )
            
              
            cumulRR = float(filtre.aggregate(Sum('RR'))['RR__sum'])
            PMERM = float(filtre.aggregate(Avg('PMERM'))['PMERM__avg'])
            TN = float(filtre.aggregate(Avg('TN'))['TN__avg'])
            TX = float(filtre.aggregate(Avg('TX'))['TX__avg'])
            UMM = float(filtre.aggregate(Avg('UM'))['UM__avg'])
            try:
                INST = float(filtre.aggregate(Sum('INST'))['INST__sum'])
            except :
                INST = None
            Humiditemini = filtre.order_by('UN')[0]
            UNAB,UNABDAT = Humiditemini.UN,Humiditemini.DATJ
            Humiditemaxi = filtre.order_by('-UX')[0]
            UXAB,UXABDAT = Humiditemini.UX,Humiditemaxi.DATJ   
            NBJGELEE = filtre.filter(TN__lte=0).count()
            NBJTN5 = filtre.filter(TN__lte=-5).count()
            NBJTNI10 = filtre.filter(TN__lte=10).count()
            NBJTNI15 = filtre.filter(TN__lte=15).count()
            NBJTNI20 = filtre.filter(TN__lte=20).count()
            NBJTNS20 = filtre.filter(TN__gte=20).count()
            NBJTNS25 = filtre.filter(TN__gte=25).count()    
            Tempemini = filtre.order_by('TN')[0]
            TNAB,TNDAT = Tempemini.TN, Tempemini.DATJ
            Tempeminimaxi = filtre.order_by('-TN')[0]
            TNMAX, TNMAXDAT = Tempeminimaxi.TN, Tempeminimaxi.DATJ    
            Pmermini = filtre.order_by('PMERM')[0]
            PMERMINAB, PMERMINABDAT= Pmermini.PMERM, Pmermini.DATJ
            Precipmax = filtre.order_by('-RR')[0]
            RRAB, RRABDAT= Precipmax.RR, Precipmax.DATJ
            NBJRR1 = filtre.filter(RR__gte=1).count()
            NBJRR5 = filtre.filter(RR__gte=5).count()
            NBJRR10 = filtre.filter(RR__gte=10).count()
            NBJRR30 = filtre.filter(RR__gte=30).count()
            NBJRR50 = filtre.filter(RR__gte=50).count()
            NBJRR100 = filtre.filter(RR__gte=100).count()    
            Tempemaxi = filtre.order_by('-TX')[0]
            TXAB,TXABDAT = Tempemaxi.TX, Tempemaxi.DATJ
            Tempemaximini = filtre.order_by('TX')[0]
            TXMIN, TXMINDAT = Tempemaximini.TX, Tempemaximini.DATJ
            NBJTX0 = filtre.filter(TX__lte=0).count() 
            NBJTX25 = filtre.filter(TX__gte=25).count()
            NBJTX30 = filtre.filter(TX__gte=30).count()
            NBJTX32 = filtre.filter(TX__gte=32).count()
            NBJTX35 = filtre.filter(TX__gte=35).count()
            NBJTXI20 = filtre.filter(TX__lte=20).count()
            NBJTXI27 = filtre.filter(TX__lte=27).count()
            Rafales = filtre.order_by('-FXI')[0]
            FXIAB, DXIAB, HXIAB  = Rafales.FXI, Rafales.DXI, Rafales.DATJ
            Ventmoyen = filtre.order_by('-FXY')[0]
            FXYAB, DXYAB, FXYABDAT = Ventmoyen.FXY, Ventmoyen.DXY, Ventmoyen.DATJ
            NBJFF10 = filtre.filter(FXI__gte=36).count()
            NBJFF16 = filtre.filter(FXI__gte=57.6).count()
            NBJFF28 = filtre.filter(FXI__gte=100.8).count()
            NBJFXY8 = filtre.filter(FXY__gte=28.8).count()
            NBJFXY10 = filtre.filter(FXY__gte=36).count()
            NBJFXY15 = filtre.filter(FXY__gte=54).count()
            
            
            recu,created = MENSQ.objects.get_or_create(POSTE = poste, DATJ = q[i].DATJ)
#             if created: 
            MENSQ.objects.filter(POSTE = poste, DATJ = q[i].DATJ).update( 
                                        RR = cumulRR, STATUS_DRR = 2,
                  RRAB = RRAB, STATUS_RRAB = 2, RRABDAT = RRABDAT, 
                  NBJRR1 = NBJRR1, NBJRR5 = NBJRR5, NBJRR10 = NBJRR10, 
                  NBJRR30 = NBJRR30, NBJRR50 = NBJRR50, NBJRR100 = NBJRR100,
                  PMERM = PMERM, PMERMINAB = PMERMINAB, 
                  PMERMINABDAT = PMERMINABDAT, TX = TX, TXAB = TXAB,
                  TXABDAT = TXABDAT, TXMIN = TXMIN, TXMINDAT = TXMINDAT,
                  NBJTX0 = NBJTX0, NBJTX25 = NBJTX25, NBJTX30 = NBJTX30,
                  NBJTX32 = NBJTX32, NBJTX35 = NBJTX35, NBJTXI20 = NBJTXI20,
                  NBJTXI27 = NBJTXI27, TN = TN, TNAB = TNAB, TNDAT = TNDAT,
                  TNMAX = TNMAX, TNMAXDAT = TNMAXDAT, NBJTN5 = NBJTN5,
                  NBJTNI10 = NBJTNI10, NBJTNI15 = NBJTNI15, NBJTNI20 = NBJTNI20,
                  NBJTNS20 = NBJTNS20, NBJTNS25 = NBJTNS25, NBJGELEE = NBJGELEE,
                  UNAB = UNAB, UNABDAT = UNABDAT, UXAB = UXAB, 
                  UXABDAT = UXABDAT, FXIAB = FXIAB, DXIAB = DXIAB, 
                  FXIDAT = HXIAB, NBJFF10 = NBJFF10, NBJFF16 = NBJFF16,
                  NBJFF28 = NBJFF28, FXYAB = FXYAB, DXYAB = DXYAB, 
                  FXYABDAT = FXYABDAT, NBJFXY8 = NBJFXY8, NBJFXY10 = NBJFXY10,
                  NBJFXY15 = NBJFXY15, INST = INST)
#             else:
#                 recu,____ = MENSQ.objects.get_or_create(POSTE = poste, DATJ = q[i].DATJ)
#       
#                 recu.RR = cumulRR
#                 recu.STATUS_DRR = 2
#                 recu.RRAB = RRAB
#                 recu.STATUS_RRAB = 2
#                 recu.RRABDAT = RRABDAT
#                 recu.NBJRR1 = NBJRR1
#                 recu.NBJRR5 = NBJRR5
#                 recu.NBJRR10 = NBJRR10
#                 recu.NBJRR30 = NBJRR30
#                 recu.NBJRR50 = NBJRR50
#                 recu.NBJRR100 = NBJRR100
#                 recu.PMERM = PMERM
#                 recu.PMERMINAB = PMERMINAB 
#                 recu.PMERMINABDAT = PMERMINABDAT
#                 recu.TX = TX
#                 recu.TXAB = TXAB
#                 recu.TXABDAT = TXABDAT
#                 recu.TXMIN = TXMIN
#                 recu.TXMINDAT = TXMINDAT
#                 recu.NBJTX0 = NBJTX0
#                 recu.NBJTX25 = NBJTX25
#                 recu.NBJTX30 = NBJTX30
#                 recu.NBJTX32 = NBJTX32
#                 recu.NBJTX35 = NBJTX35
#                 recu.NBJTXI20 = NBJTXI20
#                 recu.NBJTXI27 = NBJTXI27
#                 recu.TN = TN
#                 recu.TNAB = TNAB
#                 recu.TNDAT = TNDAT
#                 recu.TNMAX = TNMAX
#                 recu.TNMAXDAT = TNMAXDAT
#                 recu.NBJTN5 = NBJTN5,
#                 recu.NBJTNI10 = NBJTNI10
#                 recu.NBJTNI15 = NBJTNI15
#                 recu.NBJTNI20 = NBJTNI20
#                 recu.NBJTNS20 = NBJTNS20
#                 recu.NBJTNS25 = NBJTNS25
#                 recu.NBJGELEE = NBJGELEE
#                 recu.UNAB = UNAB
#                 recu.UNABDAT = UNABDAT
#                 recu.UXAB = UXAB 
#                 recu.UXABDAT = UXABDAT
#                 recu.FXIAB = FXIAB
#                 recu.DXIAB = DXIAB 
#                 recu.FXIDAT = HXIAB
#                 recu.NBJFF10 = NBJFF10
#                 recu.NBJFF16 = NBJFF16
#                 recu.NBJFF28 = NBJFF28
#                 recu.FXYAB = FXYAB
#                 recu.DXYAB = DXYAB 
#                 recu.FXYABDAT = FXYABDAT
#                 recu.NBJFXY8 = NBJFXY8
#                 recu.NBJFXY10 = NBJFXY10
#                 recu.NBJFXY15 = NBJFXY15
#                 recu.INST = INST
#                 recu.save()
           