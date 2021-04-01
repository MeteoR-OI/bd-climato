from app.classes.repository.posteMeteor import PosteMeteor
from app.models import Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Agg_todo
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.metier.typeInstrumentAll import TypeInstrumentAll
from app.tools.jsonPlus import JsonPlus
from app.tools.jsonValidator import checkJson
from django.db import transaction
import datetime
import json


class Calculus():

    def delete_obs_agg(self):
        """clean_up all our tables"""
        Observation.objects.all().delete()
        Agg_hour.objects.all().delete()
        Agg_day.objects.all().delete()
        Agg_month.objects.all().delete()
        Agg_year.objects.all().delete()
        Agg_global.objects.all().delete()
        Agg_todo.objects.all().delete()

    def run(self, m_j: json, trace_flag: bool, delete_flag: bool = True) -> json:
        """
            run
            old fashion calculus. will be deleted in future
            calculus v1
        """
        all_instr = TypeInstrumentAll()
        ret = []
        if delete_flag:
            self.delete_obs_agg()

        # validate our json
        check_result = checkJson(m_j)
        if check_result is not None:
            raise Exception('doCalculus', check_result)

        idx = 0
        while idx < m_j['data'].__len__():
            if idx == 286:
                idx = 286
            pid = PosteMeteor.getPosteIdByMeteor(m_j['meteor'])
            if pid is None:
                raise Exception('doCalculus', 'unknown code meteor: ' + m_j['meteor'])
            # we use the stop_dat of our measure json as the start date for our processing
            m_stop_date_agg_start_date = m_j['data'][idx]['current']['stop_dat']
            self.my_poste = PosteMetier(pid, m_stop_date_agg_start_date)
            self.my_obs = self.my_poste.observation(m_stop_date_agg_start_date)
            # load duration and stop_dat if not already loaded
            if self.my_obs.data.duration == 0:
                self.my_obs.data.duration = m_j['data'][idx]['current']['duration']
                measure_duration = datetime.timedelta(minutes=int(self.my_obs.data.duration))
                self.my_obs.data.start_dat = self.my_obs.data.stop_dat - measure_duration
            # the stop_dat of the measure is used as the start_dat in all agregations
            self.my_agg_array = self.my_poste.aggregations(m_stop_date_agg_start_date, True)

            # call the method to update obs, and return delta_val
            all_instr.process_json(self.my_poste, m_j, idx, self.my_obs, self.my_agg_array, trace_flag)

            # save our data
            self.my_obs.save()
            i = 0
            while i < self.my_agg_array.__len__():
                # self.my_agg_array[i].data.j['dv'] = {}
                self.my_agg_array[i].save()
                i += 1
            if trace_flag:
                if idx == 0:
                    helper = ' - cut and paste this data into https://codebeautify.org/jsonviewer'
                else:
                    helper = ''
                ret.append({
                    'info': 'idx=' + str(idx) + helper,
                    'start_dat': m_j['data'][idx]['current']['start_dat'],
                    'stop_dat': m_j['data'][idx]['current']['stop_dat'],
                    'observation': JsonPlus().loads(JsonPlus().dumps(self.my_obs.data.j)),
                    'agg_hour': {'start_dat': self.my_agg_array[0].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.my_agg_array[0].data.j))},
                    'agg_day': {'start_dat': self.my_agg_array[1].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.my_agg_array[1].data.j))},
                    'agg_month': {'start_dat': self.my_agg_array[2].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.my_agg_array[2].data.j))},
                    'agg_year': {'start_dat': self.my_agg_array[3].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.my_agg_array[3].data.j))},
                    'agg_all': {'start_dat': self.my_agg_array[4].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.my_agg_array[4].data.j))},
                    'agg_day before': {'start_dat': self.my_agg_array[5].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.my_agg_array[5].data.j))},
                    'agg_day after': {'start_dat': self.my_agg_array[6].data.start_dat, 'j': JsonPlus().loads(JsonPlus().dumps(self.my_agg_array[6].data.j))},
                    }
                )
            else:
                ret = []
            print('calc ' + str(idx) + ' done')
            idx += 1

        return ret

    def loadJson(self, m_j: json, trace_flag: bool = False, delete_flag: bool = False):
        """
            processJson

            calulus v2, load json in the obs & agg_toto tables
        """
        if delete_flag:
            self.delete_obs_agg()

        self.loadJson_ttx(m_j, trace_flag)

    @transaction.atomic
    def loadJson_ttx(self, m_j: json, trace_flag: bool = False):
        """
            processJson

            calulus v2, load json in the obs & agg_toto tables
        """
        all_instr = TypeInstrumentAll()
        ret = []

        # validate our json
        check_result = checkJson(m_j)
        if check_result is not None:
            raise Exception('calculus::processJson', check_result)

        measure_idx = 0
        debut_process = datetime.datetime.now()
        while measure_idx < m_j['data'].__len__():
            # print('processing idx: ' + str(measure_idx))
            # we use the stop_dat of our measure json as the start date for our processing
            m_stop_date_agg_start_date = m_j['data'][measure_idx]['current']['stop_dat']
            poste_metier = PosteMetier(m_j['poste_id'], m_stop_date_agg_start_date)
            obs_meteor = poste_metier.observation(m_stop_date_agg_start_date)
            if m_j['data'][measure_idx].__contains__('aggregations'):
                obs_meteor.data.j_agg = m_j['data'][measure_idx]['aggregations']

            # load duration and stop_dat if not already loaded
            if obs_meteor.data.duration == 0:
                obs_meteor.data.duration = m_j['data'][measure_idx]['current']['duration']
                measure_duration = datetime.timedelta(minutes=int(obs_meteor.data.duration))
                obs_meteor.data.start_dat = obs_meteor.data.stop_dat - measure_duration

            delta_values = {"maxminFix": []}

            # for all type_instruments
            for an_intrument in all_instr.all_instruments:
                an_intrument['object'].loadJson(
                    poste_metier,
                    m_j,
                    measure_idx,
                    obs_meteor,
                    delta_values,
                    trace_flag,
                )

            # save our new data
            obs_meteor.save()
            a_todo = AggTodoMeteor(obs_meteor.data.id)
            a_todo.data.j_dv.append(delta_values)
            a_todo.save()

            if trace_flag:
                if measure_idx == 0:
                    helper = ' - cut and paste this data into https://codebeautify.org/jsonviewer'
                else:
                    helper = ''
                ret.append({
                    'info': 'idx=' + str(measure_idx) + helper,
                    'start_dat': m_j['data'][measure_idx]['current']['start_dat'],
                    'stop_dat': m_j['data'][measure_idx]['current']['stop_dat'],
                    'obs data': JsonPlus().loads(JsonPlus().dumps(self.my_obs.data.j)),
                    'obs aggregations': JsonPlus().loads(JsonPlus().dumps(self.my_obs.data.j_agg)),
                    'agg_todo dv': JsonPlus().loads(JsonPlus().dumps(a_todo.j_dv)),
                })
            else:
                ret = []
            measure_idx += 1

        print('time to Exec for ' + str(m_j['data'].__len__()) + ' measures: ' + str(datetime.datetime.now() - debut_process))
        print('                    1 measure: ' + str((datetime.datetime.now() - debut_process)/m_j['data'].__len__()))

        return ret
