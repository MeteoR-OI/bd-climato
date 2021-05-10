from app.classes.repository.aggMeteor import AggMeteor
from app.classes.calcul.aggregations.aggSumCompute import AggSumCompute
from app.tools.aggTools import isFlagged
from app.tools.climConstant import MeasureProcessingBitMask
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
        if m_stop_date.minute > 0 or m_stop_date.second > 1:
            return
        if str(agg_decas[1].getLevel()[0]).lower() == 'h':
            # get the max/min of the value from the agg_hour
            target_key = my_measure['target_key']
            src_key = my_measure['src_key']
            agg_j = agg_decas[0].data.j
            for maxmin_suffix in ['_max', '_min']:
                if agg_j.__contains__(src_key + maxmin_suffix):
                    delta_values[target_key + maxmin_suffix] = my_measure['dataType'](agg_j[src_key + maxmin_suffix])
                    delta_values[target_key + maxmin_suffix + '_time'] = agg_j[src_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if agg_j.__contains__(src_key + maxmin_suffix + '_dir') is True:
                            delta_values[target_key + maxmin_suffix + '_dir'] = float(agg_j[target_key + maxmin_suffix + '_dir'])

        super().loadDVMaxMinInAggregation(my_measure, m_stop_date, agg_decas, m_agg_j, delta_values, dv_next, trace_flag)
