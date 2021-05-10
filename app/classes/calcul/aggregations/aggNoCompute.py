from app.classes.repository.aggMeteor import AggMeteor
from app.classes.calcul.aggregations.aggCompute import AggCompute
import json
import datetime


class AggNoCompute(AggCompute):
    """
        AvgCompute

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """
    def loadDVDataInAggregation(
        self,
        my_measure: json,
        m_stop_dat: datetime,
        agg_deca: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        avg_suffix: str = '_avg',
    ):
        return

    def loadDVMaxMinInAggregation(
        self,
        my_measure: json,
        m_stop_date: datetime,
        agg_decas: list,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        b_use_rate: bool = False,
    ):
        super().loadDVMaxMinInAggregation(my_measure, m_stop_date, agg_decas, m_agg_j, delta_values, dv_next, trace_flag)
