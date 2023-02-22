# from operator import is_
from app.classes.json_loader.processJsonData import ProcessJsonData
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.workers.svcMigrate import SvcAggregate
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
            t.logError("LoadJsonControler", "wrong data")
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
        for j_fileInfo in self._getJsonFileNameAndData(params, isError):
            if CalcObs.lock.acquire(True, 500) is False:
                t.logwarning("LoadJsonControler", "LoadJsonControler lock time-out !")
                return

            with self.tracer.start_as_current_span("Load Obs") as my_span:
                try:
                    my_span.set_attribute('filename', j_fileInfo["f"])
                    self.loadJsonArrayTransaction(j_fileInfo["j"], trace_flag, j_fileInfo.get("f"))

                except Exception as exc:
                    isError.set(True)
                    t.logException(exc, my_span, {'filename': j_fileInfo.get("f")})

                finally:
                    CalcObs.lock.release()
                    my_span.end()

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
        idx_item = 0
        meteor = "???"
        my_span = self.tracer.get_current_span()

        # validate our json
        meteor = str(json_data_array[0].get("meteor"))
        pid = PosteMeteor.getPosteIdByMeteor(json_data_array[0]["meteor"])
        if pid is None:
            raise Exception("code meteor inconnu: " + json_data_array[0]["meteor"])

        check_result = checkJson(json_data_array, pid, filename)
        if check_result is not None:
            raise Exception("Invalid Json file: " + filename + ": " + check_result)

        # now load our data in obs table
        while idx_item < json_data_array.__len__():
            with self.tracer.start_as_current_span("Item_" + str(idx_item)):
                json_item_data = json_data_array[idx_item]

                if idx_item == 0:
                    # set attributes in parent spam
                    my_span.set_attribute("meteor", meteor)
                    my_span.set_attribute("filename", filename)

                self.loadOneJsonItemInObs(json_item_data, trace_flag, filename, idx_item)

                item_processed += json_item_data["data"].__len__()
                idx_item += 1

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
    def loadOneJsonItemInObs(self, json_item_data: json, trace_flag: bool = False, filename: str = '???', outside_idx: int = 0):
        all_instr = AllTypeInstruments()
        my_current_span = self.tracer.get_current_span()

        json_data_idx = 0
        json_type = json_item_data['info']['json_type']
        json_is_obs = True if json_type in ["O", "C"] else False

        # load extremes from data file
        j_xtreme = json_item_data.get("extremes") if None else {}

        while json_data_idx < json_item_data["data"].__len__():
            one_data_item = json_item_data["data"][json_data_idx]
            try:
                # prepare obs_meteor
                j_start_dat, j_stop_dat, j_duration = self.get_timing_info(one_data_item, json_type, json_is_obs)
                poste_metier = PosteMetier(json_item_data["poste_id"], j_start_dat)
                poste_metier.lock()

                if json_data_idx == 0:
                    my_current_span.set_attribute("posteId", poste_metier.data.id)
                    my_current_span.set_attribute("stop_dat", str(j_stop_dat))
                    my_current_span.set_attribute("json_type", json_type)

                obs_meteor = poste_metier.observation(j_stop_dat)
                obs_meteor.data.filename = filename
                obs_meteor.data.j.append({})
                obs_meteor.data.j_xtreme.append(j_xtreme)

                if obs_meteor.data.id is not None:
                    if one_data_item.__contains__("force_replace") is True:
                        # basic asumption - probably not needed...
                        if obs_meteor.data.j.__len__() != 1 or obs_meteor.data.j_xtreme.__len__() != 1:
                            raise Exception('Json array not processed in obs, retry later, or fix it. obs id = ' + str(obs_meteor.data.id))
                    else:
                        t.logInfo(
                                'already loaded', my_current_span,
                                {'meteor': poste_metier.data.meteor, 'filename': filename, 'data_idx': str(outside_idx), 'idx': json_data_idx, 'stop_dat': str(j_stop_dat)})
                        continue
                else:
                    # basic asumption
                    if obs_meteor.data.j.__len__() != 1 or obs_meteor.data.j_xtreme.__len__() != 1:
                        raise Exception(
                            'Invalid new obs_meteor structure-' +
                            str(obs_meteor.data.j.__len__()) + '/' + str(obs_meteor.data.j_xtreme.__len__()))
                    obs_meteor.data.duration = j_duration

                # load json values in obs
                self.load_obs_data_j(all_instr, one_data_item, j_duration, json_is_obs, poste_metier, obs_meteor)

                # prepare agg_Todo
                a_todo = AggTodoMeteor(obs_meteor.data.id, json_type)

                #  update agg_todo with obs.j data
                self.load_agg_todo(all_instr, a_todo, obs_meteor, json_is_obs, j_start_dat, j_stop_dat, j_duration, json_type)

                obs_meteor.data.duration = j_duration
                obs_meteor.data.json_type = json_type
                obs_meteor.save()
                a_todo.data.id = obs_meteor.data.id
                my_current_span.set_attribute("data_" + str(json_data_idx), obs_meteor.data.id)
                a_todo.save()

            finally:
                json_data_idx += 1
                poste_metier.unlock()

        return

    def load_obs_data_j(self, all_instr, one_data_item, j_duration, json_is_obs, poste_metier, obs_meteor):
        if json_is_obs is True:
            # load each value if json_is_obs
            obs_meteor.data.j[obs_meteor.data.j.__len__() - 1]['duration'] = j_duration

            # need to normalize data given
            for an_intrument in all_instr.get_all_instruments():
                # for all measures
                for my_measure in an_intrument["object"].get_all_measures():
                    self.processJsonData.loadOneMeasureInObs(
                        poste_metier,
                        obs_meteor,
                        my_measure,
                        one_data_item,
                        j_duration,
                        json_is_obs,
                    )
        else:
            # data should have the same syntax as the data used in agg_xxx.j
            obs_meteor.data.j[obs_meteor.data.j.__len__() - 1] = one_data_item['valeurs']
            obs_meteor.data.j[obs_meteor.data.j.__len__() - 1]['duration'] = j_duration

    def load_agg_todo(self, all_instr, a_todo, obs_meteor, json_is_obs, j_start_dat, j_stop_dat, j_duration, json_type):
        idx_obs_data_j = obs_meteor.data.j.__len__() - 1
        while idx_obs_data_j >= 0:
            # in delete mode: data.j[0] => data to remove, data.j[1] => data to add
            # in normal mode (add only) data.j[0] => data to add
            mode_delete = False if obs_meteor.data.j.__len__() <= 1 else True

            if json_is_obs is True:
                # measures coming from weeWX
                if mode_delete is True:
                    delta_values = {'duration': obs_meteor.data.duration * -1, 'maxminFix': []}
                else:
                    delta_values = {'duration': j_duration, 'maxminFix': []}

                # we need to remove the original data kept in obs_meteor.data.j[0]
                for an_intrument in all_instr.get_all_instruments():
                    # for all measures
                    for my_measure in an_intrument["object"].get_all_measures():
                        self.processJsonData.loadDeltaValues(
                            my_measure,
                            obs_meteor,
                            0,
                            delta_values,
                            mode_delete,
                            j_start_dat,
                            j_stop_dat,
                        )
            else:
                # we need to remove the old aggregated data
                delta_values = obs_meteor.data.j[0]
                delta_values['duration'] = j_duration if mode_delete is False else obs_meteor.data.duration * -1
                delta_values['maxminFix'] = []

            delta_values['json_type'] = json_type
            a_todo.data.j.append(delta_values)

            # remove first element in obs, just keep the data to add
            if mode_delete is True:
                del obs_meteor.data.j[0]
                del obs_meteor.data.j_xtreme[0]

            idx_obs_data_j -= 1

    def get_timing_info(self, one_data_item: json, json_type, json_is_obs: bool):
        if json_is_obs is True:
            j_stop_dat = one_data_item["stop_dat"]
            j_duration = one_data_item["duration"]
            j_start_dat = j_stop_dat - datetime.timedelta(minutes=j_duration)
        else:
            j_start_dat = one_data_item["start_dat"]
            j_start_dat = calcAggDate(json_type, j_start_dat, 0, False)
            j_duration = getAggDuration(json_type, j_start_dat)
            j_stop_dat = j_start_dat + datetime.timedelta(minutes=j_duration)

        return j_start_dat, j_stop_dat, j_duration

    def _getJsonFileNameAndData(self, params: json, isError: IsErrorClass):
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
            for file_spec in files:
                if self.stopRequested is True:
                    continue
                if file_spec["f"].endswith(".json"):
                    # load our json file
                    texte = ""

                    with open(file_spec["p"] + '/' + file_spec["f"], "r") as f:
                        lignes = f.readlines()
                        for aligne in lignes:
                            texte += str(aligne)
                    my_json = JsonPlus().loads(texte)
                    if 'dict' in str(type(my_json)):
                        my_json = [my_json]

                    # load_span.set_attribute("filename", aFile)
                    yield {"f": file_spec["f"], "j": my_json}

                    str_annee = 'inconnu'
                    str_mois = 'inconnu'
                    try:
                        str_annee = str(file_spec['f']).split(".")[2].split("-")[0]
                        str_mois = str(file_spec['f']).split(".")[2].split("-")[1]
                    except Exception:
                        pass
                    meteor = str(file_spec['f']).split(".")[1]

                    if isError.get() is False:
                        filename_prefix = archive_dir + "/" + meteor + "/" + str_annee + "/" + str_mois + "/"
                        if not os.path.exists(filename_prefix):
                            os.makedirs(filename_prefix)

                        os.rename(file_spec["p"] + "/" + file_spec["f"], filename_prefix + file_spec["f"])
                    else:
                        j_info = {"filename": file_spec["f"], "dest": archive_dir + "/" + meteor + "/failed/" + file_spec["f"]}
                        t.logInfo("file moved to fail directory", None, j_info)
                        IncidentMeteor.new('_getJsonFileNameAndData', 'error', 'file moved to failed directory', j_info)

                        if not os.path.exists(archive_dir + "/" + meteor + '/failed'):
                            os.makedirs(archive_dir + "/" + meteor + '/failed')
                        os.rename(file_spec["p"] + "/" + file_spec["f"],  archive_dir + "/" + meteor + "/failed/" + file_spec["f"])

        except Exception as exc:
            t.logCritical(exc)
            raise exc
