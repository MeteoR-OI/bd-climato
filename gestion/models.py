

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from gestion.tools import fonction_direction

# Create your models here.

# PAYS,COMMUNE,POSTE,PANNE,INSTRUMENT,MAINTENANCE,INS,H,Q,DECADQ,MENSQ,RECMENS,HISTMAINT,HISTPOST


data_fs = FileSystemStorage(location=settings.DATA_FS_PATH)

#Données 5min 
class PAYS(models.Model):
    #id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    CODPAYS = models.IntegerField(primary_key=True, default=None)
    NOMPAYS = models.CharField(null=False, max_length =20,default=None)

    class Meta:
        verbose_name = "Pays"
        
    def __str__(self):
        return self.NOMPAYS
    
class COMMUNE(models.Model):
    NOMCOMMUNE = models.CharField(null=False, max_length=25,default=None)
    PAYS = models.ForeignKey('PAYS', on_delete=models.CASCADE,default=None) #Pour chaque commune on a qu'un seul pays
    CP = models.IntegerField(primary_key=True, null=False, verbose_name = "Code postal",default=None, unique=True) 
    
    def __str__(self):
        return self.NOMCOMMUNE
    
    class Meta:
        verbose_name = "Commune"
    
class POSTE(models.Model):
    NUM_POSTE = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID Numero de poste')
    CP = models.IntegerField(null=False, verbose_name = "Code postal",default=None)
    CODE_POSTE = models.CharField(null=False, max_length = 50, default=None, unique=True)
    REF_MF = models.CharField(null=True,max_length = 10,default=None, unique=True)
    NOM = models.CharField(null=False, verbose_name="Nom du poste (ex : NDLP)", max_length = 50,default=None)
    COMMUNE =  models.ForeignKey('COMMUNE', on_delete=models.CASCADE) #Pour chaque poste on a qu'une commune
    LAT = models.FloatField(null=False,default=None)
    LON = models.FloatField(null=False,default=None)
    ALT = models.FloatField(null=False, verbose_name = "Altitude du poste en m",default=None)
    POS = models.IntegerField(null=False, verbose_name = "Personne physique(1) - Morale (2)",default=None)
    AUT = models.IntegerField(null=False,verbose_name = "Autorisation de stockage/diffusion",default=None)
    PROP = models.CharField(null=False, verbose_name = "Nom du propriétaire/entreprise", max_length =20,default=None)
    DATEOUV = models.DateTimeField(null=False,default=None)
    DATEFERM = models.DateTimeField(null=True,default=None, blank=True)
    MAINT = models.IntegerField(null=True, verbose_name = "Code maintenance (tableau)",default=None)
    TYPE = models.CharField(null=False, verbose_name = "Modèle de station", max_length=20,default=None) 
    TYPINFO = models.CharField(null=False,verbose_name = "Type de donnees (route,agricole,pédagogique,..)", max_length=20,default=None)
    ADRESSE = models.CharField(null=False, max_length = 100,default=None)
    LIEU_DIT = models.CharField(null=True,max_length=30,default=None)
    MEL = models.CharField(null=True, max_length = 40,default=None) 
    TEL = models.CharField(null=True,max_length = 10,default=None)
    COMM = models.TextField(null=True,default=None)  
    PDT = models.IntegerField(null=False, verbose_name = "Pas de temps d'envoie (min)",default=5)
    INIT = models.IntegerField(null=True, verbose_name = "Etat d'initialisation",default=None)
    def __str__(self):
        return self.CODE_POSTE
    
class PANNE(models.Model): 
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)   
    DEBUT = models.DateTimeField(null= True)
    FIN = models.DateTimeField(null=True)
    CAPTEUR = models.CharField(null=True,max_length = 25)
    COMM = models.TextField(null=True)
    
