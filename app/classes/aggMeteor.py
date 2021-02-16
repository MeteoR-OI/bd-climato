from app.models import Poste   # ,Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global
from app.tools.agg_tools import get_agg_object
from app.tools.climConstant import AggLevel
import datetime


class AggMeteor():
    """
        AggMeteor

        gere les objets Aggregation metier
        Act as a super Class for all aggregation objects

        o=AggMeteor(poste, dat)
        o.data -> Aggregation object (data, methods...)

    """

    def __init__(self, poste: Poste, agg_niveau: AggLevel, dt_agg_utc: datetime):
        """
            Init a new AggMeteor object

            poste: Poste object
            agg_niveau: 'H','D', 'M', 'Y', 'A'
            dt_agg_utc: date rounded for the aggregation level
        """
        try:
            self.agg_niveau = agg_niveau
            agg_object = get_agg_object(agg_niveau)
            if agg_object.objects.filter(poste_id_id=poste.id).filter(dat=dt_agg_utc).exists():
                self.data = agg_object.objects.filter(
                    poste_id_id=poste.id).filter(dat=dt_agg_utc).first()
            else:
                self.data = agg_object(
                    poste_id=poste, dat=dt_agg_utc, last_rec_dat=dt_agg_utc, duration=0)
                self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def save(self):
        """ save Poste and Exclusions """
        try:
            self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "AggMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat) + ", level: " + self.agg_niveau
