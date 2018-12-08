

import datetime, os
import matplotlib 
import matplotlib.dates as dates
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from decimal import Decimal
from windrose import WindroseAxes

from django.conf import settings
from django.db.models import Sum, Min, Max, Avg
from django.shortcuts import render, redirect

from gestion.management.commands import init
from gestion.models import INSTAN,POSTE,PAYS,COMMUNE,H,Q,INSTRUMENT,MENSQ,Files,RECMENS,EVENEMENTS,POSTE_EVENEMENTS
from .forms import InitFormPays,InitPoste,UploadFileForm,InitPosteTotal


data_dir = 'media/data/'

def home(request):
    choixevenement = False
    postes = POSTE.objects.all()
    liste = []
    liste_type_ev = ['Cyclone','Front froid','Pluvio-orageux','Canicule','Autre']
    for p in postes:
        liste+=[p.CODE_POSTE]
        
    evenement = EVENEMENTS.objects.all()
    liste_evenement = []
    for p in evenement:
        liste_evenement+=[p.NOM_EVENEMENT]
         
    try:
        code = request.POST['codeposte_instrument']
        return redirect("InfoPoste/"+code+"/Autre/T/",code=302)
    except: 
        pass
    try:
        code = request.POST['codeposte_instan']
        return redirect("station/"+code,code=302)
    except: 
        pass    
    try:
        code = request.POST['codeposte_recapj']
        return redirect("recap/J/"+code,code=302)
    except: 
        pass      
    try:
        code = request.POST['codeposte_recapm']
        return redirect("recap/M/"+code,code=302)
    except: 
        pass 
    try:
        code = request.POST['codeposte_rapportm']
        mois = request.POST['rapportmois']
        annee = request.POST['rapportmoisannee']
        return redirect("rapport/M/"+str(mois)+"_"+str(annee)+"/"+code,code=302)
    except: 
        pass 
    try:
        code = request.POST['codeposte_rapporta']
        annee = request.POST['rapportannee']
        return redirect("rapport/A/"+str(annee)+"/"+code,code=302)
    except: 
        pass 
    
    #ajout d'evenements
    try:
        nom_evenement = request.POST['nom_evenement']
        type_evenement = request.POST['type_evenement']
        date_debut = request.POST['debut_evenement']
        date_debut = date_debut.split(' ')
        jour_debut = date_debut[1].split('/')
        hr_debut = date_debut[0].split(':')
        date_fin = request.POST['fin_evenement']
        date_fin = date_fin.split(' ')
        jour_fin = date_fin[1].split('/')
        hr_fin = date_fin[0].split(':')
        
        EVENEMENTS(NOM_EVENEMENT=nom_evenement,TYPE_EVENEMENT = type_evenement, DEBUT=datetime.datetime(int(jour_debut[2]),int(jour_debut[1]),int(jour_debut[0]),int(hr_debut[0]),int(hr_debut[1])),
                   FIN=datetime.datetime(int(jour_fin[2]),int(jour_fin[1]),int(jour_fin[0]),int(hr_fin[0]),int(hr_fin[1]))
                   ).save()
        
    except:
        pass
    
    #ajout de postes à un évènement
    try:
        nom_evenementposte = request.POST['nom_evenementposte']
        codeposte_evenement = request.POST['codeposte_evenement']
        poste = POSTE.objects.get(CODE_POSTE=codeposte_evenement)
        ev = EVENEMENTS.objects.get(NOM_EVENEMENT=nom_evenementposte) 
        POSTE_EVENEMENTS(POSTE=poste, EVENEMENTS=ev).save()
    except: 
        pass
    
    #page d'affichage récap d'un évènement sélectionné
    try:
        affichage_evenement = request.POST['affichage_evenement']
        nom_evenement_choisi = affichage_evenement
        ev = EVENEMENTS.objects.get(NOM_EVENEMENT=affichage_evenement)
        debut_evenement_choisi = ev.DEBUT.strftime('%d/%m/%Y à %Hh%M')
        fin_evenement_choisi = ev.FIN.strftime('%d/%m/%Y à %Hh%M')
        choixevenement = True
        liste_evenement_poste = []
        postes = POSTE_EVENEMENTS.objects.filter(EVENEMENTS=ev)
        for poste in postes:
            liste_evenement_poste +=[poste.POSTE.CODE_POSTE]
        
    except: 
        pass
    
    try:
        converti = False
       
        codeposte_extraction = request.POST['codeposte_extraction']
        poste = POSTE.objects.get(CODE_POSTE=codeposte_extraction)
        
        debutextraction = request.POST['debutextraction']
        debutextraction = debutextraction.split(' ')
        hrdebut = debutextraction[0].split(':')
        jrdebut = debutextraction[1].split('/')
        debut = datetime.datetime(int(jrdebut[2]),int(jrdebut[1]),int(jrdebut[0]),int(hrdebut[0]),int(hrdebut[1]))
        
        finextraction = request.POST['finextraction']
        finextraction = finextraction.split(' ')
        hrfin = finextraction[0].split(':')
        jrfin = finextraction[1].split('/')
        fin = datetime.datetime(int(jrfin[2]),int(jrfin[1]),int(jrfin[0]),int(hrfin[0]),int(hrfin[1]))
        
        link = '%s/export'+codeposte_extraction+"_"+str(jrdebut[0])+str(jrdebut[1])+str(jrdebut[2])+"-"+str(jrfin[0])+str(jrfin[1])+str(jrfin[2])+'.csv' % settings.MEDIAT_ROOT
        
        
        
        inst = INSTAN.objects.filter(POSTE=poste,DATJ__gte=debut,DATJ__lte=fin)
        entetes = [
                 u'DAT',
                 u'RR',
                 u'RRI',
                 u'FF',
                 u'DD',
                 u'FXI',
                 u'DXI',
                 u'T',
                 u'TD',
                 u'U',
                 u'PMER',
                 u'UV',
                 u'RAD',
                 u'IC',
                 u'WINDCHILL',
        
            ]
        
        
        f = open(link, 'w')
        ligneEntete = ";".join(entetes) + "\n"
        f.write(ligneEntete)
        
        
        for ins in inst:
            valeurs = [ins.DATJ.strftime('%d/%m/%Y-%H:%M'), str(ins.RR)
                       , str(ins.RRI), str(ins.FF), str(ins.DD), str(ins.FXI)
                       , str(ins.DXI), str(ins.T), str(ins.TD), str(ins.U)
                       , str(ins.PMER), str(ins.UV), str(ins.RAD), str(ins.IC)
                       , str(ins.WINDCHILL)]
            
            ligne = ";".join(valeurs) + "\n"
            f.write(ligne)
        f.close()
        converti = True
    except: 
        pass
        
    
        
    return render(request, 'accueil.html', locals())
    
    

#------------------------------------------------------------------------------
#-------------------------------------INITIALISATION DE DONNEES----------------
#------------------------------------------------------------------------------

#Toutes les fonctions ci-dessous ont pour but l'initialisation complète 
#d'une station à partir du formulaire sur la page initialisation.



def initPays(request): 
    
    #On initialise le formulaire   
    form = InitFormPays(request.POST or None, request.FILES or None)
    # Nous vérifions que les données envoyées sont valides.
    if form.is_valid(): 
        nompays = form.cleaned_data['NOM_DU_PAYS']
        if nompays == 'France':
            codpays = 1
        elif nompays == 'Reunion' :
            codpays = 2
        else:
            codpays = 0
        #Si le pays existe déjà, on ne le recrée pas.    
        PAYS.objects.get_or_create(NOMPAYS=nompays,CODPAYS=codpays)
        nomcommune = form.cleaned_data['NOM_DE_LA_COMMUNE']
        pays = PAYS.objects.get(NOMPAYS=nompays)
        COMMUNE.objects.get_or_create(NOMCOMMUNE=nomcommune,PAYS=pays)
        CP = form.cleaned_data['CODE_POSTAL']
        CODE_POSTE = form.cleaned_data['CODE_POSTE']
        
        lien = form.cleaned_data['lien']
        if lien == None :
            archive = False
        else:
            archive = True
            
        print(archive)
        REF_MF = form.cleaned_data['REFERENCE_METEO_FRANCE']
       
        PDT = form.cleaned_data['PDT']
        NOM = form.cleaned_data['NOM_PUBLIQUE']
        LAT = form.cleaned_data['LATITUDE']
        LON = form.cleaned_data['LONGITUDE']
        ALT = form.cleaned_data['ALTITUDE']
        POS = form.cleaned_data['PERSONNE']
        AUT = form.cleaned_data['AUTORISATION']
        PROP = form.cleaned_data['PROPRIETAIRE']
        DATEOUV = form.cleaned_data['DATE_ET_HEURE_OUVERTURE']
        MAINT = form.cleaned_data['MAINTENANCE']
        TYPE = form.cleaned_data['TYPE']
        TYPINFO = form.cleaned_data['TYPE_D_INFORMATIONS']
        ADRESSE = form.cleaned_data['ADRESSE']
        LIEU_DIT = form.cleaned_data['LIEU_DIT']
        MEL = form.cleaned_data['MEL']
        TEL = form.cleaned_data['TEL']
        COMM = form.cleaned_data['COMMS']
        commune = COMMUNE.objects.get(NOMCOMMUNE=nomcommune)
        if TYPE != 'SPIEA' and archive == True:
            print('jsuis la')
            POSTE(CP = CP, CODE_POSTE = CODE_POSTE, REF_MF = REF_MF, 
                  DATEOUV = DATEOUV, NOM = NOM, LAT = LAT, LON = LON, ALT = ALT, 
                  POS = POS, AUT = AUT, PROP = PROP, MAINT = MAINT, TYPE = TYPE, 
                  TYPINFO = TYPINFO, ADRESSE = ADRESSE, LIEU_DIT = LIEU_DIT, 
                  MEL = MEL, TEL = TEL, COMM = COMM, COMMUNE = commune,INIT=0,PDT=PDT).save()
            poste = POSTE.objects.get(CODE_POSTE = CODE_POSTE)
            c = Files(POSTE = poste, lien = lien)
            c.save()
            #link servira à récupérer le fichier archive de la station
            #dans les dossiers
            link = str(c.lien.path)
            link = link.split('\\')[-1]
            link = link.split('.')[0]             
            #Initialisation des tables       
            init.initDonnees(link,CODE_POSTE) 
            init.initH(CODE_POSTE)
            init.initQ(CODE_POSTE)
            init.initMensQ(CODE_POSTE)
            #init = 1 autorise l'automatisation de la récupération
            poste.INIT = 1
            poste.save()
            #Une fois que toutes les tables seront initialisées, on redirige
            #vers la page d'initialisation des instruments.
            return redirect("../InfoPoste/" + CODE_POSTE + '/' + 
                            TYPE + '/T/', code=302)
        else: 
            POSTE(CP = CP, CODE_POSTE = CODE_POSTE, REF_MF = REF_MF, 
                  DATEOUV = DATEOUV, NOM = NOM, LAT = LAT, LON = LON, ALT = ALT, 
                  POS = POS, AUT = AUT, PROP = PROP, MAINT = MAINT, TYPE = TYPE, 
                  TYPINFO = TYPINFO, ADRESSE = ADRESSE, LIEU_DIT = LIEU_DIT, 
                  MEL = MEL, TEL = TEL, COMM = COMM, COMMUNE = commune, INIT=1, PDT = PDT).save()
            
        envoi = True
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'initialisation.html', locals())




   
#Table des records    
def initRecMens(nom_poste):
    poste = POSTE.objects.get(CODE_POSTE=nom_poste)
    mensq = MENSQ.objects.filter(POSTE=poste).order_by('DATJ') 
    
    mois_dispo = []
    for value in mensq:
        mois_dispo+=[value.DATJ.month]    
    mois_dispo = list(set(mois_dispo))
    
    print(mois_dispo)
    for mois in range(1,13):
        if mois in mois_dispo:
            TX = -30
            TXDAT = None
            TN = 50
            TNDAT = None
            for i in range(0,mensq.count()):   
    
                    
                if mensq[i].DATJ.month == mois: 
                            
                        if mensq[i].TXAB > TX:
                            TX=mensq[i].TXAB
                            TXDAT=mensq[i].TXABDAT
                        if mensq[i].TNAB < TN:
                            TN=mensq[i].TNAB
                            TNDAT=mensq[i].TNDAT
                    
                   
            RECMENS(POSTE = poste, PARAM = 'TX', NUM_MOIS = mensq[i].DATJ.month, 
                    RECORD = TX, DATERECORD = TXDAT).save()
            RECMENS(POSTE = poste, PARAM = 'TN', NUM_MOIS = mensq[i].DATJ.month,
                    RECORD = TN, DATERECORD = TNDAT).save()
     

#------------------------------------------------------------------------------
#-------------------------------------INITIALISATION DES INFOS POSTES----------
#------------------------------------------------------------------------------


