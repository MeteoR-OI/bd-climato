from django import forms
from .models import PAYS,COMMUNE,INSTRUMENT,POSTE
from .tools import BootStrapForm

    


class InitFormPays(BootStrapForm):
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


class InitPoste(forms.ModelForm):
    class Meta:

        model = INSTRUMENT
        exclude = ['POSTE','SEUILMIN','SEUILMAX','PRECISION','PASDETEMPS','UNITE','CAPTEUR','DATFIN']
        #fields = '__all__'
class InitPosteTotal(forms.ModelForm):
    class Meta:

        model = INSTRUMENT
        exclude = ['POSTE','DATFIN','CAPTEUR']
        
# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = Files
#         fields = '__all__'
        
