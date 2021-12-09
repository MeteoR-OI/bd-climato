# from app.models import AggHisto, TmpAggHisto
from app.tools.modelTools import getAggHistoTableWithBool, getObservationTable
from django.db import connection
import datetime
from app.tools.aggTools import calcAggDate


class ObsMeteor():
    """
        ObsMeteor

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    def __init__(self, poste_id: int, stop_dt_utc: datetime, is_tmp: bool = None):
        """Init a new ObsMeteor object"""
        # todo: block if my_datetime_utc > previous dat+duration
        self.is_tmp = is_tmp
        myObsObj = getObservationTable(is_tmp)
        if myObsObj.objects.filter(poste_id=poste_id).filter(stop_dat=stop_dt_utc).exists():
            self.data = myObsObj.objects.filter(poste_id=poste_id).filter(stop_dat=stop_dt_utc).first()
        else:
            agg_start_dat = calcAggDate('H', stop_dt_utc, 0, True)
            self.data = myObsObj(poste_id=poste_id, stop_dat=stop_dt_utc, duration=0, agg_start_dat=agg_start_dat, j={}, j_agg={})

    def save(self):
        """ save Poste and Exclusions """
        # we only save if there is some data
        if self.data.j != {} or self.data.j_agg != {}:
            # self.data.agg_start_dat = calcAggDate('H', self.data.stop_dat, 0, True)
            self.data.save()

    def delete(self):
        # delete cascade linked agg_histo rows
        agg_histo_table = getAggHistoTableWithBool(self.is_tmp)
        agg_histo_table.objects.filter(obs_id=self.data.id).delete()
        self.data.delete()

    def count(self, poste_id: int = None, stop_dat_mask: str = '', is_tmp: bool = None) -> int:
        # return count of aggregations
        myObsObj = self.getObsObject(is_tmp)
        if poste_id is None:
            return myObsObj.objects.filter(stop_dat__contains=stop_dat_mask).count()
        return myObsObj.objects.filter(poste_id=poste_id).filter(stop_dat__contains=stop_dat_mask).count()

    def getAggUpdates(self, field_name: str = None):
        agg_histo_table_name = 'agg_histo'
        if self.is_tmp is True:
            agg_histo_table_name = 'tmp_agg_histo'
        if field_name is None:
            sql = '''
                select h.id as id, h.obs_id as obsId, o.stop_dat as stopDate, h.agg_id as aggId, h.agg_level as aggLevel, h.delta_duration as duration, h.j as j
                from ''' + agg_histo_table_name + ''' h join obs o
                    on.id = h.obs_id
                where obs_id = " + str(self.data.id)
            '''
        else:
            sql = '''
                select id, obs_id, agg_id, agg_level, delta_duration, j['" + field_name + "']"
                from " + agg_histo_table_name + " where obs_id = " + str(self.data.id) + " and j['" + field_name + "'] is not null
            '''
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id) + ", fin periode: " + str(self.data.dat)
