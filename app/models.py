from app.tools.dateTools import str_to_date, date_to_str
from app.tools.jsonPlus import JsonPlus
# from django_prometheus.models import ExportModelOperationsMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import DateTimeField
# import app.tools.myTools as t
import datetime


class DateTimeWithoutTZField(DateTimeField):
    """ timestamp with no time zone """
    def db_type(self, connection):
        return 'timestamp'


class DateCharField(DateTimeWithoutTZField):

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
            return ret

    def from_db_value(self, value, expression, connection):
        ret = value
        try:
            ret = str_to_date(value)
        except Exception:
            pass
        finally:
            return ret

    def to_python(self, value):
        ret = value
        try:
            ret = str_to_date(value)
        except Exception:
            pass
        finally:
            return ret


class DateJSONField(models.JSONField):
    # __metaclass__ = models.JSONField
    # description = "JSON field, with date enabled fields"

    def __init__(self, *args, **kwargs):
        self.max_length = 64000
        # self.default = dict
        super(DateJSONField, self).__init__(*args, **kwargs)

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
            return ret


# class Poste(ExportModelOperationsMixin('poste'), models.Model):
class Poste(models.Model):
    # mandatory fields
    id = models.AutoField(primary_key=True)
    meteor = models.CharField(null=False, max_length=10, verbose_name="Code MeteoR.OI")
    lock_calculus = models.SmallIntegerField(null=True, default=0, verbose_name="internal field used to lock the calculus on one poste")

    # optional fields - will be used
    fuseau_delta = models.SmallIntegerField(null=True, default=0, verbose_name="delta entre TU station et default UTC+4")
    meteofr = models.CharField(null=True, default='', max_length=10, verbose_name="Code Meteo France")

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
    name = models.CharField(null=False, max_length=10, verbose_name="Type Instrument")
    model_value = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name="Model Json")

    def __str__(self):
        return "type_instrument id: " + str(self.id) + ", name: " + self.name

    class Meta:
        db_table = "type_instrument"


# class Exclusion(ExportModelOperationsMixin('exclusion'), models.Model):
class Exclusion(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)
    type_instrument = models.ForeignKey(null=False, to="TypeInstrument", on_delete=models.CASCADE)

    start_dat = DateCharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="start date")
    stop_dat = DateCharField(null=False, max_length=20, default="2100-12-31T23:59:59", verbose_name="stop date")
    value = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name="Exclusion")

    def __str__(self):
        return "exclusion id: " + str(self.id) + ", poste: " + str(self.poste) + ", on " + str(self.type_instrument)

    class Meta:
        db_table = "exclusion"


# class Observation(ExportModelOperationsMixin('obs'), models.Model):
class Observation(models.Model):
    id = models.BigAutoField(primary_key=True)

    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)

    agg_start_dat = DateCharField(null=False, max_length=20, default="1900-01-01T00:00:00", verbose_name="date début période")
    # just to allow a join with agg_hour... Could be removed in future..

    stop_dat = DateCharField(null=False, max_length=20, verbose_name="date de fin de période")

    duration = models.IntegerField(null=False, verbose_name="durée période", default=0)

    filename = models.CharField(default='???', max_length=100, null=False, verbose_name='filename used to load data')

    json_type = models.CharField(max_length=1, null=False, verbose_name='data type stored in j')
    # O => Observation data (data sent every 5 mn)
    # C => Measure regenerated, extremes computed from measures values + xtreme field
    # H => Hourly data agregated by weeWX. extremes computed from measures values + xtreme field
    # D,M,Y,A => data agregated by weeWX, extremes are weeWX saved extremes (no xtreme data)

    # quality fields
    qa_modifications = models.IntegerField(null=False, default=0, verbose_name='qa_modifications')
    qa_incidents = models.IntegerField(null=False, default=0, verbose_name='qa_incidents')
    qa_check_done = models.BooleanField(null=False, default=False, verbose_name='qa_check_done')

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name='mesures Json')
    # j is an array. content depend on number of element in j:
    # j.__len__() == 1 => j hold the measure values (normal situation)
    # j.__len__() == 2 => update to be processed (short transition):
    #       j[0] => current values in agregation to be removed. j[1] => new values to add in aggregations

    j_xtreme = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name='données pré-agrégées')
    # j_xtreme is an array. content depend on number of element in j_xtreme:
    # j_xtreme.__len__() == 1 => j_xtreme hold the measure values (normal situation)
    # j_xtreme.__len__() == 2 => update to be processed (short transition):
    #       j_xtreme[0] => current values in agregation to be removed. j_xtreme[1] => new values to add in aggregations

    def __str__(self):
        return "Observation id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat " + str(self.stop_dat - datetime.timedelta(minutes=self.duration)) + ", stop_dat: " + str(self.stop_dat)

    class Meta:
        db_table = "obs"
        unique_together = (("poste", "stop_dat"))


# class AggHour(ExportModelOperationsMixin('agg_hour'), models.Model):
class AggHour(models.Model):
    id = models.BigAutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)

    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")
    # start_dat is rounded to the beginning of the aggregation period

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    # Sum of data aggregated in this aggregation

    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    # length of the aggregation

    # quality indicators
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    # data
    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggHour id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for an hour'

    class Meta:
        db_table = "agg_hour"
        unique_together = (("poste", "start_dat"))


# class AggDay(ExportModelOperationsMixin('agg_day'), models.Model):
class AggDay(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)

    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")
    # start_dat is rounded to the beginning of the aggregation period

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    # Sum of data aggregated in this aggregation

    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    # length of the aggregation

    # quality indicators
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    # data
    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggDay id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a day'

    class Meta:
        db_table = "agg_day"
        unique_together = (("poste", "start_dat"))


