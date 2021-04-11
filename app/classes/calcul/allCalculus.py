from app.models import Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Agg_todo
from app.classes.calcul.observation.processJsonDataAvg import ProcessJsonDataAvg
from app.classes.calcul.observation.processJsonDataAvgOmm import ProcessJsonDataAvgOmm
from app.classes.calcul.observation.processJsonDataRate import ProcessJsonDataRate
from app.classes.calcul.aggregations.aggAvgCompute import AggAvgCompute
from app.classes.calcul.aggregations.aggAvgOmmCompute import AvgOmmCompute
from app.classes.calcul.aggregations.aggRateCompute import RateCompute
from app.tools.refManager import RefManager


class AllCalculus():
    all_calculus = [
        {"agg": "avg", "calc_obs": ProcessJsonDataAvg(), "calc_agg": AggAvgCompute()},
        {"agg": "avgomm", "calc_obs": ProcessJsonDataAvgOmm(), "calc_agg": AvgOmmCompute()},
        # {"agg": "no", "calc_obs": None, "calc_agg": None},
        # {"agg": "sum", "calc_obs": None, "calc_agg": None},    # sumCompute(), "calc_agg": None}
        {"agg": "rate", "calc_obs": ProcessJsonDataRate(), "calc_agg": RateCompute()}    # ProcessJsonDataRate()}
    ]

    def __init__(self):
        self.ref_mgr = RefManager.GetInstance()

    def delete_obs_agg(self):
        """clean_up all our tables"""
        Observation.objects.all().delete()
        Agg_hour.objects.all().delete()
        Agg_day.objects.all().delete()
        Agg_month.objects.all().delete()
        Agg_year.objects.all().delete()
        Agg_global.objects.all().delete()
        Agg_todo.objects.all().delete()