class EVENEMENTS(models.Model):
    NOM_EVENEMENT = models.CharField(null=True,max_length = 100)
    TYPE_EVENEMENT = models.CharField(null=True,max_length = 100)
    DEBUT = models.DateTimeField(null= True)
    FIN = models.DateTimeField(null=True)

class POSTE_EVENEMENTS(models.Model): 
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)   
    EVENEMENTS = models.ForeignKey('EVENEMENTS',on_delete=models.CASCADE) 
    
class INSTRUMENT(models.Model):
    VENTILATION_CHOICES = (
    (0, 'Non ventilé'),
    (1, 'Ventilé'),
    
  
    )
    
    
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE) 
    CAPTEUR = models.CharField('Capteur', null=False, max_length = 25)
    DATDEB = models.DateTimeField(verbose_name="Date et heure de la mise en service", null=True,blank=True,help_text="AAAA-MM-JJ HH:MM")
    DATFIN = models.DateTimeField(null=True,blank=True)
    MODELE = models.CharField(null=True,verbose_name="Version et modele du capteur", max_length=25,blank=True)
    HAUTEUR = models.FloatField(verbose_name="Hauteur", null=True,blank=True,help_text="(en mètres)")
    VENTILATION = models.IntegerField(null=True, verbose_name="Ventilation du capteur ",blank=True,choices=VENTILATION_CHOICES)
    SEUILMIN = models.FloatField('Seuil min', null=True,blank=True)
    SEUILMAX = models.FloatField('Seuil max', null=True,blank=True)
    PRECISION = models.FloatField('Précision', null=True,blank=True)
    QUALITE = models.CharField(null=True,max_length=2,verbose_name="Qualite du site d'installation (voir classification)",blank=True)
    PASDETEMPS = models.FloatField(null=True, verbose_name = "Intervalle de mesure en s",blank=True)
    TYPE_TERRAIN= models.CharField(max_length=15,null=True, verbose_name = "Type de terrain sur l'implantation du capteur",blank=True)
    UNITE = models.CharField(null=True,max_length = 10, verbose_name= "Unite de mesure",blank=True)
    COMM = models.CharField(verbose_name = "Commentaires", null=True, max_length = 100,blank=True)
 
        
class MAINTENANCE(models.Model):
    
    

    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)   
    CAPTEUR = models.CharField(null=False, max_length = 25)
    DATMAINT = models.DateTimeField(null=True,verbose_name="Date de la derniere maintenance")
    DATPMAINT = models.DateTimeField(null=True,verbose_name="Date de la prochaine maintenance")
    TYPE = models.CharField(null=True, max_length=100, verbose_name = "Type de maintenance")
    IMPORTANCE = models.IntegerField(null=True,verbose_name = "1 si alteration de la mesure - 2 aucune alteration")
    ACTEUR = models.CharField(max_length=15,null=True, verbose_name="Personne s'occupant de la maintenance")
    TELACTEUR = models.IntegerField(null=True)
    COMM = models.CharField(null=True,max_length=100)


