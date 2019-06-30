

from datetime import datetime, timedelta
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
from windrose import WindroseAxes


from django import forms
from django.db.models import Sum, Min, Max, Avg

from .models import PAYS, COMMUNE, INSTRUMENT, POSTE, INSTAN, H
from .form_templates import BootStrapForm
from .tools import format_date, ParamatersList


class FormPosteInit(BootStrapForm):
    PAYS_CHOICES = (
    ('France', 'France'),
    ('Reunion', 'Réunion'),
    )
    
    TYPEPERS_CHOICES = (
    (1, 'Personne physique'),
    (2, 'Personne morale'),
    )
    
    AUTORIS_CHOICES = (
    ('0', 'Aucune diffusion/Aucun stockage'),
    ('1', 'Diffusion autorisée/Aucun stockage'),
    ('2', 'Diffusion autorisée/Stockage autorisée'),
    )
    
    MAINT_CHOICES = (
    ('0', 'Aucune maintenance'),
    ('1', 'Maintenance non urgente (pas d\'altération de la mesure ou > 1 mois )'),
    ('2', 'Maintenance urgente (pas d\'altération de la mesure ou < 1 mois)'),
    )
    
    TYPESTATION_CHOICES = (
    ('VP2', 'Vantage Pro 2'),
    ('VP2P', 'Vantage Pro 2 +'),
    ('Pro', 'Station professionnelle'),
    ('SPIEA', 'SPIEA'),
    ('Autre', 'Autre'),
    )
    
    TYPEINFO_CHOICES = (
    ('Meteo', 'Météorologique'),
    ('Agrometeo', 'Agrométéorologique'),
    ('Aeronautique', 'Aéronautique'),
    ('Route', 'Route'),
    ('Plage', 'Plage'),
    )
    
#     def clean_COMMS(self):
# 
#         message = self.cleaned_data['COMMS']
# 
#         if "pizza" in message:
# 
#             raise forms.ValidationError("On ne veut pas entendre parler de pizza !")
# 
# 
#         return message
    
    #CODE_PAYS = forms.IntegerField(label='Code du pays*',help_text='Ex : 1(France-Reunion)',widget=forms.Select(choices=PAYS_CHOICES))
    NOM_DU_PAYS = forms.ModelChoiceField(label='Nom du pays*',initial=2, queryset = PAYS.objects.all())
    NOM_DE_LA_COMMUNE = forms.ModelChoiceField(label='Nom de la commune*', queryset = COMMUNE.objects.all().order_by('NOMCOMMUNE'))
#    CODE_POSTAL = forms.IntegerField(label='Code postal*')
    CODE_POSTE = forms.CharField(label='Nom du poste*',max_length =50,help_text = 'Ex : GDC030 ')
    REFERENCE_METEO_FRANCE = forms.CharField(label='Référence Météo France',max_length =10,required=False)
    NOM_PUBLIQUE = forms.CharField(label="Nom d'affichage public*",max_length = 50, help_text ='Nom qui sera affiché au grand public')
    PDT = forms.IntegerField(label="Intervalle d'envoie des données (min)*")
    LATITUDE = forms.FloatField(label="Latitude*",help_text='En degrés')
    LONGITUDE = forms.FloatField(label="Longitude*", help_text='En degrés')
    ALTITUDE = forms.FloatField(label="Altitude*", help_text='En mètres')
    PERSONNE = forms.IntegerField(label="Type de personne*",widget=forms.Select(choices=TYPEPERS_CHOICES))
    AUTORISATION = forms.IntegerField(label="Autorisation de stockage/diffusion*",widget=forms.Select(choices=AUTORIS_CHOICES))
    PROPRIETAIRE = forms.CharField(max_length=20,label="Nom du propriétaire*",help_text="Ex : MF-MeteoROI-Alexandre")
    DATE_ET_HEURE_OUVERTURE = forms.DateTimeField(label="Date et heure de mise en fonctionnement*",help_text="Format: AAAA-MM-JJ HH:MM")                                       
    #DATEFERM = forms.DateTimeField()
    MAINTENANCE = forms.IntegerField(label="Nécessité de maintenance",required=False,widget=forms.Select(choices=MAINT_CHOICES))
    TYPE = forms.CharField(label="Type de station*", max_length=20,widget=forms.Select(choices=TYPESTATION_CHOICES)) 
    TYPE_D_INFORMATIONS = forms.CharField(label="Type d'informations*", max_length=20,widget=forms.Select(choices=TYPEINFO_CHOICES))
    ADRESSE = forms.CharField(label = "Adresse d'installation*", max_length=100)
    LIEU_DIT = forms.CharField(max_length=30,required=False)
    MEL = forms.CharField(max_length = 40,required=False) 
    TEL = forms.CharField(max_length = 10,required=False)
    COMMS = forms.CharField(widget=forms.Textarea,required=False)  

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
#         self.fields['NOM_DE_LA_COMMUNE'].queryset = COMMUNE.objects.all()


