from django.contrib import admin

from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, TypeData, Exclusion

admin.site.register(TypeData)

admin.site.register(Exclusion)

class PosteAdmin(admin.ModelAdmin):
    fields = (
        ('meteor', 'meteofr'),
        'title',
        'owner',
        ('email', 'phone'),
        ('address', 'zip'),
        ('city', 'country'),
        ('latitude', 'longitude'),
        ('start', 'end'),
        ('cas_gestion_extreme', 'agg_min_extreme'),
        'comment'
    )

admin.site.register(Poste, PosteAdmin)


class ObservationAdmin(admin.ModelAdmin):
    fields = (
        ('dat', 'last_rec_dat'),
        ('duration'),
        ('qa_modifications', 'qa_incidents', 'qa_check_done'),
        ('poste_id'),
        ('barometer', 'barometer_max', 'barometer_max_time', 'barometer_min', 'barometer_min_time', 'pressure'),
        ('dewpoint', 'etp', 'heat_index'),
        ('humidity', 'inHumidity'),
        ('humidity_max', 'humidity_max_time'),
        ('humidity_min', 'humidity_min_time'),
        ('insolation_duration'),
        ('out_temp', 'in_temp'),
        ('out_temp_max', 'out_temp_max_time'),
        ('out_temp_min', 'out_temp_min_time'),
        ('rain_rate_max', 'rain_rate_max_time', 'rain_sum'),
        ('soil_temp'),
        ('soil_temp_min', 'soil_temp_min_time'),
        ('solar_radiation', 'uv', 'uv_indixe'),
        ('wind_dir', 'wind_speed', 'windchill'),
        ('wind_gust', 'wind_gust_dir', 'wind_gust_time'),
        ('rx', 'voltage')
    )

admin.site.register(Observation, ObservationAdmin)


class Agg_hourAdmin(admin.ModelAdmin):
    fields = (
        ('dat', 'last_rec_dat'),
        ('duration'),
        ('qa_modifications', 'qa_incidents', 'qa_check_done'),
        ('poste_id'),
        ('barometer_avg', 'barometer_sum', 'barometer_duration'),
        ('barometer_max', 'barometer_max_time'),
        ('barometer_min', 'barometer_min_time'),
        ('dewpoint_max', 'dewpoint_max_time', 'dewpoint_min', 'dewpoint_min_time'),
        ('etp_max', 'etp_max_time', 'etp_min', 'etp_min_time'),
        ('heat_index_max', 'heat_index_max_time'),
        ('humidity_max', 'humidity_max_time', 'humidity_min', 'humidity_min_time'),
        ('in_humidity_max', 'in_humidity_max_time', 'in_humidity_min', 'in_humidity_min_time'),
        ('in_temp_max', 'in_temp_max_time', 'in_temp_min', 'in_temp_min_time'),
        ('out_temp_avg', 'out_temp_sum', 'out_temp_duration'),
        ('out_temp_max', 'out_temp_max_time', 'out_temp_min', 'out_temp_min_time', 'rain_avg'),
        ('rain_duration', 'rain_sum', 'rain_rate_max', 'rain_rate_max_time', 'rx_avg'),
        ('rx_duration', 'rx_sum', 'rx_max', 'rx_max_time', 'rx_min', 'rx_min_time'),
        ('soil_temp_in_time', 'soil_temp_min'),
        ('uv_max', 'uv_max_time', 'uv_min', 'uv_min_time'),
        ('voltage_avg', 'voltage_sum', 'voltage_duration', 'voltage_max', 'voltage_max_time', 'voltage_min', 'voltage_min_time'),
        ('wind_speed_avg', 'win_speed_duration',  'wind_speed_sum', 'wind_dir_avg', 'wind_dir_duration', 'wind_dir_sum', 'wind_gust', 'wind_gust_dir', 'wind_gust_time'),
        ('windchill_max', 'windchill_max_time', 'windchill_min', 'windchill_min_time')
    )

admin.site.register(Agg_hour, Agg_hourAdmin)


