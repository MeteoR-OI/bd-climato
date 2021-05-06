

from app.tools.jsonPlus import JsonPlus
from app.classes.calcul.calcObservation import CalcObs
from app.classes.workers.svcAggreg import SvcAggreg
from app.classes.workers.workerRoot import WorkerRoot
from app.tools.telemetry import TracerTriage
import app.tools.myTools as t
import os
import json


class SvcAutoLoad(WorkerRoot):
    """
        SvcAggreg

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcAutoLoad, self).__init__(str(SvcAutoLoad), self.LoadFiles, 60, ['autoload', 'auto'])

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcAutoLoad)

    @staticmethod
    def runMe(params: json = {}):
        svc_agg_instance = SvcAutoLoad.GetInstance()
        if svc_agg_instance.IsRunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunIt(params)

    # views to update
    def LoadFiles(self, my_tracer: TracerTriage, params: json = {}, trace_flag: bool = False):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/../../data/json_auto_load'
            if params.get('base_dir') is not None:
                base_dir = params['base_dir']
            if params.get('filename') is not None:
                files = []
                files.append(params['filename'])
            else:
                files = os.listdir(base_dir)

            for aFile in files:
                if aFile.endswith('.json'):
                    # with my_tracer.start_as_current_span as my_span:
                    try:
                        # my_span.set_attribute('filename', aFile)
                        # my_span.set_attribute('base.dir', base_dir)
                        ret_json = self.loadJson(base_dir + '/' + aFile, False, False, False)
                        # my_span.set_event('file.moved', {'dest': base_dir + '/done/' + aFile})
                        if trace_flag is True:
                            t.logTrace('task ' + self.name + " file processed", None, ret_json)
                        os.rename(base_dir + '/' + aFile, base_dir + '/done/' + aFile)
                    except Exception as exc:
                        t.LogException(exc)
                        # t.LogException(exc, my_span)
                        # my_span.record_exception(exc)
                        # my_span.set_event('file.moved', {'dest': base_dir + '/failed/' + aFile})
                        os.rename(base_dir + '/' + aFile, base_dir + '/failed/' + aFile)

        except Exception as inst:
            t.LogException(inst, my_span)
            my_span.record_insteption(inst)

    def loadJson(self, file_name: str, delete_flag: bool, trace_flag: bool, is_tmp: bool = None):
        calc_obs = CalcObs()
        texte = ''

        with open(file_name, "r") as f:
            lignes = f.readlines()
            for aligne in lignes:
                texte += str(aligne)

            my_json_array = JsonPlus().loads(texte)
            ret = calc_obs.loadJson(my_json_array, delete_flag, trace_flag, is_tmp)

            # start in sync the calculus if our aggregations
            agg_j_ret = {'loadObs': ret}
            SvcAggreg.runMe({"is_tmp": False})
            agg_j_ret['loadAgg'] = 'started'

            return agg_j_ret
