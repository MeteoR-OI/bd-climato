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

    def loadObservationDatarow(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        isOmm: bool = False,
        avg_suffix: str = '_rate',
    ):
        """ generate deltaValues from ObsMeteor.data """
        # force avg to be computed
        my_measure['avg'] = True
        super(RateCompute, self).loadObservationDatarow(
            my_measure,
            measures,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            exclusion,
            delta_values,
            False,
            '_rate'
        )

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
            '_rate'
        )

    def loadMaxMinInObservation(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        b_use_rate: bool = False,
    ):
        super(RateCompute, self).loadMaxMinInObservation(
            my_measure,
            measures,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            delta_values,
            True,
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
            True,
        )