class Agg_dayAdmin(admin.ModelAdmin):
    fields = (
        ('dat', 'last_rec_dat'),
        ('duration'),
        ('qa_modifications', 'qa_incidents', 'qa_check_done'),
        ('poste_id'),
        ('barometer_avg', 'barometer_sum', 'barometer_duration'),
        ('barometer_max', 'barometer_max_time'),
        ('barometer_min', 'barometer_min_time'),
        ('dewpoint_max', 'dewpoint_max_time', 'dewpoint_min', 'dewpoint_min_time'),
        ('etp_max', 'etp_max_time', 'etp_min', 'etp_min_time'),
        ('heat_index_max', 'heat_index_max_time'),
        ('humidity_max', 'humidity_max_time', 'humidity_min', 'humidity_min_time'),
        ('in_humidity_max', 'in_humidity_max_time', 'in_humidity_min', 'in_humidity_min_time'),
        ('in_temp_max', 'in_temp_max_time', 'in_temp_min', 'in_temp_min_time'),
        ('out_temp_avg', 'out_temp_sum', 'out_temp_duration'),
        ('out_temp_max', 'out_temp_max_time', 'out_temp_min', 'out_temp_min_time', 'rain_avg'),
        ('rain_duration', 'rain_sum', 'rain_rate_max', 'rain_rate_max_time', 'rx_avg'),
        ('rx_duration', 'rx_sum', 'rx_max', 'rx_max_time', 'rx_min', 'rx_min_time'),
        ('soil_temp_in_time', 'soil_temp_min'),
        ('uv_max', 'uv_max_time', 'uv_min', 'uv_min_time'),
        ('voltage_avg', 'voltage_sum', 'voltage_duration', 'voltage_max', 'voltage_max_time', 'voltage_min', 'voltage_min_time'),
        ('wind_speed_avg', 'win_speed_duration',  'wind_speed_sum', 'wind_dir_avg', 'wind_dir_duration', 'wind_dir_sum', 'wind_gust', 'wind_gust_dir', 'wind_gust_time'),
        ('windchill_max', 'windchill_max_time', 'windchill_min', 'windchill_min_time')
    )

admin.site.register(Agg_day, Agg_dayAdmin)


class Agg_monthAdmin(admin.ModelAdmin):
    fields = (
        ('dat', 'last_rec_dat'),
        ('duration'),
        ('qa_modifications', 'qa_incidents', 'qa_check_done'),
        ('poste_id'),
        ('barometer_avg', 'barometer_sum', 'barometer_duration'),
        ('barometer_max', 'barometer_max_time'),
        ('barometer_min', 'barometer_min_time'),
        ('dewpoint_max', 'dewpoint_max_time', 'dewpoint_min', 'dewpoint_min_time'),
        ('etp_max', 'etp_max_time', 'etp_min', 'etp_min_time'),
        ('heat_index_max', 'heat_index_max_time'),
        ('humidity_max', 'humidity_max_time', 'humidity_min', 'humidity_min_time'),
        ('in_humidity_max', 'in_humidity_max_time', 'in_humidity_min', 'in_humidity_min_time'),
        ('in_temp_max', 'in_temp_max_time', 'in_temp_min', 'in_temp_min_time'),
        ('out_temp_avg', 'out_temp_sum', 'out_temp_duration'),
        ('out_temp_max', 'out_temp_max_time', 'out_temp_min', 'out_temp_min_time', 'rain_avg'),
        ('rain_duration', 'rain_sum', 'rain_rate_max', 'rain_rate_max_time', 'rx_avg'),
        ('rx_duration', 'rx_sum', 'rx_max', 'rx_max_time', 'rx_min', 'rx_min_time'),
        ('soil_temp_in_time', 'soil_temp_min'),
        ('uv_max', 'uv_max_time', 'uv_min', 'uv_min_time'),
        ('voltage_avg', 'voltage_sum', 'voltage_duration', 'voltage_max', 'voltage_max_time', 'voltage_min', 'voltage_min_time'),
        ('wind_speed_avg', 'win_speed_duration',  'wind_speed_sum', 'wind_dir_avg', 'wind_dir_duration', 'wind_dir_sum', 'wind_gust', 'wind_gust_dir', 'wind_gust_time'),
        ('windchill_max', 'windchill_max_time', 'windchill_min', 'windchill_min_time')
    )
admin.site.register(Agg_month, Agg_monthAdmin)