class INSTAN(models.Model): #Classe de données instantanées
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
    DATJ = models.DateTimeField(verbose_name="AAAA-MM-JJ HH-MM de la mesure")
    DATRECU = models.DateTimeField(default=timezone.now,verbose_name="AAAA-MM-JJ HH-MM de la derniere modification")
    RR = models.FloatField(null=True, default = None)
    RRI = models.FloatField(null=True,verbose_name="Intensité max des precipitations", default = None)
    FF = models.FloatField(null=True, default = None)
    DD = models.FloatField(null=True, default = None)
    FXI = models.FloatField(null=True, default = None)
    DXI = models.FloatField(null=True, default = None)
    T = models.FloatField(null=True, default = None)
    TD = models.FloatField(null=True, default = None)
    U = models.FloatField(null=True, default = None)
    PMER = models.FloatField(null=True, default = None)
    UV = models.FloatField(null=True,verbose_name = "Indice UV", default = None)
    RAD =models.FloatField(null=True, default = None)
    IC = models.FloatField(null=True,verbose_name = "Indice de chaleur", default = None)
    WINDCHILL = models.FloatField(null=True, default = None)
    ETP = models.FloatField(null=True,verbose_name="Evapotranspiration", default = None)
    HF = models.FloatField(null=True, verbose_name="Humidite du feuillage", default = None)
    HS = models.FloatField(null=True,verbose_name="Humidite du sol", default = None)
    TS = models.FloatField(null=True,verbose_name="Temperature du sol", default = None)

    def wind_dir(self):
        import numpy as np
        if self.DD:
            return self.DD
 
        return np.NaN
 
    def windgust_dir(self):
        import numpy as np
        if self.DXI:
            return self.DXI
 
        return np.NaN
 
    def wind_dir_cardinal(self):
        return fonction_direction(self.DD)
 
    def windgust_dir_cardinal(self):
        return fonction_direction(self.DXI)
     
    def rain(self):
        from decimal import Decimal
        return Decimal(str(round(self.RR,2)))
 
    def rain_rate(self):
        from decimal import Decimal
        return Decimal(str(round(self.RRI,2)))


class H(models.Model):
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
    DATJ = models.DateTimeField(null=False,default=timezone.now,verbose_name="AAAA-MM-JJ HH-MM de la mesure")
    DATRECU = models.DateTimeField(default=timezone.now,verbose_name="AAAA-MM-JJ HH-MM de la derniere modification")   
    RR1 = models.FloatField(null=True, default = None)
    DRR1 = models.IntegerField(null=True,verbose_name="Durée de la précipitation en min", default = None)
    STATUS_DRR1 = models.IntegerField(null=True,verbose_name="1 - Relevé manuel, 2 - Relevé automatique", default = None)
    RRI = models.FloatField(null=True, default = None)
    HRRI = models.DateTimeField(null=True, default = None)
    FF = models.FloatField(null=True,verbose_name = "Force du vent moyenné sur 10 dernieres min", default = None)
    DD = models.FloatField(null=True, default = None)
    FXY = models.FloatField(null=True,verbose_name="Valeur max de FF dans l'heure", default = None)
    DXY = models.FloatField(null=True,verbose_name="Direction de FXY", default = None)
    HXY = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de FXY", default = None)
    FXI = models.FloatField(null=True,verbose_name="Rafales max de FF dans l'heure", default = None)
    DXI = models.FloatField(null=True,verbose_name="Direction de FXI", default = None)
    HXI = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de FXI", default = None)
    T= models.FloatField(null=True, default = None)
    TD = models.FloatField(null=True, default = None)
    TN = models.FloatField(null=True, default = None)
    HTN = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de TN", default = None)
    TX = models.FloatField(null=True, default = None)
    HTX = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de TX", default = None)
    U= models.FloatField(null=True, default = None)
    UN= models.FloatField(null=True,verbose_name="Humidite minimale dans l'heure", default = None)
    HUN =  models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de UN", default = None)
    UX= models.FloatField(null=True,verbose_name="Humidite maximale dans l'heure", default = None)
    HUX =  models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de UX", default = None)
    PMER = models.FloatField(null=True, default = None)
    PMERMIN = models.FloatField(null=True, default = None)
    HPERMIN = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de PMERMIN", default = None)
    UV = models.IntegerField(null=True, default = None)
    RAD = models.FloatField(null=True, default = None)
    IC = models.FloatField(null=True, default = None)
    WINDCHILL = models.FloatField(null=True, default = None)
    ETP = models.FloatField(null=True, default = None)
    ETPX = models.FloatField(null=True, default = None)
    ETPN = models.FloatField(null=True, default = None)
    HF = models.FloatField(null=True, default = None)
    HFX = models.FloatField(null=True, default = None)
    HFN = models.FloatField(null=True, default = None)
    HS = models.FloatField(null=True, default = None)
    HSX = models.FloatField(null=True, default = None)
    HSN = models.FloatField(null=True, default = None)
    TS = models.FloatField(null=True, default = None)
    TSX = models.FloatField(null=True, default = None)
    TSN = models.FloatField(null=True, default = None)
    INST = models.FloatField(null=True, default = None)

    def __str__(self):
        return "%s / %s" % (self.POSTE, self.DATJ)
   
