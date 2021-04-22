

from app.tools.jsonPlus import JsonPlus
from app.classes.calcul.calcObservation import CalcObs
from app.classes.workers.svcAggreg import SvcAggreg
from app.classes.workers.workerRoot import WorkerRoot
import os


class SvcAutoLoad(WorkerRoot):
    """
        SvcAggreg

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcAutoLoad, self).__init__(str(SvcAutoLoad), self.CheckFiles, 60)

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcAutoLoad)

    @staticmethod
    def runMe():
        svc_agg_instance = SvcAutoLoad.GetInstance()
        if svc_agg_instance.IsRunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunIt()

    # views to update
    def CheckFiles(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/../../data/json_auto_load'
            files = os.listdir(base_dir)

            for aFile in files:
                if aFile.endswith('.json'):
                    try:
                        ret_json = self.loadJson(base_dir + '/' + aFile, False, False, False)
                        print('------------------ SvcAutoLoad: ' + aFile + ' -----------')
                        print(JsonPlus().dumps(ret_json))
                        print('-------------------------------------------------------------------------')
                        os.rename(base_dir + '/' + aFile, base_dir + '/done/' + aFile)
                    except Exception as exc:
                        print('------------------ SvcAutoLoad: ' + aFile + ' -----------')
                        print(exc.args)     # arguments stored in .args
                        print(exc)
                        print('-------------------------------------------------------------------------')
                        os.rename(base_dir + '/' + aFile, base_dir + '/failed/' + aFile)

        except Exception as inst:
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

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
            SvcAggreg.runMe()
            agg_j_ret['loadAgg'] = 'started'

            # SvcAggreg.GetInstance().RunIt()

            return agg_j_ret
