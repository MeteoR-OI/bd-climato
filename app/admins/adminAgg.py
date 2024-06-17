from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from app.models import AggHour, AggDay, AggMonth, AggYear, AggAll, Poste, DateJSONField, Observation
from app.tools.dateTools import date_to_str
from django.utils.html import format_html
from app.admins.yearMonthFiltering import MonthListFilterStartDat, YearListFilterStartDat
from app.tools.aggTools import calcAggDateNextLevel
from django.urls import reverse
from django.utils.http import urlencode


class AggHourAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AggHour: Agrégations Horaires'}
        return super(AggHourAdmin, self).changelist_view(request, extra_context=extra_context)

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'view_aggregations',
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
        """ get a link to the poste of the aggregtion """
        post = Poste.objects.filter(id=obj.poste_id).first()
        if post is None:
            return 'n/a'
        url = reverse("admin:app_poste_change", args=(obj.poste_id,))
        return format_html('<a href="{}">{}</a>', url, post.meteor)
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_day(self, obj):
        """ get a link to the aggregation day where our data are aggregated """
        day_start_dat = calcAggDateNextLevel('H', obj.start_dat, 0, False)
        agg = AggDay.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        url = reverse("admin:app_aggday_change", args=(agg.id,))
        return format_html('<a href="{}">{}</a>', url, '{0}'.format(agg.start_dat)[0:10])
    show_clickage_agg_day.short_description = "goto day"

    def view_aggregations(self, obj):
        """ get the list of observations that were agregated in this agregate """
        url = reverse("admin:app_agghistobyagg_changelist") + "?" + urlencode({"agg_id": f"{obj.id}"})
        return format_html('<a href="{}">{}</a>', url, "agrégat")
    view_aggregations.short_description = "Composition"


class AggDayAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AggDay: Agrégations Journalières'}
        return super(AggDayAdmin, self).changelist_view(request, extra_context=extra_context)

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'view_aggregations',
        'show_clickage_agg_month',
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
        url = reverse("admin:app_poste_change", args=(obj.poste_id,))
        return format_html('<a href="{}">{}</a>', url, post.meteor)
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_month(self, obj):
        """ get a link to the aggregation month where our data are aggregated """
        day_start_dat = calcAggDateNextLevel('D', obj.start_dat, 0, False)
        agg = AggMonth.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        url = reverse("admin:app_aggmonth_change", args=(agg.id,))
        return format_html('<a href="{}">{}</a>', url, '{0}'.format(agg.start_dat)[0:7])
    show_clickage_agg_month.short_description = "goto Month"

    def view_aggregations(self, obj):
        """ get the list of observations that were agregated in this agregate """
        url = reverse("admin:app_agghistobyagg_changelist") + "?" + urlencode({"agg_id": f"{obj.id}"})
        return format_html('<a href="{}">{}</a>', url, "agrégat")
    view_aggregations.short_description = "Composition"


class AggMonthAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AggMonth: Agrégations Mensuelles'}
        return super(AggMonthAdmin, self).changelist_view(request, extra_context=extra_context)

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'show_clickage_agg_year',
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
        url = reverse("admin:app_poste_change", args=(obj.poste_id,))
        return format_html('<a href="{}">{}</a>', url, post.meteor)
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_year(self, obj):
        """ get a link to the aggregation month where our data are aggregated """
        day_start_dat = calcAggDateNextLevel('M', obj.start_dat, 0, False)
        agg = AggYear.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        url = reverse("admin:app_aggyear_change", args=(agg.id,))
        return format_html('<a href="{}">{}</a>', url, '{0}'.format(agg.start_dat)[0:4])
    show_clickage_agg_year.short_description = "goto Year"


class AggYearAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AggYear: Agrégations Annuelles'}
        return super(AggYearAdmin, self).changelist_view(request, extra_context=extra_context)

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'show_clickage_agg_all',
    )
    ordering = ('start_dat',)
    search_fields = ('start_dat',)
    list_filter = ('poste',)
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
        url = reverse("admin:app_poste_change", args=(obj.poste_id,))
        return format_html('<a href="{}">{}</a>', url, post.meteor)
    show_clickage_poste_id.short_description = "poste"

    def show_clickage_agg_all(self, obj):
        """ get a link to the aggregation month where our data are aggregated """
        day_start_dat = calcAggDateNextLevel('Y', obj.start_dat, 0, False)
        agg = AggAll.objects.filter(poste_id=obj.poste_id).filter(start_dat=day_start_dat).first()
        if agg is None:
            return 'n/a'
        url = reverse("admin:app_aggall_change", args=(agg.id,))
        return format_html('<a href="{}">{}</a>', url, 'All')
    show_clickage_agg_all.short_description = "goto All"


class AggAllAdmin(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AggAll: Agrégations globales'}
        return super(AggAllAdmin, self).changelist_view(request, extra_context=extra_context)

    list_display = (
        'start_dat',
        'show_clickage_poste_id',
        'duration_sum',
        'duration_max'
    )
    ordering = ('start_dat',)
    search_fields = ('start_dat',)
    list_filter = ('poste',)
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
        url = reverse("admin:app_poste_change", args=(obj.poste_id,))
        return format_html('<a href="{}">{}</a>', url, post.meteor)
    show_clickage_poste_id.short_description = "poste"


class AggHistoAdminByObs(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'HistoAgg by Obs: Historique (search by obs_id)'}
        return super(AggHistoAdminByObs, self).changelist_view(request, extra_context=extra_context)

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
            return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/agghour/" + '{0}'.format(obj.agg_id) + "/change/", '{0}'.format(obj.agg_id))
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggday/" + '{0}'.format(obj.agg_id) + "/change/", '{0}'.format(obj.agg_id))
    show_clickage_agg_id.short_description = "agg_id"

    def show_clickage_obs_id(self, obj):
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/observation/" + '{0}'.format(obj.obs_id) + "/change/", '{0}'.format(obj.obs_id))
    show_clickage_obs_id.short_description = "obs_id"


class AggHistoAdminByAgg(admin.ModelAdmin):
    formfield_overrides = {
        DateJSONField: {'widget': JSONEditorWidget},
    }

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'HistoAgg by Agg: Historique (search by agg_id)'}
        return super(AggHistoAdminByAgg, self).changelist_view(request, extra_context=extra_context)

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
            return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/agghour/" + '{0}'.format(obj.agg_id) + "/change/", '{0}'.format(obj.agg_id))
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/aggday/" + '{0}'.format(obj.agg_id) + "/change/", '{0}'.format(obj.agg_id))
    show_clickage_agg_id.short_description = "agg_id"

    def show_clickage_obs_id(self, obj):
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/observation/" + '{0}'.format(obj.obs_id) + "/change/", '{0}'.format(obj.obs_id))
    show_clickage_obs_id.short_description = "obs_id"
