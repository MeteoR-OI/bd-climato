from app.tools.climConstant import AggLevel
from app.tools.aggTools import getAggObject
from app.tools.jsonPlus import JsonPlus
import datetime


class AggMeteor():
    """
        AggMeteor

        gere les objets Aggregation metier
        Act as a super Class for all aggregation objects

        o=AggMeteor(poste, dat)
        o.data -> Aggregation object (data, methods...)

    """

    def __init__(self, poste_id: int, agg_niveau: AggLevel, dt_agg_utc: datetime):
        """
            Init a new AggMeteor object

            poste: Poste object
            agg_niveau: 'H','D', 'M', 'Y', 'A'
            dt_agg_utc: date rounded for the aggregation level
        """
        try:
            self.agg_niveau = agg_niveau
            agg_object = getAggObject(agg_niveau)
            if agg_object.objects.filter(poste_id_id=poste_id).filter(dat=dt_agg_utc).exists():
                self.data = agg_object.objects.filter(poste_id_id=poste_id).filter(dat=dt_agg_utc).first()
                JsonPlus().deserialize(self.data.j)
            else:
                self.data = agg_object(poste_id_id=poste_id, dat=dt_agg_utc, last_rec_dat=dt_agg_utc, duration=0, j={})
                self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def save(self):
        """ save Poste and Exclusions """
        try:
            if self.data.j != {}:
                JsonPlus().serialize(self.data.j)
            self.data.save()
            JsonPlus().deserialize(self.data.j)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "AggMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat) + ", level: " + self.agg_niveau
