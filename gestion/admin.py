from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import PAYS,COMMUNE,POSTE,PANNE,INSTRUMENT,MAINTENANCE,INSTAN,H,Q,DECADQ,MENSQ,RECMENS,HISTMAINT,HISTPOST

admin.site.register(POSTE)
admin.site.register(COMMUNE)

