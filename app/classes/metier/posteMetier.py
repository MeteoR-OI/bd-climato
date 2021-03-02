from app.tools.climConstant import AggLevel
import datetime
import json
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.excluMeteor import ExcluMeteor
from app.classes.repository.posteMeteor import PosteMeteor
from app.tools.aggTools import calcAggDate


class PosteMetier(PosteMeteor):
    """
        PosteMeteor

        Add obs/agg/exclu info to PosteMeteor
    """

    def __init__(self, poste_id: int, start_date: datetime = datetime.datetime.now(datetime.timezone.utc), end_date: datetime = datetime.datetime(2100, 12, 21, 0, 0, 0, 0, datetime.timezone.utc)):
        """ load our instance from db, load exclusions at date_histo """
        super().__init__(poste_id)
        self.exclus = ExcluMeteor.getAllForAPoste(self.data.id, start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date

    def exclusion(self, type_intrument_id) -> json:
        """ retourne la premiere exclusion active pour le type instrument """
        for anExclu in self.exclus:
            if anExclu['type_instrument'] == type_intrument_id:
                return anExclu['value']
        return None

    def getAllForAPoste(self, start_date: datetime = datetime.datetime.now(datetime.timezone.utc), end_date: datetime = datetime.datetime(2100, 12, 21, 0, 0, 0, 0, datetime.timezone.utc)) -> json:
        return ExcluMeteor.getAllForAPoste(self.data.id, start_date, end_date)

    def aggregations(self, my_datetime_utc: datetime):
        """
        get_agg

        my_datetime_utc: date en UTC.

        return an array of AggMeteor to be used by our process_xxx methods
            [0] -> Agg_hour
            [1] -> Agg_day
            [2] -> Agg_month
            [3] -> Agg-year
            [4] -> Agg_all
            [5] -> Agg_day for day - 1
            [6] -> Agg_day for day + 1

        create them if needed
        """
        try:
            ret = []
            # push aggregations of all levels for the given date
            for agg_niveau in AggLevel:
                tmp_dt = calcAggDate(agg_niveau, my_datetime_utc)
                ret.append(AggMeteor(self.data.id, agg_niveau, tmp_dt))

            # get aggregation of day - 1 for measures that will aggregate yesteray
            tmp_dt = calcAggDate('D', my_datetime_utc, -1)
            ret.append(AggMeteor(self.data.id, 'D', tmp_dt))

            # get aggregation of day + 1 for measures that will aggregate the day after
            tmp_dt = calcAggDate('D', my_datetime_utc, 1)
            ret.append(AggMeteor(self.data.id, 'D', tmp_dt))

            return ret
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def observation(self, my_datetime_utc: datetime) -> ObsMeteor:
        """get or create an observation at a given datetime"""
        try:
            return ObsMeteor(self.data.id, my_datetime_utc)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        super()
        return "....PosteXMeteor, #exclu: " + str(self.exclus.__len__())
