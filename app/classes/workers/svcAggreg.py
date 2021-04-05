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
