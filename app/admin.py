from django.contrib import admin

from app.models import AggAll, TypeInstrument, Exclusion, Poste, Observation
from app.models import AggHour, AggDay, AggMonth, AggYear, AggHisto

from app.admins.adminObservation import ObservationAdmin
from app.admins.adminPoste import PosteAdmin
from app.admins.adminAgg import AggHourAdmin, AggDayAdmin, AggMonthAdmin, AggYearAdmin, AggAllAdmin, AggHistoAdminByAgg, AggHistoAdminByObs

admin.site.register(Poste, PosteAdmin)

admin.site.register(Observation, ObservationAdmin)

admin.site.register(TypeInstrument)

admin.site.register(Exclusion)

admin.site.register(AggHour, AggHourAdmin)

admin.site.register(AggDay, AggDayAdmin)

admin.site.register(AggMonth, AggMonthAdmin)

admin.site.register(AggYear, AggYearAdmin)

admin.site.register(AggAll, AggAllAdmin)


class AggHistoByAgg(AggHisto):
    class Meta:
        proxy = True


admin.site.register(AggHistoByAgg, AggHistoAdminByAgg)


class AggHistoByObs(AggHisto):
    class Meta:
        proxy = True


admin.site.register(AggHistoByObs, AggHistoAdminByObs)
