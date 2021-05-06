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
    def loadDVInAggregation(
        self,
        my_measure: json,
        m_stop_dat: datetime,
        agg_deca: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        key_suffix: str = '_avg',
    ):
        """
            loadLevelAggregation

            Load one aggretation level with values from delta_values, update dv_next

            parameters:
                my_measure: measure definition
                mesures: json data used as input
                mesure_idx: indice in the data section
                agg_deca
                m_agg_j: aggregations clause in json file
                delta_values: json for forced values
                dv_next: delta_values for next level
                flag: True=insert, False=delete
        """
        json_key = self.get_json_key(my_measure)
        agg_j = agg_deca.data.j
        tmp_value = None
        has_data = False

        # load old measure values in case of an update of Observation, and only in agg_hour
        tmp_s_old = tmp_duration_old = 0
        if delta_values.__contains__(json_key + '_s_old'):
            tmp_s_old = delta_values[json_key + '_s_old']
            tmp_duration_old = delta_values[json_key + '_duration_old']
            has_data = True

        # ------------------------------------------------------------------
        # get our new data
        # 1 from dv[json_key + '_s']
        # 2 from m_agg_j[json_key_s]
        # 3 from m_agg_j[json_key_avg]
        # last win
        # ------------------------------------------------------------------

#a virer
        if delta_values.get('duration') is None:
            tmp_duration = 5
        else:
            tmp_duration = float(delta_values["duration"])

        # get our M_s from our delta_values
        tmp_ss = self.get_json_value(delta_values, json_key + '_s', [], True)
        if tmp_ss is not None:
            has_data = True
            tmp_s = float(tmp_ss)

        tmp_sagg = self.get_json_value(m_agg_j, json_key, [key_suffix, '_s'], None)
        if tmp_sagg is not None:
            has_data = True
            tmp_s = float(tmp_sagg)
            if m_agg_j.__contains__(json_key + '_duration') is True:
                tmp_duration = float(m_agg_j[json_key + '_duration'])
                tmp_s = tmp_value * tmp_duration

        # return if the aggregation should not be sent to upper levels
        if has_data is False:
            return

        agg_deca.dirty = True

        addJson(agg_j, json_key + '_s', tmp_s - tmp_s_old)
        addJson(agg_j, json_key + '_duration', tmp_duration - tmp_duration_old)

        tmp_s_new = agg_j[json_key + '_s']
        tmp_duration_new = agg_j[json_key + '_duration']

        if tmp_duration_new == 0:
            # no duration, delete all keys
            delKey(agg_j, json_key + '_s')
            delKey(agg_j, json_key + '_duration')
            delta_values[json_key + '_delete_me'] = True
        else:
            agg_j[json_key + key_suffix] = tmp_s_new / tmp_duration_new

        if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
            return

        # propagate to next level if no limitation on aggregation level
        dv_next[json_key + '_s'] = tmp_s - tmp_s_old
        dv_next[json_key + '_duration'] = tmp_duration - tmp_duration_old
        dv_next["duration"] = tmp_duration
