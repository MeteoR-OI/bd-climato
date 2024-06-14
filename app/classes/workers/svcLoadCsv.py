from app.classes.csv_loader.csvLoader import CsvLoader
from app.classes.workers.workerRoot import WorkerRoot
import json


class SvcCsvLoader(WorkerRoot):
    """
        SvcAggregate

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcCsvLoader, self).__init__(
            self,
            '{0}'.format(SvcCsvLoader),
            CsvLoader(),
            30,
            ['svcCsvLoader', 'autoloadcsv', 'loadcsv', 'csv'],
        )

    def GetWorkerRoot(self):
        return super(SvcCsvLoader, self)

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcCsvLoader)

    @staticmethod
    def runMe(params: json = {}):
        svc_json_loader = SvcCsvLoader.GetInstance()
        if svc_json_loader.IsRunning() is False:
            svc_json_loader.Start()
        # svc_json_loader.RunMe(params)
