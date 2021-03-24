from django.db import models


class Poste(models.Model):
    GESTION_EXTREME = (
        (0, 'Inconnu'),
        (1, 'Auto dans observation'),
        (2, 'Auto dans agrégation'),
        (3, 'Manuel'),
    )
    NIVEAU_AGGREGATION = (
        ('',  'not set'),
        ('H', 'Heure'),
        ('D', 'Day'),
        ('M', 'Month'),
        ('Y', 'Year'),
        ('A', 'Global'),
    )
    # mandatory fields
    meteor = models.CharField(null=False, max_length=10, verbose_name="Code MeteoR.OI")
    fuseau = models.SmallIntegerField(null=False, verbose_name="nombre heure entre TU et heure fuseau, default UTC+4")

    # optional fields
    meteofr = models.CharField(null=True, default='', max_length=10, verbose_name="Code Meteo France")
    cas_gestion_extreme = models.SmallIntegerField(null=False, default=0, choices=GESTION_EXTREME, verbose_name="Gestion des extrêmes")
    agg_min_extreme = models.CharField(null=False, max_length=1, default='', choices=NIVEAU_AGGREGATION, verbose_name="Niveau Agregation, Auto dans agregation")
    lock_calculus = models.SmallIntegerField(null=True, default=0, verbose_name="internal field used to lock the calculus on one poste")

    # la suite n'est pas utilise par climato - a revoir pour pages html...
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
    start_dat = models.CharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="start date")
    stop_dat = models.CharField(null=False, max_length=20, default="2100-12-31T23:59:59", verbose_name="stop date")
    comment = models.TextField(null=True, default="")

    def __str__(self):
        return self.meteor + ", id: " + str(self.id)

    class Meta:
        db_table = "poste"


class TypeInstrument(models.Model):
    name = models.CharField(null=False, max_length=10, verbose_name="Type de Donnees")
    model_value = models.JSONField(default=dict, verbose_name="JsonB")

    def __str__(self):
        return "type_instrument id: " + str(self.id) + ", name: " + self.name

    class Meta:
        db_table = "type_instrument"


class Exclusion(models.Model):
    poste_id = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    type_instrument = models.ForeignKey(null=False, to="TypeInstrument", on_delete=models.CASCADE)
    start_dat = models.CharField(null=False, max_length=20, verbose_name="start date")

    start_dat = models.CharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="start date")
    stop_dat = models.CharField(null=False, max_length=20, default="2100-12-31T23:59:59", verbose_name="stop date")
    value = models.JSONField(null=False, default=dict, verbose_name="JsonB")

    def __str__(self):
        return "exclusion id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.type_instrument)

    class Meta:
        db_table = "exclusion"


class Observation(models.Model):
    poste_id = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    agg_start_dat = models.CharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="date agregation horaire utilisée")
    stop_dat = models.CharField(null=False, max_length=20, verbose_name="stop date, date de la mesure")
    duration = models.IntegerField(null=False, verbose_name="duration in minutes", default=0)

    qa_modifications = models.IntegerField(null=False, default=0, verbose_name='qa_modifications')
    qa_incidents = models.IntegerField(null=False, default=0, verbose_name='qa_incidents')
    qa_check_done = models.BooleanField(null=False, default=False, verbose_name='qa_check_done')
    j = models.JSONField(null=False, default=dict)
    j_agg = models.JSONField(null=False, default=dict)

    def __str__(self):
        return "observation id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.start_dat)

    class Meta:
        db_table = "obs"
        unique_together = (("poste_id", "stop_dat"))


class Agg_hour(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.CharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Somme des durations des donnees de cette agregation", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = models.JSONField(null=False, default=dict)

    def __str__(self):
        return "agg_hour id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.start_dat)

    class Meta:
        db_table = "agg_hour"
        unique_together = (("poste_id", "start_dat"))


class Agg_day(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.CharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Somme des durations des donnees de cette agregation", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = models.JSONField(null=False, default=dict)

    def __str__(self):
        return "agg_day id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.start_dat)

    class Meta:
        db_table = "agg_day"
        unique_together = (("poste_id", "start_dat"))


class Agg_month(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.CharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Somme des durations des donnees de cette agregation", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = models.JSONField(null=False, default=dict)

    def __str__(self):
        return "agg_month id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.start_dat)

    class Meta:
        db_table = "agg_month"
        unique_together = (("poste_id", "start_dat"))


class Agg_year(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.CharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Somme des durations des donnees de cette agregation", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = models.JSONField(null=False, default=dict)

    def __str__(self):
        return "agg_year id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.start_dat)

    class Meta:
        db_table = "agg_year"
        unique_together = (("poste_id", "start_dat"))


class Agg_global(models.Model):
    poste_id = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = models.CharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Somme des durations des donnees de cette agregation", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = models.JSONField(null=False, default=dict)

    def __str__(self):
        return "agg_global id: " + str(self.id) + ", poste: " + str(self.poste_id) + ", on " + str(self.start_dat)

    class Meta:
        db_table = "agg_global"
        unique_together = (("poste_id", "start_dat"))
