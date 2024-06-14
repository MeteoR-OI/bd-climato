from django.db import models
from django.db.models import Index

class DateTimeFieldNoTZ(models.Field):
    def db_type(self, connection):
        return 'timestamp'

class Code_QA(models.IntegerChoices):
    UNSET = 0
    VALIDATED = 1
    UNVALIDATED = 9

class Data_Source(models.IntegerChoices):
    NONE = 0
    METEOR_OI = 1
    METEO_FR = 2
    OVPF = 3

class Load_Type(models.IntegerChoices):
    NONE = 0
    LOAD_FROM_DUMP = 1
    LOAD_FROM_JSON = 2
    LOAD_FROM_DUMP_THEN_JSON = 3
    LOAD_CSV_FOR_METEOFR = 4
    LOAD_CSV_FOR_OVPF = 8

class Aggreg_Type(models.IntegerChoices):
    NONE = 0
    AVG = 1
    SUM = 2
    MAX = 3
    MIN = 4

class Poste(models.Model):
    # mandatory fields
    id = models.SmallAutoField(primary_key=True)
    meteor = models.CharField(null=False, max_length=50, verbose_name="Code station")
    delta_timezone = models.SmallIntegerField(null=False, verbose_name="delta heure locale et UTC")
    data_source = models.IntegerField(null=True, choices=Data_Source.choices, db_default=Data_Source.NONE.value, verbose_name="Source des donnees")
    load_type = models.IntegerField(null=True, choices=Load_Type.choices, db_default=Load_Type.NONE, verbose_name="Type de chargement des donnees")
    api_key = models.CharField(null=True, max_length=50, verbose_name="Api Key")

    # optional fields
    type = models.CharField(null=True, max_length=50, db_default="", verbose_name="Type de station")
    altitude = models.FloatField(null=True, db_default=0, verbose_name="Altitude")
    lat = models.FloatField(null=True, db_default=0, verbose_name="Latitude")
    long = models.FloatField(null=True, db_default=0, verbose_name="Longitude")
    info = models.JSONField(null=True, verbose_name="autre info station")
    stop_date = DateTimeFieldNoTZ(null=True, verbose_name="Datetime local d'arret de la station")

    # la suite n'est pas utilise par climato - a revoir pour pages html...
    other_code = models.CharField(null=True, max_length=50, db_default="", verbose_name="Autre code utilisé dans la data source")
    owner = models.CharField(null=True, max_length=50, db_default="", verbose_name="Propriétaire")
    email = models.CharField(null=True, max_length=50, db_default="", verbose_name="E-Mail")
    phone = models.CharField(null=True, max_length=50, db_default="", verbose_name="Téléphone")
    quartier = models.CharField(null=True, max_length=50, db_default="", verbose_name="Addresse")
    city = models.CharField(null=True, max_length=50, db_default="", verbose_name="Ville")
    country = models.CharField(null=True, max_length=50, db_default="", verbose_name="Pays")
    comment = models.TextField(null=True, db_default="", verbose_name="Commentaire")

    # information de synchronisation
    last_obs_date_local = DateTimeFieldNoTZ(null=True, db_default="2000-01-01T00:00:00", verbose_name="Datetime local de derniere reception de donnees")
    last_obs_id = models.BigIntegerField(null=True, db_default=0, verbose_name="ID obs de la derniere reception de donnees")
    last_json_date_local = DateTimeFieldNoTZ(null=True, db_default="2100-01-01T00:00:00", verbose_name="Datetime UTC du premier JSON archivé")
    info_sync = models.JSONField(null=True, verbose_name="Autre info de synchro")


    def __str__(self):
        return self.meteor + ", id: " + str(self.id) + ', load_type: ' + str(self.load_type) + ', TZ: ' + str(self.delta_timezone)

    class Meta:
        db_table = "postes"


class Mesure(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100, verbose_name="Nom de la mesure")
    json_input = models.CharField(null=True, max_length=20, verbose_name="Clé utilisée dans le json")
    json_input_bis = models.CharField(null=True, max_length=20, verbose_name="Autre clé utilisée dans le json")
    archive_col = models.CharField(null=True, max_length=20, verbose_name="nom colonne table weewx.archive")
    archive_table = models.CharField(null=True, db_default=None, max_length=20, verbose_name="nom table weewx.archive")
    field_dir = models.SmallIntegerField(null=True, verbose_name="id de la mesure wind dans table weewx.archive")
    max = models.BooleanField(null=True, db_default=True, verbose_name="Calcul des max")
    min = models.BooleanField(null=True, db_default=True, verbose_name="Calcul des min")
    agreg_type = models.IntegerField(null=True, choices=Aggreg_Type.choices, db_default=Aggreg_Type.NONE, verbose_name="Type d'agregation des donnees")
    is_wind = models.BooleanField(null=True, db_default=False, verbose_name="Calcul du wind_dir")
    allow_zero = models.BooleanField(null=True, db_default=True, verbose_name="Zero est une valeur valide")
    convert = models.JSONField(null=True, verbose_name="Conversion")
    j = models.JSONField(null=True, verbose_name="json data")

    def __str__(self):
        return "Mesure id: " + str(self.id) + ", name: " + self.name + ", agreg_type: " + str(self.agreg_type)

    class Meta:
        db_table = "mesures"