#Fonction permettant d'initialiser les données des instruments des 
#différents postes. Champs pré-remplis.
def infoposte(request,code=None,typestation='Autre',capteur='T'):
    
    #Formulaire pré-rempli
    if typestation == 'VP2' or typestation == 'VP2P': 
        formAutre = False
        form = InitPoste(request.POST or None)
        liste_capteur = ['T','P','A','Pl','Ray','UV']
        liste_nomcapteur = ['Température','Pression','Anéomètre',
                            'Pluviomètre','Rayonnement','UV']
        liste_seuilmin = [-40,540,3,0,0,0]
        liste_seuilmax = [65,1100,290,999.8,1800,16]
        liste_precision = [0.3,1,3,3,5,0]
        liste_pasdetemps = [10,60,2.5,24,60,60]
        liste_unite = ['°C','hPa','km/h','mm','W/m²','Indice']
        indice = liste_capteur.index(capteur)
        nomcapteur = liste_nomcapteur[indice]
        seuilmin = liste_seuilmin[indice]
        seuilmax = liste_seuilmax[indice]
        precision = liste_precision[indice]
        pasdetemps = liste_pasdetemps[indice]
        unite = liste_unite[indice]
        
    elif typestation=='Autre':
        nomcapteur = 'Capteur'
        formAutre = True
        form = InitPosteTotal(request.POST or None)
        #POSTE = form.cleaned_data['POSTE']
        #CAPTEUR = form.cleaned_data['CAPTEUR']
    if form.is_valid() or request.method == "POST": 
            if typestation != 'Autre':
                seuilmin = request.POST['seuilmin']
                seuilmax = request.POST['seuilmax']
                precision = request.POST['precision']
                pasdetemps = request.POST['pasdetemps']
                unite = request.POST['unite']
            else: 
                seuilmin = form.cleaned_data['SEUILMIN']
                seuilmax = form.cleaned_data['SEUILMAX']
                precision = form.cleaned_data['PRECISION']
                pasdetemps = form.cleaned_data['PASDETEMPS']
                unite = form.cleaned_data['UNITE']
            
            nomcapteur = request.POST['nomcapteur']    
            typestation = request.POST['typestation']
            DATDEB = form.cleaned_data['DATDEB']
            MODELE = form.cleaned_data['MODELE']
            HAUTEUR = form.cleaned_data['HAUTEUR']
            VENTILATION = form.cleaned_data['VENTILATION']
            TYPE_TERRAIN = form.cleaned_data['VENTILATION']
            QUALITE = form.cleaned_data['QUALITE']
            COMM = form.cleaned_data['COMM']
            envoi = True
            #On récupère le poste correspondant à l'instrument
            poste = POSTE.objects.get(CODE_POSTE = code)
            if typestation == "VP2" or typestation == "VP2P":
                if nomcapteur == "Température":
                    INSTRUMENT.objects.get_or_create(POSTE = poste,
CAPTEUR = nomcapteur, DATDEB = DATDEB, MODELE = MODELE, HAUTEUR = HAUTEUR,
VENTILATION = VENTILATION, SEUILMIN = seuilmin, SEUILMAX = seuilmax,
PRECISION = precision, PASDETEMPS = pasdetemps, TYPE_TERRAIN = TYPE_TERRAIN, 
UNITE = unite, COMM = COMM)
                    INSTRUMENT.objects.get_or_create(POSTE = poste,
CAPTEUR = "Hygromètre", DATDEB = DATDEB, MODELE = MODELE, HAUTEUR = HAUTEUR,
VENTILATION = VENTILATION, SEUILMIN = 1, SEUILMAX = 100,
PRECISION = 2, PASDETEMPS = 60, TYPE_TERRAIN = TYPE_TERRAIN, UNITE = '%',
COMM = COMM)
                
                elif nomcapteur == "Anémomètre":
                    INSTRUMENT.objects.get_or_create(POSTE = poste,
CAPTEUR = nomcapteur, DATDEB = DATDEB, MODELE = MODELE, HAUTEUR = HAUTEUR,
VENTILATION = VENTILATION, SEUILMIN = seuilmin, SEUILMAX = seuilmax,
PRECISION = precision, PASDETEMPS = pasdetemps, TYPE_TERRAIN = TYPE_TERRAIN,
UNITE = unite, COMM = COMM)
                    INSTRUMENT.objects.get_or_create(POSTE = poste,
CAPTEUR = "Girouette", DATDEB = DATDEB, MODELE = MODELE, HAUTEUR = HAUTEUR,
VENTILATION = VENTILATION, SEUILMIN = 0, SEUILMAX = 360, PRECISION = 3,
PASDETEMPS = 2.5, TYPE_TERRAIN = TYPE_TERRAIN, UNITE = '°', COMM = COMM)
                
                elif nomcapteur == "Pluviomètre":
                    INSTRUMENT.objects.get_or_create(POSTE = poste,
CAPTEUR = nomcapteur, DATDEB = DATDEB, MODELE = MODELE, HAUTEUR = HAUTEUR,
VENTILATION = VENTILATION, SEUILMIN = seuilmin, SEUILMAX = seuilmax,
PRECISION = precision, PASDETEMPS = pasdetemps, TYPE_TERRAIN = TYPE_TERRAIN,
UNITE = unite, COMM = COMM)
                    INSTRUMENT.objects.get_or_create(POSTE = poste, 
CAPTEUR = "IntensitéPluvio", DATDEB = DATDEB, MODELE = MODELE, 
HAUTEUR = HAUTEUR, VENTILATION = VENTILATION, SEUILMIN = 1, SEUILMAX = 2438,
PRECISION = 4, PASDETEMPS = 24, TYPE_TERRAIN = TYPE_TERRAIN, UNITE = 'mm/h',
COMM = COMM)
                
                else:
                    INSTRUMENT.objects.get_or_create(POSTE = poste, 
CAPTEUR = nomcapteur, DATDEB = DATDEB, MODELE = MODELE, HAUTEUR = HAUTEUR,
VENTILATION = VENTILATION, SEUILMIN = seuilmin, SEUILMAX = seuilmax,
PRECISION = precision, PASDETEMPS = pasdetemps, TYPE_TERRAIN = TYPE_TERRAIN,
UNITE = unite, COMM = COMM)
            elif typestation=='Autre':
                INSTRUMENT.objects.get_or_create(POSTE = poste, 
CAPTEUR = nomcapteur, DATDEB = DATDEB, MODELE = MODELE, HAUTEUR = HAUTEUR,
VENTILATION = VENTILATION, SEUILMIN = seuilmin, SEUILMAX = seuilmax,
PRECISION = precision, PASDETEMPS = pasdetemps, TYPE_TERRAIN = TYPE_TERRAIN,
UNITE = unite, COMM = COMM)
           
    return render(request, 'InfoPoste', locals())



#------------------------------------------------------------------------------
#----------------------------------------RELEVE MANUEL SPIEA -------------------
#--------------------------------------------------------------------------------
#Création d'un poste SPIEA

#Interface de soumission manuelle de données pluviomètriques
def releve(request):
     
    postes = POSTE.objects.all()
    liste = []
    for p in postes:
        liste+=[p.CODE_POSTE]
         
    #if request.method == "POST":
    try:
        code = request.POST['code']
        poste = POSTE.objects.get(CODE_POSTE=code)
        h = H.objects.filter(POSTE=poste)
        envoiCODE = True
    except:
        pass
    
    
    
    #Soumission de données
    try:
        rain = request.POST['mm']
        date = request.POST['date'].split('/')
        hrfin = request.POST['hrfin'].split(':')
       
        envoi = True
        #Complèter de 0mm entre l'avant dernier et dernier relevé
        
        date_senddonnee= datetime.datetime(int(date[2]),int(date[1]),int(date[0]),
                                   int(hrfin[0]),int(hrfin[1]))
        try:
            date_lastdonnee = h.order_by('-DATJ')[0].DATJ
            date_lastdonnees = datetime.datetime(int(date_lastdonnee.year),int(date_lastdonnee.month),
                                                int(date_lastdonnee.day),
                                       int(date_lastdonnee.hour),int(date_lastdonnee.minute))
            delta = ((date_senddonnee-date_lastdonnees).total_seconds())/3600
            
            
            delta= int(delta) 
            for hours in range(1,delta):
                newdate = date_lastdonnee+datetime.timedelta(hours=hours)
                print(newdate)
                H(POSTE = poste, RR1 = 0, STATUS_DRR1 = 1,
                DATJ = newdate).save()
        except:
            pass #Aucune donnée actuellement     
        H(POSTE = poste, RR1 = rain, STATUS_DRR1 = 1,
          DATJ = datetime.datetime(int(date[2]),int(date[1]),int(date[0]),
                                  int(hrfin[0]),int(hrfin[1]))).save()
                                    
                     
    except:
        pass #Aucun envoie de cumul
    
    
    
    
    
    try:
        #Afficher le cumul en cours de la derniere journee
        h_filtre = H.objects.filter(POSTE=poste).order_by('DATJ')
        
        #A defaut, la derniere journee de donnee dispo
        j_lastdonnee = h_filtre.order_by('-DATJ')[0].DATJ
        j_premieredonnee = datetime.datetime(j_lastdonnee.year,j_lastdonnee.month,
                                                  j_lastdonnee.day,0,0)
        mois_choisi = j_lastdonnee.month
        annee_choisi = j_lastdonnee.year
        
        datejour = j_lastdonnee.strftime('%d/%m/%Y')
        #Choix d'une journée
        annee_dispo = []
        mois_dispo = range(1,13)
        jour_dispo = range(1,32)
        for date in h_filtre:
            if date.DATJ.year not in annee_dispo:
                annee_dispo+=[date.DATJ.year]
        try:
            jour_choisi = request.POST['jour']
            mois_choisi = request.POST['mois']
            annee_choisi = request.POST['annee']
            datejour = str(jour_choisi)+'/'+str(mois_choisi)+'/'+str(annee_choisi)
            j_premieredonnee= datetime.datetime(int(annee_choisi),int(mois_choisi),int(jour_choisi),0,0)
            j_lastdonnee= datetime.datetime(int(annee_choisi),int(mois_choisi),int(jour_choisi),0,0) \
                            +datetime.timedelta(hours=24)
        except:
            pass
        
        
        
        j_filter = h_filtre.filter(DATJ__gte=j_premieredonnee,DATJ__lte = j_lastdonnee)
           
        RR1 = []
        hr = []
        cumulj = 0 
        barWidth = 1
        
        for values in j_filter:
            RR1 += [values.RR1]
            cumulj += values.RR1
            hr += [values.DATJ]
        cumulj = Decimal(str(round(float(cumulj),2)))
        cumul1hmax = Decimal(str(round(float(np.nanmax(RR1)),2)))
        r = range(len(RR1))     
        fig, ax1 = plt.subplots(figsize=(5, 3))
        ax1.bar(r, RR1, width = barWidth, color = ['blue' for i in RR1],
                edgecolor = ['yellow' for i in RR1], 
                linestyle = 'solid',linewidth = 1,label='Cumul')
        ax1.set_ylabel('Pluviomètrie mm')
        fig.legend()
        #plt.bar(r, y2, width = barWidth, bottom = y1, color = ['pink' for i in y1],edgecolor = ['green' for i in y1], linestyle = 'dotted', hatch = 'o',linewidth = 3)
        plt.xticks([r + barWidth / 2 for r in range(len(RR1))],
                    [hr[i].strftime('%H h') for i in range(0,len(RR1))])       
        plt.xticks(rotation=70)    
        
        plt.grid()
        link = code+'/SPIEA/'+str(j_lastdonnee.day)+str(j_lastdonnee.month)+str(j_lastdonnee.year)+'/'  
        if not os.path.exists(data_dir+link):
                        os.makedirs(data_dir+link)
        plt.savefig(data_dir+link+'J.png', bbox_inches="tight")
        linkJ = link+'J.png'
        plt.close()
    except:
        pass    
        
        #journalier sur le mois 
    try:    
        #on boucle sur le mois en cours
        #m_lastdonnee = h_filtre.order_by('-DATJ')[0].DATJ
        #m_premieredonnee =  datetime.datetime(m_lastdonnee.year,m_lastdonnee.month,
        #                                          1,0,0)
         
        cumul_j = []
        cumulm = 0
        j = []
        cumul1hmaxmois = 0
        for i in range(1,32):
            try:
                jm_premieredonnee =  datetime.datetime(int(annee_choisi),int(mois_choisi),
                                                      i,0,0)
                jm_lastdonnee =  datetime.datetime(int(annee_choisi),int(mois_choisi),
                                                      i,0,0)+datetime.timedelta(hours=24)
                cumul = H.objects.filter(POSTE=poste, DATJ__lte = jm_lastdonnee,
                                         DATJ__gte = jm_premieredonnee ) \
                                         .aggregate(Sum('RR1'))['RR1__sum']
                cumulmax = H.objects.filter(POSTE=poste, DATJ__lte = jm_lastdonnee,
                                         DATJ__gte = jm_premieredonnee ) \
                                         .aggregate(Max('RR1'))['RR1__max']
                if cumulmax >= cumul1hmaxmois:
                    cumul1hmaxmois = cumulmax                    
                if cumul == None:
                    cumul_j += [np.NaN]
                else:
                    cumul_j += [cumul]
                    cumulm+=cumul
                j += [i]
            except: 
                pass
             
                                    
        cumulm = Decimal(str(round(float(cumulm),2)))
        cumul1hmaxmois = Decimal(str(round(float(cumul1hmaxmois),2)))
        cumuljmaxmois = Decimal(str(round(float(np.nanmax(cumul_j)),2)))
        r = range(len(cumul_j))     
        fig, ax1 = plt.subplots(figsize=(5, 3))
        ax1.bar(r, cumul_j, width = barWidth, color = ['blue' for i in cumul_j],
                edgecolor = ['yellow' for i in cumul_j], 
                linestyle = 'solid',linewidth = 1,label='Cumul')
        ax1.set_ylabel('Pluviomètrie mm')
        fig.legend()
        #plt.bar(r, y2, width = barWidth, bottom = y1, color = ['pink' for i in y1],edgecolor = ['green' for i in y1], linestyle = 'dotted', hatch = 'o',linewidth = 3)
        plt.xticks([r + barWidth / 2 for r in range(len(cumul_j))],
                    [j[i] for i in range(0,len(cumul_j))])       
        plt.xticks(rotation=70)    
         
        plt.grid()
        link = code+'/SPIEA/'+str(mois_choisi)+str(annee_choisi)+'/'  
        if not os.path.exists(data_dir+link):
                        os.makedirs(data_dir+link)
        plt.savefig(data_dir+link+'M.png', bbox_inches="tight")
        linkM = link+'M.png'
        plt.close()
    
    except:
        error = "Pas d'affichage car aucune donnée"
        
        #mensuel sur l'année
        
        
        
          
    return render(request, 'Releve.html', locals())


