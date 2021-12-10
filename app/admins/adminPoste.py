from django.contrib import admin
from django.utils.html import format_html


class PosteAdmin(admin.ModelAdmin):
    list_display = (
        'meteor',
        'meteofr',
        'email',
        'view_observations'
    )
    ordering = ('meteor',)
    search_fields = ('meteor',)
    list_per_page = 20
    fields = (
        ('meteor', 'fuseau'),
        ('meteofr', 'owner'),
        ('email', 'phone'),
        'address',
        ('zip', 'city', 'country'),
        ('longitude', 'latitude'),
        ('start_dat', 'stop_dat'),
        'comment'
    )

    def view_observations(self, obj):
        return format_html('<a href="{}">{}</a>', "http://127.0.0.1:8000/admin/app/observation/?poste__id__exact=" + str(obj.id), 'Obs')
    view_observations.short_description = "Obs"
