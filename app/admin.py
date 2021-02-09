from django.contrib import admin

from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, TypeData, Exclusion

admin.site.register(TypeData)

admin.site.register(Exclusion)

class PosteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                              {'fields': ['meteor', 'meteofr', 'title']}),
        ('Information',                     {'fields': ['owner', 'email', 'phone', 'address', 'zip', 'city', 'country']}),
        ('GeoLocalisation',                 {'fields': ['latitude', 'longitude']}),
        ('Date Activation dans meteoR.OI',  {'fields': ['start', 'end']}),
        ('Extremes',                        {'fields': ['cas_gestion_extreme', 'agg_min_extreme']}),
        ('Commentaire',                     {'fields': ['comment']})
    ]

admin.site.register(Poste, PosteAdmin)


class ObservationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['poste_id', 'dat', 'duration']}),
        ('Observations',    {'fields': ['j']}),
    ]

admin.site.register(Observation, ObservationAdmin)


class Agg_hourAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['poste_id', 'dat', 'duration']}),
        ('Observations',    {'fields': ['j']}),
    ]

admin.site.register(Agg_hour, Agg_hourAdmin)


class Agg_dayAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['poste_id', 'dat', 'duration']}),
        ('Observations',    {'fields': ['j']}),
    ]

admin.site.register(Agg_day, Agg_dayAdmin)


class Agg_monthAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['poste_id', 'dat', 'duration']}),
        ('Observations',    {'fields': ['j']}),
    ]

admin.site.register(Agg_month, Agg_monthAdmin)


class Agg_yearAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['poste_id', 'dat', 'duration']}),
        ('Observations',    {'fields': ['j']}),
    ]

admin.site.register(Agg_year, Agg_yearAdmin)


class Agg_globalAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['poste_id', 'dat', 'duration']}),
        ('Observations',    {'fields': ['j']}),
    ]

admin.site.register(Agg_global, Agg_globalAdmin)

