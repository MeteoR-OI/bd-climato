from app.classes.calcul.allCalculus import AllCalculus
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.workers.svcAggreg import SvcAggreg
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


class CalcObs(AllCalculus):
    """
    Control all the processing of a json data, with our Observation table
    """

    def __init__(self):
        self.tracer = Telemetry.Start("calculus")
        CalcObs.lock = threading.Lock()

    @staticmethod
    def GetInstance():
        if hasattr(CalcObs, "MyInstance") is False:
            CalcObs.MyInstance = CalcObs()
        return CalcObs.MyInstance

    def LoadJsonFromSvc(self, data: json):
        """
        common params:
                "json: json_data pre loaded
                "delete": delete_flag,
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
        is_tmp = delete_flag = use_validation = False
        ret = []
        if params.get("is_tmp") is not None:
            is_tmp = params["is_tmp"]
        if params.get("delete") is not None:
            delete_flag = params["delete"]
        if params.get("validation") is not None:
            use_validation = params["validation"]

        # delete is not part of the transaction
        if delete_flag:
            self.delete_obs_agg(is_tmp)

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
        SvcAggreg.runMe({"is_tmp": is_tmp, "trace_flag": trace_flag})
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
        processJson

        calulus v2, load json in the obs & agg_toto tables
        """
        debut_full_process = datetime.datetime.now()
        ret_data = []
        item_processed = 0
        all_item_processed = 0
        idx = 0
        meteor = "???"

        with self.tracer.start_as_current_span("Load Obs", trace_flag) as my_span:
            try:
                # validate our json
                meteor = str(json_data_array[0].get("meteor"))
                check_result = checkJson(json_data_array)
                if check_result is not None:
                    raise Exception("Meteor: " + meteor + ", filenme: " + filename + str(check_result))

                while idx < json_data_array.__len__():
                    try:
                        # start_time = datetime.datetime.now()
                        json_file_data = json_data_array[idx]
                        if idx == 0:
                            my_span.set_attribute("meteor", meteor)
                            my_span.set_attribute("filename", filename)

                        item_processed = json_file_data["data"].__len__()
                        all_item_processed += item_processed

                        self._loadJsonItemInObs(json_file_data, trace_flag, is_tmp, use_validation, filename)

                        # duration = datetime.datetime.now() - start_time
                        # dur_millisec = round(duration.total_seconds() * 1000)

                        # my_span.set_attribute("items_" + str(idx), item_processed)
                        # my_span.set_attribute("timeExec_" + str(idx), dur_millisec)
                        # ret_data.append(ret)

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
    ) -> json:
        """
        processJson

        calulus v2, load json in the obs & agg_toto tables
        """
        all_instr = AllTypeInstruments()

        measure_idx = 0
        # debut_process = datetime.datetime.now()
        my_span = self.tracer.get_current_or_new_span("Load Obs", trace_flag)

        while measure_idx < json_file_data["data"].__len__():
            # we use the stop_dat of our measure json as the start date for our processing
            m_stop_date_agg_start_date = json_file_data["data"][measure_idx]["stop_dat"]

            if (json_file_data["data"][measure_idx].get("current") is not None and use_validation is False):
                m_duration = json_file_data["data"][measure_idx]["current"]["duration"]
            else:
                # we don't care as we don't have current data
                m_duration = 0
                # in validation mode, we don't use the 'current'
                json_file_data["data"][measure_idx]["current"] = {"duration": 0}
            poste_metier = PosteMetier(json_file_data["poste_id"], m_stop_date_agg_start_date)
            if measure_idx == 0:
                my_span.set_attribute("posteId", poste_metier.data.id)
                my_span.set_attribute("stopDat", str(m_stop_date_agg_start_date))
                my_span.set_attribute("isTmp", is_tmp)
            try:
                poste_metier.lock()
                obs_meteor = poste_metier.observation(m_stop_date_agg_start_date, is_tmp)
                if (obs_meteor.data.id is not None and json_file_data["data"][measure_idx].__contains__("update_me") is False):
                    t.logInfo(
                        "file: " + filename + " skipping data[" + str(measure_idx) + "], stop_dat: " + str(m_stop_date_agg_start_date) + " already loaded",
                        my_span,
                    )
                    continue
                # load aggregations data in obs_meteor.data.j_agg
                m_agg_j = []
                if use_validation is True:
                    if (json_file_data["data"][measure_idx].get("validation") is not None):
                        m_agg_j = json_file_data["data"][measure_idx]["validation"]
                    if m_agg_j.__len__() == 0:
                        t.logInfo("skipping data[" + str(measure_idx) + "], no data in JSON !!! stop_dat: " + str(m_stop_date_agg_start_date), my_span)
                        continue
                else:
                    if json_file_data["data"][measure_idx].__contains__("aggregations"):
                        m_agg_j = json_file_data["data"][measure_idx]["aggregations"]
                obs_meteor.data.j_agg = m_agg_j

                # load duration and stop_dat if not already loaded
                if (obs_meteor.data.duration == 0 and json_file_data["data"][measure_idx].get("current") is not None):
                    obs_meteor.data.duration = json_file_data["data"][measure_idx]["current"]["duration"]

                delta_values = {"maxminFix": [], "duration": m_duration}

                # for all type_instruments
                for an_intrument in all_instr.get_all_instruments():
                    # for all measures
                    for my_measure in an_intrument["object"].get_all_measures():
                        # find the calculus object for my_mesure
                        for a_calculus in self.all_calculus:
                            if a_calculus["agg"] == my_measure["agg"]:
                                if a_calculus["calc_obs"] is not None:
                                    # load our json in obs row
                                    a_calculus["calc_obs"].loadInObs(
                                        poste_metier,
                                        my_measure,
                                        json_file_data,
                                        measure_idx,
                                        m_agg_j,
                                        obs_meteor,
                                        delta_values,
                                        trace_flag,
                                    )
                                break

                # save our new data
                obs_meteor.save()
                my_span.set_attribute("obsId_" + str(measure_idx), obs_meteor.data.id)

                a_todo = AggTodoMeteor(obs_meteor.data.id, is_tmp)
                a_todo.data.j_dv.append(delta_values)
                if measure_idx < json_file_data["data"].__len__() <= 1:
                    a_todo.data.priority = 0
                if obs_meteor.data.id is not None:
                    a_todo.save()

                # j_trace = {}

                # if trace_flag:
                #     duration2 = datetime.datetime.now() - debut_process
                #     j_trace["info"] = "idx=" + str(measure_idx)
                #     j_trace["total_exec"] = int(duration2.total_seconds() * 1000)
                #     j_trace["item_processed"] = json_file_data["data"].__len__()
                #     j_trace["one_exec"] = int(duration2.total_seconds() * 1000 / json_file_data["data"].__len__())
                #     # j_trace['start_dat'] = json_file_data['data'][measure_idx]['current']['start_dat']
                #     j_trace["stop_dat"] = str(json_file_data["data"][measure_idx]["stop_dat"])
                #     j_trace["obs data"] = JsonPlus().loads(JsonPlus().dumps(obs_meteor.data.j))
                #     j_trace["obs aggregations"] = JsonPlus().loads(JsonPlus().dumps(obs_meteor.data.j_agg))
                #     j_trace["agg_todo dv"] = (JsonPlus().loads(JsonPlus().dumps(a_todo.data.j_dv)) if not (a_todo.data.id is None) else "{}")
                    # t.LogDebug("json item loaded", my_span, {'idx': measure_idx, 'time_exec': j_trace["total_exec"], 'items': j_trace["item_processed"], "stop_dat": j_trace["stop_dat"]})

            finally:
                measure_idx += 1
                poste_metier.unlock()

        return

    def _getJsonData(self, params: json, isError: IsErrorClass):
        """
            yield filename, file_content
        """
        try:
            # content loaded on client side
            if params.get("json") is not None:
                # load our json data
                my_json = params["json"]
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

                        # load_span.set_attribute("filename", aFile)
                        yield {"f": aFileSpec["f"], "j": my_json}
                        if isError.get() is False:
                            # load_span.add_event("file.moved to [dest]", {"dest": base_dir + "/done/" + aFile})
                            if not os.path.exists(aFileSpec["p"] + '/done'):
                                os.makedirs(aFileSpec["p"] + '/done')
                            os.rename(aFileSpec["p"] + "/" + aFileSpec["f"], aFileSpec["p"] + "/done/" + aFileSpec["f"])
                            # t.logInfo(
                            #     "json file loaded",
                            #     load_span,
                            #     {"filename": aFile, "dest": baseDir + "/done/" + aFile},
                            # )
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
