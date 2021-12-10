from django.db import models
import datetime
from app.tools.jsonPlus import JsonPlus
from app.tools.dateTools import str_to_date, date_to_str
from django.core.serializers.json import DjangoJSONEncoder
# import app.tools.myTools as t
# from django_prometheus.models import ExportModelOperationsMixin


class DateCharField(models.CharField):
    # __metaclass__ = models.CharField
    # description = "String Date in db, datetime in python"

    def __init__(self, *args, **kwargs):
        # self.max_length = 20
        super(DateCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        ret = value
        try:
            ret = date_to_str(value)
        except Exception:
            pass
        finally:
            # t.LogDebug("DateCharField..get_prep_value called for " + str(self.attname) + " with " + str(value) + " => " + str(ret))
            return ret

    def from_db_value(self, value, expression, connection):
        ret = value
        try:
            ret = str_to_date(value)
        except Exception:
            pass
        finally:
            # t.LogDebug("DateCharField..from_db_value called for " + str(self.attname) + " with " + str(value) + " => " + str(ret))
            return ret

    def to_python(self, value):
        ret = value
        try:
            ret = str_to_date(value)
        except Exception:
            pass
        finally:
            # t.LogDebug("DateCharField..to_python called for " + str(self.attname) + " with " + str(value) + " => " + str(ret))
            return ret


class DateJSONField(models.JSONField):
    # __metaclass__ = models.JSONField
    # description = "JSON field, with date enabled fields"

    def __init__(self, *args, **kwargs):
        self.max_length = 64000
        # self.default = dict
        super(DateJSONField, self).__init__(*args, **kwargs)

    # def get_prep_value(self, value):
    #     ret = value
    #     try:
    #         if value is None or value == {}:
    #             return {}
    #         if value == []:
    #             return []
    #         ret = JsonPlus().serialize(value)
    #     except Exception:
    #         pass
    #     finally:
    #         # t.LogDebug("DateJSONField..from_db_value called for " + str(self.attname) + " with " + str(value) + " => " + str(ret))
    #         return ret

    def from_db_value(self, value, expression, connection):
        ret = value
        try:
            if value is None or value == {}:
                return {}
            if value == []:
                return []
            ret = JsonPlus().deserialize(value)
        except Exception:
            pass
        finally:
            # t.LogDebug("DateJSONField..from_db_value called for " + str(self.attname) + " with " + str(value) + " => " + str(ret))
            return ret

    def to_python(self, value):
        ret = value
        try:
            if value is None or value == {}:
                return {}
            if value == []:
                return []
            ret = JsonPlus().deserialize(value)
        except Exception:
            pass
        finally:
            # t.LogDebug("DateJSONField..to_python called for " + str(self.attname) + " with " + str(value) + " => " + str(ret))
            return ret


# class Poste(ExportModelOperationsMixin('poste'), models.Model):
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
    id = models.AutoField(primary_key=True)
    meteor = models.CharField(null=False, max_length=10, verbose_name="Code MeteoR.OI")
    fuseau = models.SmallIntegerField(null=True, default=4, verbose_name="nombre heure entre TU et heure fuseau, default UTC+4")

    # optional fields
    meteofr = models.CharField(null=True, default='', max_length=10, verbose_name="Code Meteo France")
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
    start_dat = DateCharField(null=True, max_length=20, default="1900-01-01T00:00:00", verbose_name="start date")
    stop_dat = DateCharField(null=True, max_length=20, default="2100-12-31T23:59:59", verbose_name="stop date")
    comment = models.TextField(null=True, default="")

    def __str__(self):
        return self.meteor + ", id: " + str(self.id)

    class Meta:
        db_table = "poste"


# class TypeInstrument(ExportModelOperationsMixin('type_instrument'), models.Model):
class TypeInstrument(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=10, verbose_name="Type de Donnees")
    model_value = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name="JsonB")

    def __str__(self):
        return "type_instrument id: " + str(self.id) + ", name: " + self.name

    class Meta:
        db_table = "type_instrument"


# class Exclusion(ExportModelOperationsMixin('exclusion'), models.Model):
class Exclusion(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    type_instrument = models.ForeignKey(null=False, to="TypeInstrument", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    start_dat = DateCharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="start date")
    stop_dat = DateCharField(null=False, max_length=20, default="2100-12-31T23:59:59", verbose_name="stop date")
    value = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name="JsonB")

    def __str__(self):
        return "exclusion id: " + str(self.id) + ", poste: " + str(self.poste) + ", on " + str(self.type_instrument)

    class Meta:
        db_table = "exclusion"


