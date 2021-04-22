from app.classes.workers.workerRoot import WorkerRoot
from app.classes.calcul.calcAggreg import CalcAggreg


class SvcAggreg(WorkerRoot):
    """
        SvcAggreg

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcAggreg, self).__init__(str(SvcAggreg), CalcAggreg().ComputeAggreg, 120)

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcAggreg)

    @staticmethod
    def runMe():
        svc_agg_instance = SvcAggreg.GetInstance()
        if svc_agg_instance.IsRunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunIt()