class Q(models.Model):   
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
    DATJ = models.DateField(null=False,default=timezone.now) 
    DATRECU = models.DateTimeField(default=timezone.now)
    RR = models.FloatField(null=True, default = None)
    DRR = models.FloatField(null=True,verbose_name="Durée de la précipitation en min", default = None)
    STATUS_DRR = models.IntegerField(null=True,verbose_name="1 - Relevé manuel, 2 - Relevé automatique", default = None)
    TN = models.FloatField(null=True, default = None)
    HTN = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de TN", default = None)
    TX = models.FloatField(null=True, default = None)
    HTX = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de TX", default = None)
    TM = models.FloatField(null=True, default = None)
    TAMPLI = models.FloatField(null=True)
    DG = models.IntegerField(null=True, verbose_name = 'Duree du gel en min', default = None)
    PMERM = models.FloatField(null=True, default = None)
    PMERMIN = models.FloatField(null=True, default = None)
    FXY = models.FloatField(null=True,verbose_name="Valeur max de FF dans la journee", default = None)
    DXY = models.FloatField(null=True,verbose_name="Direction de FXY", default = None)
    HXY = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de FXY", default = None)
    FXI = models.FloatField(null=True,verbose_name="Rafales max de FF dans la journee", default = None)
    DXI = models.FloatField(null=True,verbose_name="Direction de FXI", default = None)
    HXI = models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de FXI", default = None)
    UM= models.FloatField(null=True, default = None)
    UN= models.FloatField(null=True,verbose_name="Humidite minimale dans la journee", default = None)
    HUN =  models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de UN", default = None)
    UX= models.FloatField(null=True,verbose_name="Humidite maximale dans l'heure", default = None)
    HUX =  models.DateTimeField(null=True,verbose_name="AAAA MM JJ HH MM de UX", default = None)
    ETPM = models.FloatField(null=True, default = None)
    HFM = models.FloatField(null=True, default = None)
    HFMX = models.FloatField(null=True, default = None)
    HFMN = models.FloatField(null=True, default = None)
    HSM = models.FloatField(null=True, default = None)
    HSMX = models.FloatField(null=True, default = None)
    HSMN = models.FloatField(null=True, default = None)
    TS = models.FloatField(null=True, default = None)
    TSX = models.FloatField(null=True, default = None)
    TSN = models.FloatField(null=True, default = None)
    INST = models.IntegerField(null=True, verbose_name = "Duree d'insolation quotidienne (min)", default = None)
    
