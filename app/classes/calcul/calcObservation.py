from app.classes.calcul.calculus import Calculus
from app.classes.metier.posteMetier import PosteMetier
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.aggTools import calcAggDate
from app.tools.jsonPlus import JsonPlus
from app.tools.jsonValidator import checkJson
from django.db import transaction
import datetime
import json


class CalcObs(Calculus):
    def loadJson(self, m_j: json, trace_flag: bool = False, delete_flag: bool = False):
        """
            processJson

            calulus v2, load json in the obs & agg_toto tables
        """
        if delete_flag:
            # delete is not part of the transaction
            self.delete_obs_agg()

        return self.loadJson_ttx(m_j, trace_flag)

    @transaction.atomic
    def loadJson_ttx(self, m_j: json, trace_flag: bool = False):
        """
            processJson

            calulus v2, load json in the obs & agg_toto tables
        """
        all_instr = AllTypeInstruments()
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
                obs_meteor.data.agg_start_dat = calcAggDate('H', obs_meteor.data.stop_dat, True)

            delta_values = {"maxminFix": []}

            # for all type_instruments
            for an_intrument in all_instr.get_all_instruments():
                # for all measures
                for my_measure in an_intrument['object'].get_all_measures():
                    # find the calculus object for my_mesure
                    for a_calculus in self.all_calculus:
                        if a_calculus['agg'] == my_measure['agg']:
                            if a_calculus['calc_obs'] is not None:
                                # load our json in obs row
                                a_calculus['calc_obs'].loadInObs(poste_metier, my_measure, m_j, measure_idx, obs_meteor, delta_values, trace_flag)
                            break

            # save our new data
            obs_meteor.save()
            a_todo = AggTodoMeteor(obs_meteor.data.id)
            a_todo.data.j_dv.append(delta_values)
            if measure_idx < m_j['data'].__len__() <= 1:
                a_todo.data.priority = 0
            a_todo.save()

            j_trace = {}
            if measure_idx == 0:
                j_trace['total_exec'] = str(datetime.datetime.now() - debut_process)
                j_trace['item_processed'] = str(m_j['data'].__len__())
                j_trace['one_exec'] = str((datetime.datetime.now() - debut_process)/m_j['data'].__len__())

            if trace_flag:
                j_trace['info'] = 'idx=' + str(measure_idx)
                j_trace['url'] = '** cut and paste this data into https://codebeautify.org/jsonviewer **'
                j_trace['total_exec'] = str(datetime.datetime.now() - debut_process)
                j_trace['item_processed'] = str(m_j['data'].__len__())
                j_trace['one_exec'] = str((datetime.datetime.now() - debut_process)/m_j['data'].__len__())
                j_trace['start_dat'] = m_j['data'][measure_idx]['current']['start_dat']
                j_trace['stop_dat'] = m_j['data'][measure_idx]['current']['stop_dat']
                j_trace['obs data'] = JsonPlus().loads(JsonPlus().dumps(self.my_obs.data.j))
                j_trace['obs aggregations'] = JsonPlus().loads(JsonPlus().dumps(self.my_obs.data.j_agg))
                j_trace['agg_todo dv'] = JsonPlus().loads(JsonPlus().dumps(a_todo.j_dv))

            if j_trace != {}:
                ret.append(j_trace)

            measure_idx += 1
        return ret
