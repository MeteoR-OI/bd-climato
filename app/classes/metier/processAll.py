from app.classes.calcul.avgCompute import AvgCompute
from app.classes.calcul.avgOmmCompute import AvgOmmCompute
from app.classes.calcul.rateCompute import RateCompute


class ProcessAll():
    """
        ProcessAll

        Manage all compute objects

    """
    process_type = [
        {"agg": "avg", "object": AvgCompute()},
        {"agg": "aggomm", "object": AvgOmmCompute()}
        {"agg": "rate", "object": RateCompute()}
    ]

    def get(self, agg: str):
        """ get a type_process instance """
        for aprocess in self.process_type:
            if aprocess['agg'] == agg:
                return aprocess['object']
        raise Exception("ProcessAll.get", "agg with no compute module: " + agg)
