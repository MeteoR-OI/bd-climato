from app.classes.calcul.observation.processJsonData import ProcessJsonData
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.workers.svcAggregate import SvcAggregate
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.jsonPlus import JsonPlus
from app.tools.jsonValidator import checkJson
from app.tools.refManager import RefManager
import app.tools.myTools as t
from app.tools.telemetry import Telemetry
from django.db import transaction
from django.conf import settings
import threading
import datetime
import json
import os


class IsErrorClass():
    isError = False

    def get(self):
        isErrorTmp = self.isError
        self.isError = False
        return isErrorTmp

    def set(self, value: bool = True):
        self.isError = value


class CalcObs():
    """
    Control all the processing of a json data, with our Observation table
    """

    def __init__(self):
        self.tracer = Telemetry.Start("calculus")
        CalcObs.lock = threading.Lock()
        self.processJsonData = ProcessJsonData()

    @staticmethod
    def GetInstance():
        if hasattr(CalcObs, "MyInstance") is False:
            CalcObs.MyInstance = CalcObs()
        return CalcObs.MyInstance

    def LoadJsonFromSvc(self, data: json):
        """
        common params:
                "json: json_data pre loaded
                "is_tmp": is_tmp,
                "validation": use_validation
        when called from command line:

        data["param]:
                "json": my_json     # mandatory !

        when called from autoLoad
                "base_dir": my_json,
        """

        # Load params
        self.stopRequested = False
        if data is None or data.get("param") is None or data["param"] == {}:
            t.LogError("wrong data")
            return
        params = data["param"]

        # stop request
        if params.get("StopMe") is True:
            self.stopRequested = True
            return

        # load parameters (global trace, then params.trace_flag)
        if RefManager.GetInstance().GetRef("loadObs_trace_flag") is None:
            trace_flag = False
        else:
            trace_flag = RefManager.GetInstance().GetRef("loadObs_trace_flag")
        if params.get("trace_flag") is not None:
            trace_flag = params["trace_flag"]

        # load other parameters
        is_tmp = use_validation = False
        ret = []
        if params.get("is_tmp") is not None:
            is_tmp = params["is_tmp"]
        if params.get("validation") is not None:
            use_validation = params["validation"]

        # load the content of files on the server
        isError = IsErrorClass()
        for j_data in self._getJsonData(params, isError):
            try:
                if CalcObs.lock.acquire(True, 500) is False:
                    t.logWarning("lock time-out !")
                    return
                try:
                    func_ret = self._loadJsonArrayInObs(j_data["j"], trace_flag, is_tmp, use_validation, j_data.get("f"))
                finally:
                    CalcObs.lock.release()

                ret.append(func_ret[0])

            except Exception as inst:
                isError.set(True)
                t.LogCritical(inst)

        # activate the computation of aggregations
        SvcAggregate.runMe({"is_tmp": is_tmp, "trace_flag": trace_flag})
        return ret

    # ----------------
    # private methods
    # ----------------
    @transaction.atomic
    def _loadJsonArrayInObs(
        self,
        json_data_array: json,
        trace_flag: bool = False,
        is_tmp: bool = None,
        use_validation: bool = False,
        filename: str = "????",
    ) -> json:
        """
            _loadJsonArrayInObs

            Load data from a Json file
        """
        debut_full_process = datetime.datetime.now()
        ret_data = []
        all_item_processed = 0
        idx = 0
        meteor = "???"

        with self.tracer.start_as_current_span("Load Obs", trace_flag) as my_span:
            # check data validity in a try/catch protection
            try:
                # validate our json
                meteor = str(json_data_array[0].get("meteor"))
                check_result = checkJson(json_data_array)

            except Exception as exc:
                if is_tmp is False:
                    IncidentMeteor.new("check_data", "Exception", str(exc), {})
                my_span.record_exception(exc)
                raise exc

            if check_result is not None:
                if is_tmp is False:
                    IncidentMeteor.new("check_data", "Error", "invalid data", {'meteor': meteor, 'filename': filename, 'check': check_result})
                raise Exception("Meteor: " + meteor + ", filenme: " + filename + str(check_result))

            # now load our data in obs table
            try:
                while idx < json_data_array.__len__():
                    try:
                        json_file_data = json_data_array[idx]
                        all_item_processed += json_file_data["data"].__len__()

                        if idx == 0:
                            my_span.set_attribute("meteor", meteor)
                            my_span.set_attribute("filename", filename)

                        self._loadJsonItemInObs(json_file_data, trace_flag, is_tmp, use_validation, filename, idx)

                    finally:
                        idx += 1

                global_duration = datetime.datetime.now() - debut_full_process
                dur_millisec = round(global_duration.total_seconds() * 1000)
                one_exec = round(dur_millisec / all_item_processed)
                ret_data.append(
                    {
                        "total_exec": dur_millisec,
                        "item_processed": all_item_processed,
                        "one_exec": one_exec,
                    }
                )
                t.logInfo(
                    "Json file loaded",
                    my_span,
                    {"filename": filename, "timeExec": dur_millisec, "avgItemExec": one_exec, "items": all_item_processed, "meteor": meteor},
                )

            except Exception as exc:
                if is_tmp is False:
                    IncidentMeteor.new("load obs", "Exception", str(exc), {})
                my_span.record_exception(exc)
                raise exc

            finally:
                self.tracer.end_span()

        return ret_data

    def _loadJsonItemInObs(
        self,
        json_file_data: json,
        trace_flag: bool = False,
        is_tmp: bool = False,
        use_validation: bool = False,
        filename: str = '???',
        outside_idx: int = 0,
    ) -> json:
        """
            _loadJsonItemInObs

            Load measures values from <data>
        """
        all_instr = AllTypeInstruments()

        json_data_idx = 0
        # debut_process = datetime.datetime.now()
        my_span = self.tracer.get_current_or_new_span("Load Obs", trace_flag)

        while json_data_idx < json_file_data["data"].__len__():
            one_data_item = json_file_data["data"][json_data_idx]

            # we use the stop_dat of our measure json as the start date for our processing
            m_stop_date_agg_start_date = one_data_item["stop_dat"]

            # load a null duration when not specified, or in validation mode
            if one_data_item.get("current") is None or one_data_item["current"].get("duration") is None or use_validation is True:
                one_data_item["current"] = {"duration": 0}

            m_duration = one_data_item["current"]["duration"]
            poste_metier = PosteMetier(json_file_data["poste_id"], m_stop_date_agg_start_date)

            if json_data_idx == 0:
                my_span.set_attribute("posteId", poste_metier.data.id)
                my_span.set_attribute("stopDat", str(m_stop_date_agg_start_date))
                if is_tmp is True:
                    my_span.set_attribute("isTmp", is_tmp)

            try:
                poste_metier.lock()
                obs_meteor = poste_metier.observation(m_stop_date_agg_start_date, is_tmp)
                obs_meteor.data.filename = filename
                if obs_meteor.data.id is not None:
                    # obs_meteor already exist
                    if one_data_item.__contains__("force_replace") is True:
                        # basic asumption
                        if obs_meteor.data.j_agg.__len__() != 1 or obs_meteor.data.j.__len__() != 1:
                            raise Exception('Non-processed changes in obs, id = ' + str(obs_meteor.data.id))

                    else:
                        if is_tmp is False:
                            IncidentMeteor.new(
                                "load_obs",
                                "info",
                                "data already loaded",
                                {'meteor': poste_metier.data.meteor, 'filename': filename, 'out_idx': str(outside_idx), 'idx': json_data_idx, 'stop_dat': str(m_stop_date_agg_start_date)})
                        t.logInfo("skipping data[" + str(outside_idx) + '/' + str(json_data_idx) + "], data already loaded !!! stop_dat: " + str(m_stop_date_agg_start_date), my_span)
                        continue
                else:
                    # basic asumption
                    if obs_meteor.data.j_agg.__len__() != 0 or obs_meteor.data.j.__len__() != 0:
                        raise Exception('Invalid new obs_meteor structure')
                    # load duration and stop_dat if not already loaded
                    if obs_meteor.data.duration == 0:
                        obs_meteor.data.duration = m_duration

                # double check that the duration are compatible
                if obs_meteor.data.duration != m_duration:
                    raise Exception('loadObsDatarow', 'incompatible durations -> in table obs: ' + str(obs_meteor.data.duration) + ', in json: ' + str(m_duration))

                # load agregations from data file
                m_agg_j = []
                if use_validation is True:
                    if (one_data_item.get("validation") is not None):
                        m_agg_j = one_data_item["validation"]
                    if m_agg_j.__len__() == 0:
                        if is_tmp is False:
                            IncidentMeteor.new(
                                "load_obs",
                                "info",
                                "no data in Validation clause",
                                {'meteor': poste_metier.data.meteor, 'filename': filename, 'out_idx': str(outside_idx), 'idx': json_data_idx, 'stop_dat': str(m_stop_date_agg_start_date)})
                        t.logInfo("skipping data[" + str(outside_idx) + '/' + str(json_data_idx) + "], no data in validation clause !!! stop_dat: " + str(m_stop_date_agg_start_date), my_span)
                        continue
                else:
                    if one_data_item.__contains__("aggregations"):
                        m_agg_j = one_data_item["aggregations"]

                # store aggregations in obs
                obs_meteor.data.j_agg.append(m_agg_j)

                # load values in obs_meteor.j[obs_data_idx] for all type_instruments
                obs_meteor.data.j.append({'duration': m_duration})
                for an_intrument in all_instr.get_all_instruments():
                    # for all measures
                    for my_measure in an_intrument["object"].get_all_measures():
                        self.processJsonData.loadJsonInObs(
                            poste_metier,
                            obs_meteor,
                            my_measure,
                            json_file_data,
                            json_data_idx,
                            trace_flag,
                        )
                obs_meteor.save()
                a_todo = AggTodoMeteor(obs_meteor.data.id, is_tmp)
                if obs_meteor.data.j.__len__() > 1:
                    # duration have to match in order to delete obs data
                    if obs_meteor.data.duration != m_duration:
                        raise Exception('Obs: ' + str(obs_meteor.data.id + ' cannot remove old values as duration does not match: ' + str(m_duration) + '/' + str(obs_meteor.data.duration)))
                    delta_values = {'duration': m_duration * -1, 'maxminFix': []}
                    for an_intrument in all_instr.get_all_instruments():
                        # for all measures
                        for my_measure in an_intrument["object"].get_all_measures():
                            self.processJsonData.loadDeltaValues(
                                my_measure,
                                obs_meteor,
                                1,
                                delta_values,
                                True,
                                trace_flag,
                            )
                    a_todo.data.j_dv.append(delta_values)
                    a_todo.data.j_agg.append(obs_meteor.data.j_agg[0])
                    # remove first element, as it is in delta_values to be processed
                    del obs_meteor.data.j[0]
                    del obs_meteor.data.j_agg[0]

                delta_values = {'duration': m_duration, 'maxminFix': []}
                for an_intrument in all_instr.get_all_instruments():
                    # for all measures
                    for my_measure in an_intrument["object"].get_all_measures():
                        self.processJsonData.loadDeltaValues(
                            my_measure,
                            obs_meteor,
                            0,
                            delta_values,
                            False,
                            trace_flag,
                        )
                a_todo.data.j_dv.append(delta_values)
                a_todo.data.j_agg.append(obs_meteor.data.j_agg[0])

                if json_data_idx < json_file_data["data"].__len__() <= 1:
                    a_todo.data.priority = 0

                obs_meteor.save()
                my_span.set_attribute("obsId_" + str(json_data_idx), obs_meteor.data.id)
                a_todo.save()

            finally:
                json_data_idx += 1
                poste_metier.unlock()
        return

