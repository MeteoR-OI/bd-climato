from app.models import Observation, AggHour, AggDay, AggMonth, AggYear, AggAll, AggTodo, ExtremeTodo, AggHisto
from app.models import TmpObservation, TmpAggHour, TmpAggDay, TmpAggMonth, TmpAggYear, TmpAggAll, TmpAggTodo, TmpExtremeTodo, TmpAggHisto
from app.classes.calcul.observation.processJsonDataAvg import ProcessJsonDataAvg
from app.classes.calcul.observation.processJsonDataAvgOmm import ProcessJsonDataAvgOmm
from app.classes.calcul.observation.processJsonDataRate import ProcessJsonDataRate
from app.classes.calcul.observation.processJsonDataSum import ProcessJsonDataSum
from app.classes.calcul.observation.processJsonDataSumOmm import ProcessJsonDataSumOmm
from app.classes.calcul.observation.processJsonDataNone import ProcessJsonDataNo
from app.classes.calcul.aggregations.aggAvgCompute import AggAvgCompute
from app.classes.calcul.aggregations.aggAvgOmmCompute import AvgOmmCompute
from app.classes.calcul.aggregations.aggRateCompute import AggRateCompute
from app.classes.calcul.aggregations.aggSumCompute import AggSumCompute
from app.classes.calcul.aggregations.aggSumOmmCompute import AggSumOmmCompute
from app.classes.calcul.aggregations.aggNoCompute import AggNoCompute
from app.tools.refManager import RefManager


class AllCalculus():
    all_calculus = [
        {"agg": "avg", "calc_obs": ProcessJsonDataAvg(), "calc_agg": AggAvgCompute()},
        {"agg": "avgomm", "calc_obs": ProcessJsonDataAvgOmm(), "calc_agg": AvgOmmCompute()},
        {"agg": "no", "calc_obs": ProcessJsonDataNo(), "calc_agg": AggNoCompute()},
        {"agg": "sum", "calc_obs": ProcessJsonDataSum(), "calc_agg": AggSumCompute()},    # sumCompute(), "calc_agg": None}
        {"agg": "sumomm", "calc_obs": ProcessJsonDataSumOmm(), "calc_agg": AggSumOmmCompute()},    # sumCompute(), "calc_agg": None}
        {"agg": "rate", "calc_obs": ProcessJsonDataRate(), "calc_agg": AggRateCompute()}    # ProcessJsonDataRate()}
    ]

    def __init__(self):
        self.ref_mgr = RefManager.GetInstance()

    def delete_obs_agg(self, is_tmp: bool = None):
        """clean_up all our tables"""
        if is_tmp is None:
            raise Exception('AllCalculus::delete_obs_agg', 'is_tmp not given')

        if is_tmp is False:
            AggHisto.objects.all().delete()
            Observation.objects.all().delete()
            AggHour.objects.all().delete()
            AggDay.objects.all().delete()
            AggMonth.objects.all().delete()
            AggYear.objects.all().delete()
            AggAll.objects.all().delete()
            AggTodo.objects.all().delete()
            ExtremeTodo.objects.all().delete()
        else:
            TmpAggHisto.objects.all().delete()
            TmpObservation.objects.all().delete()
            TmpAggHour.objects.all().delete()
            TmpAggDay.objects.all().delete()
            TmpAggMonth.objects.all().delete()
            TmpAggYear.objects.all().delete()
            TmpAggAll.objects.all().delete()
            TmpAggTodo.objects.all().delete()
            TmpExtremeTodo.objects.all().delete()
