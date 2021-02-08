from django.db import models
from django.utils import timezone
 

class OBSERVATION(models.Model):
    name = models.CharField(max_length=200)
    preferences = models.JSONField(verbose_name="JsonB")
 
    def __str__(self):
        return self.name


    class Meta:
        db_table = "observation"

class AGG_HOUR(models.Model):
    name = models.CharField(max_length=200)
    preferences = models.JSONField(verbose_name="JsonB")
 
    def __str__(self):
        return self.name


    class Meta:
        db_table = "agg_hour"


# from django.contrib.postgres.fields import JSONField
# Create your models here.

class POSTE(models.Model):
    GESTION_EXTREME = (
        ('0', 'Unconnu'),
        ('1', 'Auto dans observation'),
        ('2', 'Auto dans agrégation'),
        ('3', 'Manuel'),
    )
    NIVEAU_AGGREGATION = (
        ('', 'not set'),
        ('H', 'Heure'),
        ('D', 'Day'),
        ('M', 'Month'),
        ('Y', 'Year'),
        ('A', 'Global'),
    )
# timezone.now
#    id = models.AutoField(primary_key=True)
    meteor = models.CharField(max_length=10, verbose_name="Code MeteoR.OI")
    meteofr = models.CharField(max_length=10, verbose_name="Code Meteo France")
    title = models.CharField(max_length=50, verbose_name="Nom clair de la station")
    cas_gestion_extreme = models.CharField(default='0', max_length=1, choices=GESTION_EXTREME, verbose_name="Gestion des extrêmes")
    agg_min_extreme = models.CharField(max_length=1, default='', choices=NIVEAU_AGGREGATION, verbose_name="Niveau Agregation, Auto dans agregation")
    owner = models.CharField(max_length=50, verbose_name="Station Owner Name")
    email = models.CharField(max_length=50, verbose_name="E-Mail")
    phone = models.CharField(max_length=50, verbose_name="Phone")
    address = models.CharField(max_length=50, verbose_name="Address")
    zip = models.CharField(default="", max_length=10, verbose_name="Zip")
    city = models.CharField(max_length=50, default="", verbose_name="City")
    country = models.CharField(max_length=50, default="", verbose_name="Country")

    latitude = models.FloatField(default=0, verbose_name="Latitude")
    longitude = models.FloatField(default=0, verbose_name="Longitude")
    start = models.DateTimeField(default=timezone.now, verbose_name="Date d'entrée dans le réseau")
    end = models.DateTimeField( verbose_name="Date de sortie du réseau")
    comment = models.TextField(null=True, default=None)

    def __str__(self):
        return self.meteor

    class Meta:
        db_table = "poste"
