from django.db import models
from django.db.models import Index, UniqueConstraint, Q


class DateTimeFieldNoTZ(models.Field):
    def db_type(self, connection):
        return 'timestamp'


# class Poste(ExportModelOperationsMixin('poste'), models.Model):
class Poste(models.Model):
    # mandatory fields
    id = models.SmallAutoField(primary_key=True)
    meteor = models.CharField(null=False, max_length=10, verbose_name="Code station")
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
    json_input = models.CharField(null=False, max_length=20, verbose_name="Clé utilisée dans le json")
    json_input_bis = models.CharField(null=True, max_length=20, verbose_name="Autre clé utilisée dans le json")
    archive_col = models.CharField(null=False, max_length=20, verbose_name="nom colonne table weewx.archive")
    archive_table = models.CharField(null=True, default=None, max_length=20, verbose_name="nom table weewx.archive")
    field_dir = models.SmallIntegerField(null=True, verbose_name="id de la mesure wind dans table weewx.archive")
    csv_field = models.CharField(null=True, default=None, max_length=20, verbose_name="nom colonne csv")
    csv_minmax = models.JSONField(null=False, default=dict, verbose_name="Nom champs min, minTime, max, maxTime maxDir")
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
    id = models.BigAutoField(primary_key=True, verbose_name="id de l'observation")
    date_local = DateTimeFieldNoTZ(null=False, verbose_name="datetime locale fin période observation")
    date_utc = DateTimeFieldNoTZ(null=False, verbose_name="datetime UTC fin période observation")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.PROTECT)

    duration = models.SmallIntegerField(null=True, default=0, verbose_name="durée mesure")
    value = models.FloatField(null=False, verbose_name="pression niveau mer")
    qa_value = models.SmallIntegerField(null=True, default=0, verbose_name="pression niveau mer")

    def __str__(self):
        return "Observation id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.time) + ", mesure: " + str(self.mesure.name)

    class Meta:
        db_table = "obs"
        indexes = [
            Index(name='obs_pid', fields=['poste_id', '-date_local', 'mesure_id']),
        ]


class Extreme(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_local = models.DateField(null=False, verbose_name="date locale de l'extrême")
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.PROTECT)
    mesure = models.ForeignKey(null=False, to="Mesure", on_delete=models.PROTECT)
    min = models.FloatField(null=True, verbose_name="valeur minimum")
    min_time = DateTimeFieldNoTZ(null=True, verbose_name="date du minimum")
    max = models.FloatField(null=True, verbose_name="valeur maximum")
    max_time = DateTimeFieldNoTZ(null=True, verbose_name="date du maximum")
    max_dir = models.SmallIntegerField(null=True, verbose_name="direction du maximum")

    def __str__(self):
        return "Extreme id: " + str(self.id) + ", poste: " + str(self.poste.meteor) + ", time " + str(self.date_local) + ", mesure: " + str(self.mesure)

    class Meta:
        db_table = "extremes"
        indexes = [
            Index(name='extremes_pid', fields=['poste_id', '-date_local']),
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


class HistoObs(models.Model):
    id = models.BigAutoField(primary_key=True)
    src_obs_id = models.BigIntegerField(null=False, verbose_name="obs_id source")
    target_obs_id = models.BigIntegerField(null=False, verbose_name="obs_id modifiée")

    def __str__(self):
        return "HistoObs src_obs_id: " + str(self.src_obs_id) + ", target: " + str(self.target_obs_id)

    class Meta:
        db_table = "histo_obs"
        constraints = [
            UniqueConstraint(fields=['src_obs_id', 'target_obs_id'], name='unique_histo_obs_mapping'),
        ]
        indexes = [
            Index(name='histo_obs_target', fields=['src_obs_id', 'target_obs_id']),
            Index(name='histo_obs_src', fields=['target_obs_id', 'src_obs_id'])
        ]


class HistoExtremes(models.Model):
    id = models.BigAutoField(primary_key=True)
    target_x_id = models.BigIntegerField(null=False, verbose_name="extremes.id")
    src_min_obs_id = models.BigIntegerField(null=True, verbose_name="obs_id source")
    src_max_obs_id = models.BigIntegerField(null=True, verbose_name="obs_id source")
    target_x_id = models.BigIntegerField(null=False, verbose_name="extreme_id modifiée")

    def __str__(self):
        return "Extremes updated: " + str(self.target_x_id) + ", min obs.id: " + str(self.src_min_obs_id) + ", max obs.id: " + str(self.src_max_obs_id)

    class Meta:
        db_table = "histo_extreme"
        indexes = [
            Index(name='histo_x_src', fields=['target_x_id', 'id']),
            Index(name='histo_x_target_min', fields=['src_min_obs_id', 'target_x_id'], condition=Q(src_min_obs_id__isnull=False)),
            Index(name='histo_x_target_max', fields=['src_max_obs_id', 'target_x_id'], condition=Q(src_max_obs_id__isnull=False))

        ]


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

    # from django.db import migrations

    # class Migration(migrations.Migration):

    #     dependencies = [
    #         ('app', '0001_initial'),
    #     ]

    #     operations = [
    #         migrations.RunSQL("CREATE EXTENSION timescaledb;"),
    #         migrations.RunSQL(
    #             "ALTER TABLE obs DROP CONSTRAINT obs_pkey;"
    #         ),
    #         migrations.RunSQL("SELECT create_hypertable('obs', 'date_local');"),
    #         migrations.RunSQL(
    #             "SELECT set_chunk_time_interval('obs', 6048000000000);"
    #         ),
    #         migrations.RunSQL(
    #             "ALTER TABLE extremes DROP CONSTRAINT extremes_pkey;"
    #         ),
    #         migrations.RunSQL("SELECT create_hypertable('extremes', 'date_local');"),
    #         migrations.RunSQL(
    #             "SELECT set_chunk_time_interval('extremes', 25920000000000);"
    #         )
    #     ]
