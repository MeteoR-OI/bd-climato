from app.models import Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Agg_todo
from app.classes.calcul.observation.processJsonDataAvg import ProcessJsonDataAvg
from app.classes.calcul.observation.processJsonDataAvgOmm import ProcessJsonDataAvgOmm
from app.classes.calcul.observation.processJsonDataRate import ProcessJsonDataRate
from app.classes.calcul.aggregations.aggAvgCompute import AggAvgCompute
from app.classes.calcul.aggregations.svcAggreg import SvcAggreg
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.jsonPlus import JsonPlus
from app.tools.jsonValidator import checkJson
from app.tools.refManager import RefManager
from django.db import transaction
import datetime
import json


class Calculus():
    all_calculus = [
        {"agg": "avg", "calc_obs": ProcessJsonDataAvg(), "calc_agg": AggAvgCompute()},
        {"agg": "avgomm", "calc_obs": ProcessJsonDataAvgOmm(), "calc_agg": None},
        # {"agg": "no", "calc_obs": None, "calc_agg": None},
        # {"agg": "sum", "calc_obs": None, "calc_agg": None},    # sumCompute(), "calc_agg": None}
        {"agg": "rate", "calc_obs": ProcessJsonDataRate(), "calc_agg": None}    # ProcessJsonDataRate()}
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