class DECADQ(models.Model):
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
    DATJ = models.DateField(null=False,default=timezone.now)
    DATRECU = models.DateTimeField(default=timezone.now)
    NUM_DECADE = models.IntegerField(null=True,verbose_name="Numero de la decade", default = None)
    RR = models.FloatField(null=True, default = None)
    STATUS_DRR = models.IntegerField(null=True,verbose_name="1 - Relevé manuel, 2 - Relevé automatique", default = None)
    RRAB = models.FloatField(null=True, verbose_name = "Precipitation maxi en 24h", default = None)
    STATUS_RRAB = models.IntegerField(null=True,verbose_name="1 - Relevé manuel, 2 - Relevé automatique", default = None)
    RRABDAT = models.DateTimeField(null=True, default = None)
    NBJRR1 = models.IntegerField(null=True, verbose_name = "Nb de jours RR sup à 1mm", default = None)
    NBJRR5 = models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 5mm", default = None) 
    NBJRR10 = models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 10mm", default = None) 
    NBJRR30 = models.IntegerField(null=True, verbose_name ="Nb de jours RR sup à 30mm", default = None) 
    NBJRR50 =  models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 50mm", default = None)
    NBJRR100 =  models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 100mm, default = None")
    PMERM = models.FloatField(null=True, default = None)
    PMERMINAB = models.FloatField(null=True, default = None)
    PMERMINABDAT = models.DateTimeField(null=True, default = None)
    TX = models.FloatField(null=True,verbose_name="Moyenne des TX de la decade", default = None)
    TXAB = models.FloatField(null=True,verbose_name="TX max de la decade", default = None)
    TXABDAT = models.DateTimeField(null=True,verbose_name="Date de la TX de la decade", default = None)
    TXMIN = models.FloatField(null=True,verbose_name="TX min de la decade", default = None)
    TXMINDAT = models.DateTimeField(null=True,verbose_name="Date de la TX min de la decade", default = None)
    NBJTX0 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est inf à 0", default = None)
    NBJTX25 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 25", default = None)
    NBJTX30 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 30", default = None)
    NBJTX35 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 35", default = None)
    NBJTXI20 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est inf à 20", default = None)
    NBJTXI27 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est inf à 27", default = None)
    NBJTX32 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 32", default = None)
    TN = models.FloatField(null=True,verbose_name="Moyenne des TN de la decade", default = None)
    TNAB = models.FloatField(null=True,verbose_name="TN min de la decade", default = None)
    TNDAT = models.DateTimeField(null=True,verbose_name="Date de la TN min de la decade", default = None)
    TNMAX = models.FloatField(null=True,verbose_name="TN max de la decade", default = None)
    TNMAXDAT = models.DateTimeField(null=True,verbose_name="Date de la TN max de la decade", default = None)
    NBJTN5  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à -5", default = None)
    NBJTNI10  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 10", default = None)
    NBJTNI15  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 15", default = None)
    NBJTNI20  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 20", default = None)
    NBJTNS20  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est sup à 20", default = None)
    NBJTNS25  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est sup à 25", default = None)
    NBJGELEE  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 0", default = None)
    UNAB = models.FloatField(null=True,verbose_name="Humidite relative minimale de la decade", default = None)
    UNABDAT = models.DateTimeField(null=True,verbose_name="Date de l'Humidite relative minimale de la decade", default = None)
    UXAB = models.FloatField(null=True,verbose_name="Humidite relative maximale de la decade", default = None)
    UXABDAT = models.DateTimeField(null=True,verbose_name="Date de l'humidite relative maximale de la decade", default = None)
    UMM = models.FloatField(null=True,verbose_name="Moyenne des humidites relatives de la decade", default = None)
    FXIAB = models.FloatField(null=True,verbose_name="Rafale maxi de la décade", default = None)
    DXIAB = models.FloatField(null=True,verbose_name="Direction de la rafale maxi de la décade", default = None)
    FXIDAT =  models.DateTimeField(null=True,verbose_name="Date la rafale maxi de la decade", default = None)
    NBJFF10  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FF est sup à 10m/s", default = None)
    NBJFF16  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FF est sup à 16m/s", default = None)
    NBJFF28  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FF est sup à 28m/s", default = None)
    FXYAB = models.FloatField(null=True,verbose_name="FXY max de la decade", default = None)
    DXYAB = models.FloatField(null=True,verbose_name="Direction du FXYAB de la decade", default = None)
    FXYABDAT = models.DateTimeField(null=True,verbose_name="Date du FXYAB de la decade", default = None)
    NBJFXY8  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXY est sup à 8m/s", default = None)
    NBJFXY10  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXY est sup à 10m/s", default = None)
    NBJFXY15  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXY est sup à 15m/s", default = None)
    INST = models.IntegerField(null=True, verbose_name = "Duree d'insolation quotidienne moyenne (min, default = None)", default = None)
    HFM = models.FloatField(null=True, default = None)
    HFX = models.FloatField(null=True, default = None)
    HFN = models.FloatField(null=True, default = None)
    HSM = models.FloatField(null=True, default = None)
    HSX = models.FloatField(null=True, default = None)
    HSN = models.FloatField(null=True, default = None)
    TSM = models.FloatField(null=True, default = None)
    TSX = models.FloatField(null=True, default = None)
    TSN = models.FloatField(null=True, default = None)
    
