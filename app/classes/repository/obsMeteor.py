# check __reverse_delta_values (j_xtreme)
#
from app.models import Observation, AggHisto
from django.db import connection
import datetime
import json
from app.tools.aggTools import calcAggDate
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.repository.aggTodoMeteor import AggTodoMeteor


class ObsMeteor():
    """
        ObsMeteor

        gere les objets Observation metier

        o=Meteor(poste, dat)
        o.data -> Observation object (data, methods...)

    """

    def __init__(self, poste_id: int, stop_dt_utc: datetime, json_type: str = "?"):
        """Init a new ObsMeteor object"""
        # todo: block if my_datetime_utc > previous dat+duration
        self.is_tmp = False
        if Observation.objects.filter(poste_id=poste_id).filter(stop_dat=stop_dt_utc).exists():
            self.data = Observation.objects.filter(poste_id=poste_id).filter(stop_dat=stop_dt_utc).first()
        else:
            agg_start_dat = calcAggDate('H', stop_dt_utc, 0, True)
            self.data = Observation(poste_id=poste_id, stop_dat=stop_dt_utc, duration=0, agg_start_dat=agg_start_dat, j=[], j_xtreme=[], filename='???')
            if json_type != "?":
                self.data.json_type = json_type

    def save(self):
        """ save Poste and Exclusions """
        # we only save if there is some data
        if self.data.j[0].get('json_type') is not None:
            self.data.json_type = self.data.j[0]['json_type']
        if self.data.json_type not in ["O", "C", "H", "D", "M", "Y", "A"]:
            raise Exception('wrong json_type')
        if self.data.j.__len__() > 0 or self.data.j_xtreme.__len__() > 0:
            self.data.save()

    def delete(self):
        # delete cascade linked agg_histo rows
        AggHisto.objects.filter(obs_id=self.data.id).delete()

        # generate a todo with negative values
        a_todo = AggTodoMeteor(self.data.id, self.is_tmp)
        delta_values = self.__reverse_delta_values(self.data.j_dv, self.data.id)
        a_todo.data.j_dv = delta_values
        a_todo.data.j_xtreme = self.data.j_xtreme
        a_todo.data.priority = 0
        a_todo.save()

        # delete the obs
        self.data.delete()

    def __reverse_delta_values(self, delta_values: json, obs_id: int):
        # reverse delta_values to delete an obs
        inverse_values = {}
        for a_kv in delta_values.items():
            if str(a_kv[0]).endswith('_s') or str(a_kv[0]).endswith('_sum') or str(a_kv[0]).endswith('duration'):
                inverse_values[a_kv[0]] = a_kv[1] * -1
                continue
            if str(a_kv[0]).endswith('_min'):
                inverse_values['maxminFix'].append({
                    'ope': 'remove',
                    'type': 'min',
                    'value': a_kv[1],
                    'date': delta_values[str(a_kv[0]) + '_time'],
                })
                continue
            if str(a_kv[0]).endswith('_max'):
                inverse_values['maxminFix'].append({
                    'ope': 'remove',
                    'type': 'max',
                    'value': a_kv[1],
                    'date': delta_values[str(a_kv[0]) + '_time'],
                })
                continue
            if str(a_kv[0]).endswith('_time'):
                continue
            IncidentMeteor.new(
                'obs delete',
                'error',
                'key ' + str(a_kv[0]) + ' not processed',
                {
                    'value': str(a_kv[1]),
                    'obs_id': obs_id,
                })

        return inverse_values

    def count(self, poste_id: int = None, stop_dat_mask: str = '', is_tmp: bool = None) -> int:
        # return count of aggregations
        myObsObj = self.getObsObject(is_tmp)
        if poste_id is None:
            return myObsObj.objects.filter(stop_dat__contains=stop_dat_mask).count()
        return myObsObj.objects.filter(poste_id=poste_id).filter(stop_dat__contains=stop_dat_mask).count()

    def getAggUpdates(self, field_name: str = None):
        if field_name is None:
            sql = '''
                select h.id as id, h.obs_id as obsId, o.stop_dat as stopDate, h.agg_id as aggId, h.agg_level as aggLevel, h.delta_duration as duration, h.j as j
                from agg_histo h join obs o
                    on.id = h.obs_id
                where obs_id = " + str(self.data.id)
            '''
        else:
            sql = '''
                select id, obs_id, agg_id, agg_level, delta_duration, j['" + field_name + "']"
                from agg_histo where obs_id = " + str(self.data.id) + " and j['" + field_name + "'] is not null
            '''
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def __str__(self):
        """print myself"""
        return "ObsMeteor id: " + str(self.data.id) + ", poste_id: " + str(self.data.poste_id) + ", fin periode: " + str(self.data.dat)
