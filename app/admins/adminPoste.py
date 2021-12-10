from django.contrib import admin


class PosteAdmin(admin.ModelAdmin):
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
