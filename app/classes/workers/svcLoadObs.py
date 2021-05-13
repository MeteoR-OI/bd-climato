from app.classes.workers.workerRoot import WorkerRoot
from app.classes.calcul.calcObservation import CalcObs
import json


class SvcLoadObs(WorkerRoot):
    """
        SvcAggreg

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcLoadObs, self).__init__(str(SvcLoadObs), CalcObs().LoadJsonFromSvc, 120, ['loadobs'])

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcLoadObs)

    @staticmethod
    def runMe(params: json = {}):
        svc_agg_instance = SvcLoadObs.GetInstance()
        if svc_agg_instance.IsRunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunIt(params)
