from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.aggregations.aggCompute import AggCompute
from app.tools.aggTools import addJson, isFlagged, delKey
import json
import datetime


class AvgOmmCompute(AggCompute):
    """
        AvgOmmCompute

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """

    def loadDVInAllAggregations(
        self,
        my_measure: json,
        m_stop_date: datetime,
        agg_deca: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        avg_suffix: str = '_avg',
    ):
        """
            loadAggregationDatarows

            Load one aggretation value from delta_values, update dv_next

            parameters:
                my_measure: measure definition
                mesures: json data used as input
                mesure_idx: indice in the data section
                agg_j_relative: our aggregation to update
                json_key : key name (target_key)
                delta_value: json for forced values
                dv_next: delta_values for next level
                flag: True=insert, False=delete
        """
        json_key = self.get_json_key(my_measure)

        # if we get no data, return
        if delta_values.__contains__(json_key) is False:
            return

        dv_next["duration"] = delta_values["duration"]

        # mark our aggregation as dirty
        agg_deca.dirty = True
        agg_j = agg_deca.data.j

        # load old values
        tmp_sum_old = tmp_duration_old = 0
        if agg_j.__contains__(json_key + '_sum'):
            tmp_sum_old = agg_j[json_key + '_sum']
            tmp_duration_old = agg_j[json_key + '_duration']

        # ------------------------------------------------------------------
        # get our new data
        # 1 from dv[json_key]
        # 2 from dv[json_key_sum]
        # 3 from m_agg_j[json_key_sum]
        # 4 if m_agg_j[json_key_avg] is given, recompute a new json_key_sum
        # ------------------------------------------------------------------
        tmp_duration = float(delta_values["duration"])
        tmp_sum = float(delta_values[json_key]) * tmp_duration

        if delta_values.__contains__(json_key + '_sum'):
            tmp_sum = float(delta_values[json_key + '_sum'])
            if delta_values.__contains__(json_key + '_duration') is True:
                tmp_duration = float(delta_values[json_key + '_duration'])

        if m_agg_j.__contains__(json_key + '_sum'):
            tmp_sum = float(m_agg_j[json_key + '_sum'])
            if m_agg_j.__contains__(json_key + '_duration') is True:
                tmp_duration = float(m_agg_j[json_key + '_duration'])

        if m_agg_j.__contains__(json_key + '_avg'):
            tmp_avg = float(m_agg_j[json_key + '_avg'])
            if m_agg_j.__contains__(json_key + '_duration'):
                tmp_duration = m_agg_j[json_key + '_duration']
            tmp_sum = tmp_avg * tmp_duration

        # specific omm processing
        if agg_deca.agg_niveau == 'H':
            # we only store values a round hours
            if m_stop_date.minute > 0 or m_stop_date.second > 1:
                return

            # save in our agg_h_sum, _duration _first_time
            tmp_val = tmp_sum / tmp_duration
            tmp_sum = tmp_val * 60
            tmp_duration = 60
            agg_j[json_key] = tmp_val
            agg_j[json_key + '_time'] = m_stop_date
            agg_j[json_key + '_sum'] = tmp_sum
            agg_j[json_key + '_duration'] = tmp_duration
            if my_measure.__contains__('avg') is False or my_measure['avg'] is True:
                agg_j[json_key + '_avg'] = tmp_sum / tmp_duration

            # invalidate max/min if omm value is changed
            if tmp_sum_old != 0:
                tmp_invalid_val = tmp_sum_old/tmp_duration_old
                delta_values[json_key + '_maxmin_invalid_val_max'] = tmp_invalid_val
                dv_next[json_key + '_maxmin_invalid_val_max'] = tmp_invalid_val
                delta_values[json_key + '_maxmin_invalid_val_min'] = tmp_invalid_val
                dv_next[json_key + '_maxmin_invalid_val_min'] = tmp_invalid_val

            # propagate the delta of tmp_sum/duration to dv_next
            tmp_sum = tmp_sum - tmp_sum_old
            tmp_duration = tmp_duration - tmp_duration_old
        else:
            # return if the aggregation should not be sent to upper levels
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
                return

            addJson(agg_j, json_key + '_sum', tmp_sum)
            addJson(agg_j, json_key + '_duration', tmp_duration)
            tmp_sum_new = agg_j[json_key + '_sum']
            tmp_duration_new = agg_j[json_key + '_duration']

            if tmp_duration_new == 0:
                # no duration, delete all keys
                delKey(agg_j, json_key + '_sum')
                delKey(agg_j, json_key + '_duration')
                delKey(agg_j, json_key + '_avg')
                delKey(agg_j, json_key + '_time')
                delKey(agg_j, json_key)
                delta_values[json_key + '_delete_me'] = True
            else:
                # compute the new _avg
                if my_measure.__contains__('avg') is False or my_measure['avg'] is True:
                    agg_j[json_key + '_avg'] = tmp_sum_new / tmp_duration_new

        # propagate to next level if no limitation on aggregation level
        dv_next[json_key + '_sum'] = tmp_sum
        dv_next[json_key + '_duration'] = tmp_duration
        dv_next[json_key] = delta_values[json_key]

    def loadMaxMinInAllAggregations(
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
        super().loadMaxMinInAllAggregations(my_measure, m_stop_date, agg_deca, m_agg_j, delta_values, dv_next, trace_flag, False)