#-------------------------------------------------------------------------------
#------------------------------REACTUALISATION PERTES PANNES-------------------
#------------------------------------MANUELLE----------------------------------
def reactualisation(request):
    
    
    #FORMULAIRE CHOIX POSTE + fichier complet (.csv) 

    form = UploadFileForm(request.POST or None, request.FILES or None) 
    #GET OR CREATE TABLE INSTAN
    if form.is_valid():
        code = form.cleaned_data['POSTE']
        lien = form.cleaned_data['lien']
        
        #-----------------Lecture du fichier (.csv)---------------------------
        c = Files(POSTE=code,lien=lien)
        c.save() #on enregistre le lien dans data afin de pouvoir le lire
        link = str(c.lien.path)
        #Lecture
        premiere_date_manquante = []
        derniere_date_manquante = []
        #Récupération des dates manquantes dans la BDD
        #on parcourt les dates de la BDD
        ins = INSTAN.objects.filter(POSTE = code).order_by('DATJ')
        for i in range(0,ins.count()-1): 
            if (ins[i+1].DATJ - ins[i].DATJ).total_seconds() != 600 :
                premiere_date_manquante+=[ins[i].DATJ]
                derniere_date_manquante+=[ins[i+1].DATJ] 
        #Creneau manquant   
        Deb = premiere_date_manquante[0]
        Fin = derniere_date_manquante[-1] 
        datedeb = datetime.datetime(Deb.year,Deb.month,1)
        datefin = datetime.datetime(Fin.year,Fin.month,1)        
        
        
        with open(link, "r") as f:
            lignes = f.readlines()
            for ligne in lignes:
                #Récupération des données pour chaque ligne
                l = ligne.split(',')
                l = [None if element == '\\N' else element for element in l]
                
                dateTime = int(l[0])
                
                interval = l[2]
                barometer = l[3]
                barometer = Decimal(str(round(float(barometer),2)))
                pressure = l[4]
                altimeter = l[5]
                outTemp = l[7]
                outTemp = Decimal(str(round(float(outTemp),2)))
                outHumidity = l[9]
                outHumidity = Decimal(str(round(float(outHumidity),2)))
                windSpeed = l[10]
                windSpeed = Decimal(str(round(float(windSpeed),2)))
                windDir = l[11]
                windDir = Decimal(str(round(float(windDir),2)))
                windGust = l[12]
                windGust = Decimal(str(round(float(windGust),2)))
                windGustDir = l[13]
                windGustDir = Decimal(str(round(float(windGustDir),2)))
                rainRate = l[14]
                rainRate = Decimal(str(round(float(rainRate),2)))
                rain = l[15]
                rain = Decimal(str(round(float(rain),2)))
                dewpoint = l[16]
                dewpoint = Decimal(str(round(float(dewpoint),2)))
                windchill = l[17]
                windchill = Decimal(str(round(float(windchill),2)))
                heatindex = l[18]
                heatindex = Decimal(str(round(float(heatindex),2)))
                ET= l[19]
                ET = Decimal(str(round(float(ET),2)))
                radiation = l[20]
                radiation = Decimal(str(round(float(radiation),2)))
                UV= l[21]
                UV = Decimal(str(round(float(UV),2)))
                soilTemp = l[25]
                soilTemp = Decimal(str(round(float(soilTemp),2)))
                leafTemp = l[29]
                leafTemp = Decimal(str(round(float(leafTemp),2)))
                leafWet = l[33]
                leafWet = Decimal(str(round(float(leafWet),2)))
                
                dateTime = datetime.datetime.fromtimestamp(dateTime) \
                .strftime('%Y-%m-%d %H:%M:%S') #Conversion du temps unix
                #2 conditions se presentent 
                #Si le creneau de la perte est renseigné
                
                if dateTime > datedeb and dateTime < datefin:
                    
                    INSTAN.objects.get_or_create(POSTE = code, 
                            DATJ = dateTime, RR = float(rain),
                            RRI = float(rainRate), FF = float(windSpeed),
                            DD = float(windDir), FXI = float(windGust),
                            DXI = float(windGustDir), T = float(outTemp),
                            TD = float(dewpoint), U = float(outHumidity),
                            PMER = float(barometer), UV = float(UV),
                            RAD = float(radiation), IC=float(heatindex),
                            WINDCHILL = float(windchill), ETP = float(ET),
                            HF = float(leafWet), TS = float(soilTemp))
                
                       
               
        init.initH(code.CODE_POSTE,datedeb,datefin) #on réinitialise la période
        
    #INCREMENTATION DES DATES DE PANNE
    return render(request, 'Reactualisation.html', locals())

#------------------------------------------------------------------------------
#----------------------------------------AFFICHAGE DES DONNEES-----------------
#------------------------------------------------------------------------------
def fonction_direction(DD):
    liste_dir_inf = [11.25,33.75,65.25,78.75,101.25,123.75,146.25,168.75,191.25,
                     213.75,236.25,258.75,281.25,303.75,326.25]
    liste_dir_sup = [33.75,65.25,78.75,101.25,123.75,146.25,168.75,191.25,
                     213.75,236.25,258.75,281.25,303.75,326.25,348.75]
    dirs = ['NNE','NE','ENE','E','ESE','SE','SSE','S','SSO','SO','OSO','O','ONO'
           ,'NO','NNO']
    try:
        if DD >= 348.75 or DD <= 11.25:
            Dir = 'N'
        else:
            for i in range(0,len(liste_dir_inf)):
                if DD >= liste_dir_inf[i] and DD <= liste_dir_sup[i]:
                    Dir = dirs[i]
    except:
        Dir = 'None'
    
    return(Dir)
    
#Affichage spécifique, données instantanées + graphique avec période modifiable
def affichage(request,codeposte):

                
    liste_champ=['T','TD','U','PMER','RR','RRI','FF','DD','FXI','DXI','IC',
                 'WINDCHILL','UV','RAD','RDV'] 
    labelunite=['°C','°C','%','hPa','mm','mm/h','km/h','°','km/h','°',
                '°C','°C','','W/m²',''] 
    labelX=['Temperature','T de rosée','Humidite','Pression mer',
            'Précipitations cumul 5min','Intensité de précipitations',
            'Force du vent moyenné 10min','Direction vent moyen',
            'Rafales 2.5sec','Direction rafales','Indice Chaleur','Windchill',
            'Indice UV','Rayonnement','Rose des vents'] 
    
    liste_champ2=['Aucun','T','TD','U','PMER','RR','RRI','FF','DD','FXI','DXI','IC',
                 'WINDCHILL','UV','RAD'] 
    labelX2=['Aucun','Temperature','T de rosée','Humidite','Pression mer',
            'Précipitations cumul 5min','Intensité de précipitations',
            'Force du vent moyenné 10min','Direction vent moyen',
            'Rafales 2.5sec','Direction rafales','Indice Chaleur','Windchill',
            'Indice UV','Rayonnement'] 
    labelunite2=['Aucun','°C','°C','%','hPa','mm','mm/h','km/h','°','km/h','°',
                '°C','°C','','W/m²'] 
    
    Affichage = True   
    # Affichage des données instantanées
    posteob = POSTE.objects.get(CODE_POSTE=codeposte)
    inst = INSTAN.objects.filter(POSTE=posteob).order_by('-DATJ')
    ins = inst[0]
     
    Altitude = posteob.ALT
    Lat = posteob.LAT
    Lon = posteob.LON
    nom_public = posteob.NOM
    date_premiere_mesure = inst[inst.count()-1].DATJ.strftime('%d/%m/%Y à %Hh%M')
    date_derniere_mesure = ins.DATJ.strftime('%d/%m/%Y à %Hh%M')
    #On récupère la toute dernière données instantanées
    T = ins.T
    TD = ins.TD
    U = ins.U
    PMER = ins.PMER
    FF = ins.FF
    DD = ins.DD
    FXI = ins.FXI
    if ins.DXI != None:
        DXI = ins.DXI
    else:
        DXI = np.NaN
    RDV = False
    
    DirDD = fonction_direction(DD)
    liste_dir_inf = [11.25,33.75,65.25,78.75,101.25,123.75,146.25,168.75,191.25,
                     213.75,236.25,258.75,281.25,303.75,326.25]
    liste_dir_sup = [33.75,65.25,78.75,101.25,123.75,146.25,168.75,191.25,
                     213.75,236.25,258.75,281.25,303.75,326.25,348.75]
   
    dirs = ['NNE','NE','ENE','E','ESE','SE','SSE','S','SSO','SO','OSO','O','ONO'
           ,'NO','NNO']
    if DXI >= 348.75 or DXI <= 11.25:
        DirDXI = 'N'
    else:
        for i in range(0,len(liste_dir_inf)):
            if DXI >= liste_dir_inf[i] and DXI <= liste_dir_sup[i]:
                DirDXI = dirs[i]
    RR = Decimal(str(round(ins.RR,2)))
    RRI = Decimal(str(round(ins.RRI,2)))
    
    
    
    #Affichage graphique : choix paramètre + période
    datedebuts = "JJ-MM-AAAA HH:MM"
    dateends = "JJ-MM-AAAA HH:MM"  
    if request.method=="POST":
            choix = True
            champchoisi = request.POST['champchoisi']
            champchoisi2 = request.POST['champchoisi2']
            
            try : 
                datedebuts = request.POST['datedeb']
                datedebut=datedebuts.split(' ')
                datedeb = datedebut[0].split('-')
                hrdeb = datedebut[1].split(':')
         
                dateends = request.POST['datefin']
                dateend=dateends.split(' ')
                datefin = dateend[0].split('-')
                hrfin = dateend[1].split(':')
                nom = datedebut[0]+'_'+dateend[0]
                datedebut = datetime.datetime(int(datedeb[2]),int(datedeb[1]),
                                              int(datedeb[0]),int(hrdeb[0]),
                                              int(hrdeb[1]))
                datefin = datetime.datetime(int(datefin[2]),int(datefin[1]),
                                            int(datefin[0]),int(hrfin[0]),
                                            int(hrfin[1]))
            except:
                pass
            carte = True
            
            #Sélection des données instantanées, comme RDV n'existe pas dans la 
            #table INSTAN, il faut la traiter séparément
            if champchoisi != 'RDV': 
                values = INSTAN.objects.filter(POSTE = posteob, DATJ__lt = datefin,
                                           DATJ__gte = datedebut) \
                                           .values_list('DATJ',champchoisi) \
                                           .order_by('DATJ')
                if champchoisi2 != 'Aucun':
                    values2 = INSTAN.objects.filter(POSTE = posteob, DATJ__lt = datefin,
                                           DATJ__gte = datedebut) \
                                           .values_list('DATJ',champchoisi2) \
                                           .order_by('DATJ')
            #On plot les données demandées
            if champchoisi != 'RDV':
                fig, ax = plt.subplots()
                x=[]
                y=[]
                y2 = []
                delta_date = datefin-datedebut
                
                for value in values:
                    if value[1] != None:
                        x += [value[0]]
                        y += [value[1]]
                    else : 
                        x += [value[0]]
                        y += [np.nan]
                        
                if champchoisi2  != 'Aucun':
                    for value in values2:
                        if value[1] != None:
                            y2 += [value[1]]
                        else : 
                            y2 += [np.nan]
                
                Maxx = values.aggregate(Max(champchoisi))[champchoisi+'__max']
                Maxx = Decimal(str(round(float(Maxx),2)))
                Minx = values.aggregate(Min(champchoisi))[champchoisi+'__min']
                Minx = Decimal(str(round(float(Minx),2)))
                Avgx = values.aggregate(Avg(champchoisi))[champchoisi+'__avg']
                Avgx = Decimal(str(round(float(Avgx),2)))
             
                #Le cumul n'est pas nécessaire pour les valeurs de T,TD,PMER..
                liste_cumul = ['RR','RAD']
                if champchoisi in liste_cumul:
                    if champchoisi == 'RR': 
                        liste_cumul1 = []
                        Cumulmax = H.objects.filter(POSTE=posteob,DATJ__lt=datefin,
                                                  DATJ__gte=datedebut) \
                                                  .order_by('-RR1')
                        if Cumulmax.count() >= 3:                          
                            for i in range(0,3):
                                                         
                                Cumul1 = Decimal(str(round(float(Cumulmax[i].RR1),2)))
                                datecumulmax = (Cumulmax[i].DATJ-
                                                datetime.timedelta(hours=1)).strftime('%d/%m %Hh%M')
                                liste_cumul1+=['- '+str(Cumul1)+'mm '+str(datecumulmax)] 
                        Sumx = values.values_list('DATJ',champchoisi) \
                            .aggregate(Sum(champchoisi))[champchoisi+'__sum']
                        Sumx = Decimal(str(round(float(Sumx),2)))
                    elif champchoisi == 'RAD': 
                        Sumx = values.values_list('DATJ',champchoisi) \
                            .aggregate(Sum(champchoisi))[champchoisi+'__sum']
                        Sumx = Decimal(str(round(float(Sumx),2)))
                    cumul = True
                else:
                    cumul = False
                Comm=False
                commentaire= []
                
                #Traitement des données vent
                if champchoisi == 'FF' or champchoisi == 'FXI' or champchoisi == 'PMER': 
                    
                    Comm = True
              
                    if champchoisi == 'FF':
                        commentaire += ['Top 5 des vents moyens sur la période : ']
                        FiltreTop = INSTAN.objects.filter(POSTE=posteob,DATJ__lt=datefin,
                                            DATJ__gte=datedebut).order_by('-FF')
                        for i in range(0,5):
                            #Il n'y aura pas forcément 5 valeurs
                            try:
                                commentaire += [str(FiltreTop[i].FF) +'km/h le ' \
                                + str(FiltreTop[i].DATJ.strftime('%d/%m %Hh%M'))]
                            except: 
                                pass
                    elif champchoisi == 'FXI':
                        #Durée où la rafale est supérieure à une valeur
                        Filtre50 = INSTAN.objects.filter(POSTE=posteob,DATJ__lt=datefin,
                                            DATJ__gte=datedebut,FXI__gte=50).count()
                        Filtre70 = INSTAN.objects.filter(POSTE=posteob,DATJ__lt=datefin,
                                            DATJ__gte=datedebut,FXI__gte=70).count()
                        Filtre90 = INSTAN.objects.filter(POSTE=posteob,DATJ__lt=datefin,
                                            DATJ__gte=datedebut,FXI__gte=90).count()
                        Filtre120 = INSTAN.objects.filter(POSTE=posteob,DATJ__lt=datefin,
                                            DATJ__gte=datedebut,FXI__gte=120).count()
                        Filtre50, Filtre70, Filtre90, Filtre120 = Filtre50*5, Filtre70*5, Filtre90*5,Filtre120*5
                        commentaire += ['Durée rafales: >50 '+
                                        str(Filtre50) +'min, >70 '
                                        +str(Filtre70)+'min, >90 '
                                        +str(Filtre90)+'min, >120 '
                                        +str(Filtre120)+'min']
                
                        commentaire += ['Top 5 des rafales sur la période : ']
                        FiltreTop = INSTAN.objects.filter(POSTE=posteob,
                                            DATJ__lt=datefin,
                                            DATJ__gte=datedebut).order_by('-FXI')
                        for i in range(0,5):
                            try:
                                commentaire += [str(FiltreTop[i].FXI) +'km/h le ' \
                                + str(FiltreTop[i].DATJ.strftime('%d/%m %Hh%M'))]
                            except:
                                pass
                    elif champchoisi == 'PMER':
                        FiltrePMER = INSTAN.objects.filter(POSTE=posteob,DATJ__lt=datefin,
                                            DATJ__gte=datedebut).order_by('DATJ')
                        gradmoyen=[]  
                                        
                        for i in range(0,FiltrePMER.count()-1): 
                            gradmoyen+=[(FiltrePMER[i+1].PMER-FiltrePMER[i].PMER)/5] 
                      
                        moygrad = Decimal(str(round(np.mean(gradmoyen),2)))
                        posgrad = Decimal(str(round(max(gradmoyen),2)))
                        neggrad = Decimal(str(round(min(gradmoyen),2)))
                        commentaire+=['(5min) Gradient maximal : ('+
                                      str(posgrad)+'hPa/min) / ('+ 
                                      str(neggrad)+'hPa/min)']   
                        commentaire+=['Gradient moyen sur la période: '+
                                      str(moygrad)+'hPa/min']               
                       
                        
                plt.plot(x,y,label=str(labelX[liste_champ.index(champchoisi)]))
                ax.set_xticklabels([])
                
                
                    
                #Changement de légende axe x selon la période choisie
                format_date(delta_date.days,ax)
                
                
                    
                for text in ax.get_xminorticklabels():
                    text.set_rotation(50)    
                
                #Récupération de l'unité du paramètre choisi
                unite = labelunite[liste_champ.index(champchoisi)]
                unite2 = labelunite2[liste_champ2.index(champchoisi2)]
                
                plt.ylabel(labelX[liste_champ.index(champchoisi)] + ' - ' + unite)
               
                if champchoisi2 != "Aucun":
                    if (champchoisi == 'T' and champchoisi2 == 'TD') or \
                        (champchoisi == 'RR' and champchoisi2 == 'RRI') or \
                        (champchoisi == 'TD' and champchoisi2 == 'T')or \
                        (champchoisi == 'RRI' and champchoisi2 == 'RR')or \
                        (champchoisi == 'FF' and champchoisi2 == 'FXI')or \
                        (champchoisi == 'FXI' and champchoisi2 == 'FF'):
                        plt.plot(x,y2,'r',label=str(labelX2[liste_champ2.index(champchoisi2)]),alpha =0.5)
                        
                    else:
                        ax2 = ax.twinx()
                        ax2.plot(x,y2,'r',label=str(labelX2[liste_champ2.index(champchoisi2)]),alpha =0.5)
                        ax2.set_xticklabels([])
                        plt.ylabel(labelX2[liste_champ2.index(champchoisi2)] + ' - ' + unite2)
                plt.grid()
                fig.legend()    
                if not os.path.exists(data_dir+'nonpermanent/'+codeposte+'/'+champchoisi+'/'):
                    os.makedirs(data_dir+'nonpermanent/'+codeposte+'/'+champchoisi+'/')
                link = 'nonpermanent/'+codeposte+'/'+champchoisi+'/'+nom+'.png'
                plt.savefig(data_dir+link, 
                            bbox_inches="tight")  #choisir un nom unique
                plt.close(fig)
            else:
                RDV= True
                DDlist = []
                flist=[]
                values = INSTAN.objects.filter(POSTE = posteob, DATJ__lt = datefin,
                                           DATJ__gte = datedebut)
                for value in values:
                    if value.DD != None:
                        DDlist+=[value.DD] 
                        flist += [value.FF]
                
                ax = WindroseAxes.from_ax() 
                ax.bar(DDlist, flist, bins=np.arange(0, max(flist), 10),
                       normed=True, opening=0.8, edgecolor='white')
                
                ax.set_legend()
                if not os.path.exists(data_dir+'nonpermanent/'+codeposte+'/'+champchoisi+'/'):
                    os.makedirs(data_dir+'nonpermanent/'+codeposte+'/'+champchoisi+'/')
                #link : chemin d'accès de l'image la page station    
                link = 'nonpermanent/'+codeposte+'/RDV/'+nom+'.png'
                plt.savefig(data_dir+link, 
                            bbox_inches="tight")  #choisir un nom unique
                plt.close()
                
                #Fréquences de direction
                table = ax._info['table']
                wd_freq = np.sum(table, axis=0)
                direction = ax._info['dir']
                wd_freq = np.sum(table, axis=0)
                plt.bar(np.arange(16), wd_freq, align='center')
                xlabels = ('N','','N-E','','E','','S-E','',
                           'S','','S-O','','O','','N-O','')
                max_freq = 0
                indice_max = 0
                for i in range(0,len(wd_freq)):
                    if wd_freq[i] >= max_freq:
                        max_freq = wd_freq[i]
                        indice_max = i
                        
                listedirfreq = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
                            'S','SSO','SO','OSO','O','ONO','NO','NNO']
                dir_freqmax = listedirfreq[indice_max]

                xticks=np.arange(16)
                plt.ylabel('Fréquence (%)')
                 
                plt.gca().set_xticks(xticks)
                
                plt.gca().set_xticklabels(xlabels)
                plt.savefig('TEEEST.png', 
                            bbox_inches="tight")
                #draw()
                plt.close()
                
    else:
            carte = False
       
    return render(request, 'station.html', locals())

