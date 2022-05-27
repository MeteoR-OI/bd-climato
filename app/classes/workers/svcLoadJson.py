

from app.classes.json_loader.jsonLoader import JsonLoader
from app.classes.workers.workerRoot import WorkerRoot
import json


class SvcJsonLoader(WorkerRoot):
    """
        SvcAggregate

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcJsonLoader, self).__init__(
            self,
            str(SvcJsonLoader),
            JsonLoader(),
            30,
            ['svcJsonLoader', 'autoload', 'auto', 'load', 'loadjson', 'json'],
        )

    def GetWorkerRoot(self):
        return super(SvcJsonLoader, self)

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcJsonLoader)

    @staticmethod
    def runMe(params: json = {}):
        svc_json_loader = SvcJsonLoader.GetInstance()
        if svc_json_loader.IsRunning() is False:
            svc_json_loader.Start()
        # svc_json_loader.RunMe(params)