class Agg_yearAdmin(admin.ModelAdmin):
    fields = (
        ('dat', 'last_rec_dat'),
        ('duration'),
        ('qa_modifications', 'qa_incidents', 'qa_check_done'),
        ('poste_id'),
        ('barometer_avg', 'barometer_sum', 'barometer_duration'),
        ('barometer_max', 'barometer_max_time'),
        ('barometer_min', 'barometer_min_time'),
        ('dewpoint_max', 'dewpoint_max_time', 'dewpoint_min', 'dewpoint_min_time'),
        ('etp_max', 'etp_max_time', 'etp_min', 'etp_min_time'),
        ('heat_index_max', 'heat_index_max_time'),
        ('humidity_max', 'humidity_max_time', 'humidity_min', 'humidity_min_time'),
        ('in_humidity_max', 'in_humidity_max_time', 'in_humidity_min', 'in_humidity_min_time'),
        ('in_temp_max', 'in_temp_max_time', 'in_temp_min', 'in_temp_min_time'),
        ('out_temp_avg', 'out_temp_sum', 'out_temp_duration'),
        ('out_temp_max', 'out_temp_max_time', 'out_temp_min', 'out_temp_min_time', 'rain_avg'),
        ('rain_duration', 'rain_sum', 'rain_rate_max', 'rain_rate_max_time', 'rx_avg'),
        ('rx_duration', 'rx_sum', 'rx_max', 'rx_max_time', 'rx_min', 'rx_min_time'),
        ('soil_temp_in_time', 'soil_temp_min'),
        ('uv_max', 'uv_max_time', 'uv_min', 'uv_min_time'),
        ('voltage_avg', 'voltage_sum', 'voltage_duration', 'voltage_max', 'voltage_max_time', 'voltage_min', 'voltage_min_time'),
        ('wind_speed_avg', 'win_speed_duration',  'wind_speed_sum', 'wind_dir_avg', 'wind_dir_duration', 'wind_dir_sum', 'wind_gust', 'wind_gust_dir', 'wind_gust_time'),
        ('windchill_max', 'windchill_max_time', 'windchill_min', 'windchill_min_time')
    )


admin.site.register(Agg_year, Agg_yearAdmin)


class Agg_globalAdmin(admin.ModelAdmin):
    fields = (
        ('dat', 'last_rec_dat'),
        ('duration'),
        ('qa_modifications', 'qa_incidents', 'qa_check_done'),
        ('poste_id'),
        ('barometer_avg', 'barometer_sum', 'barometer_duration'),
        ('barometer_max', 'barometer_max_time'),
        ('barometer_min', 'barometer_min_time'),
        ('dewpoint_max', 'dewpoint_max_time', 'dewpoint_min', 'dewpoint_min_time'),
        ('etp_max', 'etp_max_time', 'etp_min', 'etp_min_time'),
        ('heat_index_max', 'heat_index_max_time'),
        ('humidity_max', 'humidity_max_time', 'humidity_min', 'humidity_min_time'),
        ('in_humidity_max', 'in_humidity_max_time', 'in_humidity_min', 'in_humidity_min_time'),
        ('in_temp_max', 'in_temp_max_time', 'in_temp_min', 'in_temp_min_time'),
        ('out_temp_avg', 'out_temp_sum', 'out_temp_duration'),
        ('out_temp_max', 'out_temp_max_time', 'out_temp_min', 'out_temp_min_time', 'rain_avg'),
        ('rain_duration', 'rain_sum', 'rain_rate_max', 'rain_rate_max_time', 'rx_avg'),
        ('rx_duration', 'rx_sum', 'rx_max', 'rx_max_time', 'rx_min', 'rx_min_time'),
        ('soil_temp_in_time', 'soil_temp_min'),
        ('uv_max', 'uv_max_time', 'uv_min', 'uv_min_time'),
        ('voltage_avg', 'voltage_sum', 'voltage_duration', 'voltage_max', 'voltage_max_time', 'voltage_min', 'voltage_min_time'),
        ('wind_speed_avg', 'win_speed_duration',  'wind_speed_sum', 'wind_dir_avg', 'wind_dir_duration', 'wind_dir_sum', 'wind_gust', 'wind_gust_dir', 'wind_gust_time'),
        ('windchill_max', 'windchill_max_time', 'windchill_min', 'windchill_min_time')
    )

admin.site.register(Agg_global, Agg_globalAdmin)

