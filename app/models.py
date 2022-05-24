from django.db import models
from django.db.models import Index, Q


class DateTimeFieldNoTZ(models.Field):
    def db_type(self, connection):
        return 'timestamp'


# class Poste(ExportModelOperationsMixin('poste'), models.Model):
class Poste(models.Model):
    # mandatory fields
    id = models.SmallAutoField(primary_key=True)
    meteor = models.CharField(null=False, max_length=10, verbose_name="Code MeteoR.OI")

    # optional fields - will be used
    delta_timezone = models.SmallIntegerField(null=True, default=0, verbose_name="delta heure locale et TU+4")
    meteofr = models.CharField(null=True, default='', max_length=10, verbose_name="Code Meteo France")

    # la suite n'est pas utilise par climato - a revoir pour pages html...
    title = models.CharField(null=True, max_length=50, default="", verbose_name="Nom clair de la station")
    owner = models.CharField(null=True, max_length=50, default="", verbose_name="Propriétaire")
    email = models.CharField(null=True, max_length=50, default="", verbose_name="E-Mail")
    phone = models.CharField(null=True, max_length=50, default="", verbose_name="Téléphone")
    address = models.CharField(null=True, max_length=50, default="", verbose_name="Addresse")
    zip = models.CharField(null=True, default="", max_length=10, verbose_name="Code Postal")
    city = models.CharField(null=True, max_length=50, default="", verbose_name="Ville")
    country = models.CharField(null=True, max_length=50, default="", verbose_name="Payse")
    altitude = models.FloatField(null=True, default=0, verbose_name="Altitude")
    lat = models.FloatField(null=True, default=0, verbose_name="Latitude")
    long = models.FloatField(null=True, default=0, verbose_name="Longitude")
    start_dat = DateTimeFieldNoTZ(null=True, default="1900-01-01T00:00:00", verbose_name="Date d'activation")
    stop_dat = DateTimeFieldNoTZ(null=True, default="2100-12-31T23:59:59", verbose_name="Date de désactivation")
    comment = models.TextField(null=True, default="")

    def __str__(self):
        return self.meteor + ", id: " + str(self.id)

    class Meta:
        db_table = "postes"


# class TypeInstrument(ExportModelOperationsMixin('type_instrument'), models.Model):
class Mesure(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100, verbose_name="Nom de la mesure")
    json_input = models.CharField(null=False, max_length=20, verbose_name="Clé utilisée dans le json")
    archive_col = models.CharField(null=False, max_length=20, verbose_name="nom colonne table weewx.archive")
    val_deca = models.SmallIntegerField(null=True, default=0, verbose_name="Décalage mesure")
    max = models.BooleanField(null=True, default=True, verbose_name="Calcul des max")
    max_deca = models.SmallIntegerField(null=True, default=0, verbose_name="Décalage du max")
    min = models.BooleanField(null=True, default=True, verbose_name="Calcul des min")
    min_deca = models.SmallIntegerField(null=True, default=0, verbose_name="Décalage du min")
    is_avg = models.BooleanField(null=True, default=True, verbose_name="Calcul de moyenne")
    is_wind = models.BooleanField(null=True, default=False, verbose_name="Calcul du wind_dir")
    omm_link = models.SmallIntegerField(null=True, default=0, verbose_name="Lien entre mesure OMM et mesure de base")
    allow_zero = models.BooleanField(null=True, default=True, verbose_name="Zero est une valeur valide")

    def __str__(self):
        return "Mesure id: " + str(self.id) + ", name: " + self.name

    class Meta:
        db_table = "mesures"