class Observation(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="id de l'observation")
    date_local = DateTimeFieldNoTZ(null=False, verbose_name="datetime locale fin période observation")
    date_utc = DateTimeFieldNoTZ(null=False, verbose_name="datetime UTC fin période observation")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    duration = models.SmallIntegerField(null=False, verbose_name="durée mesure")

    barometer = models.FloatField(null=True, verbose_name="pression niveau mer")
    pressure = models.FloatField(null=True, verbose_name="pression station")
    in_temp = models.FloatField(null=True, verbose_name="température intérieure")
    out_temp = models.FloatField(null=True, verbose_name="température extérieure")
    dewpoint = models.FloatField(null=True, verbose_name="point de rosée")
    etp = models.FloatField(null=True, verbose_name="somme etp")
    heatindex = models.FloatField(null=True, verbose_name="heatindex")
    # heating_temp = models.FloatField(null=True, verbose_name="heating temp")
    extra_temp1 = models.FloatField(null=True, verbose_name="extra temperature 1")
    extra_temp2 = models.FloatField(null=True, verbose_name="extra temperature 2")
    extra_temp3 = models.FloatField(null=True, verbose_name="extra temperature 3")
    in_humidity = models.FloatField(null=True, verbose_name="humidité intérieure")
    out_humidity = models.FloatField(null=True, verbose_name="humidité")
    extra_humid1 = models.FloatField(null=True, verbose_name="extra humidité 1")
    extra_humid2 = models.FloatField(null=True, verbose_name="extra humidité 2")
    leaf_temp1 = models.FloatField(null=True, verbose_name="temp des feuilles no 1")
    leaf_temp2 = models.FloatField(null=True, verbose_name="temp des feuilles no 2")
    leaf_wet1 = models.FloatField(null=True, verbose_name="humidité des feuilles no 1")
    leaf_wet2 = models.FloatField(null=True, verbose_name="humidité des feuilles no 2")
    radiation = models.FloatField(null=True, verbose_name="radiation")
    radiation_rate = models.FloatField(null=True, verbose_name="radiation rate")
    uv = models.FloatField(null=True, verbose_name="indice UV")
    rain = models.FloatField(null=True, verbose_name="pluie")
    rain_utc = models.FloatField(null=True, verbose_name="pluie")
    rain_rate = models.FloatField(null=True, verbose_name="rain_rate")
    rx = models.FloatField(null=True, verbose_name="taux reception station")
    soil_moist1 = models.FloatField(null=True, verbose_name="humidité du sol niveau du sol")
    soil_moist2 = models.FloatField(null=True, verbose_name="humidité du sol niveau 2")
    soil_moist3 = models.FloatField(null=True, verbose_name="humidité du sol niveau 3")
    soil_moist4 = models.FloatField(null=True, verbose_name="humidité du sol niveau 4")
    soil_temp1 = models.FloatField(null=True, verbose_name="température du sol niveau du sol")
    soil_temp2 = models.FloatField(null=True, verbose_name="température du sol niveau 2")
    soil_temp3 = models.FloatField(null=True, verbose_name="température du sol niveau 3")
    soil_temp4 = models.FloatField(null=True, verbose_name="température du sol niveau 4")
    voltage = models.FloatField(null=True, verbose_name="voltage")
    wind_dir = models.FloatField(null=True, verbose_name="direction moyenne du vent sur la période")
    wind = models.FloatField(null=True, verbose_name="vitesse moyenne du vent sur la période")
    wind_gust_dir = models.FloatField(null=True, verbose_name="direction de la rafale max")
    wind_gust = models.FloatField(null=True, verbose_name="rafale max")
    wind10 = models.FloatField(null=True, verbose_name="vent moyen sur 10")
    wind10_dir = models.FloatField(null=True, verbose_name="direction moyenne du vent sur 10 mn")
    windchill = models.FloatField(null=True, verbose_name="windchill")

    hail = models.FloatField(null=True, verbose_name="grele (mm)")
    # hail_rate = models.FloatField(null=True, verbose_name="hail rate")
    zone_1 = models.FloatField(null=True, verbose_name="zone 1")
    zone_2 = models.FloatField(null=True, verbose_name="zone 2")
    zone_3 = models.FloatField(null=True, verbose_name="zone 3")
    zone_4 = models.FloatField(null=True, verbose_name="zone 4")
    zone_5 = models.FloatField(null=True, verbose_name="zone 5")
    zone_6 = models.FloatField(null=True, verbose_name="zone 6")
    zone_7 = models.FloatField(null=True, verbose_name="zone 7")
    zone_8 = models.FloatField(null=True, verbose_name="zone 8")
    zone_9 = models.FloatField(null=True, verbose_name="zone 9")
    zone_10 = models.FloatField(null=True, verbose_name="zone 10")

    j = models.JSONField(null=True, verbose_name="données autres")

    # quality fields
    qa_all = models.IntegerField(null=True, db_default=Code_QA.UNSET.value, verbose_name='qa_modifications')
    qa_details = models.JSONField(null=True, verbose_name="details de qualite par champs")
    qa_modifications = models.IntegerField(null=True, db_default=0, verbose_name='nombre de modifications')

    def __str__(self):
        return "Observation id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", date_local " + str(self.date_local) + ", mesure: " + str(self.mesure.name) + ", value: " + str(self.value) + " qa_value:" + str(self.qa_value)

    class Meta:
        db_table = "obs"
        unique_together = (['id', 'date_local'],)