def format_date(delta,ax):
    
    if delta >= 90:
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=31))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m/%Y'))
    elif delta >= 62:
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=15))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m')) 
    elif delta >= 31:
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=5))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m')) 
    elif delta >= 20 : 
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=2))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m')) 
    elif delta >= 10 : 
        ax.xaxis.set_minor_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m'))  
        
    elif delta >= 5 : 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=12))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%d'))   
    elif delta >= 3 : 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=6))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%d'))     
    elif delta >= 1 : 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=3))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))   
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%d')) 
    else: 
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=1))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))    
        
    return  

#Récapitulatif des différentes périodes : journalier   
def recap(request,codeposte):
    

    #Journalier   
    posteob = POSTE.objects.get(CODE_POSTE=codeposte) 
    inst = INSTAN.objects.filter(POSTE=posteob).order_by('-DATJ')
    
    
    finmesure = inst[0].DATJ.strftime('%d/%m/%Y')
    debutmesure = inst[inst.count()-1].DATJ.strftime('%d/%m/%Y')
    
    #formulaire choix de journée
    annee_dispo = []
    mois_dispo = range(1,13)
    jour_dispo = range(1,32)
    for date in inst:
        if date.DATJ.year not in annee_dispo:
            annee_dispo+=[date.DATJ.year]
    #récupération données formulaire     
    if request.method == "POST":
        jourchoisi = int(request.POST['jour'])
        moischoisi = int(request.POST['mois']) 
        anneechoisi = int(request.POST['annee'])
        journee = datetime.datetime(anneechoisi,moischoisi,jourchoisi,0,0)
        finjournee = datetime.datetime(anneechoisi,moischoisi,
                                       jourchoisi,23,0) + datetime.timedelta(
                                           hours=1) 
    else: 
            
        #ins est la dernière valeur de la journée
        ins = inst[0]
        jourchoisi = ins.DATJ.day
        moischoisi = ins.DATJ.month
        anneechoisi = ins.DATJ.year
        journee = datetime.datetime(ins.DATJ.year,ins.DATJ.month,
                                    ins.DATJ.day,0,0)
        finjournee = datetime.datetime(ins.DATJ.year,ins.DATJ.month,
                                       ins.DATJ.day,23,0)+ datetime.timedelta(
                                           hours=1)
    link = codeposte+'/recapJ/'+str(jourchoisi)+str(moischoisi)+str(anneechoisi)+'/'  
    
    jour = INSTAN.objects.filter(POSTE=posteob,
            DATJ__gte=journee,DATJ__lt=finjournee).order_by('DATJ')    
        
    #On traite les données températures
    ICmax = jour.order_by('-IC')[0].IC
    WINDCHILLmax = jour.order_by('WINDCHILL')[0].WINDCHILL
    Tx,DateTx = jour.order_by('-T')[0].T,jour.order_by('-T')[0] \
                                                        .DATJ.strftime('%Hh%M')
    Tn,DateTn = jour.order_by('T')[0].T,jour.order_by('T')[0] \
                                                        .DATJ.strftime('%Hh%M')
     
    MoyT = jour.aggregate(Avg('T'))['T__avg']
    MoyTemp = Decimal(str(round(MoyT,2)))
    MoyFF = jour.aggregate(Avg('FF'))['FF__avg']
    MoyFF = Decimal(str(round(MoyFF,2)))
   
    #On trace les courbes de températures    
    fig, ax = plt.subplots(figsize=(5, 3))
    x=[]
    y2=[]
    y=[]
    for value in jour:
        x += [value.DATJ]
        y += [value.T] 
        y2 += [value.TD]   
    plt.plot(x,y,'r',label='T')
    plt.plot(x,y2,'b',label='TD') 
    plt.ylabel('Température °C')
    ax.set_xticklabels([])
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=2))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.legend()
    plt.grid()
    
    link = codeposte+'/recapJ/'+str(jourchoisi)+str(moischoisi)+str(anneechoisi)+'/'  
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'T.png', bbox_inches="tight")
    linkT = link+'T.png'
    plt.close()
    
    #On traite les données précipitations
    Precip = H.objects.filter(POSTE=posteob,DATJ__gt=journee
                              ,DATJ__lte=finjournee).order_by('DATJ')
    RR1 = []
    RRI = []
    hr=[]
    cumultotal =Precip.aggregate(Sum('RR1'))['RR1__sum']
    cumultotal = Decimal(str(round(cumultotal,2)))
    for value in Precip:
        RR1+=[value.RR1]
        hr+=[value.DATJ]
        if value.RRI == None:
            RRI+=[0]
        else:
            RRI+=[value.RRI]      
    maxRRI,hrmaxRRI = Precip.order_by('-RRI')[0].RRI,Precip.order_by('-RRI')[0] \
                        .DATJ.strftime('%Hh%M')
    plt.xlabel('Heure')        
    barWidth = 1
    r = range(len(RR1))
    #On trace les données précipitations
    fig, ax1 = plt.subplots(figsize=(5, 3))
    ax1.bar(r, RR1, width = barWidth, color = ['blue' for i in RR1],
            edgecolor = ['yellow' for i in RR1], 
            linestyle = 'solid',linewidth = 1)
    ax1.set_ylabel('Pluviomètrie mm')
    #plt.bar(r, y2, width = barWidth, bottom = y1, color = ['pink' for i in y1],edgecolor = ['green' for i in y1], linestyle = 'dotted', hatch = 'o',linewidth = 3)
    plt.xticks([r + barWidth / 2 for r in range(len(RR1))],
                [hr[i].strftime('%H h') for i in range(0,len(RR1))])       
    plt.xticks(rotation=70)
    ax2 = ax1.twinx()
    ax2.plot(r,RRI,'r',label='Intensité')        
    plt.legend()
    plt.grid()
    link = codeposte+'/recapJ/'+str(jourchoisi)+str(moischoisi)+str(anneechoisi)+'/'  
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'RR.png', bbox_inches="tight")
    linkRR = link+'RR.png'
    plt.close()
    
    #On traite les données vents
    fig, ax = plt.subplots(figsize=(5, 3))
    dir = []
    f = []
    raf=[]
    for value in jour:
        raf+=[value.FXI] 
        f+=[value.FF]
        dir+=[value.DD]      
    ventmoyenmax = jour.order_by('-FF')[0].FF
    rafmax,hrrafmax = jour.order_by('-FXI')[0].FXI,jour.order_by('-FXI')[0] \
        .DATJ.strftime('%Hh%M')
    #Tracé des données vent   
    plt.plot(x,f,'k',label='Vent moyen',linewidth=1.5  )
    plt.plot(x,raf,'r', label='Rafales',linewidth=0.3)
    plt.ylabel('Vent km/h')
    plt.legend()
    ax2 = ax.twinx()
    ax2.plot(x,dir,'*k', label='Direction vent moyen')
    ax.set_xticklabels([])
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=2))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.grid()
    plt.ylabel('Direction °')
    plt.legend()
    link = codeposte+'/recapJ/'+str(jourchoisi)+str(moischoisi)+str(anneechoisi)+'/'  
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'FF.png', bbox_inches="tight")
    linkFF = link+'FF.png'
    plt.close()
    
     #On traite les données PMER
    fig, ax = plt.subplots(figsize=(5, 3))
    PMER = []
    for value in jour:
        PMER+=[value.PMER] 
        
    pmoy = jour.aggregate(Avg('PMER'))['PMER__avg'] 
    pmax = jour.order_by('-PMER')[0].PMER
    pmin,hpmin= jour.order_by('PMER')[0].PMER,jour.order_by('PMER')[0].DATJ \
                .strftime('%Hh%M')     
    pmoy = Decimal(str(round(pmoy,2)))   
    #Tracé des données vent   
    plt.plot(x,PMER,'k',label='PMER',linewidth=1)
    ax.set_xticklabels([])
    ax.xaxis.set_minor_locator(dates.HourLocator(interval=2))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.grid()
    plt.ylabel('Pression mer hpa')
    plt.legend()
    link = codeposte+'/recapJ/'+str(jourchoisi)+str(moischoisi)+str(anneechoisi)+'/'  
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'PMER.png', bbox_inches="tight")
    linkPMER = link+'PMER.png'
    plt.close()

     #On traite les données DD
    DD = []
    for value in jour:
        if value.DD==None:
            DD+=[np.nan]
        else:
            DD+=[value.DD] 

    ax = WindroseAxes.from_ax() 
    ax.bar(DD, f, normed=True, bins=np.arange(0, max(f), 10), opening=0.8, edgecolor='white')

    ax.set_legend()
    link = codeposte+'/recapJ/'+str(jourchoisi)+str(moischoisi)+str(anneechoisi)+'/'  
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'DD2.png', bbox_inches="tight")
    linkDD2 = link+'DD2.png'
    plt.close()
    enso = False
     #On traite les données ensoleillement
    try: 
        
        fig, ax = plt.subplots(figsize=(5, 3))
        RAD = []
        for value in jour:
            RAD+=[value.RAD] 
            
        if RAD[0] != None:
            enso = True
        cumultotalRAD = H.objects.filter(POSTE=posteob,DATJ__gt=journee,
                                  DATJ__lte=finjournee) \
                                  .aggregate(Sum('INST'))['INST__sum']
        cumultotalRAD = Decimal(str(round(cumultotalRAD,2)))
        
        hRAD,mRAD=divmod(cumultotalRAD,60)
        mRAD = int(mRAD)
        #UVmax = H.objects.filter(POSTE=posteob,DATJ__gt=journee,
        #                          DATJ__lte=finjournee) \
        #                          .order_by('-UV')
        #UVmax = Decimal(str(round(UVmax[0].UV,2)))
    #Tracé des données vent   
        plt.plot(x,RAD,'y',label='Ensoleillement',linewidth=1)
    
        ax.set_xticklabels([])
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=2))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))  
        for text in ax.get_xminorticklabels():
            text.set_rotation(50)
        plt.grid()
        plt.ylabel('Ensoleillement W/m²')
        plt.legend()
        link = codeposte+'/recapJ/'+str(jourchoisi)+str(moischoisi)+str(anneechoisi)+'/'  
        if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
        plt.savefig(data_dir+link+'RAD.png', bbox_inches="tight")
        linkRAD = link+'RAD.png'
        plt.close()
    except:
        pass
    return render(request, 'recap.html', locals())



 #Récapitulatif des différentes périodes : mensuel   
