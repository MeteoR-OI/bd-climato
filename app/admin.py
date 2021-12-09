from django.contrib import admin
from django.db import models

from app.models import DateJSONField, Poste, Observation, AggHour, AggDay, AggMonth, AggYear, AggAll, TypeInstrument, Exclusion

from django_json_widget.widgets import JSONEditorWidget

admin.site.register(TypeInstrument)

admin.site.register(Exclusion)


class PosteAdmin(admin.ModelAdmin):
    fields = (
        'meteor',
        'meteofr',
        'fuseau',
        ('cas_gestion_extreme', 'agg_min_extreme'),
        'comment'
    )


admin.site.register(Poste, PosteAdmin)


class ObservationAdmin(admin.ModelAdmin):
    # all fields:
    # ('poste_id'),
    # ('start_dat'),
    # ('duration'),
    # ('qa_modifications', 'qa_incidents', 'qa_check_done'),
    # ('out_temp', 'out_temp_max', 'out_temp_max_time', 'out_temp_min', 'out_temp_min_time',
    #  'windchill', 'heat_index', 'dewpoint', 'soil_temp', 'soil_temp_min', 'soil_temp_min_time'),
    # ('humidity', 'humidity_max', 'humidity_max_time', 'humidity_min', 'humidity_min_time'),
    # ('barometer', 'barometer_max', 'barometer_max_time', 'barometer_min', 'barometer_min_time', 'pressure'),
    # ('wind_i', 'wind_i_dir', 'wind', 'wind_dir', 'wind_max', 'wind_max_dir', 'wind_max_time', 'wind10'),
    # ('rain', 'rain_rate', 'rain_rate_max', 'rain_rate_max_time'),
    # ('uv_indice', 'radiation', 'etp'),
    # ('in_temp', 'in_humidity'),
    # ('rx', 'voltage')
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste_id'),
        ('stop_dat'),
        ('duration'),
        ('j'),
        ('j_agg')
    )


admin.site.register(Observation, ObservationAdmin)


class AggHourAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_s'),
        ('j')
    )


admin.site.register(AggHour, AggHourAdmin)


class AggDayAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_s'),
        ('j')
    )


admin.site.register(AggDay, AggDayAdmin)


class AggMonthAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_s'),
        ('j')
    )


admin.site.register(AggMonth, AggMonthAdmin)


class AggYearAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_s'),
        ('j')
    )


admin.site.register(AggYear, AggYearAdmin)


class AggAllAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_s'),
        ('j')
    )


admin.site.register(AggAll, AggAllAdmin)
