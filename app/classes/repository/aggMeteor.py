from app.models import Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global   #
from app.tools.climConstant import AggLevel
from app.tools.jsonPlus import JsonPlus
from app.tools.aggTools import calcAggDate
import datetime
import pytest
import logging
from app.tools.dateTools import date_to_str, str_to_date


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
        my_start_date = date_to_str(my_start_date)
        agg_object = self.getAggObject(agg_niveau)
        if agg_object.objects.filter(poste_id_id=poste_id).filter(start_dat=my_start_date).exists():
            self.data = agg_object.objects.filter(poste_id_id=poste_id).filter(start_dat=my_start_date).first()
            JsonPlus().deserialize(self.data.j)
        else:
            self.data = agg_object(poste_id_id=poste_id, start_dat=my_start_date, duration_sum=0, j={})
        # decode start_dat
        self.data.start_dat = str_to_date(self.data.start_dat)

    def save(self):
        """ save Poste and Exclusions """
        if self.data.j != {}:
            self.data.start_dat = date_to_str(self.data.start_dat)
            JsonPlus().serialize(self.data.j)
            self.data.save()
            JsonPlus().deserialize(self.data.j)
            self.data.start_dat = str_to_date(self.data.start_dat)

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

    def count(self, niveau_agg: str, poste_id: int = None, start_dat_mask: str = '') -> int:
        # return count of aggregations
        agg_obj = self.getAggObject(niveau_agg)
        if poste_id is None:
            return agg_obj.objects.filter(start_dat__contains=start_dat_mask).count()
        return agg_obj.objects.filter(poste_id=poste_id).filter(start_dat__contains=start_dat_mask).count()

    def __str__(self):
        """print myself"""
        return "AggMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat) + ", level: " + self.agg_niveau