def recapMensuel(request,codeposte):
    
    
    
      
    posteob = POSTE.objects.get(CODE_POSTE=codeposte) 
    inst = INSTAN.objects.filter(POSTE=posteob).order_by('-DATJ')
    
    #Période de mesure possible
    finmesure = inst[0].DATJ.strftime('%d/%m/%Y')
    debutmesure = inst[inst.count()-1].DATJ.strftime('%d/%m/%Y')
    
    #formulaire choix de journée
    annee_dispo = []
    mois_dispo = range(1,13)
    for date in inst:
        if date.DATJ.year not in annee_dispo:
            annee_dispo+=[date.DATJ.year]
    #récupération données formulaire 
    #Par défaut : mois en cours    
    if request.method == "POST":
        moischoisi = int(request.POST['mois']) 
        anneechoisi = int(request.POST['annee'])
        debutmois = datetime.datetime(anneechoisi,moischoisi,1)
        if moischoisi == 12:
            nextmois = 1
            nextannee = anneechoisi+1
        else:
            nextmois= moischoisi+1
            nextannee = anneechoisi
        finmois = datetime.datetime(nextannee,nextmois,
                                       1) 
    else: 
            
        #ins est la dernière valeur de la journée
        ins = inst[0]
        moischoisi = ins.DATJ.month-1 # a changer
        anneechoisi = ins.DATJ.year
        if moischoisi == 12:
            nextmois = 1
            nextannee = anneechoisi+1
        else:
            nextmois= moischoisi+1
            nextannee = anneechoisi
        debutmois = datetime.datetime(anneechoisi,moischoisi,1) 
        finmois = datetime.datetime(nextannee,nextmois,1) 
    
    link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
    jour = Q.objects.filter(POSTE=posteob,
            DATJ__gte=debutmois,DATJ__lt=finmois).order_by('DATJ')   
    donneevent = INSTAN.objects.filter(POSTE=posteob,
            DATJ__gte=debutmois,DATJ__lt=finmois).order_by('DATJ') 
        
    #On traite les données températures
    MoyT = jour.aggregate(Avg('TM'))['TM__avg']
    MoyTemp = Decimal(str(round(MoyT,2)))
    #On trace les courbes de températures    
    
    fig, ax = plt.subplots(figsize=(5, 3))
    x=[]
    y=[]
    y1 = []
    y2=[]
    y3=[]
   
    for value in jour:
        x += [value.DATJ] 
       
        y += [value.TM] 
        y2 += [value.TX]
        y3 += [value.TN]  
    
    Tx,datTx = jour.order_by('-TX')[0].TX,jour.order_by('-TX')[0].DATJ \
                                        .strftime('%d/%m')
    Txmin,datTxmin = jour.order_by('TX')[0].TX,jour.order_by('TX')[0].DATJ \
                                        .strftime('%d/%m')
    Tn,datTn = jour.order_by('TN')[0].TN,jour.order_by('TN')[0].DATJ \
                                        .strftime('%d/%m')
    Tnmax,datTnmax = jour.order_by('-TN')[0].TN,jour.order_by('-TN')[0].DATJ \
                                        .strftime('%d/%m')                                    
    plt.plot(x,y,'k',label='T moyenne')
    plt.plot(x,y2,'--r',label='T max',linewidth=0.5)
    plt.plot(x,y3,'--b',label='T min',linewidth=0.5)
    plt.ylabel('Température °C')
    ax.set_xticklabels([])
 
    ax.xaxis.set_minor_locator(dates.DayLocator(interval=2))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.legend()
    plt.grid()
    
    link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'T.png', bbox_inches="tight")
    linkT = link+'T.png'
    plt.close()
    
    #On traite les données précipitations
    Precip = Q.objects.filter(POSTE=posteob,DATJ__gte=debutmois 
                              ,DATJ__lt=finmois).order_by('DATJ')
    PrecipINSTAN = H.objects.filter(POSTE=posteob,DATJ__gt=debutmois
                              ,DATJ__lte=finmois).order_by('DATJ')
    RR1 = []
    RRI = []
    hr=[]
    cumultotal = Precip.aggregate(Sum('RR'))['RR__sum']
    cumultotal = Decimal(str(round(float(cumultotal),2)))
    for value in Precip:
        RR1+=[value.RR]
        hr+=[value.DATJ]
    DRR = Precip.aggregate(Sum('DRR'))['DRR__sum']
    hDRR,mDRR=divmod(DRR,60)
    hDRR = int(hDRR)
    mDRR = int(mDRR)
    
    RRI, datRRI = PrecipINSTAN.order_by('-RRI')[0].RRI,PrecipINSTAN \
            .order_by('-RRI')[0].DATJ.strftime('%d/%m')
    plt.xlabel('Heure')        
    barWidth = 1
    r = range(len(RR1))
    #On trace les données précipitations
    fig, ax1 = plt.subplots(figsize=(5, 3))
    ax1.bar(r, RR1, width = barWidth, color = ['blue' for i in RR1], linestyle = 'solid',linewidth = 1)
    ax1.set_ylabel('Pluviomètrie mm')
    #plt.bar(r, y2, width = barWidth, bottom = y1, color = ['pink' for i in y1],edgecolor = ['green' for i in y1], linestyle = 'dotted', hatch = 'o',linewidth = 3)
    plt.xticks([r + barWidth / 2 for r in range(len(RR1))],
                [(hr[i]+datetime.timedelta(days=1)).strftime('%d') 
                 for i in range(0,len(RR1))])       
    plt.xticks(rotation=70)
    plt.legend()
    plt.grid()
    link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'RR1.png', bbox_inches="tight")
    linkRR1 = link+'RR1.png'
    plt.close()
    
    #On traite les données vents
    fig, ax = plt.subplots(figsize=(5, 3))
    dir = []
    f = []
    raf=[]
    for value in jour:
        raf+=[value.FXI] 
        f+=[value.FXY]
        dir+=[value.DXY]

    ventmoyenmax,datventmoyenmax = jour.order_by('-FXY')[0].FXY,jour \
            .order_by('-FXY')[0].DATJ.strftime('%d/%m')
    rafmax,datrafmax = jour.order_by('-FXI')[0].FXI,jour \
            .order_by('-FXI')[0].DATJ.strftime('%d/%m') 
    #Tracé des données vent   
    plt.plot(x,f,'k',label='Vent moyen max',linewidth=1.5)
    plt.plot(x,raf,'r', label='Rafales max',linewidth=0.3)
    ax.set_xticklabels([])
    ax.xaxis.set_minor_locator(dates.DayLocator(interval=2))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.grid()
    plt.ylabel('Vent km/h')
    plt.legend()
    link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'FF.png', bbox_inches="tight")
    linkFF = link+'FF.png'
    plt.close()
    
     #On traite les données PMER
    fig, ax = plt.subplots(figsize=(5, 3))
    PMER = []
    for value in jour:
        PMER+=[value.PMERM] 

    pmoy = jour.aggregate(Avg('PMERM'))['PMERM__avg'] 
    pmax = jour.order_by('-PMERM')[0].PMERM
    pmin,hpmin = jour.order_by('PMERMIN')[0].PMERMIN,jour \
                    .order_by('PMERMIN')[0].DATJ.strftime('%d/%m')
    pmax = Decimal(str(round(pmax,2)))
    pmin = Decimal(str(round(pmin,2)))
    pmoy = Decimal(str(round(pmoy,2)))
    #Tracé des données vent   
    plt.plot(x,PMER,'k',label='PMER',linewidth=1)

    ax.set_xticklabels([])

    ax.xaxis.set_minor_locator(dates.DayLocator(interval=2))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.grid()
    plt.ylabel('Pression mer hpa')
    plt.legend()
    link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'PMER.png', bbox_inches="tight")
    linkPMER = link+'PMER.png'
    plt.close()

     #On traite les données DD
    DIRINSTAN = []
    FFINSTAN = [] 
    for vent in donneevent:
        if vent.DD != None and vent.FF != None:
            DIRINSTAN += [vent.DD]
            FFINSTAN += [vent.FF]
        else: 
            DIRINSTAN += [np.NaN]
            FFINSTAN += [np.NaN]
    
    ax = WindroseAxes.from_ax() 
    ax.bar(DIRINSTAN, FFINSTAN, normed=True, bins=np.arange(0, max(f), 10), opening=0.8, edgecolor='white')
  
    ax.set_legend()
    link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'DD.png', bbox_inches="tight")
    linkDD = link+'DD.png'
    plt.close()
    
    
    
    
     #On traite les données humidité
    fig, ax = plt.subplots(figsize=(5, 3))
    UM = []
    UXabs = []
    UNabs = []
    UX,hUX = jour.order_by('-UX')[0].UX,jour.order_by('-UX')[0].DATJ \
                      .strftime('%d/%m') 
    UN,hUN = jour.order_by('UN')[0].UN,jour.order_by('UN')[0].DATJ \
                      .strftime('%d/%m')     
    for value in jour:
        UM+=[value.UM]
        UXabs+=[value.UX] 
        UNabs+=[value.UN]   
      
    plt.plot(x,UM,'k',label='Humidité moyenne',linewidth=1)
    plt.plot(x,UXabs,'--r',label='Humidité max',linewidth=0.5)
    plt.plot(x,UNabs,'--b',label='Humidité min',linewidth=0.5)
    ax.set_xticklabels([])

    ax.xaxis.set_minor_locator(dates.DayLocator(interval=2))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.grid()
    plt.ylabel('Humidite %')
    plt.legend()
    annee = debutmois.year
    mois = debutmois.month
    link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'H.png', bbox_inches="tight")
    linkH = link+'H.png'
    plt.close()

     #On traite les données ensoleillement
    enso = False
    try: 
        
        fig, ax = plt.subplots(figsize=(5, 3))
        RAD = []
 
        for value in jour:

            RAD+=[value.RAD] 
        if RAD[0] != None:
            enso = True
        cumultotalRAD = Q.objects.filter(POSTE=posteob,DATJ__gte=debutmois,
                                  DATJ__lt=finmois).aggregate(Sum('INST'))['INST__sum']
        cumultotalRAD = Decimal(str(round(cumultotalRAD,2)))
        
        hRAD,mRAD=divmod(cumultotalRAD,60)
        mRAD = int(mRAD)
        #UVmax = H.objects.filter(POSTE=posteob,DATJ__gte=debutmois,
        #                          DATJ__lt=finmois).aggregate(Max('UV'))['UV__max']
        #UVmax = Decimal(str(round(UVmax,2)))
    #Tracé des données vent   
        plt.plot(x,RAD,'y',label='Ensoleillement',linewidth=1)

        ax.set_xticklabels([])

        ax.xaxis.set_minor_locator(dates.DayLocator(interval=2))   
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))  
        for text in ax.get_xminorticklabels():
            text.set_rotation(50)
        plt.grid()
        plt.ylabel('Ensoleillement W/m²')
        plt.legend()
        link = codeposte+'/recapM/'+str(moischoisi)+str(anneechoisi)+'/' 
        if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
        plt.savefig(data_dir+link+'RAD.png', bbox_inches="tight")
        linkRAD = link+'RAD.png'
        
        #data_dir+codeposte+'/Mensuel/'+mois+'/RAD
        plt.close()
    except:
        pass
    mois_passe = False
    if finmois < datetime.datetime.now():
        try:
            mois_passe = True
            mois_en_cours = datetime.datetime(anneechoisi,moischoisi,1)
            mois = MENSQ.objects.filter(POSTE=posteob,DATJ=mois_en_cours)[0]
            NBJRR1 = mois.NBJRR1
            NBJRR5 = mois.NBJRR5
            NBJRR10 = mois.NBJRR10
            NBJRR30 = mois.NBJRR30
            NBJRR50 = mois.NBJRR50
            NBJRR100 = mois.NBJRR100
            
            NBJTX0 = mois.NBJTX0
            NBJTX25 = mois.NBJTX25
            NBJTX30 = mois.NBJTX30
            NBJTX35 = mois.NBJTX35
            NBJTXI20 = mois.NBJTXI20
            NBJTXI27 = mois.NBJTXI27
            NBJTX32 = mois.NBJTX32
    
            NBJTN5 = mois.NBJTN5
            NBJTNI10 = mois.NBJTNI10
            NBJTNI15 = mois.NBJTNI15
            NBJTNI20 = mois.NBJTNI20
            NBJTNS20 = mois.NBJTNS20
            NBJTNS25 = mois.NBJTNS25
            NBJGELEE = mois.NBJGELEE
        
            NBJFF10 = mois.NBJFF10
            NBJFF16 = mois.NBJFF16
            NBJFF28 = mois.NBJFF28
        except :
            pass
        
    

    
         
    return render(request, 'recapMensuel.html', locals())

