# from operator import is_
from app.classes.calcul.observation.processJsonData import ProcessJsonData
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.workers.svcAggregate import SvcAggregate
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.jsonPlus import JsonPlus
from app.tools.jsonValidator import checkJson
from app.tools.refManager import RefManager
import app.tools.myTools as t
from app.tools.aggTools import calcAggDate, getAggDuration
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

    def LoadJsonControler(self, data: json, is_killed):
        """
        common params:
                "json: json_data pre loaded
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

        # load the content of files on the server
        isError = IsErrorClass()
        for j_data in self._getJsonData(params, isError):
            try:
                if CalcObs.lock.acquire(True, 500) is False:
                    t.logWarning("LoadJsonControler lock time-out !")
                    return

                with self.tracer.start_as_current_span("Load Obs", trace_flag) as my_span:
                    try:
                        self.loadJsonArrayTransaction(j_data["j"], trace_flag, j_data.get("f"))

                    except Exception as exc:
                        isError.set(True)
                        IncidentMeteor.new("load obs", "Exception", str(exc), {})
                        my_span.record_exception(exc)

                    finally:
                        CalcObs.lock.release()
                        #  or ??self.tracer.end_span() ??
                        my_span.end()

            except Exception as inst:
                isError.set(True)
                t.LogCritical(inst)

        # activate the computation of aggregations
        SvcAggregate.runMe({"trace_flag": trace_flag})
        return

    # ----------------
    # private methods
    # ----------------
    @transaction.atomic
    def loadJsonArrayTransaction(self, json_data_array: json, trace_flag: bool = False, filename: str = "????"):
        """
            loadJsonArrayTransaction
        """
        debut_full_process = datetime.datetime.now()
        item_processed = 0
        idx = 0
        meteor = "???"

        with self.tracer.get_current_or_new_span() as my_span:

            # validate our json
            meteor = str(json_data_array[0].get("meteor"))
            pid = PosteMeteor.getPosteIdByMeteor(json_data_array[0]["meteor"])
            if pid is None:
                raise Exception("code meteor inconnu: " + json_data_array[0]["meteor"])

            check_result = checkJson(json_data_array, pid, filename)
            if check_result is not None:
                raise Exception("Invalid Json file: " + filename + ": " + check_result)

            # now load our data in obs table
            while idx < json_data_array.__len__():
                json_file_data = json_data_array[idx]

                if idx == 0:
                    my_span.set_attribute("meteor", meteor)
                    my_span.set_attribute("filename", filename)

                self.loadJsonInObs(json_file_data, trace_flag, filename, idx)

                item_processed += json_file_data["data"].__len__()
                idx += 1

            global_duration = datetime.datetime.now() - debut_full_process
            dur_millisec = round(global_duration.total_seconds() * 1000)
            one_exec = round(dur_millisec / item_processed)
            t.logInfo(
                "Json file loaded",
                my_span,
                {"filename": filename, "timeExec": dur_millisec, "avgItemExec": one_exec, "items":  item_processed, "meteor": meteor},
            )
        return

    # switch to the right function
    def loadJsonInObs(self, json_file_data: json, trace_flag: bool = False, filename: str = '???', outside_idx: int = 0):
        all_instr = AllTypeInstruments()

        json_data_idx = 0
        json_type = json_file_data['info']['json_type']
        json_is_obs = True if json_type in ["O", "C"] else False
        # json_version = json_file_data['info']['version']

        # debut_process = datetime.datetime.now()
        my_span = self.tracer.get_current_or_new_span("Load Obs", trace_flag)

        # load extremes from data file
        j_xtreme = json_file_data.get("extremes") if None else {}

        while json_data_idx < json_file_data["data"].__len__():
            one_data_item = json_file_data["data"][json_data_idx]

            if json_is_obs is True:
                j_stop_dat = one_data_item["stop_dat"]
                j_duration = one_data_item["duration"]
                j_start_dat = j_stop_dat - datetime.timedelta(minutes=j_duration)
            else:
                j_start_dat = one_data_item["start_dat"]
                j_start_dat = calcAggDate(json_type, j_start_dat, 0, False)
                j_duration = getAggDuration(json_type, j_start_dat)
                j_stop_dat = j_start_dat + datetime.timedelta(minutes=j_duration)

            ###################
            # Load data in obs
            ###################
            poste_metier = PosteMetier(json_file_data["poste_id"], j_start_dat)
            poste_metier.lock()

            if json_data_idx == 0:
                my_span.set_attribute("posteId", poste_metier.data.id)
                my_span.set_attribute("stop_dat", str(j_stop_dat))
                my_span.set_attribute("json_type", json_type)

            obs_meteor = poste_metier.observation(j_stop_dat)
            obs_meteor.data.filename = filename

            if obs_meteor.data.id is not None:
                # obs_meteor already exist
                if one_data_item.__contains__("force_replace") is True:
                    # basic asumption
                    if obs_meteor.data.j_agg.__len__() != 1 or obs_meteor.data.j.__len__() != 1 or obs_meteor.data.j_xtreme.__len__() != 1:
                        raise Exception('Json array not processed in obs, retry later, or fix it. obs id = ' + str(obs_meteor.data.id))
                else:
                    my_span.add_event(
                        'already loaded',
                        {'meteor': poste_metier.data.meteor, 'filename': filename, 'data_idx': str(outside_idx), 'idx': json_data_idx, 'stop_dat': str(j_stop_dat)})
                    json_data_idx += 1
                    continue
            else:
                # basic asumption
                if obs_meteor.data.j_agg.__len__() != 0 or obs_meteor.data.j.__len__() != 0 or obs_meteor.data.j_xtreme.__len__() != 0:
                    raise Exception('Invalid new obs_meteor structure')
                obs_meteor.data.duration = j_duration

            # push new item in j/j_agg/j_xtreme
            obs_meteor.data.j.append({})
            obs_meteor.data.j_agg.append({})
            obs_meteor.data.j_xtreme.append(j_xtreme)

            # load values in obs_meteor.j[obs_data_idx] for all type_instruments
            if json_is_obs is True:
                obs_meteor.data.j[obs_meteor.data.j.__len__() - 1]['duration'] = j_duration

                # need to normalize data given
                for an_intrument in all_instr.get_all_instruments():
                    # for all measures
                    for my_measure in an_intrument["object"].get_all_measures():
                        self.processJsonData.loadJsonInObs(
                            poste_metier,
                            obs_meteor,
                            my_measure,
                            json_file_data,
                            json_data_idx,
                            j_duration,
                            trace_flag,
                        )
            else:
                # data should have the same syntax as the data used in agg_xxx.j
                obs_meteor.data.j_agg[obs_meteor.data.j_agg.__len__() - 1] = json_file_data[json_data_idx]['valeurs']
                obs_meteor.data.j_agg[obs_meteor.data.j_agg.__len__() - 1]['duration'] = j_duration
            obs_meteor.save()

            ################
            # load agg_todo
            ################
            a_todo = AggTodoMeteor(obs_meteor.data.id, json_type)

            if obs_meteor.data.j.__len__() > 1:
                # generate delta_values to remove from all the upper aggregation levels (obs is lowest level)
                if json_is_obs is True:
                    if obs_meteor.data.j_agg[0].__len__() > 0:
                        raise Exception('cannot replace agregated data by measure data')

                    delta_values = {'duration': obs_meteor.data.j[0]['duration'] * -1, 'maxminFix': []}
                    # we need to remove the original data kept in obs_meteor.data.j[0]
                    for an_intrument in all_instr.get_all_instruments():
                        # for all measures
                        for my_measure in an_intrument["object"].get_all_measures():
                            self.processJsonData.loadDeltaValues(
                                my_measure,
                                obs_meteor,
                                0,
                                delta_values,
                                True,
                                trace_flag,
                                j_start_dat,
                                j_stop_dat,
                            )
                else:
                    if obs_meteor.data.j[1].__len__() > 0:
                        raise Exception("cannot replace measure data with agregated data")

                    # we need to remove the old aggregated data
                    delta_values = obs_meteor.data.j_agg[0]
                    delta_values['duration'] = obs_meteor.data.j_agg[0]['duration'] * -1
                    delta_values['maxminFix'] = []

                delta_values['json_type'] = json_type
                a_todo.data.j.append(delta_values)

                # remove first element in obs, just keep the last (good) data
                del obs_meteor.data.j[0]
                del obs_meteor.data.j_agg[0]
                del obs_meteor.data.j_xtreme[0]

            # generate delta_values to propagate into the upper aggregation levels (obs is lowest level)
            if json_is_obs is True:
                delta_values = {'duration': j_duration, 'maxminFix': []}
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
                            j_start_dat,
                            j_stop_dat,
                        )
            else:
                delta_values = obs_meteor.data.j_agg[0]
                delta_values['duration'] = j_duration
                delta_values['maxminFix'] = []

            a_todo.data.j.append(delta_values)

            if json_data_idx < json_file_data["data"].__len__() <= 1:
                a_todo.data.priority = 0

            obs_meteor.save()
            my_span.set_attribute("obsId_" + str(json_data_idx), obs_meteor.data.id)
            a_todo.save()

            json_data_idx += 1
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
                if 'dict' in str(type(my_json)):
                    my_json = [my_json]
                filename = "???"
                if params.get("filename") is not None:
                    filename = params["filename"]
                yield {"f": filename, "j": my_json}
                return

            # get our directories
            if params.get("base_dir") is None:
                if hasattr(settings, "AUTOLOAD_DIR") is True:
                    params["base_dir"] = settings.AUTOLOAD_DIR
                else:
                    params["base_dir"] = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/json_auto_load")
            base_dir = params["base_dir"]

            if params.get('archive_dir') is None:
                if hasattr(settings, "ARCHIVE_DIR") is True:
                    params["archive_dir"] = settings.ARCHIVE_DIR
                else:
                    params["archive_dir"] = params["base_dir"]
            archive_dir = params["archive_dir"]

            files = []
            if params.get("filename") is not None:
                files.append({"p": base_dir, "f": params["filename"]})
            else:
                # no more recursive search
                for filename in os.listdir(base_dir):
                    if str(filename).endswith('.json'):
                        files.append({"p": base_dir, "f": filename})

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

                    except Exception as exc:
                        isError.set(True)
                        t.LogCritical(exc)
                        raise exc

                    finally:
                        str_annee = 'inconnu'
                        str_mois = 'inconnu'
                        try:
                            str_annee = str(aFileSpec['f']).split(".")[2].split("-")[0]
                            str_mois = str(aFileSpec['f']).split(".")[2].split("-")[1]
                        except Exception:
                            pass
                        meteor = str(aFileSpec['f']).split(".")[1]

                        if isError.get() is False:
                            filename_prefix = archive_dir + "/" + meteor + "/" + str_annee + "/" + str_mois + "/"
                            if not os.path.exists(filename_prefix):
                                os.makedirs(filename_prefix)

                            os.rename(aFileSpec["p"] + "/" + aFileSpec["f"], filename_prefix + aFileSpec["f"])
                        else:
                            j_info = {"filename": aFileSpec["f"], "dest": archive_dir + "/" + meteor + "/failed/" + aFileSpec["f"]}
                            t.logInfo("file moved to fail directory", None, j_info)
                            IncidentMeteor.new('load_obs', 'ERROR', 'file moved to failed directory', j_info)

                            if not os.path.exists(archive_dir + "/" + meteor + '/failed'):
                                os.makedirs(archive_dir + "/" + meteor + '/failed')
                            os.rename(aFileSpec["p"] + "/" + aFileSpec["f"],  archive_dir + "/" + meteor + "/failed/" + aFileSpec["f"])

        except Exception as exc:
            t.LogCritical(exc)
            raise exc
