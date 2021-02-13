from typing import Union
from app.classes.aggregation.rootAggreg import RootAggreg
from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
from django.db import models
import json

class AggregAvg(RootAggreg):
    """AggregAvg: aggregate measures with Average"""

    def __init__(self) -> None:
        super().__init__()
        self.aggregation_type="Avg"

    # {'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},

    def compute(self, json_obs: json, measure_def: json, agg_ds: list[models.Model], flag: bool):
        """ run : compute Avg aggregation

            json_obs: measures data
            measure_def: measure aggregated
                {   'key': 'temp_out',
                    'field': 'temp_out',
                    'avg': True,
                    'min': True,
                    'max': True,
                    'hour_deca': 0,
                    'special': 0,
                },
            agg_ds: array of aggregations
            flag: True: insert, False: delete
        """