# save agg_todo
# remove agg_todo.agg_j
# agg_todo,j_dv as an array
# clean up loadJsonInObs params

    def _getJsonData(self, params: json, isError: IsErrorClass):
        """
            yield filename, file_content
        """
        try:
            # content loaded on client side
            if params.get("json") is not None:
                # load our json data
                my_json = params["json"]
                if 'dict' in str(type(my_json)):
                    my_json = [my_json]
                filename = "???"
                if params.get("filename") is not None:
                    filename = params["filename"]
                yield {"f": filename, "j": my_json}
                return

            # content to load from the server
            use_recursivity = False,

            if params.get("base_dir") is None:
                use_recursivity = True
                if hasattr(settings, "AUTOLOAD_DIR") is True:
                    params["base_dir"] = settings.AUTOLOAD_DIR
                else:
                    params["base_dir"] = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/json_auto_load")
            base_dir = params["base_dir"]
            files = []
            if params.get("filename") is not None:
                files.append({"p": base_dir, "f": params["filename"]})
            else:
                if use_recursivity is False:
                    for filename in os.listdir(base_dir):
                        if str(filename).endswith('.json'):
                            files.append({"p": base_dir, "f": filename})
                else:
                    for (dirpath, dirnames, filenames) in os.walk(base_dir):
                        for filename in filenames:
                            if str(filename).endswith('.json') and str(dirpath).endswith('/done') is False and str(dirpath).endswith('/failed') is False:
                                files.append({"p": dirpath, "f": filename})

            files = sorted(files, key=lambda k: k['f'], reverse=False)
            for aFileSpec in files:
                if self.stopRequested is True:
                    continue
                if aFileSpec["f"].endswith(".json"):
                    try:
                        # load our json file
                        texte = ""

                        with open(aFileSpec["p"] + '/' + aFileSpec["f"], "r") as f:
                            lignes = f.readlines()
                            for aligne in lignes:
                                texte += str(aligne)
                        my_json = JsonPlus().loads(texte)
                        if 'dict' in str(type(my_json)):
                            my_json = [my_json]

                        # load_span.set_attribute("filename", aFile)
                        yield {"f": aFileSpec["f"], "j": my_json}
                        if isError.get() is False:
                            # load_span.add_event("file.moved to [dest]", {"dest": base_dir + "/done/" + aFile})
                            if not os.path.exists(aFileSpec["p"] + '/done'):
                                os.makedirs(aFileSpec["p"] + '/done')
                            os.rename(aFileSpec["p"] + "/" + aFileSpec["f"], aFileSpec["p"] + "/done/" + aFileSpec["f"])
                        else:
                            t.logInfo(
                                "file moved to fail directory",
                                None,
                                {"filename": aFileSpec["f"], "dest": aFileSpec["p"] + "/failed/" + aFileSpec["f"]},
                            )
                            if not os.path.exists(aFileSpec["p"] + '/failed'):
                                os.makedirs(aFileSpec["p"] + '/failed')
                            os.rename(aFileSpec["p"] + "/" + aFileSpec["f"],  aFileSpec["p"] + "/failed/" + aFileSpec["f"])

                    except Exception as exc:
                        t.LogCritical(exc)
                        raise exc

        except Exception as exc:
            t.LogCritical(exc)
            raise exc