# class AggMonth(ExportModelOperationsMixin('agg_month'), models.Model):
class AggMonth(models.Model):
    id = models.AutoField(primary_key=True)
    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)

    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")
    # start_dat is rounded to the beginning of the aggregation period

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    # Sum of data aggregated in this aggregation

    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    # length of the aggregation

    # quality indicators
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    # data
    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggMonth id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a month'

    class Meta:
        db_table = "agg_month"
        unique_together = (("poste", "start_dat"))


# class AggYear(ExportModelOperationsMixin('agg_year'), models.Model):
class AggYear(models.Model):
    id = models.AutoField(primary_key=True)

    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)

    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")
    # start_dat is rounded to the beginning of the aggregation period

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    # Sum of data aggregated in this aggregation

    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    # length of the aggregation

    # quality indicators
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    # data
    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggYear id: " + str(self.id) + ", poste: " + str(self.poste) + ", start_dat: " + str(self.start_dat) + ' for a year'

    class Meta:
        db_table = "agg_year"
        unique_together = (("poste", "start_dat"))


# class AggAll(ExportModelOperationsMixin('agg_all'), models.Model):
class AggAll(models.Model):
    id = models.AutoField(primary_key=True)

    poste = models.ForeignKey(to="Poste", on_delete=models.CASCADE)

    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date")
    # start_dat is rounded to the beginning of the aggregation period

    duration_sum = models.IntegerField(null=False, verbose_name="Durées agrégées", default=0)
    # Sum of data aggregated in this aggregation

    duration_max = models.IntegerField(null=False, verbose_name="Durée max", default=0)
    # length of the aggregation

    # quality indicators
    qa_modifications = models.IntegerField(null=False, default=0)
    qa_incidents = models.IntegerField(null=False, default=0)
    qa_check_done = models.BooleanField(null=False, default=False)

    # data
    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Agrégations")

    def __str__(self):
        return "AggAll id: " + str(self.id) + ", poste: " + str(self.poste) + " for ever"

    class Meta:
        db_table = "agg_all"
        unique_together = (("poste", "start_dat"))


# class AggTodo(ExportModelOperationsMixin('agg_todo'), models.Model):
class AggTodo(models.Model):
    id = models.IntegerField(primary_key=True)

    # obs = models.ForeignKey(null=False, to="Observation", on_delete=models.CASCADE)

    priority = models.IntegerField(null=True, default=9, verbose_name='priority, 0: one current-data, 9: multiple current-data')

    status = models.IntegerField(null=False, default=0, verbose_name='status, 0: wait, 9: error, 99: processed')

    json_type = models.CharField(null=False, max_length=1, verbose_name='json_type')
    # O,C,H,D,M,Y,A

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name='default_values coming from obs processing')
    # delta_values to push into aggregations

    j_error = DateJSONField(encoder=DjangoJSONEncoder, null=False, default=dict, verbose_name='error info, when status = 99')
    # error information when status = 999

    def __str__(self):
        return "AggTodo id: " + str(self.id) + ", obs: " + str(self.obs) + ", priority: " + str(self.priority)

    class Meta:
        db_table = "agg_todo"


# class ExtremeTodo(ExportModelOperationsMixin('extreme_todo'), models.Model):
class ExtremeTodo(models.Model):
    id = models.BigAutoField(primary_key=True)

    poste = models.ForeignKey(null=False, to="Poste", on_delete=models.CASCADE)

    level = models.CharField(null=False, max_length=2, verbose_name="Aggregation level")

    start_dat = DateCharField(null=False, max_length=20, verbose_name="start date de l agregation'")

    invalid_type = models.CharField(null=False, max_length=3, verbose_name="Type Invalidation (max or min)")

    status = models.IntegerField(null=False, default=0, verbose_name='status, 0: wait, 9: error, 99: processed')

    j_recompute = DateJSONField(encoder=DjangoJSONEncoder, null=False)

    def __str__(self):
        return "ExtremeTodo id: " + str(self.id) + ", level: " + self.level + ", start_dat: " + str(self.start_dat) + ", type: " + str.invalid_type

    class Meta:
        db_table = "extreme_todo"


class AggHisto(models.Model):
    id = models.AutoField(primary_key=True)

    obs_id = models.IntegerField(null=False, default=0, verbose_name="Obs_id")

    agg_id = models.IntegerField(null=False, default=0, verbose_name="Agg_id")

    agg_level = models.CharField(null=False, max_length=2, verbose_name="level")

    delta_duration = models.IntegerField(null=False, verbose_name="Delta duration added in aggregation")

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Delta values added in aggregation")

    def __str__(self):
        return "AggHisto id: " + str(self.id) + ", obs: " + str(self.obs_id) + ", Aggreg: " + str(self.agg_id) + ", level: " + self.agg_level

    class Meta:
        db_table = "agg_histo"
        indexes = [
            models.Index(fields=('agg_level', 'agg_id')),
            models.Index(fields=('obs_id', 'agg_level', 'agg_id')),
        ]


class Incident(models.Model):
    id = models.AutoField(primary_key=True)

    dat = DateCharField(null=False, max_length=30, verbose_name="Incident date'")

    source = models.CharField(null=False, max_length=100, verbose_name='source')

    level = models.CharField(null=False, max_length=20, verbose_name='level')
    # error, critical, exception

    reason = models.TextField(null=False, verbose_name='reason')

    j = DateJSONField(encoder=DjangoJSONEncoder, null=False, verbose_name="Details")
    # stack for exception

    active = models.BooleanField(default=True, verbose_name='active')

    def __str__(self):
        return "Incident id: " + str(self.id) + ", date: " + str(self.dat) + ", Source: " + str(self.source) + ", Reason: " + str(self.reason)

    class Meta:
        db_table = "incident"
