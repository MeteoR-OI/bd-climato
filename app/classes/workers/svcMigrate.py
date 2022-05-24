from app.classes.workers.workerRoot import WorkerRoot
from app.classes.migrate.migrate import MigrateDB
import json


class SvcMigrate(WorkerRoot):
    """
        SvcAggregate

        Service for Aggregation Computations
    """

    def __init__(self, is_tmp: bool = None):
        # call parent __init__
        super(SvcMigrate, self).__init__(
            str(SvcMigrate),
            MigrateDB(),
            120,
            ['migrate'],
            True)

    @staticmethod
    def GetInstance(myClass: object = None):
        return WorkerRoot.GetInstance(SvcMigrate)

    @staticmethod
    def runMe(params: json = {}):
        svc_agg_instance = SvcMigrate.GetInstance()
        if svc_agg_instance.IsRunning() is False:
            svc_agg_instance.Start()
        svc_agg_instance.RunMe(params)