class FormInstrumentsInit(forms.ModelForm):
    class Meta:

        model = INSTRUMENT
        exclude = ['POSTE','SEUILMIN','SEUILMAX','PRECISION','PASDETEMPS','UNITE','CAPTEUR','DATFIN']
        #fields = '__all__'

class InitPosteTotal(forms.ModelForm):
    class Meta:

        model = INSTRUMENT
        exclude = ['POSTE','DATFIN','CAPTEUR']


parametres_choices = ParamatersList.get_choices(with_rdv=True)
parametres_choices2 = ParamatersList.get_choices(with_rdv=False, with_none=True)
 
class tracerInstantanees(BootStrapForm):
    date_debut = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M"],
                                     help_text="Exemple 24/12/2018 22:55",
                                     required=True,
                                     label="Début de la période")
    date_fin = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M"],
                                   help_text="Exemple 26/12/2018 22:55",
                                   required=True,
                                   label="Fin de la période")
    parametre1 = forms.ChoiceField(choices=parametres_choices,
                                   required=True,
                                   label="Paramètre à afficher",
                                   initial="T")
    parametre2 = forms.ChoiceField(choices=parametres_choices2,
                                   label="Autre paramètre à afficher (optionnel)",
                                   initial="",
                                   required=False)
    station = forms.ModelChoiceField(queryset=POSTE.objects.all(), widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(tracerInstantanees, self).__init__(*args, **kwargs)
        self.fields['date_debut'].initial = (datetime.now()-timedelta(hours=24)).strftime("%d/%m/%Y %H:%M")
        self.fields['date_fin'].initial = datetime.now().strftime("%d/%m/%Y %H:%M")

    def __graph_file_name(self):
        prefix = self.cleaned_data.get('station').CODE_POSTE
        part_params = self.cleaned_data.get('parametre1')
        if self.cleaned_data.get('parametre2'):
            part_params = "%s_%s" % (part_params, self.cleaned_data.get('parametre2'))
            
        file_name = '%(code_station)s_%(params)s_%(date_start)s_%(date_end)s' % {
                'code_station'  : prefix,
                'params'        : part_params,
                'date_start'    : self.cleaned_data.get('date_debut').isoformat().replace(':',''),
                'date_end'      : self.cleaned_data.get('date_fin').isoformat().replace(':','')
            }
        
        return file_name

    def draw_graph(self):
        parametre1 = self.cleaned_data.get('parametre1')

        if parametre1 == 'RDV':
            return self.__draw_RDV()

        return self.__draw_params() 

    def is_RDV(self):
        if not self.is_valid():
            return False

        parametre1 = self.cleaned_data.get('parametre1')
        parametre2 = self.cleaned_data.get('parametre2')

        return parametre1 == 'RDV' or parametre2 == 'RDV'

    def __draw_params(self):
        is_rain = False
        rain_top_list = []

        parametre1 = self.cleaned_data.get('parametre1')
        parametre2 = self.cleaned_data.get('parametre2')

        datedebut   = self.cleaned_data.get('date_debut')
        datefin     = self.cleaned_data.get('date_fin')

        poste = self.cleaned_data.get('station')

        nom = self.__graph_file_name()

        double_trace = False
        if parametre2 and parametre1 != parametre2:
            double_trace = True

        # Sélection des données instantanées
        parametre1_values = INSTAN.objects.filter(POSTE = poste,
                                                  DATJ__lt = datefin,
                                                  DATJ__gte = datedebut) \
                                          .values_list('DATJ', parametre1) \
                                          .order_by('DATJ')
        if double_trace:
            parametre2_values = INSTAN.objects.filter(POSTE = poste,
                                                      DATJ__lt = datefin,
                                                      DATJ__gte = datedebut) \
                                              .values_list('DATJ', parametre2) \
                                              .order_by('DATJ')

        # On plot les données demandées
        fig, ax = plt.subplots()
        x=[]
        y=[]
        y2 = []
        delta_date = datefin-datedebut
        
        for value in parametre1_values:
            if value[1] != None:
                x += [value[0]]
                y += [value[1]]
            else : 
                x += [value[0]]
                y += [np.nan]
                
        if double_trace:
            for value in parametre2_values:
                if value[1] != None:
                    y2 += [value[1]]
                else : 
                    y2 += [np.nan]

        Maxx = parametre1_values.aggregate(Max(parametre1))[parametre1+'__max']
        Maxx = Decimal(str(round(float(Maxx),2)))
        Minx = parametre1_values.aggregate(Min(parametre1))[parametre1+'__min']
        Minx = Decimal(str(round(float(Minx),2)))
        Avgx = parametre1_values.aggregate(Avg(parametre1))[parametre1+'__avg']
        Avgx = Decimal(str(round(float(Avgx),2)))

        # Le cumul n'est pas nécessaire pour les valeurs de T,TD,PMER
        Sumx = False
        if parametre1 in ['RR','RAD']:
            if parametre1 == 'RR': 
                Cumulmax = H.objects.filter(POSTE=poste,DATJ__lt=datefin,
                                            DATJ__gte=datedebut) \
                                    .order_by('-RR1')
                if Cumulmax.count() >= 3:
                    for i in range(0,3):

                        Cumul1 = Decimal(str(round(float(Cumulmax[i].RR1),2)))
                        datecumulmax = (Cumulmax[i].DATJ-
                                        datetime.timedelta(hours=1)).strftime('%d/%m %Hh%M')
                        rain_top_list+=['- '+str(Cumul1)+'mm '+str(datecumulmax)] 
                Sumx = parametre1_values.values_list('DATJ',parametre1) \
                    .aggregate(Sum(parametre1))[parametre1+'__sum']
                Sumx = Decimal(str(round(float(Sumx),2)))
            elif parametre1 == 'RAD': 
                Sumx = parametre1_values.values_list('DATJ',parametre1) \
                    .aggregate(Sum(parametre1))[parametre1+'__sum']
                Sumx = Decimal(str(round(float(Sumx),2)))
            is_rain = True

        has_comment = False
        comments = []
        
        #Traitement des données vent
        if parametre1 in ('FF', 'FXI', 'PMER'): 
            
            has_comment = True
      
            if parametre1 == 'FF':
                comments += ['Top 5 des vents moyens sur la période : ']
                FiltreTop = INSTAN.objects.filter(POSTE=poste,DATJ__lt=datefin,
                                    DATJ__gte=datedebut).order_by('-FF')
                for i in range(0,5):
                    #Il n'y aura pas forcément 5 valeurs
                    try:
                        comments += [str(FiltreTop[i].FF) +'km/h le ' \
                        + str(FiltreTop[i].DATJ.strftime('%d/%m %Hh%M'))]
                    except: 
                        pass
            elif parametre1 == 'FXI':
                #Durée où la rafale est supérieure à une valeur
                Filtre50 = INSTAN.objects.filter(POSTE=poste,DATJ__lt=datefin,
                                    DATJ__gte=datedebut,FXI__gte=50).count()
                Filtre70 = INSTAN.objects.filter(POSTE=poste,DATJ__lt=datefin,
                                    DATJ__gte=datedebut,FXI__gte=70).count()
                Filtre90 = INSTAN.objects.filter(POSTE=poste,DATJ__lt=datefin,
                                    DATJ__gte=datedebut,FXI__gte=90).count()
                Filtre120 = INSTAN.objects.filter(POSTE=poste,DATJ__lt=datefin,
                                    DATJ__gte=datedebut,FXI__gte=120).count()
                Filtre50, Filtre70, Filtre90, Filtre120 = Filtre50*5, Filtre70*5, Filtre90*5,Filtre120*5
                comments += ['Durée rafales: >50 '+
                                str(Filtre50) +'min, >70 '
                                +str(Filtre70)+'min, >90 '
                                +str(Filtre90)+'min, >120 '
                                +str(Filtre120)+'min']
        
                comments += ['Top 5 des rafales sur la période : ']
                FiltreTop = INSTAN.objects.filter(POSTE=poste,
                                    DATJ__lt=datefin,
                                    DATJ__gte=datedebut).order_by('-FXI')
                for i in range(0,5):
                    try:
                        comments += [str(FiltreTop[i].FXI) +'km/h le ' \
                        + str(FiltreTop[i].DATJ.strftime('%d/%m %Hh%M'))]
                    except:
                        pass
            elif parametre1 == 'PMER':
                FiltrePMER = INSTAN.objects.filter(POSTE=poste,DATJ__lt=datefin,
                                    DATJ__gte=datedebut).order_by('DATJ')
                gradmoyen=[]

                for i in range(0,FiltrePMER.count()-1): 
                    gradmoyen+=[(FiltrePMER[i+1].PMER-FiltrePMER[i].PMER)/5] 

                moygrad = Decimal(str(round(np.mean(gradmoyen),2)))
                posgrad = Decimal(str(round(max(gradmoyen),2)))
                neggrad = Decimal(str(round(min(gradmoyen),2)))
                comments+=['(5min) Gradient maximal : ('+
                              str(posgrad)+'hPa/min) / ('+
                              str(neggrad)+'hPa/min)']
                comments+=['Gradient moyen sur la période: '+
                              str(moygrad)+'hPa/min']

        label_x = ParamatersList.get_parameter_label(parametre1)

        plt.plot(x,y,label=str(label_x))
        ax.set_xticklabels([])

        # Changement de légende axe x selon la période choisie
        format_date(delta_date.days,ax)

        for text in ax.get_xminorticklabels():
            text.set_rotation(50)

        # Récupération de l'unité du paramètre choisi
        unite = ParamatersList.get_unit_label(parametre1)

        plt.ylabel(label_x + ' - ' + unite)

        if parametre2:
            unite2 = ParamatersList.get_unit_label(parametre2)
            label_x2 = ParamatersList.get_parameter_label(parametre2)
            if (parametre1 == 'T' and parametre2 == 'TD') or \
                (parametre1 == 'RR' and parametre2 == 'RRI') or \
                (parametre1 == 'TD' and parametre2 == 'T')or \
                (parametre1 == 'RRI' and parametre2 == 'RR')or \
                (parametre1 == 'FF' and parametre2 == 'FXI')or \
                (parametre1 == 'FXI' and parametre2 == 'FF'):
                plt.plot(x,y2,'r',label=str(label_x2),alpha=0.5)
            else:
                ax2 = ax.twinx()
                ax2.plot(x,y2,'r',label=str(label_x2),alpha=0.5)
                ax2.set_xticklabels([])
                plt.ylabel(label_x2 + ' - ' + unite2)

        plt.grid()
        fig.legend()

        data_dir = 'media/data/'

        if not os.path.exists(data_dir+'nonpermanent/'+poste.CODE_POSTE+'/'+parametre1+'/'):
            os.makedirs(data_dir+'nonpermanent/'+poste.CODE_POSTE+'/'+parametre1+'/')
        link = 'nonpermanent/'+poste.CODE_POSTE+'/'+parametre1+'/'+nom+'.png'
        plt.savefig(data_dir+link, 
                    bbox_inches="tight")  #choisir un nom unique
        plt.close(fig)
        
        return {
            'is_rain'       : is_rain,
            'rain_top_list' : rain_top_list,
            'graph_link'    : link,
            'parameter_max' : Maxx,
            'parameter_min' : Minx,
            'parameter_avg' : Avgx,
            'parameter_sum' : Sumx,
            'parameter_unit': unite,
            'has_comment'   : has_comment,
            'comments'      : comments
        }

    def __draw_RDV(self):
        parametre1 = self.cleaned_data.get('parametre1')

        datedebut   = self.cleaned_data.get('date_debut')
        datefin     = self.cleaned_data.get('date_fin')

        poste = self.cleaned_data.get('station')

        nom = self.__graph_file_name()

        RDV= True
        DDlist = []
        flist=[]
        values = INSTAN.objects.filter(POSTE = poste,
                                       DATJ__lt = datefin,
                                       DATJ__gte = datedebut)

        for value in values:
            if value.DD != None:
                DDlist+=[value.DD] 
                flist += [value.FF]

        ax = WindroseAxes.from_ax() 
        ax.bar(DDlist, flist, bins=np.arange(0, max(flist), 5),
               normed=True, opening=0.8, edgecolor='white')

        data_dir = 'media/data/'

        ax.set_legend()
        if not os.path.exists(data_dir+'nonpermanent/'+poste.CODE_POSTE+'/'+parametre1+'/'):
            os.makedirs(data_dir+'nonpermanent/'+poste.CODE_POSTE+'/'+parametre1+'/')
        # link : chemin d'accès de l'image la page station    
        link1 = 'nonpermanent/'+poste.CODE_POSTE+'/RDV/'+nom+'.png'
        plt.savefig(data_dir+link1,
                    bbox_inches="tight") # choisir un nom unique
        plt.close()

        # Fréquences de direction
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

        if not os.path.exists(data_dir+'nonpermanent/'+poste.CODE_POSTE+'/'+parametre1+'/'):
            os.makedirs(data_dir+'nonpermanent/'+poste.CODE_POSTE+'/'+parametre1+'/')
        # link : chemin d'accès de l'image la page station    
        link2 = 'nonpermanent/'+poste.CODE_POSTE+'/RDV/'+nom+'_hist.png'
        plt.savefig(data_dir+link2,
                    bbox_inches="tight")

        plt.close()

        return {
            'graph_link'    : link1,
        }

# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = Files
#         fields = '__all__'

