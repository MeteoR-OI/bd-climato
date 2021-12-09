from django.contrib import admin
from app.models import DateJSONField
from django_json_widget.widgets import JSONEditorWidget
from django.utils.html import format_html
from app.admins.yearMonthFiltering import MonthListFilter, YearListFilter


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

    list_display = (
        'poste',
        'stop_dat',
        'view_aggregations'
    )
    fields = (
        ('poste'),
        ('agg_start_dat', 'stop_dat', 'duration'),
        ('j'),
        ('j_agg')
    )
    ordering = ('stop_dat',)
    list_filter = ('poste', YearListFilter, MonthListFilter)
    search_fields = ('stop_dat',)
    list_per_page = 20

    def view_aggregations(self, obj):
        return format_html('<a href="{}">Details {}</a>', "https://google.com", obj.id)
    view_aggregations.short_description = "Agg"
