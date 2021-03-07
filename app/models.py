from django.db import models
from django.utils import timezone
import datetime


class Poste(models.Model):
    GESTION_EXTREME = (
        ('0', 'Inconnu'),
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

    meteor = models.CharField(max_length=10, verbose_name="Code MeteoR.OI")
    meteofr = models.CharField(null=True, max_length=10, verbose_name="Code Meteo France")
    fuseau = models.SmallIntegerField(default=0, verbose_name="nombre heure entre TU et heure fuseau")
    cas_gestion_extreme = models.CharField(default='0', max_length=1, choices=GESTION_EXTREME, verbose_name="Gestion des extrêmes")
    agg_min_extreme = models.CharField(null=True, max_length=1, default='', choices=NIVEAU_AGGREGATION, verbose_name="Niveau Agregation, Auto dans agregation")

    # la suite n'est pas utilise par climato
    title = models.CharField(null=True, max_length=50, default="", verbose_name="Nom clair de la station")
    owner = models.CharField(null=True, max_length=50, default="", verbose_name="Station Owner Name")
    email = models.CharField(null=True, max_length=50, default="", verbose_name="E-Mail")
    phone = models.CharField(null=True, max_length=50, default="", verbose_name="Phone")
    address = models.CharField(null=True, max_length=50, default="", verbose_name="Address")
    zip = models.CharField(null=True, default="", max_length=10, verbose_name="Zip")
    city = models.CharField(null=True, max_length=50, default="", verbose_name="City")
    country = models.CharField(null=True, max_length=50, default="", verbose_name="Country")
    latitude = models.FloatField(null=True, default=0, verbose_name="Latitude")
    longitude = models.FloatField(null=True, default=0, verbose_name="Longitude")
    start = models.DateTimeField(null=True, default=timezone.now, verbose_name="Date d'entrée dans le réseau")
    end = models.DateTimeField(null=True, verbose_name="Date de sortie du réseau")
    comment = models.TextField(null=True, default="")

    def __str__(self):
        return self.meteor + ", id: " + str(self.id)

    class Meta:
        db_table = "poste"


class TypeInstrument(models.Model):
    name = models.CharField(max_length=10, verbose_name="Type de Donnees")
    model_value = models.JSONField(verbose_name="JsonB")

    def __str__(self):
        return "type_instrument id: " + str(self.id) + ", name: " + self.name

    class Meta:
        db_table = "type_instrument"


class Exclusion(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    type_instrument = models.ForeignKey(to="TypeInstrument", on_delete=models.CASCADE)
    start_x = models.DateTimeField(default=timezone.now)
    end_x = models.DateTimeField(default=timezone.datetime(2100, 12, 21))
    value = models.JSONField(verbose_name="JsonB")

    def __str__(self):
        return "exclusion id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.type_instrument)

    class Meta:
        db_table = "exclusion"


class Observation(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    dat = models.DateTimeField()
    start_dat = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(verbose_name="duration", default=0)
    qa_modifications = models.IntegerField(default=0)
    qa_incidents = models.IntegerField(default=0)
    qa_check_done = models.BooleanField(default=False)
    j = models.JSONField(default=dict)

    def __str__(self):
        return "observation id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "obs"
        unique_together = (("poste_id", "dat"))


class Agg_hour(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    level = models.CharField(max_length=1, default='?')
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(verbose_name="duration", default=0)
    qa_modifications = models.IntegerField(default=0)
    qa_incidents = models.IntegerField(default=0)
    qa_check_done = models.BooleanField(default=False)
    j = models.JSONField(default=dict)

    def __str__(self):
        return "agg_hour id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_hour"


class Agg_day(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    level = models.CharField(max_length=1, default='?')
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(verbose_name="duration", default=0)
    qa_modifications = models.IntegerField(default=0)
    qa_incidents = models.IntegerField(default=0)
    qa_check_done = models.BooleanField(default=False)
    j = models.JSONField(default=dict)

    def __str__(self):
        return "agg_day id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_day"


class Agg_month(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    level = models.CharField(max_length=1, default='?')
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(verbose_name="duration", default=0)
    qa_modifications = models.IntegerField(default=0)
    qa_incidents = models.IntegerField(default=0)
    qa_check_done = models.BooleanField(default=False)
    j = models.JSONField(default=dict)

    def __str__(self):
        return "agg_month id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_month"


class Agg_year(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    level = models.CharField(max_length=1, default='?')
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(verbose_name="duration", default=0)
    qa_modifications = models.IntegerField(default=0)
    qa_incidents = models.IntegerField(default=0)
    qa_check_done = models.BooleanField(default=False)
    j = models.JSONField(default=dict)

    def __str__(self):
        return "agg_year id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_year"


class Agg_global(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.DateTimeField(default=datetime.datetime(1900, 1, 1))
    level = models.CharField(max_length=1, default='?')
    last_rec_dat = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(verbose_name="duration", default=0)
    qa_modifications = models.IntegerField(default=0)
    qa_incidents = models.IntegerField(default=0)
    qa_check_done = models.BooleanField(default=False)
    j = models.JSONField(default=dict)

    def __str__(self):
        return "agg_global id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.dat)

    class Meta:
        db_table = "agg_global"
