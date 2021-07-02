from app.models import AggHour, AggDay, AggMonth, AggYear, AggAll   #
from app.models import TmpAggHour, TmpAggDay, TmpAggMonth, TmpAggYear, TmpAggAll   #
from app.tools.aggTools import calcAggDate, getAggDuration
import datetime
import pytest
import app.tools.myTools as t


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    t.logInfo('fixture aggMeteor::enable_db_access_for_all_tests called')
    pass


class AggMeteor():
    """
        AggMeteor

        gere les objets Aggregation metier
        Act as a super Class for all aggregation objects

        o=AggMeteor(poste, dat)
        o.data -> Aggregation object (data, methods...)

    """

    def __init__(self, poste_id: int, agg_niveau: str, start_dt_agg_utc: datetime, is_measure_date: bool = False, b_need_to_sum_duration: bool = False):
        """
            Init a new AggMeteor object

            poste: Poste object
            agg_niveau: 'H','D', 'M', 'Y', 'A'
            start_dt_agg_utc: start_date for the aggregation level, will be rounded
            id_main_date: flag main aggregations (to update duration_sum)
        """
        self.agg_niveau = agg_niveau
        my_start_date = calcAggDate(agg_niveau, start_dt_agg_utc, 0, is_measure_date)
        # my_start_date = date_to_str(my_start_date)
        agg_object = self.getAggObject(agg_niveau)
        if agg_object.objects.filter(poste_id_id=poste_id).filter(start_dat=my_start_date).exists():
            self.data = agg_object.objects.filter(poste_id_id=poste_id).filter(start_dat=my_start_date).first()
        else:
            self.data = agg_object(poste_id_id=poste_id, start_dat=my_start_date, duration_sum=0, duration_max=0, j={})
            self.data.duration_max = getAggDuration(agg_niveau, my_start_date)
        self.b_need_to_sum_duration = b_need_to_sum_duration

    def save(self):
        """ save Poste and Exclusions """
        dirty_found = False
        if self.data.j != {}:
            for akey in self.__dir__():
                if akey == 'dirty':
                    dirty_found = True
                    break
            if dirty_found is False or self.dirty is True:
                if self.data.duration_sum > self.data.duration_max:
                    raise Exception("duration overflow for agg_" + self.agg_niveau + ', id: ' + str(self.data.id))
                self.data.save()

    def add_duration(self, duration: int):
        if self.b_need_to_sum_duration is True:
            self.data.duration_sum += duration
            self.b_need_to_sum_duration = False
            self.dirty = True

    def getAggObject(self, niveau_agg: str):
        """get the aggregation depending on the level"""
        if niveau_agg == "H":
            return AggHour
        elif niveau_agg == "D":
            return AggDay
        elif niveau_agg == "M":
            return AggMonth
        elif niveau_agg == "Y":
            return AggYear
        elif niveau_agg == "A":
            return AggAll
        elif niveau_agg == "HT":
            return TmpAggHour
        elif niveau_agg == "DT":
            return TmpAggDay
        elif niveau_agg == "MT":
            return TmpAggMonth
        elif niveau_agg == "YT":
            return TmpAggYear
        elif niveau_agg == "AT":
            return TmpAggAll
        else:
            raise Exception("get_agg_object", "wrong niveau_agg: " + niveau_agg)

    @staticmethod
    def GetAggObj(niveau_agg: str):
        """get the aggregation depending on the level"""
        if niveau_agg == "H":
            return AggHour
        elif niveau_agg == "D":
            return AggDay
        elif niveau_agg == "M":
            return AggMonth
        elif niveau_agg == "Y":
            return AggYear
        elif niveau_agg == "A":
            return AggAll
        elif niveau_agg == "HT":
            return TmpAggHour
        elif niveau_agg == "DT":
            return TmpAggDay
        elif niveau_agg == "MT":
            return TmpAggMonth
        elif niveau_agg == "YT":
            return TmpAggYear
        elif niveau_agg == "AT":
            return TmpAggAll
        else:
            raise Exception("get_agg_object", "wrong niveau_agg: " + niveau_agg)

    def count(self, niveau_agg: str, poste_id: int = None, start_dat_mask: str = '') -> int:
        # return count of aggregations
        agg_obj = self.getAggObject(niveau_agg)
        if poste_id is None:
            if start_dat_mask == '':
                return agg_obj.objects.count()
            else:
                return agg_obj.objects.filter(start_dat__contains=start_dat_mask).count()
        if start_dat_mask == '':
            return agg_obj.objects.filter(poste_id=poste_id).count()
        return agg_obj.objects.filter(poste_id=poste_id).filter(start_dat__contains=start_dat_mask).count()

    def getLevel(self):
        lvl_mapping = {'H': 'hour', 'D': 'day', 'M': 'month', 'Y': 'year', 'A': 'all'}
        my_level = self.agg_niveau[0]
        if lvl_mapping.get(my_level) is None:
            return 'xxxxx'
        else:
            return lvl_mapping[my_level]

    def getLevelCode(self):
        return self.agg_niveau

    def __str__(self):
        """print myself"""
        return "AggMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id.id) + ", date: " + str(self.data.dat) + ", level: " + self.agg_niveau
