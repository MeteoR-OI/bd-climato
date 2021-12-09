from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from app.models import DateJSONField, Observation
from app.tools.dateTools import date_to_str
from django.utils.html import format_html


class AggHourAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )


class AggDayAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )


class AggMonthAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )


class AggYearAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )


class AggAllAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )


class AggHistoAdminByObs(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'agg_level',
        'show_clickage_agg_id',
        'show_clickage_obs_id',
        'show_obs_stop_dat',
    )
    ordering = ('agg_level', 'agg_id',)
    list_filter = ('agg_level',)
    search_fields = ('obs_id',)
    list_per_page = 20
    fields = (
        ('obs_id', 'agg_id', 'agg_level'),
        ('delta_duration'),
        ('j')
    )

    def show_obs_stop_dat(self, obj):
        obs = Observation.objects.filter(id=obj.obs_id).first()
        if obs is None:
            return 'n/a'
        return date_to_str(obs.stop_dat)
    show_obs_stop_dat.short_description = "stop_dat"

    def show_clickage_agg_id(self, obj):
        if obj.agg_level == "H":
            return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/agghour/" + str(obj.agg_id) + "/change/", str(obj.agg_id))
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggday/" + str(obj.agg_id) + "/change/", str(obj.agg_id))
    show_clickage_agg_id.short_description = "agg_id"

    def show_clickage_obs_id(self, obj):
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/observation/" + str(obj.obs_id) + "/change/", str(obj.agg_id))
    show_clickage_obs_id.short_description = "obs_id"


class AggHistoAdminByAgg(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'agg_id',
        'agg_level',
        'obs_id',
    )
    ordering = ('obs_id',)
    search_fields = ('agg_id',)
    list_per_page = 20
    fields = (
        ('obs_id', 'agg_id', 'agg_level'),
        ('delta_duration'),
        ('j')
    )