def recapevenement(request,codeposte,codeevenement):
    #Récupération des données
    
    #Période concernée
    evenement = EVENEMENTS.objects.filter(NOM_EVENEMENT=codeevenement)[0]
    date_Debut = evenement.DEBUT
    Debut = date_Debut.strftime('%d/%m/%Y à %Hh%M')
    date_Fin = evenement.FIN
    Fin = date_Fin.strftime('%d/%m/%Y à %Hh%M')  
    
    poste = POSTE.objects.get(CODE_POSTE=codeposte)
    ins = INSTAN.objects.filter(POSTE=poste,DATJ__gte=date_Debut,DATJ__lte=date_Fin).order_by('DATJ')
     
     
    #Température
    
    #Traitement des données
    fig, ax = plt.subplots(figsize=(5, 3))
    x=[]
    y2=[]
    y=[]
    y3=[]
    for value in ins:
        x += [value.DATJ]
        y += [value.T] 
        y2 += [value.TD]   
        y3 += [value.U]  
    plt.plot(x,y,'r',label='T')
    plt.plot(x,y2,'b',label='TD') 
    plt.ylabel('Température °C')
    ax.set_xticklabels([])
    
    delta_date = date_Fin - date_Debut
    format_date(delta_date.days,ax)
    
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    ax2=ax.twinx()
    ax2.set_xticklabels([])
    ax2.plot(x,y3,'k',label='Humidité') 
    ax2.set_xticklabels([])
    plt.ylabel('Humidité %')
    fig.legend(loc="upper right")
    plt.grid()
    
    link = codeposte+'/recap/ev/'+codeposte+'/'+codeevenement +'/' 
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'T.png', bbox_inches="tight")
    linkT = link+'T.png'
    plt.close()
    #Affichage des données
    Tempemax = ins.order_by('-T')[0]
    Tx,DateTx = Tempemax.T,Tempemax.DATJ.strftime('%d/%m à %Hh%M')
    Tempemin = ins.order_by('T')[0]
    Tn,DateTn = Tempemin.T,Tempemin.DATJ.strftime('%d/%m à %Hh%M')
    MoyTemp = ins.aggregate(Avg('T'))['T__avg']
    MoyTemp = Decimal(str(round(float(MoyTemp),2)))
    ICmax = ins.order_by('-IC')[0].IC
    WINDCHILLmax = ins.order_by('-WINDCHILL')[0].WINDCHILL
    
    
    #Pluviomètrie
    Precip = H.objects.filter(POSTE=poste,DATJ__gt=date_Debut
                              ,DATJ__lte=date_Fin).order_by('DATJ')
    RR1 = []
    RRI = []
    hr=[]
    cumulmax= Precip.order_by('-RR1')[0].RR1
    cumulmax=Decimal(str(round(float(cumulmax),2)))
    cumulmaxH = Precip.order_by('-RR1')[0].DATJ.strftime('%d/%m à %Hh%M')
    cumultotal =Precip.aggregate(Sum('RR1'))['RR1__sum']
    cumultotal = Decimal(str(round(cumultotal,2)))
    for value in Precip:
        RR1+=[value.RR1]
        hr+=[value.DATJ]
        if value.RRI == None:
            RRI+=[0]
        else:
            RRI+=[value.RRI]      
    maxRRI,hrmaxRRI = Precip.order_by('-RRI')[0].RRI,Precip.order_by('-RRI')[0] \
                        .DATJ.strftime('%Hh%M')
    plt.xlabel('Heure')        
    barWidth = 1
    r = range(len(RR1))
    #On trace les données précipitations
    fig, ax1 = plt.subplots(figsize=(5, 3))
    ax1.bar(r, RR1, width = barWidth, color = ['blue' for i in RR1],
            edgecolor = ['yellow' for i in RR1], 
            linestyle = 'solid',linewidth = 1)
    ax1.set_ylabel('Pluviomètrie mm')
    #plt.bar(r, y2, width = barWidth, bottom = y1, color = ['pink' for i in y1],edgecolor = ['green' for i in y1], linestyle = 'dotted', hatch = 'o',linewidth = 3)
    plt.xticks([r + barWidth / 2 for r in range(0,len(RR1),5)],
                [hr[i].strftime('%H h') for i in range(0,len(RR1),5)])       
    plt.xticks(rotation=70)
    ax2 = ax1.twinx()
    ax2.plot(r,RRI,'r',label='Intensité')        
    plt.legend()
    plt.grid()
    link = codeposte+'/recap/ev/'+codeposte+'/'+codeevenement +'/' 
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'RR.png', bbox_inches="tight")
    linkRR = link+'RR.png'
    plt.close()
    
     #On traite les données PMER
    fig, ax = plt.subplots(figsize=(5, 3))
    PMER = []
    for value in ins:
        PMER+=[value.PMER] 
        
    pmoy = ins.aggregate(Avg('PMER'))['PMER__avg'] 
    pmax = ins.order_by('-PMER')[0].PMER
    pmin,hpmin= ins.order_by('PMER')[0].PMER,ins.order_by('PMER')[0].DATJ \
                .strftime('%Hh%M')     
    pmoy = Decimal(str(round(pmoy,2)))   
    #Tracé des données vent   
    plt.plot(x,PMER,'k',label='PMER',linewidth=1)
    ax.set_xticklabels([])
    format_date(delta_date.days,ax)  
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.grid()
    plt.ylabel('Pression mer hpa')
    plt.legend()
    link = codeposte+'/recap/ev/'+codeposte+'/'+codeevenement +'/' 
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'PMER.png', bbox_inches="tight")
    linkPMER = link+'PMER.png'
    plt.close()
    
    #On traite les données vents
    fig, ax = plt.subplots(figsize=(5, 3))
    dir = []
    f = []
    raf=[]
    for value in ins:
        raf+=[value.FXI] 
        f+=[value.FF]
        dir+=[value.DD]   
  
    ventmoyenmax = ins.order_by('-FF')[0].FF
    rafmax,hrrafmax = ins.order_by('-FXI')[0].FXI,ins.order_by('-FXI')[0] \
        .DATJ.strftime('%Hh%M')
    #Tracé des données vent   
    plt.plot(x,f,'k',label='Vent moyen',linewidth=1.5  )
    plt.plot(x,raf,'r', label='Rafales',linewidth=0.3)
    plt.legend()
    ax2 = ax.twinx()
    ax2.plot(x,dir,'*k', label='Direction vent moyen')
    ax.set_xticklabels([])
    format_date(delta_date.days,ax) 
    for text in ax.get_xminorticklabels():
        text.set_rotation(50)
    plt.grid()
    plt.ylabel('Vent km/h')
    plt.legend()
    link = codeposte+'/recap/ev/'+codeposte+'/'+codeevenement +'/' 
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'FF.png', bbox_inches="tight")
    linkFF = link+'FF.png'
    plt.close()
    
     #On traite les données DD
    DD = []
    for value in ins:
        if value.DD==None:
            DD+=[np.nan]
        else:
            DD+=[value.DD] 

    ax = WindroseAxes.from_ax() 
    ax.bar(DD, f, normed=True, bins=np.arange(0, max(f), 10), opening=0.8, edgecolor='white')

    ax.set_legend()
    link = codeposte+'/recap/ev/'+codeposte+'/'+codeevenement +'/' 
    if not os.path.exists(data_dir+link):
                    os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'DD2.png', bbox_inches="tight")
    linkDD2 = link+'DD2.png'
    plt.close()
    
    couleur_pluie = ['0400d6','006ed6','0082fe','','','','','ff003a','c1002c','ab0000']
    couleur_vent = ['aa00e1','e13300','e1bc00','','','','','','','']
    couleur_intensite = ['0400d6','006ed6','0082fe','','','','','','','']
    couleur_X = ['ab0000','c1002c','ff003a','','','','','','','']
    #Comparaison des stations d'un épisode
    
    #Récupérations des stations concernées
    ev = EVENEMENTS.objects.get(NOM_EVENEMENT=codeevenement)
    postes_evenement = POSTE_EVENEMENTS.objects.filter(EVENEMENTS=ev)
    
    liste_cumul1h= []
    liste_RRI = []
    liste_FXI = []
    liste_TX = []
    liste_TN = []
    liste_UX = []
    liste_UN = []
    liste_cumul = []
   
    #Récupération des données des stations concernées
    for poste in postes_evenement:
        Precip_comp = H.objects.filter(POSTE=poste.POSTE,DATJ__gt=date_Debut
                              ,DATJ__lte=date_Fin).order_by('DATJ')
        H_comp = H.objects.filter(POSTE=poste.POSTE,DATJ__gte=date_Debut,DATJ__lt=date_Fin).order_by('DATJ')
        try:
            cumultotal= Precip_comp.aggregate(Sum('RR1'))['RR1__sum']
            if cumultotal != None:
                liste_cumul +=[[cumultotal,poste.POSTE]]
            
        except:
            pass
        for valuesRR in Precip_comp:
            
            liste_cumul1h += [[Decimal(str(round(float(valuesRR.RR1),2))),valuesRR.DATJ.strftime('%d/%m à %Hh%M'),poste.POSTE.CODE_POSTE]]
        
        for values in H_comp:
            liste_FXI += [[Decimal(str(round(float(values.FXI),2))),values.HXI.strftime('%d/%m à %Hh%M'),poste.POSTE.CODE_POSTE]]
            liste_TX += [[Decimal(str(round(float(values.TX),2))),values.HTX.strftime('%d/%m à %Hh%M'),poste.POSTE.CODE_POSTE]]
            liste_TN += [[Decimal(str(round(float(values.TN),2))),values.HTN.strftime('%d/%m à %Hh%M'),poste.POSTE.CODE_POSTE]]
            liste_UX += [[Decimal(str(round(float(values.UX),2))),values.HUX.strftime('%d/%m à %Hh%M'),poste.POSTE.CODE_POSTE]]
            liste_UN += [[Decimal(str(round(float(values.UN),2))),values.HUN.strftime('%d/%m à %Hh%M'),poste.POSTE.CODE_POSTE]]
            liste_RRI += [[Decimal(str(round(float(values.RRI),2))),values.HRRI.strftime('%d/%m à %Hh%M'),poste.POSTE.CODE_POSTE]]
       
    #Top des RR1
  
    liste_cumul1h = sorted(liste_cumul1h,reverse=True)
    liste_cumul1h = liste_cumul1h[0:10]
    for i in range(0,10):
        liste_cumul1h[i] += [couleur_pluie[i]]
        
    #Top des RRI
    liste_RRI = sorted(liste_RRI,reverse=True)
    liste_RRI = liste_RRI[0:10]
    for i in range(0,10):
        liste_RRI[i] += [couleur_intensite[i]]
    #Top des FXI
    liste_FXI = sorted(liste_FXI,reverse=True)
    liste_FXI = liste_FXI[0:10]
    for i in range(0,10):
        liste_FXI[i] += [couleur_vent[i]]
    #Top des TX
    liste_TX = sorted(liste_TX,reverse=True)
    liste_TX = liste_TX[0:10]
    for i in range(0,10):
        liste_TX[i] += [couleur_X[i]]
    #Top des TN
    liste_TN = sorted(liste_TN,reverse=False)
    liste_TN = liste_TN[0:10]
    for i in range(0,10):
        liste_TN[i] += [couleur_intensite[i]]
    #Top des UX
    liste_UX = sorted(liste_UX,reverse=True)
    liste_UX = liste_UX[0:10]
    for i in range(0,10):
        liste_UX[i] += [couleur_intensite[i]]
    #Top des TN
    liste_UN = sorted(liste_UN,reverse=False)
    liste_UN = liste_UN[0:10]
    for i in range(0,10):
        liste_UN[i] += [couleur_X[i]]
    #Top cumul
    liste_cumul = sorted(liste_cumul,reverse=False)
    liste_cumul = liste_cumul[0:3]
    for i in range(0,len(liste_cumul)):
        liste_cumul[i] += [couleur_intensite[i]]
    return render(request, 'recapEvenement.html', locals())


def rapport(request,codeposte,date):   
    
   
    date = date.split('_')
    mois = int(date[0])
    annee = int(date[1])
    mois=str(mois)
    
    
    liste_mois_chiffre = [str(i) for i in range(1,13)]
    liste_mois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet',
                  'Août','Septembre','Octobre','Novembre','Décembre']
    indice = liste_mois_chiffre.index(mois)
    mois_entier = liste_mois[indice]
    date_rapport = mois_entier  + ' ' + str(annee)
    poste = POSTE.objects.get(CODE_POSTE=codeposte)
    nomposte = poste.NOM
    ville = poste.COMMUNE.NOMCOMMUNE
    lat = poste.LAT
    lon = poste.LON
    alt = poste.ALT 
    type = poste.TYPE 
    typinfo = poste.TYPINFO 
    
    #----------------COMMENTAIRES TEMPERATURE--------------------------------
    
    #Traitement des données du mois en cours
    mois = int(mois)
    if mois == 12:
            nextmois = 1
            nextannee = annee+1
    else:
            nextmois= mois+1
            nextannee = annee
    #FILTRE QUOTIDIEN SUR LES JOURNEES DU MOIS
    Filtre = Q.objects.filter(POSTE=poste, 
                        DATJ__gte=datetime.datetime(annee,mois,1),
                        DATJ__lt=datetime.datetime(nextannee,nextmois,1)).order_by('DATJ')
    #FILTRE DONNEES 5 MIN DU MOIS
    FiltreDD = INSTAN.objects.filter(POSTE=poste, 
                        DATJ__gte=datetime.datetime(annee,mois,1),
                        DATJ__lt=datetime.datetime(nextannee,nextmois,1)).order_by('DATJ')
    
    TM = Filtre.aggregate(Avg('TM'))['TM__avg']
    TM = Decimal(str(round(float(TM),2)))
    #FILTRE DONNEES MENSUEL DU MOIS
    FiltreMois = MENSQ.objects.filter(POSTE=poste, 
                        DATJ=datetime.datetime(annee,mois,1))[0]
    #moyenne des Tx, Tn                    
    TX=FiltreMois.TX
    TX = Decimal(str(round(float(TX),2))) 
    TN=FiltreMois.TN
    TN = Decimal(str(round(float(TN),2)))                     
    
    #Récupération de tous les mois identiques sur toutes les années
    T_autresmois = [] #liste des T moyennes
    DATT_autresmois = [] 
    TXAB_autremois = [] #liste des TX des mois identiques
    TNAB_autremois = [] #liste des TN des mois identiques
    derniereannee = datetime.datetime.now()
    for iannee in range(2000,derniereannee.year+1):
        #Mois identiques
        try:
            if mois == 12:
                nextmois = 1
                nextannee = iannee+1
            else:
                nextmois= mois+1
                nextannee = iannee
            FiltreT = Q.objects.filter(POSTE=poste,
                                       DATJ__gte=datetime.datetime(iannee,mois,1),
                                       DATJ__lt=datetime.datetime(nextannee,nextmois,1)).order_by('DATJ')
            
                                       
            T_mois = FiltreT.aggregate(Avg('TM'))['TM__avg']
            T_mois = Decimal(str(round(float(T_mois),2)))  
            T_autresmois+=[T_mois]
            DATT_autresmois+=[annee]
        except:
            pass
        try:
            FiltreTAB = MENSQ.objects.filter(POSTE=poste,
                                       DATJ=datetime.datetime(iannee,mois,1)).order_by('DATJ')
            
            TXAB_autremois +=[FiltreTAB[0].TXAB]
            TNAB_autremois +=[FiltreTAB[0].TNAB]                           
            
        except:
            pass
        
    #Valeurs dans l'ordre croissante/décroissant    
    T_autresmois_classe = sorted(T_autresmois)
    TM_autresmois = np.mean(T_autresmois)    
    TXAB_autresmois_classe = sorted(TXAB_autremois,reverse = True)  
    TNAB_autresmois_classe = sorted(TNAB_autremois) 
     
    delta_T = TM - TM_autresmois 
    if delta_T > 0:
        color_T = 'red'
    elif delta_T < 0:
        color_T = 'blue'
    else:
        color_T= 'black'                       
    TXAB = FiltreMois.TXAB
    TXABDAT = FiltreMois.TXABDAT.strftime('%d')
    TNAB = FiltreMois.TNAB
    TNDAT = FiltreMois.TNDAT.strftime('%d')
    
    indiceTXAB = TXAB_autresmois_classe.index(TXAB) +1
    indiceTNAB = TNAB_autresmois_classe.index(TNAB) +1
    #----------------RECORDS TEMPERATURE--------------------------------
    link = codeposte+'/recapM/'+str(mois)+str(annee)+'/' 
    linkT = link+'T.png'
    linkRR = link+'RR1.png'
    linkDD = link+'DD.png'
    #Record - Classement
    
  
    Record_T = []
    divT=False
    if T_autresmois_classe[0] == TM_autresmois:
        divT = True
        Record_T += ["Il s'agit du mois de " +str(mois_entier) + " le plus \
         froid depuis la mise en route de la station."]
    if T_autresmois_classe[-1] == TM_autresmois:
        divT = True
        Record_T += ["Il s'agit du mois de " +str(mois_entier) + " le plus \
         chaud depuis la mise en route de la station."]
    if indiceTXAB < 5: 
        divT = True
        Record_T  += ["La TX est classée en position "+str(indiceTXAB)+" parmi les TX des mois de " + str(mois_entier) +"."]  
    if indiceTNAB < 5:
        divT = True
        Record_T  += ["La TN est classée en position "+str(indiceTNAB)+" parmi les TN des mois de " + str(mois_entier) +"."]    
      
    FiltreT_annee = MENSQ.objects.filter(POSTE=poste,DATJ__lte=derniereannee).order_by('DATJ')
    #Classement Moyenne de T sur toute l'année
    TXABSOLU = FiltreT_annee.order_by('-TXAB')[0].TXAB
    if TXABSOLU <= TXAB:
        divT = True
        Record_T+=["Il s'agit de la TX la plus élevée depuis la mise en route de la station, tous mois confondus."]
    TNABSOLU = FiltreT_annee.order_by('TNAB')[0].TNAB
    if TNABSOLU >= TNAB:
        divT = True
        Record_T+=["Il s'agit de la TN la plus basse depuis la mise en route de la station, tous mois confondus."]
     
    #Image comparative des mois de Février
    fig, ax = plt.subplots(figsize=(6, 2))
       
    p1 = plt.bar(DATT_autresmois, T_autresmois, width=0.35)
    plt.ylabel('T moyenne - °C', size=7)
    plt.title('Moyenne des températures du mois de '+mois_entier, size=7)
    plt.xlim(2013,derniereannee.year)
    plt.savefig(data_dir+'RapportT.png', bbox_inches="tight")
    
    link = codeposte+'/recapM/'+str(mois)+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'compT.png', bbox_inches="tight")
    linkcompT = link+'compT.png'
    
    plt.close()
    
    #----------------COMMENTAIRES PLUVIOMETRIE--------------------------------
    cumul = FiltreMois.RR
    cumul24 = FiltreMois.RRAB
    datecumul24 = FiltreMois.RRABDAT.strftime('%d')
    RR_autremois = []
    DATRR_autremois = []
    #Moyenne RR des mois identiques
    for annee in range(2000,derniereannee.year+1):
        #Mois identiques
        try:
            FiltreRR = MENSQ.objects.filter(POSTE=poste,
                                       DATJ=datetime.datetime(annee,mois,1)).order_by('DATJ')
            RR_autremois +=[FiltreRR[0].RR]
            DATRR_autremois +=[annee]                          
        except:
            pass
    RR_mean = np.mean(RR_autremois)
    
    exc_def = ((cumul - RR_mean)*100)/RR_mean
    if exc_def > 0:
        Comm_exc_def = " en excédent de " + str(exc_def)
        colorRR="blue"
    elif exc_def < 0:
        Comm_exc_def = " en déficit de " + str(exc_def)
        colorRR="red"
    else:
        Comm_exc_def = " normal"
        colorRR="black"
        
    #----------------RECORDS PLUVIOMETRIE--------------------------------
    
    
    #Classement par rapport aux autres mois identiques
    RR_autresmois_classe_def = sorted(RR_autremois)
    RR_autresmois_classe_exc = sorted(RR_autremois,reverse=True)
    Record_RR = []
    indiceRRexc = RR_autresmois_classe_exc.index(cumul) +1
    indiceRRdef = RR_autresmois_classe_def.index(cumul) +1
    divRR = False
    if indiceRRexc == 1:
        divRR=True
        Record_RR+=["Mois de "+str(mois_entier)+
                    " le plus pluvieux parmi tous les mois de Février de la station."]
    elif indiceRRexc <= 5:
        divRR=True
        Record_RR+=[str(indiceRRexc)+ "ème mois de "+str(mois_entier)+
                    " le plus pluvieux parmi tous les mois de Février de la station."]

    if indiceRRdef == 1:
        divRR=True
        Record_RR+=["Mois de "+str(mois_entier)+
                    " le plus sec parmi tous les mois de Février de la station."]
    elif indiceRRdef <= 5:
        divRR=True
        Record_RR+=[str(indiceRRdef)+ "ème mois de "+str(mois_entier)+
                    " le plus sec parmi tous les mois de Février de la station."]
    
    
    #Classement absolu
    FiltreRR_annee = MENSQ.objects.filter(POSTE=poste,DATJ__lte=derniereannee).order_by('DATJ')
    RRABSOLU = FiltreRR_annee.order_by('-RR')[0].RR
    if RRABSOLU <= cumul:
        divRR=True
        Record_RR+=["Il s'agit du mois le plus pluvieux depuis la mise en route de la station, tous mois confondus."]
    RRMINABSOLU = FiltreRR_annee.order_by('RR')[0].RR
    if RRMINABSOLU >= cumul:
        divRR=True
        Record_RR+=["Il s'agit du mois le plus sec depuis la mise en route de la station, tous mois confondus."]
    
    #Image comparative des mois identiques
    fig, ax = plt.subplots(figsize=(6, 2))
       
    p1 = plt.bar(DATRR_autremois, RR_autremois, width=0.35)
    plt.ylabel('Pluviomètrie - mm', size=7)
    plt.title('Précipitations du mois de '+mois_entier, size=7)
    plt.xlim(2013,derniereannee.year)
    link = codeposte+'/recapM/'+str(mois)+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'compRR.png', bbox_inches="tight")
    linkcompRR = link+'compRR.png'
    
    plt.close()
    
    #----------------VENT--------------------------------
    
   
    
    DD=[]
    FF=[]
    for value in FiltreDD:
        FF+=[value.FF]
        if value.DD==None:
            DD+=[np.nan]
        else:
            DD+=[value.DD] 
    DDmoy = np.nanmean(DD)
    DDmoy = Decimal(str(round(float(DDmoy),2))) 
    
    ax = WindroseAxes.from_ax() 
    ax.bar(DD, FF, normed=True, bins=np.arange(0, max(FF), 10), opening=0.8, edgecolor='white')
   
    ax.set_legend()
     
     
    link = codeposte+'/rapportM/'+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'DD.png', bbox_inches="tight")
    linkDD = link+'DD.png'
    plt.close()    
