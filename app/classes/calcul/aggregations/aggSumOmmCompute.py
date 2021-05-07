from app.classes.repository.aggMeteor import AggMeteor
from app.classes.calcul.aggregations.aggSumCompute import AggSumCompute
import json
import datetime


class AggSumOmmCompute(AggSumCompute):
    """
        AvgOmmCompute

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
    ):
        # specific omm processing
        if agg_deca.agg_niveau[0] == 'H':
            if m_stop_dat.minute > 0 or m_stop_dat.second > 1:
                return
        super().loadDVDataInAggregation(my_measure, m_stop_dat, agg_deca, m_agg_j, delta_values, dv_next, trace_flag)

    def loadMaxMinInAggregation(
        self,
        my_measure: json,
        m_stop_date: datetime,
        agg_deca: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        b_use_rate: bool = False,
    ):
        if m_stop_date.minute > 0 or m_stop_date.second > 1:
            return
        super().loadMaxMinInAggregation(my_measure, m_stop_date, agg_deca, m_agg_j, delta_values, dv_next, trace_flag, False)
