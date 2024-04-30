from app.classes.csv_loader.pluvioLoader import PluvioLoader
from app.classes.workers.workerRoot import WorkerRoot
import json


class SvcPluvioLoader(WorkerRoot):
    """
        SvcAggregate

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcPluvioLoader, self).__init__(
            self,
            str(SvcPluvioLoader),
            PluvioLoader(),
            30,
            ['SvcPluvioLoader', 'autoloadpluvio', 'loadpluvio', 'pluvio'],
        )

    def GetWorkerRoot(self):
        return super(SvcPluvioLoader, self)

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcPluvioLoader)

    @staticmethod
    def runMe(params: json = {}):
        svc_json_loader = SvcPluvioLoader.GetInstance()
        if svc_json_loader.IsRunning() is False:
            svc_json_loader.Start()
        # svc_json_loader.RunMe(params)