#     
#     
#     #Fréquences de direction
#     table = ax._info['table']
#     wd_freq = np.sum(table, axis=0)
#     direction = ax._info['dir']
#     wd_freq = np.sum(table, axis=0)
#     max_freq = 0
#     indice_max = 0
#     for i in range(0,len(wd_freq)):
#         if wd_freq[i] >= max_freq:
#             max_freq = round(wd_freq[i],2)
#             indice_max = i
#             
#     listedirfreq = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
#                 'S','SSO','SO','OSO','O','ONO','NO','NNO']
#     dir_freqmax = listedirfreq[indice_max]
    
    
    FFmoy = np.nanmean(FF)
    FFmoy = Decimal(str(round(float(FFmoy),2))) 
    
    DirDD=fonction_direction(DDmoy)
    
    Ventmoyenmax = Filtre.order_by('-FXY')[0]
    FXY= Ventmoyenmax.FXY
    DXY= Ventmoyenmax.DXY
    HXY= Ventmoyenmax.HXY.strftime('%d')
    DirDXY=fonction_direction(DXY)
    Rafmax = Filtre.order_by('-FXI')[0]
    FXI= Rafmax.FXI
    HXI= Rafmax.HXI.strftime('%d')
    NBJFF10 = FiltreMois.NBJFF10
    NBJFF16 = FiltreMois.NBJFF16
    NBJFF28 = FiltreMois.NBJFF28
    
    if NBJFF28 > 0:
        CommFF = "On relève " + str(NBJFF28) +" jours de vents très forts sur cette période (rafales supérieures à 100km/h)."
    elif NBJFF16 > 0:
        CommFF = "On relève " + str(NBJFF16) + " jours de vents forts sur cette période (rafales supérieures à 58km/h)."
    elif NBJFF10 > 0:
        CommFF = "On relève " + str(NBJFF10) +" jours de vents modérés sur cette période (rafales supérieures à 36km/h)."
    
    FiltreDD_tousmois = INSTAN.objects.filter(POSTE=poste, DATJ__lt=derniereannee).order_by('DATJ')
    divFF = False
    FFABS = FiltreDD_tousmois.order_by('-FXI')[0].FXI
    if FFABS <= FXI:
        divFF = True
        RecordFF = str(FFmoy) +"km/h est le nouveau record absolu de vent pour cette station."
        
        
    #Autres paramètres    
    #Pression
    donneesPMERMAX = FiltreDD.order_by('-PMER')[0]
    PMERMAX,datePMERMAX = donneesPMERMAX.PMER,donneesPMERMAX.DATJ.strftime('%d/%m')
    donneesPMERMIN = FiltreDD.order_by('PMER')[0]
    PMERMIN,datePMERMIN = donneesPMERMIN.PMER,donneesPMERMIN.DATJ.strftime('%d/%m')
    #Ensoleillement
    INST = FiltreMois.INST 
    h = FiltreMois.INST/60
    if h >= 24:
        j = int(INST/60/24)
        h = int(INST%60) 
        commINST = str(j)+'j'+str(h)+'h'
    else: 
        h= int(INST/60)
        m=int(INST%60)
        commINST = str(h)+'j'+str(h)+'m'
    #IC
    donneesICMAX = FiltreDD.order_by('-IC')[0]
    ICMAX,dateICMAX = donneesICMAX.IC,donneesICMAX.DATJ.strftime('%d/%m')
    donneesICMIN = FiltreDD.order_by('IC')[0]
    ICMIN,dateICMIN = donneesICMIN.IC,donneesICMIN.DATJ.strftime('%d/%m')
    #wc
    donneesWCMAX = FiltreDD.order_by('-WINDCHILL')[0]
    WCMAX,dateWCMAX = donneesWCMAX.WINDCHILL,donneesWCMAX.DATJ.strftime('%d/%m')
    donneesWCMIN = FiltreDD.order_by('WINDCHILL')[0]
    WCMIN,dateWCMIN = donneesWCMIN.WINDCHILL,donneesWCMIN.DATJ.strftime('%d/%m')
    return render(request, 'rapport.html', locals())
 

