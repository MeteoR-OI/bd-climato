from django.contrib import admin

from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, TypeInstrument, Exclusion

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
    fields = (
        ('poste_id'),
        ('start_dat', 'stop_dat'),
        ('duration'),
        ('j'),
        ('j_agg')
    )


admin.site.register(Observation, ObservationAdmin)


class Agg_hourAdmin(admin.ModelAdmin):
    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_sum'),
        ('j')
    )

admin.site.register(Agg_hour, Agg_hourAdmin)


class Agg_dayAdmin(admin.ModelAdmin):
    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_sum'),
        ('j')
    )

admin.site.register(Agg_day, Agg_dayAdmin)


class Agg_monthAdmin(admin.ModelAdmin):
    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_sum'),
        ('j')
    )

admin.site.register(Agg_month, Agg_monthAdmin)


class Agg_yearAdmin(admin.ModelAdmin):
    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_sum'),
        ('j')
    )

admin.site.register(Agg_year, Agg_yearAdmin)


class Agg_globalAdmin(admin.ModelAdmin):
    fields = (
        ('poste_id'),
        ('start_dat'),
        ('duration_sum'),
        ('j')
    )

admin.site.register(Agg_global, Agg_globalAdmin)
