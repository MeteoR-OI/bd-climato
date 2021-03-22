from app.models import Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global   #
from app.tools.climConstant import AggLevel
from app.tools.jsonPlus import JsonPlus
from app.tools.aggTools import calcAggDate
import datetime
import pytest
import logging


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    logging.info('fixture aggMeteor::enable_db_access_for_all_tests called')
    pass


class AggMeteor():
    """
        AggMeteor

        gere les objets Aggregation metier
        Act as a super Class for all aggregation objects

        o=AggMeteor(poste, dat)
        o.data -> Aggregation object (data, methods...)

    """

    def __init__(self, poste_id: int, agg_niveau: AggLevel, start_dt_agg_utc: datetime, is_measure_date: bool = False):
        """
            Init a new AggMeteor object

            poste: Poste object
            agg_niveau: 'H','D', 'M', 'Y', 'A'
            start_dt_agg_utc: start_date for the aggregation level, will be rounded
        """
        self.agg_niveau = agg_niveau
        my_start_date = calcAggDate(agg_niveau, start_dt_agg_utc, 0, is_measure_date)
        agg_object = self.getAggObject(agg_niveau)
        if agg_object.objects.filter(poste_id_id=poste_id).filter(start_dat=my_start_date).exists():
            self.data = agg_object.objects.filter(poste_id_id=poste_id).filter(start_dat=my_start_date).first()
            JsonPlus().deserialize(self.data.j)
        else:
            self.data = agg_object(poste_id_id=poste_id, start_dat=my_start_date, duration_sum=0, j={})

    def save(self):
        """ save Poste and Exclusions """
        if self.data.j != {}:
            JsonPlus().serialize(self.data.j)
            self.data.save()
            JsonPlus().deserialize(self.data.j)

    def getAggObject(self, niveau_agg: str):
        """get the aggregation depending on the level"""
        if niveau_agg == "H":
            return Agg_hour
        elif niveau_agg == "D":
            return Agg_day
        elif niveau_agg == "M":
            return Agg_month
        elif niveau_agg == "Y":
            return Agg_year
        elif niveau_agg == "A":
            return Agg_global
        else:
            raise Exception("get_agg_object", "wrong niveau_agg: " + niveau_agg)

    def __str__(self):
        """print myself"""
        return "AggMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat) + ", level: " + self.agg_niveau
