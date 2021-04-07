from app.classes.workers.workerRoot import WorkerRoot
from app.classes.calcul.calcAggreg import CalcAggreg


class SvcAggreg(WorkerRoot):
    """
        SvcAggreg

        Service for Aggregation Computations
    """

    def __init__(self, name: str = 'SvcAggreg'):
        # call parent __init__
        super(SvcAggreg, self).__init__(name, CalcAggreg.ComputeAggreg)

    @staticmethod
    def CreateInstance():
        return SvcAggreg()

    @staticmethod
    def GetInstance(name: str = ''):
        return WorkerRoot.GetInstance(SvcAggreg.name)

    @staticmethod
    def runMe():
        svc_agg_instance = SvcAggreg.GetInstance()
        if svc_agg_instance.Isrunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunIt()
