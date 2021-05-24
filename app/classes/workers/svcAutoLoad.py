

from app.classes.calcul.calcObservation import CalcObs
from app.classes.workers.workerRoot import WorkerRoot
import json


class SvcAutoLoad(WorkerRoot):
    """
        SvcAggreg

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcAutoLoad, self).__init__(str(SvcAutoLoad), CalcObs.GetInstance().LoadJsonFromSvc, 60, ['autoload', 'auto'])

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcAutoLoad)

    @staticmethod
    def runMe(params: json = {}):
        svc_agg_instance = SvcAutoLoad.GetInstance()
        if svc_agg_instance.IsRunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunIt(params)