# class Observation(ExportModelOperationsMixin('obs'), models.Model):
class Observation(models.Model):
    id = models.BigAutoField(primary_key=True)
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    agg_start_dat = DateCharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="date début période")
    stop_dat = DateCharField(null=False, max_length=20, verbose_name="date de fin de période")
    duration = models.IntegerField(null=False, verbose_name="durée période", default=0)

    qa_modifications = models.IntegerField(null=False, default=0, verbose_name='qa_modifications')
    qa_incidents = models.IntegerField(null=False, default=0, verbose_name='qa_incidents')
    qa_check_done = models.BooleanField(null=False, default=False, verbose_name='qa_check_done')
    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name='mesures Json')
    j_agg = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name='données pré-agrégées')

    def __str__(self):
        return "Observation id: " + str(self.id) + ", poste: " + str(self.poste) + ", de " + str(self.stop_dat - datetime.timedelta(minutes=self.duration)) + " a: " + str(self.stop_dat)

    class Meta:
        db_table = "obs"
        unique_together = (("poste", "stop_dat"))


class TmpObservation(models.Model):
    id = models.BigAutoField(primary_key=True)
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    agg_start_dat = DateCharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="date agregation horaire utilisée")
    stop_dat = DateCharField(null=False, max_length=20, verbose_name="stop date, date de la mesure")
    duration = models.IntegerField(null=False, verbose_name="duration in minutes", default=0)

    qa_modifications = models.IntegerField(null=False, default=0, verbose_name='qa_modifications')
    qa_incidents = models.IntegerField(null=False, default=0, verbose_name='qa_incidents')
    qa_check_done = models.BooleanField(null=False, default=False, verbose_name='qa_check_done')
    j = DateJSONField(encoder=DjangoJSONEncoder, null=False)
    j_agg = DateJSONField(encoder=DjangoJSONEncoder, null=False)

    def __str__(self):
        return "TmpObservation id: " + str(self.id) + ", poste: " + str(self.poste) + ", stop_dat: " + str(self.stop_dat)

    class Meta:
        db_table = "tmp_obs"
        unique_together = (("poste", "stop_dat"))


# class AggTodo(ExportModelOperationsMixin('agg_todo'), models.Model):
class AggTodo(models.Model):
    id = models.AutoField(primary_key=True)
    obs = models.ForeignKey(null=False, to="Observation", on_delete=models.CASCADE)
    priority = models.IntegerField(null=True, default=9, verbose_name='priority, 0: one current-data, 9: multiple current-data')
    status = models.IntegerField(null=False, default=0, verbose_name='status, 0: wait, 9: error, 99: processed')
    j_dv = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name='default_values coming from obs processing')
    j_error = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name='error reporting')

    def __str__(self):
        return "AggTodo id: " + str(self.id) + ", obs: " + str(self.obs) + ", priority: " + str(self.priority)

    class Meta:
        db_table = "agg_todo"


class TmpAggTodo(models.Model):
    id = models.AutoField(primary_key=True)
    obs = models.ForeignKey(null=False, to="TmpObservation", on_delete=models.CASCADE)
    priority = models.IntegerField(null=True, default=9, verbose_name='priority, 0: one current-data, 9: multiple current-data')
    status = models.IntegerField(null=False, default=0, verbose_name='status, 0: wait, 9: error, 99: processed')
    j_dv = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name='default_values coming from obs processing')
    j_error = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name='error reporting')

    def __str__(self):
        return "Tmp_agg_todo id: " + str(self.id) + ", obs: " + str(self.obs) + ", priority: " + str(self.priority)

    class Meta:
        db_table = "tmp_agg_todo"


# class ExtremeTodo(ExportModelOperationsMixin('extreme_todo'), models.Model):
class ExtremeTodo(models.Model):
    id = models.BigAutoField(primary_key=True)
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    level = models.CharField(null=False, max_length=2, verbose_name="Aggregation level")
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date de l agregation'")
    invalid_type = models.CharField(null=False, max_length=3, verbose_name="Type Invalidation (max or min)")
    status = models.IntegerField(null=False, default=0, verbose_name='status, 0: wait, 9: error, 99: processed')
    j_invalid = DateJSONField(encoder=DjangoJSONEncoder, null=False)

    def __str__(self):
        return "ExtremeTodo id: " + str(self.id) + ", level: " + self.level + ", start_dat: " + str(self.start_dat) + ", type: " + str.invalid_type

    class Meta:
        db_table = "extreme_todo"


