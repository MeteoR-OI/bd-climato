from app.tools.aggTools import calcAggDate, getAggDuration
from app.tools.modelTools import isTmpLevel, getAggTable, getAggHistoTable, getAggTableName
from django.db import connection
import datetime


class AggMeteor():
    """
        AggMeteor

        gere les objets Aggregation metier
        Act as a super Class for all aggregation objects

        o=AggMeteor(poste, obs_id, agg_level, dat)
            is_obs_date: is it a stop_dat
            b_need_to_sum_duration: please do not add duration (for omm updates)

        o.data -> Aggregation object (data, methods...)

    """

    def __init__(self, poste_id: int, obs_id: int, agg_niveau: str, start_dt_agg_utc: datetime, is_obs_date: bool = False, b_need_to_sum_duration: bool = False):
        """
            Init a new AggMeteor object

            poste: Poste object
            agg_niveau: 'H','D', 'M', 'Y', 'A', HT, DT, MT, YT, AT
            start_dt_agg_utc: start_date for the aggregation level, will be rounded
            is_obs_date: is it a stop_dat
            b_need_to_sum_duration: please do not add duration (for omm updates)
        """
        self.agg_niveau = agg_niveau
        self.is_tmp = isTmpLevel(agg_niveau)
        self.obs_id = obs_id
        self.b_need_to_sum_duration = b_need_to_sum_duration
        my_start_date = calcAggDate(agg_niveau, start_dt_agg_utc, 0, is_obs_date)
        # my_start_date = date_to_str(my_start_date)
        agg_object = getAggTable(agg_niveau)
        if agg_object.objects.filter(poste_id=poste_id).filter(start_dat=my_start_date).exists():
            self.data = agg_object.objects.filter(poste_id=poste_id).filter(start_dat=my_start_date).first()
        else:
            self.data = agg_object(poste_id=poste_id, start_dat=my_start_date, duration_sum=0, duration_max=0, j={})
            self.data.duration_max = getAggDuration(agg_niveau, my_start_date)

        # histo data only on hourly/daily agregations
        if self.agg_niveau[0] == 'A' or self.agg_niveau[0] == 'Y' or self.agg_niveau[0] == 'M':
            self.j_ori = {}
            self.duration_ori = 0
        else:
            # save original values allowing us to generate agg_histo
            self.j_ori = self.data.j.copy()
            self.duration_ori = self.data.duration_sum

    def save(self):
        """ save Poste and Exclusions """
        dirty_found = False
        delta_j = {}
        if self.data.j != {}:
            for k in self.data.j.keys():
                if self.j_ori.get(k) is None or self.j_ori.get(k) != self.data.j.get(k):
                    delta_j[k] = self.data.j.get(k)
                    dirty_found = True
        if self.j_ori != {}:
            for k in self.j_ori.keys():
                if self.data.j.get(k) is None:
                    delta_j[k] = self.j.get(k)
                    dirty_found = True

        if self.data.duration_sum != self.duration_ori:
            dirty_found = True

        if dirty_found is True:
            if self.data.duration_sum > self.data.duration_max:
                raise Exception("duration overflow for agg_" + self.agg_niveau + ', id: ' + str(self.data.id))
            self.data.save()

            # histo data only on hourly/daily agregations
            if self.agg_niveau[0] == 'A' or self.agg_niveau[0] == 'Y' or self.agg_niveau[0] == 'M':
                return

            agg_histo_table = getAggHistoTable(self.agg_niveau)
            if agg_histo_table.objects.filter(obs_id=self.obs_id).filter(agg_id=self.data.id).filter(agg_level=self.agg_niveau).exists():
                my_agg_histo = agg_histo_table.objects.filter(obs_id=self.obs_id, agg_id=self.data.id, agg_level=self.agg_niveau).first()
                my_agg_histo.j = delta_j
                my_agg_histo.delta_duration = self.data.duration_sum - self.duration_ori
            else:
                my_agg_histo = agg_histo_table(obs_id=self.obs_id, agg_id=self.data.id, agg_level=self.agg_niveau, delta_duration=(self.data.duration_sum - self.duration_ori), j=delta_j)

            my_agg_histo.save()
            # refresh copy data, just if this instance of object is re-used later
            self.j_ori = self.data.j.copy()
            self.duration_ori = self.data.duration_sum

    def add_duration(self, duration: int):
        if self.b_need_to_sum_duration is True:
            self.data.duration_sum += duration
            self.b_need_to_sum_duration = False

    def count(self, niveau_agg: str, poste_id: int = None, start_dat_mask: str = '') -> int:
        # return count of aggregations
        agg_obj = getAggTable(niveau_agg)
        if poste_id is None:
            if start_dat_mask == '':
                return agg_obj.objects.count()
            else:
                return agg_obj.objects.filter(start_dat__contains=start_dat_mask).count()
        if start_dat_mask == '':
            return agg_obj.objects.filter(poste_id=poste_id).count()
        return agg_obj.objects.filter(poste_id=poste_id).filter(start_dat__contains=start_dat_mask).count()

    def getAggUpdates(self, field_name: str = None):
        agg_table_name = getAggTableName(self.agg_niveau)
        if field_name is None:
            sql = "select id, obs_id, agg_id, agg_level, delta_duration, j from " + agg_table_name + " where id = " + str(self.data.id)
        else:
            sql = "select id, obs_id, agg_id, agg_level, delta_duration, j['" + field_name + "']"
            sql += " from " + agg_table_name + " where id = " + str(self.data.id) + " and j['" + field_name + "'] is not null"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    # def getLevel(self):
    #     lvl_mapping = {'H': 'hour', 'D': 'day', 'M': 'month', 'Y': 'year', 'A': 'all'}
    #     my_level = self.agg_niveau[0]
    #     if lvl_mapping.get(my_level) is None:
    #         return 'xxxxx'
    #     else:
    #         return lvl_mapping[my_level]

    def getLevelCode(self):
        return self.agg_niveau

    def getLevel(self):
        lvl_mapping = {'H': 'hour', 'D': 'day', 'M': 'month', 'Y': 'year', 'A': 'all'}
        my_level = self.agg_niveau[0]
        if lvl_mapping.get(my_level) is None:
            return 'xxxxx'

    def __str__(self):
        """print myself"""
        return "AggMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id) + ", date: " + str(self.data.dat) + ", level: " + self.agg_niveau
