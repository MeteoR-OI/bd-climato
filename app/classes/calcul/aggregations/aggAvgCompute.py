from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.aggregations.aggCompute import AggCompute
from app.tools.aggTools import addJson, isFlagged, delKey
import json
import datetime


class AggAvgCompute(AggCompute):
    """
        AvgCompute

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """

    def loadLevelAggregation(
        self,
        my_measure: json,
        m_stop_date: datetime,
        current_agg: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        avg_suffix: str = '_avg',
    ):
        """
            loadLevelAggregation

            Load one aggretation level with values from delta_values, update dv_next

            parameters:
                my_measure: measure definition
                mesures: json data used as input
                mesure_idx: indice in the data section
                current_agg
                json_key : key name (target_key)
                delta_values: json for forced values
                dv_next: delta_values for next level
                flag: True=insert, False=delete
        """
        json_key = self.get_json_key(my_measure)

        # if we get no data, return
        if delta_values.__contains__(json_key) is False:
            return

        # mark our aggregation as dirty
        current_agg.dirty = True
        agg_j = current_agg.data.j

        if my_measure['avg'] is True:
            tmp_sum = tmp_duration = None

            # load old measure values (only in agg_hour)
            tmp_sum_old = tmp_duration_old = 0
            if delta_values.__contains__(json_key + '_sum_old'):
                tmp_sum_old = delta_values[json_key + '_sum_old']
                tmp_duration_old = delta_values[json_key + '_duration_old']

            # get our new data
            if delta_values.__contains__(json_key + '_sum'):
                tmp_sum = float(delta_values[json_key + '_sum'])
                tmp_duration = float(delta_values[json_key + '_duration'])

            # if we got a forced sum/duration
            if m_agg_j.__contains__(json_key + '_sum'):
                tmp_sum = m_agg_j[json_key + '_sum']
                if m_agg_j.__contains__(json_key + "_duration"):
                    tmp_duration = m_agg_j[json_key + '_duration']
                else:
                    tmp_duration = delta_values["duration"]

            # we got a forced avg in the aggregation part of our json.
            # avg can be given without a sum, or a duration...
            if m_agg_j.__contains__(json_key + avg_suffix):
                tmp_avg = float(m_agg_j[json_key + avg_suffix])
                if m_agg_j.__contains__(json_key + '_duration'):
                    tmp_duration = m_agg_j[json_key + '_duration']
                else:
                    tmp_duration = delta_values["duration"]
                tmp_sum = tmp_avg * tmp_duration

            addJson(agg_j, json_key + '_sum', tmp_sum - tmp_sum_old)
            addJson(agg_j, json_key + '_duration', tmp_duration - tmp_duration_old)

            tmp_duration_new = agg_j[json_key + '_duration']
            if tmp_duration_new == 0:
                # no duration, delete all keys
                delKey(agg_j, json_key + '_sum')
                delKey(agg_j, json_key + '_duration')
                delKey(agg_j, json_key + avg_suffix)
                delKey(agg_j, json_key)
                agg_j[json_key + '_delete_me'] = True
                dv_next = {"maxminFix": []}
            else:
                # compute the new _avg
                tmp_sum_new = agg_j[json_key + '_sum']
                tmp_duration_new = agg_j[json_key + '_duration']
                if isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False:
                    agg_j[json_key + avg_suffix] = tmp_sum_new / tmp_duration_new

            # propagate to next level if no limitation on aggregation level
            dv_next[json_key + '_sum'] = tmp_sum - tmp_sum_old
            dv_next[json_key + '_duration'] = tmp_duration - tmp_duration_old
            dv_next[json_key] = delta_values[json_key]

        # propagate our value to next level
        dv_next[json_key] = delta_values[json_key]
        dv_next["duration"] = delta_values["duration"]

        # return if the aggregation should not be sent to upper levels
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
            dv_next = {"maxminFix": []}
