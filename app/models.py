from django.db import models
from django.db.models import Index
# , UniqueConstraint, Q


class DateTimeFieldNoTZ(models.Field):
    def db_type(self, connection):
        return 'timestamp'


# class Poste(ExportModelOperationsMixin('poste'), models.Model):
class Poste(models.Model):
    # mandatory fields
    id = models.SmallAutoField(primary_key=True)
    meteor = models.CharField(null=False, max_length=50, verbose_name="Code station")
    delta_timezone = models.SmallIntegerField(null=False, verbose_name="delta heure locale et UTC")
    data_source = models.SmallIntegerField(null=False, verbose_name="Data Source: 0 meteoire, 1 meteofr,..")
    type = models.CharField(null=True, max_length=50, default="", verbose_name="Type de station")

    # optional fields
    altitude = models.FloatField(null=True, default=0, verbose_name="Altitude")
    lat = models.FloatField(null=True, default=0, verbose_name="Latitude")
    long = models.FloatField(null=True, default=0, verbose_name="Longitude")
    info = models.JSONField(null=True, default=dict, verbose_name="autre info station")
    load_dump = models.BooleanField(null=True, default=False, verbose_name="Charge les donnees a partir des dumps")
    load_raw_data = models.BooleanField(null=True, default=False, verbose_name="Charge les donnees a partir des donnees brutes")
    pause_raw_data = models.BooleanField(null=True, default=False, verbose_name="Ne traite pas les fichiers Jsde donnees brutes")
    stop_date = DateTimeFieldNoTZ(null=True, verbose_name="Datetime local de stop de la station")

    # la suite n'est pas utilise par climato - a revoir pour pages html...
    other_code = models.CharField(null=True, max_length=50, default="", verbose_name="Nom clair de la station")
    owner = models.CharField(null=True, max_length=50, default="", verbose_name="Propriétaire")
    email = models.CharField(null=True, max_length=50, default="", verbose_name="E-Mail")
    phone = models.CharField(null=True, max_length=50, default="", verbose_name="Téléphone")
    quartier = models.CharField(null=True, max_length=50, default="", verbose_name="Addresse")
    city = models.CharField(null=True, max_length=50, default="", verbose_name="Ville")
    country = models.CharField(null=True, max_length=50, default="", verbose_name="Payse")
    comment = models.TextField(null=True, default="")

    # reception donnees
    last_obs_date = DateTimeFieldNoTZ(null=True, default="2000-01-01T00:00:00", verbose_name="Datetime locale de derniere reception de donnees")
    last_obs_id = models.BigIntegerField(null=True, default=0, verbose_name="ID obs de la derniere reception de donnees")
    last_extremes_date = DateTimeFieldNoTZ(null=True, default="2000-01-01T00:00:00", verbose_name="Datetime locale de dernier record")
    last_extremes_id = models.BigIntegerField(null=True, default=0, verbose_name="ID du dernier record")

    def __str__(self):
        return self.meteor + ", id: " + str(self.id) + ', data_source: ' + str(self.data_source) + ', TZ: ' + str(self.delta_timezone)

    class Meta:
        db_table = "postes"


# class TypeInstrument(ExportModelOperationsMixin('type_instrument'), models.Model):
class Mesure(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100, verbose_name="Nom de la mesure")
    json_input = models.CharField(null=True, max_length=20, verbose_name="Clé utilisée dans le json")
    json_input_bis = models.CharField(null=True, max_length=20, verbose_name="Autre clé utilisée dans le json")
    archive_col = models.CharField(null=True, max_length=20, verbose_name="nom colonne table weewx.archive")
    archive_table = models.CharField(null=True, default=None, max_length=20, verbose_name="nom table weewx.archive")
    field_dir = models.SmallIntegerField(null=True, verbose_name="id de la mesure wind dans table weewx.archive")
    csv_field = models.CharField(null=True, default=None, max_length=20, verbose_name="nom colonne csv")
    csv_minmax = models.JSONField(null=True, default=dict, verbose_name="Nom champs min, minTime, max, maxTime maxDir")
    val_deca = models.SmallIntegerField(null=True, default=0, verbose_name="Décalage mesure")
    max = models.BooleanField(null=True, default=True, verbose_name="Calcul des max")
    max_deca = models.SmallIntegerField(null=True, default=0, verbose_name="Décalage du max")
    min = models.BooleanField(null=True, default=True, verbose_name="Calcul des min")
    min_deca = models.SmallIntegerField(null=True, default=0, verbose_name="Décalage du min")
    is_avg = models.BooleanField(null=True, default=True, verbose_name="Calcul de moyenne")
    is_wind = models.BooleanField(null=True, default=False, verbose_name="Calcul du wind_dir")
    omm_link = models.SmallIntegerField(null=True, default=0, verbose_name="Lien entre mesure OMM et mesure de base")
    allow_zero = models.BooleanField(null=True, default=True, verbose_name="Zero est une valeur valide")
    is_hourly = models.BooleanField(null=True, default=False, verbose_name="Must be agregated by hour(s) or more, not less")

    def __str__(self):
        return "Mesure id: " + str(self.id) + ", name: " + self.name

    class Meta:
        db_table = "mesures"


# class Observation(ExportModelOperationsMixin('obs'), models.Model):
class Observation(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="id de l'observation")
    date_local = DateTimeFieldNoTZ(null=False, verbose_name="datetime locale fin période observation")
    date_utc = DateTimeFieldNoTZ(null=False, verbose_name="datetime UTC fin période observation")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.PROTECT)
    duration = models.SmallIntegerField(null=False, verbose_name="durée mesure")
    value = models.FloatField(null=False, verbose_name="valeur")
    qa_value = models.SmallIntegerField(null=True, default=0, verbose_name="Qualite de la valeur")

    def __str__(self):
        return "Observation id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.time) + ", mesure: " + str(self.mesure.name)

    class Meta:
        db_table = "obs"
        unique_together = (['id', 'date_local'],)


class XMin(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="id du minimum")
    obs_id = models.BigIntegerField(null=True, verbose_name="id de l'observation")
    date_local = DateTimeFieldNoTZ(null=False, verbose_name="date locale de l'extrême")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.PROTECT)
    min = models.FloatField(null=False, verbose_name="valeur minimum")
    min_time = DateTimeFieldNoTZ(null=True, verbose_name="date du minimum")
    qa_min = models.SmallIntegerField(null=False, default=0, verbose_name="Qualite du min")

    def __str__(self):
        return "Extreme Min id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.date_local) + ", mesure: " + str(self.mesure)

    class Meta:
        db_table = "x_min"
        indexes = [
            Index(name='x_min_obs_id', fields=['obs_id', 'date_local'])
        ]


class XMax(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="id du maximum")
    obs_id = models.BigIntegerField(null=True, verbose_name="id de l'observation")
    date_local = DateTimeFieldNoTZ(null=False, verbose_name="date locale de l'extrême")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.PROTECT)
    max = models.FloatField(null=False, verbose_name="valeur maximum")
    max_time = DateTimeFieldNoTZ(null=False, verbose_name="date du maximum")
    max_dir = models.SmallIntegerField(null=True, verbose_name="direction du maximum")
    qa_max = models.SmallIntegerField(null=False, default=0, verbose_name="Qualite du max")

    def __str__(self):
        return "Extreme Max id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.date_local) + ", mesure: " + str(self.mesure)

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
    details = models.JSONField(null=False, default=dict, verbose_name="details")
    # stack for exception
    active = models.BooleanField(null=True, default=True, verbose_name='active')

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