class MENSQ(models.Model):
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
    DATJ = models.DateField(null=False,default=timezone.now)
    DATRECU = models.DateTimeField(default=timezone.now)
    RR = models.FloatField(null=True,default=None)
    STATUS_DRR = models.IntegerField(null=True,verbose_name="1 - Relevé manuel, 2 - Relevé automatique",default=None)
    RRAB = models.FloatField(null=True, verbose_name = "Precipitation maxi en 24h",default=None)
    STATUS_RRAB = models.IntegerField(null=True,verbose_name="1 - Relevé manuel, 2 - Relevé automatique",default=None)
    RRABDAT = models.DateTimeField(null=True,default=None)
    NBJRR1 = models.IntegerField(null=True, verbose_name = "Nb de jours RR sup à 1mm",default=None)
    NBJRR5 = models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 5mm",default=None) 
    NBJRR10 = models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 10mm",default=None) 
    NBJRR30 = models.IntegerField(null=True, verbose_name ="Nb de jours RR sup à 30mm",default=None) 
    NBJRR50 =  models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 50mm",default=None)
    NBJRR100 =  models.IntegerField(null=True, verbose_name= "Nb de jours RR sup à 100mm",default=None)
    PMERM = models.FloatField(null=True,default=None)
    PMERMINAB = models.FloatField(null=True,default=None)
    PMERMINABDAT = models.DateTimeField(null=True,default=None)
    TX = models.FloatField(null=True,verbose_name="Moyenne des TX du mois",default=None)
    TXAB = models.FloatField(null=True,verbose_name="TX max du mois",default=None)
    TXABDAT = models.DateTimeField(null=True,verbose_name="Date de la TX max du mois",default=None)
    TXMIN = models.FloatField(null=True,verbose_name="TX min du mois",default=None)
    TXMINDAT = models.DateTimeField(null=True,verbose_name="Date de la TX min du mois",default=None)
    NBJTX0 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est inf à 0",default=None)
    NBJTX25 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 25",default=None)
    NBJTX30 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 30",default=None)
    NBJTX35 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 35",default=None)
    NBJTXI20 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est inf à 20",default=None)
    NBJTXI27 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est inf à 27",default=None)
    NBJTX32 = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TX est sup à 32",default=None)
    TN = models.FloatField(null=True,verbose_name="Moyenne des TN du mois",default=None)
    TNAB = models.FloatField(null=True,verbose_name="TN min du mois",default=None)
    TNDAT = models.DateTimeField(null=True,verbose_name="Date de la TN min du mois",default=None)
    TNMAX = models.FloatField(null=True,verbose_name="TN max du mois",default=None)
    TNMAXDAT = models.DateTimeField(null=True,verbose_name="Date de la TN max du mois",default=None)
    NBJTN5  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à -5",default=None)
    NBJTNI10  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 10",default=None)
    NBJTNI15  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 15",default=None)
    NBJTNI20  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 20",default=None)
    NBJTNS20  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est sup à 20",default=None)
    NBJTNS25  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est sup à 25",default=None)
    NBJGELEE  = models.IntegerField(null=True,verbose_name="Nombre de jours ou la TN est inf à 0",default=None)
    UNAB = models.FloatField(null=True,verbose_name="Humidite relative minimale du mois",default=None)
    UNABDAT = models.DateTimeField(null=True,verbose_name="Date de l'Humidite relative minimale du mois",default=None)
    UXAB = models.FloatField(null=True,verbose_name="Humidite relative maximale du mois",default=None)
    UXABDAT = models.DateTimeField(null=True,verbose_name="Date de l'humidite relative maximale du mois",default=None)
    UMM = models.FloatField(null=True,verbose_name="Moyenne des humidites relatives du mois",default=None)
    FXIAB = models.FloatField(null=True,verbose_name="Rafale maxi du mois",default=None)
    DXIAB = models.FloatField(null=True,verbose_name="Direction de la rafale maxi du mois",default=None)
    FXIDAT =  models.DateTimeField(null=True,verbose_name="Date la rafale maxi du mois",default=None)
    NBJFF10  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXI est sup à 10m/s",default=None)
    NBJFF16  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXI est sup à 16m/s",default=None)
    NBJFF28  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXI est sup à 28m/s",default=None)
    FXYAB = models.FloatField(null=True,verbose_name="FXY max du mois",default=None)
    DXYAB = models.FloatField(null=True,verbose_name="Direction du FXYAB du mois",default=None)
    FXYABDAT = models.DateTimeField(null=True,verbose_name="Date du FXYAB du moise",default=None)
    NBJFXY8  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXY est sup à 8m/s",default=None)
    NBJFXY10  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXY est sup à 10m/s",default=None)
    NBJFXY15  = models.IntegerField(null=True,verbose_name="Nombre de jours ou FXY est sup à 15m/s",default=None)
    INST = models.IntegerField(null=True, verbose_name = "Duree d'insolation quotidienne moyenne (min,default=None)",default=None)
    HFM = models.FloatField(null=True,default=None)
    HFX = models.FloatField(null=True,default=None)
    HFN = models.FloatField(null=True,default=None)
    HSM = models.FloatField(null=True,default=None)
    HSX = models.FloatField(null=True,default=None)
    HSN = models.FloatField(null=True,default=None)
    TSM = models.FloatField(null=True,default=None)
    TSX = models.FloatField(null=True,default=None)
    TSN = models.FloatField(null=True,default=None)
    