# class Exclusion(ExportModelOperationsMixin('exclusion'), models.Model):
class Exclusion(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    start_dat = DateTimeFieldNoTZ(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="Date début exclusion")
    stop_dat = DateTimeFieldNoTZ(null=False, max_length=20, default="2100-12-31T23:59:59", verbose_name="Date fin exclusion")
    value = models.JSONField(null=False, default=dict, verbose_name="Exclusion")

    def __str__(self):
        return "exclusion id: " + str(self.id) + ", poste: " + str(self.poste) + ", start: " + str(self.start_dat) + ", stop: " + str(self.stop_dat)

    class Meta:
        db_table = "exclusions"


# class Observation(ExportModelOperationsMixin('obs'), models.Model):
class Observation(models.Model):

    # ??  hail | hailRate | heatingTemp ??

    id = models.BigAutoField(primary_key=True, verbose_name="id de l'observation")
    time = DateTimeFieldNoTZ(null=False, verbose_name="date fin période observation")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    duration = models.SmallIntegerField(null=True, default=0, verbose_name="durée période")
    # null data
    barometer = models.FloatField(null=True, verbose_name="pression niveau mer")
    barometer_omm = models.FloatField(null=True, verbose_name="pression niveau mer OMM")
    dewpoint = models.FloatField(null=True, verbose_name="point de rosée")
    et = models.FloatField(null=True, verbose_name="somme etp")
    extra_humid1 = models.FloatField(null=True, verbose_name="extra humidité 1")
    extra_humid2 = models.FloatField(null=True, verbose_name="extra humidité 2")
    extra_temp1 = models.FloatField(null=True, verbose_name="extra temperature 1")
    extra_temp2 = models.FloatField(null=True, verbose_name="extra temperature 2")
    extra_temp3 = models.FloatField(null=True, verbose_name="extra temperature 3")
    hail = models.FloatField(null=True, verbose_name="hail")
    hail_rate = models.FloatField(null=True, verbose_name="hail rate")
    heatindex = models.FloatField(null=True, verbose_name="heatindex")
    heating_temp = models.FloatField(null=True, verbose_name="heating temp")
    out_humidity = models.FloatField(null=True, verbose_name="humidité")
    out_humidity_omm = models.FloatField(null=True, verbose_name="humidité OMM")
    in_humidity = models.FloatField(null=True, verbose_name="humidité intérieure")
    in_temp = models.FloatField(null=True, verbose_name="température intérieure")
    leaf_temp1 = models.FloatField(null=True, verbose_name="temp des feuilles no 1")
    leaf_temp2 = models.FloatField(null=True, verbose_name="temp des feuilles no 2")
    leaf_wet1 = models.FloatField(null=True, verbose_name="humidité des feuilles no 1")
    leaf_wet2 = models.FloatField(null=True, verbose_name="humidité des feuilles no 2")
    out_temp = models.FloatField(null=True, verbose_name="température extérieure")
    out_temp_omm = models.FloatField(null=True, verbose_name="température OMM extérieure")
    pressure = models.FloatField(null=True, verbose_name="pression station")
    radiation = models.FloatField(null=True, verbose_name="radiation")
    rain = models.FloatField(null=True, verbose_name="pluie")
    rain_omm = models.FloatField(null=True, verbose_name="pluie OMM")
    rain_rate = models.FloatField(null=True, verbose_name="rain_rate")
    rx = models.FloatField(null=True, verbose_name="taux reception station")
    soil_moist1 = models.FloatField(null=True, verbose_name="humidité du sol niveau du sol")
    soil_moist2 = models.FloatField(null=True, verbose_name="humidité du sol niveau 1")
    soil_moist3 = models.FloatField(null=True, verbose_name="humidité du sol niveau 2")
    soil_moist4 = models.FloatField(null=True, verbose_name="humidité du sol niveau 3")
    soil_temp1 = models.FloatField(null=True, verbose_name="température du sol niveau du sol")
    soil_temp2 = models.FloatField(null=True, verbose_name="température du sol niveau 1")
    soil_temp3 = models.FloatField(null=True, verbose_name="température du sol niveau 2")
    soil_temp4 = models.FloatField(null=True, verbose_name="température du sol niveau 3")
    uv = models.FloatField(null=True, verbose_name="indice UV")
    voltage = models.FloatField(null=True, verbose_name="voltage")
    wind = models.FloatField(null=True, verbose_name="vitesse moyenne du vent sur la période")
    wind_dir = models.FloatField(null=True, verbose_name="direction moyenne du vent sur la période")
    wind_gust = models.FloatField(null=True, verbose_name="rafale max")
    wind_gust_dir = models.FloatField(null=True, verbose_name="direction de la rafale max")
    wind10 = models.FloatField(null=True, verbose_name="vent moyen sur 10")
    wind10_dir = models.FloatField(null=True, verbose_name="direction moyenne du vent sur 10 mn")
    wind10_omm = models.FloatField(null=True, verbose_name="vent moyen 10 mn OMM")
    windchill = models.FloatField(null=True, verbose_name="windchill")
    j = models.JSONField(null=True, default=dict, verbose_name="données autres")

    # quality fields
    qa_modifications = models.IntegerField(null=True, default=0, verbose_name='qa_modifications')
    qa_incidents = models.IntegerField(null=True, default=0, verbose_name='qa_incidents')
    qa_check_done = models.BooleanField(null=True, default=False, verbose_name='qa_check_done')

    def __str__(self):
        return "Observation id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.time) + ", durée: " + str(self.duration)

    class Meta:
        db_table = "obs"


class Extreme(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(null=False, verbose_name="date de l'extrême")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    id_obs = models.BigIntegerField(null=False, verbose_name="id de l'obs associée")
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.CASCADE)
    min = models.FloatField(null=True, verbose_name="valeur minimum")
    min_time = DateTimeFieldNoTZ(null=True, verbose_name="date du minimum")
    max = models.FloatField(null=True, verbose_name="valeur maximum")
    max_time = DateTimeFieldNoTZ(null=True, verbose_name="date du maximum")
    max_dir = models.SmallIntegerField(null=True, verbose_name="direction du maximum")

    def __str__(self):
        return "Extreme id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.time) + ", mesure: " + str(self.mesure)

    class Meta:
        db_table = "extremes"
        indexes = [
            Index(name='extremes_id_obs', fields=['id_obs', ], condition=Q(id_obs__gt=0)),
        ]


class Incident(models.Model):
    id = models.AutoField(primary_key=True)
    dat = DateTimeFieldNoTZ(null=False, max_length=30, verbose_name="date'")
    source = models.CharField(null=False, max_length=100, verbose_name='source')
    level = models.CharField(null=False, max_length=20, verbose_name='niveau')
    # error, critical, exception

    reason = models.TextField(null=False, verbose_name='raison')
    details = models.JSONField(null=False, default=dict, verbose_name="details")
    # stack for exception
    active = models.BooleanField(null=True, default=True, verbose_name='active')

    def __str__(self):
        return "Incident id: " + str(self.id) + ", date: " + str(self.dat) + ", Source: " + str(self.source) + ", Reason: " + str(self.reason)

    class Meta:
        db_table = "incidents"


class Annotation(models.Model):
    id = models.AutoField(primary_key=True)
    time = DateTimeFieldNoTZ(null=False, max_length=30, verbose_name="date'")
    timeend = DateTimeFieldNoTZ(null=False, max_length=30, verbose_name="date'")
    text = models.CharField(null=False, max_length=100, verbose_name='source')
    tags = models.CharField(null=False, max_length=100, verbose_name='source')

    def __str__(self):
        return "Annotation id: " + str(self.id) + ", time: " + str(self.time) + ", timeend: " + str(self.timeend) + ", text: " + self.text + ", tags: " + self.tags

    class Meta:
        db_table = "annotations"

    #  ----------------------------------------
    #  data to add to the first migration file
    #  ----------------------------------------
    # migrations.RunSQL("CREATE EXTENSION timescaledb;"),
    # migrations.RunSQL(
    #     "ALTER TABLE obs DROP CONSTRAINT obs_pkey;"
    # ),
    # migrations.RunSQL("SELECT create_hypertable('obs', 'time');"),
    # migrations.RunSQL(
    #     "SELECT set_chunk_time_interval('obs', 6048000000000);"
    # ),
    # migrations.RunSQL(
    #     "ALTER TABLE extremes DROP CONSTRAINT extremes_pkey;"
    # ),
    # migrations.RunSQL("SELECT create_hypertable('extremes', 'time');"),
    # migrations.RunSQL(
    #     "SELECT set_chunk_time_interval('extremes', 25920000000000);"
    # ),