class TmpExtremeTodo(models.Model):
    id = models.BigAutoField(primary_key=True)
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    level = models.CharField(null=False, max_length=2, verbose_name="Aggregation level")
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date de l agregation'")
    invalid_type = models.CharField(null=False, max_length=3, verbose_name="Type Invalidation (max or min)")
    status = models.IntegerField(null=False, default=0, verbose_name='status, 0: wait, 9: error, 99: processed')
    j_invalid = DateJSONField(encoder=DjangoJSONEncoder, null=False)

    def __str__(self):
        return "ExtremeTodo id: " + str(self.id) + ", level: " + self.level + ", start_dat: " + str(self.start_dat) + ", type: " + str.invalid_type

    class Meta:
        db_table = "tmp_extreme_todo"


# class AggHour(ExportModelOperationsMixin('agg_hour'), models.Model):
class AggHour(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggHour id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for an hour'

    class Meta:
        db_table = "agg_hour"
        unique_together = (("poste", "start_dat"))


class TmpAggHour(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "TmpAggHour id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for an hour'

    class Meta:
        db_table = "tmp_agg_hour"
        unique_together = (("poste", "start_dat"))


# class AggDay(ExportModelOperationsMixin('agg_day'), models.Model):
class AggDay(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggDay id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a day'

    class Meta:
        db_table = "agg_day"
        unique_together = (("poste", "start_dat"))


class TmpAggDay(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "TmpAggDay id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a day'

    class Meta:
        db_table = "tmp_agg_day"
        unique_together = (("poste", "start_dat"))


# class AggMonth(ExportModelOperationsMixin('agg_month'), models.Model):
class AggMonth(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggMonth id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a month'

    class Meta:
        db_table = "agg_month"
        unique_together = (("poste", "start_dat"))


class TmpAggMonth(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "TmpAggMonth id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a month'

    class Meta:
        db_table = "tmp_agg_month"
        unique_together = (("poste", "start_dat"))


# class AggYear(ExportModelOperationsMixin('agg_year'), models.Model):
class AggYear(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggYear id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a year'

    class Meta:
        db_table = "agg_year"
        unique_together = (("poste", "start_dat"))


class TmpAggYear(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "TmpAggYear id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a year'

    class Meta:
        db_table = "tmp_agg_year"
        unique_together = (("poste", "start_dat"))


# class AggAll(ExportModelOperationsMixin('agg_all'), models.Model):
class AggAll(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggAll id: " + str(self.id) + ", poste: " + str(self.poste) + " for ever"

    class Meta:
        db_table = "agg_all"
        unique_together = (("poste", "start_dat"))


class TmpAggAll(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)
    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "TmpAggAll id: " + str(self.id) + ", poste: " + str(self.poste) + " for ever"

    class Meta:
        db_table = "tmp_agg_all"
        unique_together = (("poste", "start_dat"))


class AggHisto(models.Model):
    id = models.AutoField(primary_key=True)
    obs_id = models.IntegerField(null=False, default=0, verbose_name="Obs_id")
    agg_id = models.IntegerField(null=False, default=0, verbose_name="Agg_id")
    agg_level = models.CharField(null=False, max_length=2, verbose_name="level")
    delta_duration = models.IntegerField(null=False, verbose_name="Delta durées")

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Delta agrégation")

    def __str__(self):
        return "AggHisto id: " + str(self.id) + ", obs: " + str(self.obs_id) + ", Aggreg: " + str(self.agg_id) + ", level: " + self.agg_level

    class Meta:
        db_table = "agg_histo"
        indexes = [
            models.Index(fields=('agg_level', 'agg_id')),
            models.Index(fields=('obs_id', 'agg_level', 'agg_id')),
        ]


class TmpAggHisto(models.Model):
    id = models.AutoField(primary_key=True)
    obs_id = models.IntegerField(null=False, default=0, verbose_name="Observation source")
    agg_id = models.IntegerField(null=False, default=0, verbose_name="Aggregation_id updated")
    agg_level = models.CharField(null=False, max_length=2, verbose_name="level")
    delta_duration = models.IntegerField(null=False, verbose_name="Delta des durées")

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Delta agrégation")

    def __str__(self):
        return "TmpAggHisto id: " + str(self.id) + ", obs: " + str(self.obs_id) + ", Aggreg: " + str(self.agg_id) + ", level: " + self.agg_level

    class Meta:
        db_table = "tmp_agg_histo"
        indexes = [
            models.Index(fields=('agg_level', 'agg_id')),
            models.Index(fields=('obs_id', 'agg_level', 'agg_id')),
        ]