class RECMENS(models.Model):
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
    PARAM = models.CharField(null=True, max_length=25)
    DATRECU = models.DateTimeField(default=timezone.now)
    NUM_MOIS = models.IntegerField(null=True,verbose_name="13 = record mini annuel, 14 = record maxi annuel")
    DATDEB = models.DateTimeField(null=True)
    DATFIN = models.DateTimeField(null=True)
    RECORD = models.FloatField(null=True)
    DATERECORD = models.DateTimeField(null=True)
    
class HISTMAINT(models.Model):
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
    DATMAINT = models.DateTimeField(null=True)
    TYPE = models.CharField(null=True,max_length=100)
    CAPT= models.CharField(null=True,max_length=25)
    ACTEUR= models.CharField(null=True,max_length=25)
    COMM= models.CharField(null=True,max_length=100)
    
class HISTPOST(models.Model):
    POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)    
    COMMUNE =  models.ForeignKey('COMMUNE', on_delete=models.CASCADE)
    LIEU_DIT = models.CharField(null=True,max_length=30)
    DATDEB = models.DateTimeField(null=True)
    DATFIN = models.DateTimeField(null=True)
    LAT = models.FloatField(null=False)
    LON = models.FloatField(null=False)
    ALT = models.FloatField(null=False, verbose_name = "Altitude du poste en m")
    DATRECU = models.DateTimeField(null=False,default=timezone.now)
    PROP = models.CharField(null=False, verbose_name = "Nom du propriétaire/entreprise", max_length =20)
    ADRESSE = models.CharField(null=False, max_length = 100)
    MEL = models.CharField(null=True, max_length = 40) 
    TEL = models.CharField(null=True,max_length = 10)
    COMM = models.TextField(null=True)  
    
# class Files(models.Model):
# 
#     POSTE = models.ForeignKey('POSTE',on_delete=models.CASCADE)
# 
# 
#     lien = models.FileField(help_text="Contenant les données complètes (.csv)",storage=data_fs, null = True)
#     
    

    