from app.classes.workers.workerRoot import WorkerRoot
from app.classes.migrate import 
import json


class SvcAggregate(WorkerRoot):
    """
        SvcAggregate

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcAggregate, self).__init__(
            str(SvcAggregate), CalcAggreg().ComputeAggregFromSvc,
            120,
            ['agg', 'aggreg', 'agreg', 'agregation', 'aggregation', 'agregate', 'aggregate'],
            True)

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcAggregate)

    @staticmethod
    def runMe(params: json = {}):
        svc_agg_instance = SvcAggregate.GetInstance()
        if svc_agg_instance.IsRunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunMe(params)
