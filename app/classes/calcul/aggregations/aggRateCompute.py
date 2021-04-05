from app.classes.repository.obsMeteor import ObsMeteor
# from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.avgCompute import AvgCompute
from app.classes.repository.aggMeteor import AggMeteor
# from app.tools.aggTools import addJson, isFlagged, getAggDuration, loadFromExclu, calcAggDate, delKey
import json


class RateCompute(AvgCompute):
    """
        RateCompute

        Computation specific to a measure type

        M_avg becomes M_rate
        max/min are computed on M_rates, not on values

    """

    def loadAggregationDatarows(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        current_agg: AggMeteor,
        json_key: str,
        delta_values: json,
        dv_next: json,
        avg_suffix: str = '_avg',
    ):
        super(RateCompute, self).loadAggregationDatarows(
            my_measure,
            measures,
            measure_idx,
            current_agg,
            json_key,
            delta_values,
            dv_next,
            trace_flag,
            '_rate'
        )

    def loadMaxMinInAggregation(
        self, my_measure: json,
        measures: json,
        measure_idx: int,
        my_aggreg,
        json_key: str,
        exclusion: json,
        delta_values: json,
        dv_next: json,
        b_use_rate: bool = False,
    ):
        super(RateCompute, self).loadMaxMinInObservation(
            my_measure,
            measures,
            measure_idx,
            my_aggreg,
            json_key,
            exclusion,
            delta_values,
            dv_next,
            trace_flag,
            True,
        )