def rapportannuel(request,codeposte,date):   
    
   
    annee = int(date)
   
    
    
    
    date_rapport =  str(annee)
    poste = POSTE.objects.get(CODE_POSTE=codeposte)
    
    nomposte = poste.NOM
    ville = poste.COMMUNE.NOMCOMMUNE
    lat = poste.LAT
    lon = poste.LON
    alt = poste.ALT 
    type = poste.TYPE 
    typinfo = poste.TYPINFO 
    
    liste_mois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet',
                  'Août','Septembre','Octobre','Novembre','Décembre']
    
    
    #----------------COMMENTAIRES TEMPERATURE--------------------------------
    
    
    #FILTRE QUOTIDIEN DE L'ANNEE
    FiltreQ = Q.objects.filter(POSTE=poste, 
                        DATJ__gte=datetime.datetime(annee,1,1),
                        DATJ__lte=datetime.datetime(annee,12,31)).order_by('DATJ')
                        
    donneevent = INSTAN.objects.filter(POSTE=poste, 
                        DATJ__gte=datetime.datetime(annee,1,1),
                        DATJ__lte=datetime.datetime(annee,12,31)).order_by('DATJ')
  
    #Graphs sur l'année
    
    #Moyenne des températures de chaque mois, + TX + TN, +moyenne TX Tn
 
    T = []
    TX = []
    TN = []
    liste_NBJTX35 = []
    liste_NBJTX32 = []
    liste_NBJTX30 = []
    liste_NBJTX25 = []
    
    liste_NBJTN5  = []
    liste_NBJTNI10  = []
    liste_NBJTNI15  = []
    liste_NBJTNI20  = []
    liste_NBJTNS20  = []
    liste_NBJTNS25  = []
    liste_NBJGELEE  = []
    test = []
    mois_liste= [int(i) for i in range(1,13)]
    for mois in range(1,13):
        if mois == 12:
            nextmois = 1
            nextannee= annee+1
        else:
            nextmois = mois+1
            nextannee = annee
            
        FiltreQMois = Q.objects.filter(POSTE=poste, 
                        DATJ__gte=datetime.datetime(annee,mois,1),
                        DATJ__lt=datetime.datetime(nextannee,nextmois,1)).order_by('DATJ')
        FiltreMensq = MENSQ.objects.filter(POSTE=poste, 
                        DATJ=datetime.datetime(annee,mois,1)).order_by('DATJ')
                        
                        
        TM_mois = FiltreQMois.aggregate(Avg('TM'))['TM__avg']
        
        souscumul = 0
        for sousmois in range(1,mois+1):
            sousFiltreMensq = MENSQ.objects.filter(POSTE=poste, 
                        DATJ=datetime.datetime(annee,sousmois,1)).order_by('DATJ')
            try:            
                souscumul += sousFiltreMensq[0].RR 
            except:
                souscumul = souscumul 
        test+=[souscumul]
        try :
            TX_mois = FiltreQMois.order_by('-TX')[0].TX
            TN_mois = FiltreQMois.order_by('TN')[0].TN
        except: 
            TX_mois = np.NaN
            TN_mois = np.NaN
        try:
            liste_NBJTX35 += [FiltreMensq[0].NBJTX35]
            liste_NBJTX32 += [FiltreMensq[0].NBJTX32]
            liste_NBJTX30 += [FiltreMensq[0].NBJTX30]
            liste_NBJTX25 += [FiltreMensq[0].NBJTX25]
            liste_NBJTN5  += [FiltreMensq[0].NBJTN5]
            liste_NBJTNI10  += [FiltreMensq[0].NBJTNI10]
            liste_NBJTNI15  += [FiltreMensq[0].NBJTNI15]
            liste_NBJTNI20  += [FiltreMensq[0].NBJTNI20]
            liste_NBJTNS20  += [FiltreMensq[0].NBJTNS20]
            liste_NBJTNS25 += [FiltreMensq[0].NBJTNS25]
            liste_NBJGELEE  += [FiltreMensq[0].NBJGELEE]
        except:
            
            liste_NBJTX35 += [np.NaN]
            liste_NBJTX32 += [np.NaN]
            liste_NBJTX30 += [np.NaN]
            liste_NBJTX25 += [np.NaN]
            liste_NBJTN5  += []
            liste_NBJTNI10  += []
            liste_NBJTNI15  += []
            liste_NBJTNI20  += []
            liste_NBJTNS20  += []
            liste_NBJTNS25  += []
            liste_NBJGELEE  += []
        if TM_mois != None:
            TM_mois = Decimal(str(round(float(TM_mois),2)))
        else:
            TM_mois = np.NaN
        
        #moyenne des T, chaque mois    
        T += [TM_mois]
        TX+=[Decimal(str(round(float(TX_mois),2)))]
        TN+=[Decimal(str(round(float(TN_mois),2)))]
        
    fig, ax = plt.subplots(figsize=(6, 3))
    plt.bar(mois_liste, TX, width=0.5, color='red',label='TX') 
    plt.bar(mois_liste, T, width=0.5, color='black',label='TM') 
    plt.bar(mois_liste, TN, width=0.5, color='blue',label='TN') 
    plt.grid()
    plt.ylabel('Température °C')
    plt.title("Températures de l'année " +str(annee))
    plt.xlim(0,12)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
    fig.legend(loc="upper right")
    
    link = codeposte+'/rapportA/'+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'T.png', bbox_inches="tight")
    linkT = link+'T.png'
    plt.close()   
    
    #Commentaires
    TMmax = np.nanmax(T)
    indiceTMmax = T.index(TMmax)+1
    TMmaxdate = liste_mois[indiceTMmax]
    
    TMmin = np.nanmin(T)
    indiceTMmin = T.index(TMmin)+1
    TMmindate = liste_mois[indiceTMmin]
    
    TXabs = np.nanmax(TX)
    indiceTXabs = TX.index(TXabs)+1
    dateTX = liste_mois[indiceTXabs]
    
    TNabs = np.nanmax(TN)
    indiceTNabs = TN.index(TNabs)+1
    dateTN = liste_mois[indiceTNabs]
    Comm_T=[]
    if np.nanmax(liste_NBJTX35) > 0:
        datemax35 = liste_mois[liste_NBJTX35.index(np.nanmax(liste_NBJTX35))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTX35)) +
                 'j avec plus des maxis de plus de 35°C en ' + datemax35 +'.']
    elif np.nanmax(liste_NBJTX32) > 0:
        datemax32 = liste_mois[liste_NBJTX32.index(np.nanmax(liste_NBJTX32))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTX32)) +
                 'j avec des maxis de plus de 32°C en ' + datemax32+'.']
    elif np.nanmax(liste_NBJTX30) > 0:
        datemax30 = liste_mois[liste_NBJTX30.index(np.nanmax(liste_NBJTX30))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTX30)) +
                 'j avec des maxis de plus de 30°C en ' + datemax30+'.']
    elif np.nanmax(liste_NBJTX25) > 0:
        datemax25 = liste_mois[liste_NBJTX25.index(np.nanmax(liste_NBJTX25))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTX25)) +
                 'j avec des maxis de plus de 25°C en ' + datemax25+'.']
        
    if np.nanmax(liste_NBJTN5) > 0:
        datemin5 = liste_mois[liste_NBJTN5.index(np.nanmax(liste_NBJTN5))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTN5)) +
                 'j avec des minis de moins de -5°C en ' + datemin5+'.']
    elif np.nanmax(liste_NBJGELEE) > 0:
        dateminGE = liste_mois[liste_NBJGELEE.index(np.nanmax(liste_NBJGELEE))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJGELEE)) +
                 'j avec des minis de moins de 0°C en ' + dateminGE+'.']      
    elif np.nanmax(liste_NBJTNI10) > 0:
        datemin10 = liste_mois[liste_NBJTNI10.index(np.nanmax(liste_NBJTNI10))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTNI10)) +
                 'j avec des minis de moins de 10°C en ' + datemin10+'.'] 
    elif np.nanmax(liste_NBJTNI15) > 0:
        datemin15 = liste_mois[liste_NBJTNI15.index(np.nanmax(liste_NBJTNI15))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTNI15)) +
                 'j avec des minis de moins de 15°C en ' + datemin15+'.'] 
    elif np.nanmax(liste_NBJTNI20) > 0:
        datemin20 = liste_mois[liste_NBJTNI20.index(np.nanmax(liste_NBJTNI20))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTNI20)) +
                 'j avec des minis de moins de 20°C en ' + datemin20+'.'] 
    if np.nanmax(liste_NBJTNS20) > 0:
        dateminS20 = liste_mois[liste_NBJTNS20.index(np.nanmax(liste_NBJTNS20))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTNS20)) +
                 'j avec des minis de plus de 20°C en ' + dateminS20+'.']
    elif np.nanmax(liste_NBJTNS25) > 0:
        dateminS25 = liste_mois[liste_NBJTNS25.index(np.nanmax(liste_NBJTNS25))+1]
        Comm_T+=['Il y a eu ' + str(np.nanmax(liste_NBJTNS25)) +
                 'j avec des minis de plus de 25°C en ' + dateminS25+'.']    
    
    #----------------PARTIE PRECIPITATIONS--------------------------------
    Cumul = []
    Cumul1j =[]
    Cumul1jdate =[]
    DRR_mois = []
    NBJRR1 = 0
    NBJRR5 = 0
    NBJRR10 =  0
    NBJRR30 = 0
    NBJRR50 =  0
    NBJRR100 = 0 
    for mois in range(1,13):
        if mois == 12:
            nextmois = 1
            nextannee= annee+1
        else:
            nextmois = mois+1
            nextannee = annee
            
        FiltreMensq = MENSQ.objects.filter(POSTE=poste, 
                        DATJ=datetime.datetime(annee,mois,1)).order_by('DATJ')
        FiltreQ = Q.objects.filter(POSTE=poste,DATJ__gte=datetime.datetime(annee,mois,1),
                                   DATJ__lt=datetime.datetime(nextannee,nextmois,1)).order_by('DATJ')
        
        try:
            DRR = FiltreQ.aggregate(Sum('DRR'))['DRR__sum']
            if DRR != None:
                DRR_mois+=[DRR]  
            else:
                DRR_mois+=[np.NaN] 
        except: 
            DRR_mois+=[np.NaN]                    
        try:                
            Cumul+=[FiltreMensq[0].RR]
            Cumul1j+=[FiltreMensq[0].RRAB]
            Cumul1jdate+=[FiltreMensq[0].RRABDAT.strftime('%d/%m')] 
        except:
            Cumul+=[np.NaN]
            Cumul1j+=[np.NaN]
            Cumul1jdate+=[np.NaN]

        try:
            NBJRR1+=FiltreMensq[0].NBJRR1
            NBJRR5+=FiltreMensq[0].NBJRR5
            NBJRR10+=FiltreMensq[0].NBJRR10
            NBJRR30+=FiltreMensq[0].NBJRR30
            NBJRR50+=FiltreMensq[0].NBJRR50
            NBJRR100+=FiltreMensq[0].NBJRR100
        except: 
            pass
        
    fig, ax = plt.subplots(figsize=(6, 3))
    plt.bar(mois_liste,Cumul, width=0.5,color='black',label='Cumul')
    plt.fill_between(mois_liste, test,alpha = 0.3,facecolor='blue') 
    plt.ylabel('Pluviométrie mm') 
    
    ax2= ax.twinx()
    ax2.bar(mois_liste,DRR_mois,color='red',label='Durée',width=0.5,alpha=0.4)
    plt.ylabel('Durée (min)') 
    plt.grid()
    plt.title("Précipitations de l'année " +str(annee))
    plt.xlim(0,13)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
   
    fig.legend(loc="upper right")
    link = codeposte+'/rapportA/'+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'RR.png', bbox_inches="tight")
    linkRR = link+'RR.png'
    plt.close()      
    
    #Commentaires 
    Cumulannee = np.nansum(Cumul)
    cumulpluvieux = np.nanmax(Cumul)
    indicecumulpluvieux = Cumul.index(cumulpluvieux)
    moispluvieux = liste_mois[indicecumulpluvieux]
    
    cumulsec = np.nanmin(Cumul)
    indicecumulsec = Cumul.index(cumulsec)
    moissec = liste_mois[indicecumulsec]
    
    Cumul1jmax = np.nanmax(Cumul1j)
    indiceCumul1jmax = Cumul1j.index(Cumul1jmax)
    Datecumul1jmax = Cumul1jdate[indiceCumul1jmax]
    
    Comm_RR = []
    if NBJRR100 > 0:
        Comm_RR += ["Sur l'année, il y a eu " +str(NBJRR1) + "j de pluie dont "+
                     str(NBJRR100) + "j avec plus de 100mm sur la journée."]
    elif NBJRR50 > 0:
        Comm_RR += ["Sur l'année, il y a eu " +str(NBJRR1) + "j de pluie dont " 
                    + str(NBJRR50) + "j avec plus de 50mm sur la journée."]
    elif NBJRR30 > 0:
        Comm_RR += ["Sur l'année, il y a eu " +str(NBJRR1) + "j de pluie dont " 
                    + str(NBJRR30) + "j avec plus de 30mm sur la journée."]
    elif NBJRR10 > 0:
        Comm_RR += ["Sur l'année, il y a eu " +str(NBJRR1) + "j de pluie dont " 
                    + str(NBJRR10) + "j avec plus de 10mm sur la journée."]
    elif NBJRR5 > 0:
        Comm_RR += ["Sur l'année, il y a eu " +str(NBJRR1) + "j de pluie dont " 
                    + str(NBJRR5) + "j avec plus de 5mm sur la journée."]
        
        
    #----------------PARTIE VENT-------------------------------
    
    DD = []
    FF = []
    DXYAB = []
    FXYAB = []
    FXYABDAT = []
    FXIAB = []
    FXIABDAT = []
    list_NBJFF10 = []
    list_NBJFF16 = []
    list_NBJFF28 = []
    #Rose des vents
    FiltreH = H.objects.filter(POSTE=poste,DATJ__gte=datetime.datetime(annee,1,1),
                                   DATJ__lte=datetime.datetime(nextannee,12,31,23,59)).order_by('DATJ')
    for donnees_vent in FiltreH:
        if donnees_vent.DD != None:
            DD+= [donnees_vent.DD]
        else:
            DD+=[np.NaN]
        if donnees_vent.FF != None:
            FF+= [donnees_vent.FF]
        else:
            FF+=[np.NaN]
                                   
    for mois in range(1,13):
        if mois == 12:
            nextmois = 1
            nextannee= annee+1
        else:
            nextmois = mois+1
            nextannee = annee
        FiltreMensq = MENSQ.objects.filter(POSTE=poste, 
                        DATJ=datetime.datetime(annee,mois,1)).order_by('DATJ') 
                        
        try : 
            DXYAB += [FiltreMensq[0].DXYAB] 
            FXYAB += [FiltreMensq[0].FXYAB]  
            FXYABDAT += [FiltreMensq[0].FXYABDAT]
            FXIAB += [FiltreMensq[0].FXIAB]  
            FXIABDAT += [FiltreMensq[0].FXIDAT]
            list_NBJFF10 += [FiltreMensq[0].NBJFF10]
            list_NBJFF16 += [FiltreMensq[0].NBJFF16]
            list_NBJFF28 += [FiltreMensq[0].NBJFF28]
        except:
            DXYAB += [np.NaN] 
            FXYAB += [np.NaN]
            FXYABDAT += [np.NaN]  
            FXIAB += [np.NaN]  
            FXIABDAT += [np.NaN]
            list_NBJFF10 += [np.NaN]
            list_NBJFF16 += [np.NaN]
            list_NBJFF28 += [np.NaN]
    DDmoy = np.nanmean(DD)
    DDmoy = Decimal(str(round(float(DDmoy),2)))
    
    FXY = np.nanmax(FXYAB)
    indiceFXY = FXYAB.index(FXY)
    DXY,HXY = DXYAB[indiceFXY],FXYABDAT[indiceFXY].strftime('%d/%m')
    
    FXI = np.nanmax(FXIAB)
    indiceFXI = FXIAB.index(FXI)
    HXI = FXIABDAT[indiceFXI].strftime('%d/%m')
    
    DirDXY=fonction_direction(DXY)
   
    DirDD = fonction_direction(DDmoy)     
    
    DIRINSTAN = []
    FFINSTAN = [] 
    for vent in donneevent:
        if vent.DD != None and vent.FF != None:
            DIRINSTAN += [vent.DD]
            FFINSTAN += [vent.FF]
        else: 
            DIRINSTAN += [np.NaN]
            FFINSTAN += [np.NaN]       
    ax = WindroseAxes.from_ax() 
    ax.bar(DIRINSTAN, FFINSTAN, normed=True, bins=np.arange(0, max(FF), 10), opening=0.8, edgecolor='white')
  
    ax.set_legend()
    
    
    link = codeposte+'/rapportA/'+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'DD.png', bbox_inches="tight")
    linkDD = link+'DD.png'
    plt.close()    
    
    
    #Fréquences de direction
    table = ax._info['table']
    wd_freq = np.sum(table, axis=0)
    direction = ax._info['dir']
    wd_freq = np.sum(table, axis=0)
    max_freq = 0
    indice_max = 0
    for i in range(0,len(wd_freq)):
        if wd_freq[i] >= max_freq:
            max_freq = round(wd_freq[i],2)
            indice_max = i
            
    listedirfreq = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
                'S','SSO','SO','OSO','O','ONO','NO','NNO']
    dir_freqmax = listedirfreq[indice_max]

         
    
    
                             
    #Histo nb de jours FF + FXI
    fig, ax = plt.subplots(figsize=(5, 2))
    plt.bar(mois_liste,list_NBJFF10, width=0.5,color='black',label='Rafales > 36km/h')
    plt.bar(mois_liste,list_NBJFF16, width=0.5,color='red',label='Rafales > 58km/h')
    plt.bar(mois_liste,list_NBJFF28, width=0.5,color='purple',label='Rafales > 100km/h')
    plt.ylabel('Nombre de jours') 
    plt.grid()
    plt.xlim(0,13)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
    fig.legend(loc="upper right")
    link = codeposte+'/rapportA/'+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'NBJFXI.png', bbox_inches="tight")
    linkNBJFXI = link+'NBJFXI.png'
    plt.close() 
    #Histo FXYAB FXIAB  
    fig, ax = plt.subplots(figsize=(5, 2))
    plt.bar(mois_liste,FXIAB, width=0.5,color='red',label='Rafales max')
    plt.bar(mois_liste,FXYAB, width=0.5,color='black',label='Vent moyen max')
    plt.ylabel('Vent km/h') 
    plt.grid()
    plt.xlim(0,13)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
    fig.legend(loc="upper right")
    link = codeposte+'/rapportA/'+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'FFAB.png', bbox_inches="tight")
    linkFFAB = link+'FFAB.png'
    plt.close()  
    
    #----------------PARTIE PRESSION-------------------------------
    #Graph
    FiltreQ = Q.objects.filter(POSTE=poste,DATJ__gte=datetime.datetime(annee,1,1),
                                   DATJ__lte=datetime.datetime(nextannee,12,31)).order_by('DATJ')
    
    PMER = []
    DATEPMER = []
    list_PMERMIN = []
    list_DATEPMERMIN = []
    for values in FiltreQ:
        PMER+= [values.PMERM]
        DATEPMER+= [values.DATJ]
    fig, ax = plt.subplots(figsize=(6, 3))
    plt.plot(DATEPMER,PMER,color='black',label='Pression moyenne')
    plt.ylabel('Pression (hPa)') 
    plt.grid()
    ax.set_xticklabels([])
    ax.xaxis.set_minor_locator(dates.DayLocator(interval=15))   
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d/%m'))
    for text in ax.get_xminorticklabels():
                    text.set_rotation(50)  
    fig.legend(loc="upper right")
    link = codeposte+'/rapportA/'+str(annee)+'/' 
    if not os.path.exists(data_dir+link):
            os.makedirs(data_dir+link)
    plt.savefig(data_dir+link+'PMER.png', bbox_inches="tight")
    linkPMER = link+'PMER.png'
    plt.close()  
    #Commentaires : PMIN / PMAX
    for mois in range(1,13):
        if mois == 12:
            nextmois = 1
            nextannee= annee+1
        else:
            nextmois = mois+1
            nextannee = annee
            
        FiltreMensq = MENSQ.objects.filter(POSTE=poste, 
                        DATJ=datetime.datetime(annee,mois,1)).order_by('DATJ')
        try:
            list_PMERMIN += [FiltreMensq[0].PMERMINAB]
            list_DATEPMERMIN += [FiltreMensq[0].PMERMINABDAT]
        except: 
            list_PMERMIN += [np.NaN]
            list_DATEPMERMIN += [np.NaN]
        
    PMERMIN = np.nanmin(list_PMERMIN)
    indicePMERMIN = list_PMERMIN.index(PMERMIN)
    DATEPMERMIN = list_DATEPMERMIN[indicePMERMIN].strftime('%d/%m')
    PMERMIN =Decimal(str(round(float(PMERMIN),2)))
    return render(request, 'rapportannuel.html', locals())


#EXTRACTION DE DONNEES EN CSV : CHOIX DE STATION + CHOIX DE PERIODE