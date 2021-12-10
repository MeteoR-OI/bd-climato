from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from app.models import AggHour, AggDay, AggMonth, AggYear, AggAll, Poste, DateJSONField, Observation
from app.tools.dateTools import date_to_str
from django.utils.html import format_html
from app.admins.yearMonthFiltering import MonthListFilterStartDat, YearListFilterStartDat
from app.tools.aggTools import calcAggDateNextLevel


class AggHourAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'show_clickage_agg_day',
    )
    ordering = ('start_dat',)
    list_filter = ('poste', YearListFilterStartDat, MonthListFilterStartDat)
    search_fields = ('start_dat',)
    list_per_page = 20
    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )

    def show_clickage_poste_id(self, obj):
        post = Poste.objects.filter(id=obj.poste_id).first()
        if post is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/poste/" + str(obj.poste_id) + "/change/", str(obj.poste_id))
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_day(self, obj):
        day_start_dat = calcAggDateNextLevel('H', obj.start_dat, 0, False)
        agg = AggDay.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggday/" + str(agg.id) + "/change/", str(agg.id))
    show_clickage_agg_day.short_description = "agg Day"


class AggDayAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'show_clickage_agg_day',
    )
    ordering = ('start_dat',)
    list_filter = ('poste', YearListFilterStartDat, MonthListFilterStartDat)
    search_fields = ('start_dat',)
    list_per_page = 20
    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )

    def show_clickage_poste_id(self, obj):
        post = Poste.objects.filter(id=obj.poste_id).first()
        if post is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/poste/" + str(obj.poste_id) + "/change/", str(obj.poste_id))
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_day(self, obj):
        day_start_dat = calcAggDateNextLevel('D', obj.start_dat, 0, False)
        agg = AggMonth.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggmonth/" + str(agg.id) + "/change/", str(agg.id))
    show_clickage_agg_day.short_description = "agg Month"


class AggMonthAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'show_clickage_agg_day',
    )
    ordering = ('start_dat',)
    list_filter = ('poste', YearListFilterStartDat)
    search_fields = ('start_dat',)
    list_per_page = 20
    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )

    def show_clickage_poste_id(self, obj):
        post = Poste.objects.filter(id=obj.poste_id).first()
        if post is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/poste/" + str(obj.poste_id) + "/change/", str(obj.poste_id))
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_day(self, obj):
        day_start_dat = calcAggDateNextLevel('M', obj.start_dat, 0, False)
        agg = AggYear.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggyear/" + str(agg.id) + "/change/", str(agg.id))
    show_clickage_agg_day.short_description = "agg Year"


class AggYearAdmin(admin.ModelAdmin):

    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'show_clickage_agg_day',
    )
    ordering = ('start_dat',)
    search_fields = ('start_dat',)
    list_per_page = 20
    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )

    def show_clickage_poste_id(self, obj):
        post = Poste.objects.filter(id=obj.poste_id).first()
        if post is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/poste/" + str(obj.poste_id) + "/change/", str(obj.poste_id))
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_day(self, obj):
        day_start_dat = calcAggDateNextLevel('Y', obj.start_dat, 0, False)
        agg = AggAll.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggall/" + str(agg.id) + "/change/", str(agg.id))
    show_clickage_agg_day.short_description = "agg All"


class AggAllAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'duration_max'
    )
    ordering = ('start_dat',)
    search_fields = ('start_dat',)
    list_per_page = 20
    fields = (
        ('poste'),
        ('start_dat'),
        ('duration_sum', 'duration_max'),
        ('j')
    )

    def show_clickage_poste_id(self, obj):
        post = Poste.objects.filter(id=obj.poste_id).first()
        if post is None:
            return 'n/a'
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/poste/" + str(obj.poste_id) + "/change/", str(obj.poste_id))
    show_clickage_poste_id.short_description = "poste"


class AggHistoAdminByObs(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'agg_level',
        'show_clickage_agg_id',
        'show_agg_start_dat',
        'show_clickage_obs_id',
    )
    ordering = ('obs_id',)
    list_filter = ('agg_level',)
    search_fields = ('obs_id',)
    list_per_page = 20
    fields = (
        ('obs_id', 'agg_id', 'agg_level'),
        ('delta_duration'),
        ('j')
    )

    def show_agg_start_dat(self, obj):
        if obj.agg_level[0] == 'H':
            agg = AggHour.objects.filter(id=obj.agg_id).first()
        else:
            agg = AggDay.objects.filter(id=obj.agg_id).first()
        if agg is None:
            return 'n/a'
        return date_to_str(agg.start_dat)
    show_agg_start_dat.short_description = "Agg start"

    def show_clickage_agg_id(self, obj):
        if obj.agg_level[0] == "H":
            return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/agghour/" + str(obj.agg_id) + "/change/", str(obj.agg_id))
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggday/" + str(obj.agg_id) + "/change/", str(obj.agg_id))
    show_clickage_agg_id.short_description = "agg_id"

    def show_clickage_obs_id(self, obj):
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/observation/" + str(obj.obs_id) + "/change/", str(obj.obs_id))
    show_clickage_obs_id.short_description = "obs_id"


class AggHistoAdminByAgg(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    list_display = (
        'agg_level',
        'show_clickage_agg_id',
        'show_obs_stop_dat',
        'show_clickage_obs_id',
    )
    ordering = ('obs_id',)
    search_fields = ('agg_id',)
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
    show_obs_stop_dat.short_description = "Obs fin"

    def show_clickage_agg_id(self, obj):
        if obj.agg_level == "H":
            return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/agghour/" + str(obj.agg_id) + "/change/", str(obj.agg_id))
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggday/" + str(obj.agg_id) + "/change/", str(obj.agg_id))
    show_clickage_agg_id.short_description = "agg_id"

    def show_clickage_obs_id(self, obj):
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/observation/" + str(obj.obs_id) + "/change/", str(obj.obs_id))
    show_clickage_obs_id.short_description = "obs_id"
