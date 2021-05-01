from app.classes.calcul.allCalculus import AllCalculus
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.jsonPlus import JsonPlus
from app.tools.jsonValidator import checkJson
from app.tools.myTools import CopyJson, LogException
from app.tools.telemetry import Telemetry
from django.db import transaction
import datetime
import json


class CalcObs(AllCalculus):
    """
        Control all the processing of a json data, with our Observation table
    """
    def __init__(self):
        self.tracer = Telemetry.Start("calculus", __name__)

    def loadJson(self, json_file_data_array: json, trace_flag: bool = False, delete_flag: bool = False, is_tmp: bool = None, use_validation: bool = False) -> json:
        """
            processJson

            calulus v2, load json in the obs & agg_toto tables
        """
        if delete_flag:
            # delete is not part of the transaction
            self.delete_obs_agg(is_tmp)

        with self.tracer.start_as_current_span('Obs') as my_span:
            ret = {}
            try:
                ret = self._loadJson_array_ttx(json_file_data_array, trace_flag, is_tmp, use_validation)
                my_span.set_attribute("items_processed", ret[ret.__len__() - 1].get('item_processed'))

            except Exception as exc:
                LogException(exc, my_span)
                ret.append({"Exception": str(exc), "args": str(exc.args)})

            finally:
                return ret

    @transaction.atomic
    def _loadJson_array_ttx(self, json_file_data_array: json, trace_flag: bool = False, is_tmp: bool = None, use_validation: bool = False) -> json:
        debut_full_process = datetime.datetime.now()
        ret_data = []
        item_processed = 0

        # validate our json
        check_result = checkJson(json_file_data_array)
        if check_result is not None:
            raise Exception('calculus::processJson', check_result)

        idx = 0
        while idx < json_file_data_array.__len__():
            json_file_data = json_file_data_array[idx]
            item_processed += json_file_data['data'].__len__()
            ret = self._loadJson(json_file_data, trace_flag, is_tmp, use_validation)
            if trace_flag is True:
                ret_data.append({"item": idx, "ret": ret})
            idx += 1

        ret_data.append({
            'total_exec': str(datetime.datetime.now() - debut_full_process),
            'item_processed': item_processed,
            'one_exec': str((datetime.datetime.now() - debut_full_process)/item_processed)
        })
        return ret_data

    def _loadJson(self, json_file_data: json, trace_flag: bool = False, is_tmp: bool = False, use_validation: bool = False) -> json:
        """
            processJson

            calulus v2, load json in the obs & agg_toto tables
        """
        all_instr = AllTypeInstruments()
        ret = []

        measure_idx = 0
        debut_process = datetime.datetime.now()
        my_span = self.tracer.get_current_span()

        while measure_idx < json_file_data['data'].__len__():
            # print('processing idx: ' + str(measure_idx))
            # we use the stop_dat of our measure json as the start date for our processing
            m_stop_date_agg_start_date = json_file_data['data'][measure_idx]['stop_dat']
            m_duration = json_file_data['data'][measure_idx]['current']['duration']
            poste_metier = PosteMetier(json_file_data['poste_id'], m_stop_date_agg_start_date)
            if measure_idx == 0:
                my_span.set_attribute("poste_id", str(poste_metier.data.id))
                my_span.set_attribute("stopDat", str(m_stop_date_agg_start_date))
            try:
                poste_metier.lock()
                obs_meteor = poste_metier.observation(m_stop_date_agg_start_date, is_tmp)
                if obs_meteor.data.id is not None and json_file_data['data'][measure_idx].__contains__('update_me') is False:
                    print('CalcObs: skipping data[' + str(measure_idx) + '], stop_dat: ' + str(m_stop_date_agg_start_date) + ' already loaded')
                    continue
                if use_validation is True:
                    tmp_agg = []
                    if json_file_data['data'][measure_idx].__contains__('aggregations'):
                        CopyJson(json_file_data['data'][measure_idx]['aggregations'], tmp_agg)
                    if json_file_data['data'][measure_idx].__contains__('validation'):
                        CopyJson(json_file_data['data'][measure_idx]['validation'], tmp_agg)
                    obs_meteor.data.j_agg = tmp_agg
                    if tmp_agg.__len__() == 0:
                        print('CalcObs: skipping data[' + str(measure_idx) + '], stop_dat: ' + str(m_stop_date_agg_start_date))
                        continue
                    json_file_data['data'][measure_idx]['current'] = {
                        "duration": m_duration
                    }
                else:
                    if json_file_data['data'][measure_idx].__contains__('aggregations'):
                        obs_meteor.data.j_agg = json_file_data['data'][measure_idx]['aggregations']

                # load duration and stop_dat if not already loaded
                if obs_meteor.data.duration == 0:
                    obs_meteor.data.duration = json_file_data['data'][measure_idx]['current']['duration']

                delta_values = {"maxminFix": [], "duration": m_duration}

                # for all type_instruments
                for an_intrument in all_instr.get_all_instruments():
                    # for all measures
                    for my_measure in an_intrument['object'].get_all_measures():
                        # find the calculus object for my_mesure
                        for a_calculus in self.all_calculus:
                            if a_calculus['agg'] == my_measure['agg']:
                                if a_calculus['calc_obs'] is not None:
                                    # load our json in obs row
                                    a_calculus['calc_obs'].loadInObs(poste_metier, my_measure, json_file_data, measure_idx, obs_meteor, delta_values, trace_flag)
                                break

                # save our new data
                obs_meteor.save()
                a_todo = AggTodoMeteor(obs_meteor.data.id, is_tmp)
                a_todo.data.j_dv.append(delta_values)
                if measure_idx < json_file_data['data'].__len__() <= 1:
                    a_todo.data.priority = 0
                if obs_meteor.data.id is not None:
                    a_todo.save()

                j_trace = {}

                if trace_flag:
                    j_trace['info'] = 'idx=' + str(measure_idx)
                    j_trace['total_exec'] = str(datetime.datetime.now() - debut_process)
                    j_trace['item_processed'] = str(json_file_data['data'].__len__())
                    j_trace['one_exec'] = str((datetime.datetime.now() - debut_process)/json_file_data['data'].__len__())
                    # j_trace['start_dat'] = json_file_data['data'][measure_idx]['current']['start_dat']
                    j_trace['stop_dat'] = json_file_data['data'][measure_idx]['stop_dat']
                    j_trace['obs data'] = JsonPlus().loads(JsonPlus().dumps(obs_meteor.data.j))
                    j_trace['obs aggregations'] = JsonPlus().loads(JsonPlus().dumps(obs_meteor.data.j_agg))
                    j_trace['agg_todo dv'] = JsonPlus().loads(JsonPlus().dumps(a_todo.data.j_dv)) if not (a_todo.data.id is None) else '{}'

                if j_trace != {}:
                    ret.append(j_trace)

            finally:
                measure_idx += 1
                poste_metier.unlock()

        return ret