class XMin(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="id du minimum")
    obs_id = models.BigIntegerField(null=True, verbose_name="id de l'observation")
    date_local = DateTimeFieldNoTZ(null=False, verbose_name="date locale de la fin de la periode d'observation")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.PROTECT)
    min = models.FloatField(null=False, verbose_name="valeur minimum")
    min_time = DateTimeFieldNoTZ(null=False, verbose_name="date locale de l'extrême")
    qa_min = models.SmallIntegerField(null=True, choices=Code_QA.choices, db_default=0, verbose_name="Code Qualité")

    def __str__(self):
        return "Extreme Min id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.date_local) + ", mesure: " + str(self.mesure.name)

    class Meta:
        db_table = "x_min"
        indexes = [
            Index(name='x_min_obs_id', fields=['obs_id', 'date_local'])
        ]


class XMax(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="id du maximum")
    obs_id = models.BigIntegerField(null=True, verbose_name="id de l'observation")
    date_local = DateTimeFieldNoTZ(null=False, verbose_name="date locale de la fin de la periode d'observation")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.PROTECT)
    max = models.FloatField(null=False, verbose_name="valeur maximum")
    max_time = DateTimeFieldNoTZ(null=False, verbose_name="date locale de l'extrême")
    max_dir = models.FloatField(null=True, verbose_name="direction du maximum")
    qa_max = models.SmallIntegerField(null=True, choices=Code_QA.choices, db_default=Code_QA.UNSET.value, verbose_name="Code Qualité")

    def __str__(self):
        return "Extreme Max id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.date_local) + ", mesure: " + str(self.mesure.name)

    class Meta:
        db_table = "x_max"
        indexes = [
            Index(name='x_max_obs_id', fields=['obs_id', 'date_local'])
        ]


class Incident(models.Model):
    id = models.AutoField(primary_key=True)
    date_utc = DateTimeFieldNoTZ(null=False, max_length=30, verbose_name="date")
    source = models.CharField(null=False, max_length=100, verbose_name='source')
    level = models.CharField(null=False, max_length=20, verbose_name='niveau')
    # error, critical, exception

    reason = models.TextField(null=False, verbose_name='raison')
    details = models.JSONField(null=True, verbose_name="details")
    # stack for exception
    active = models.BooleanField(null=True, db_default=True, verbose_name='active')

    def __str__(self):
        return "Incident id: " + str(self.id) + ", date: " + str(self.date_utc) + ", Source: " + str(self.source) + ", Reason: " + str(self.reason)

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

    # -------------------------------------------------------------
    # First migration to execute to initialize timescaleDB features
    # -------------------------------------------------------------

    # Generated by Django 3.2.9 on 2022-05-01 20:32

# from django.db import migrations


# class Migration(migrations.Migration):

#     dependencies = [
#         ('app', '0001_initial'),
#     ]

#     operations = [
#         migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS timescaledb;"),
#         migrations.RunSQL("ALTER TABLE obs DROP CONSTRAINT obs_pkey;"),
#         migrations.RunSQL("SELECT create_hypertable('obs', 'date_local');"),
#         migrations.RunSQL("SELECT set_chunk_time_interval('obs', 6048000000000);"),
#         migrations.RunSQL("DROP index if exists obs_poste_id_7ed1db30;"),
#         migrations.RunSQL("DROP index if exists obs_mesure_id_2198080c;"),


#         migrations.RunSQL("ALTER TABLE x_min DROP CONSTRAINT x_min_pkey;"),
#         migrations.RunSQL("SELECT create_hypertable('x_min', 'date_local');"),
#         migrations.RunSQL("SELECT set_chunk_time_interval('x_min', 25920000000000);"),
#         migrations.RunSQL("DROP index if exists x_min_mesure_id_915a2d2e;"),
#         migrations.RunSQL("DROP index if exists x_min_poste_id_a7ee3864;"),

#         migrations.RunSQL("ALTER TABLE x_max DROP CONSTRAINT x_max_pkey;"),
#         migrations.RunSQL("SELECT create_hypertable('x_max', 'date_local');"),
#         migrations.RunSQL("SELECT set_chunk_time_interval('x_max', 25920000000000);"),
#         migrations.RunSQL("DROP index if exists x_max_mesure_id_a633699c;"),
#         migrations.RunSQL("DROP index if exists x_max_poste_id_529ea905;")

#     ]
