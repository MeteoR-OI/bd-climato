from app.classes.repository.aggMeteor import AggMeteor
from app.classes.calcul.aggregations.aggCompute import AggCompute
import json
import datetime


class AggRateCompute(AggCompute):
    """
        RateCompute

        Computation specific to a measure type

        M_avg becomes M_rate
        max/min are computed on M_rates, not on values

    """

    def loadDVDataInAggregation(
        self,
        my_measure: json,
        m_stop_date: datetime,
        agg_deca: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
    ):
        super(AggRateCompute, self).loadDVDataInAggregation(
            my_measure,
            m_stop_date,
            agg_deca,
            m_agg_j,
            delta_values,
            dv_next,
            trace_flag,
            '_rate'
        )

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

