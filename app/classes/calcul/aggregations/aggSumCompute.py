from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.aggregations.aggCompute import AggCompute
from app.tools.aggTools import addJson, isFlagged, delKey, getAggDuration
import json
import datetime


class AggSumCompute(AggCompute):
    """
        AggSumCompute

        Computation specific to a measure type

        must load dv[M_s], and dv[M_duration]

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
        agg_suffix: str = '_sum'
    ):
        """
            loadDVDataInAggregation

            Load one aggretation level with values from delta_values, update dv_next

            parameters:
                my_measure: measure definition
                stop_dat: mesure stop_dat
                agg_deca
                m_agg_j: aggregations clause in json file
                delta_values: json for forced values
                dv_next: delta_values for next level
                flag: True=insert, False=delete
        """
        target_key = my_measure['target_key']
        agg_j = agg_deca.data.j
        agg_level = agg_deca.getLevelCode()
        has_data = False

        if target_key == 'rain_omm':
            has_data = False

        # load old measure values in case of an update of Observation, and only in agg_hour
        tmp_sum_old = tmp_duration_old = 0
        if delta_values.__contains__(target_key + '_sum_old'):
            tmp_sum_old = delta_values[target_key + '_sum_old']
            tmp_duration_old = delta_values[target_key + '_duration_old']
            has_data = True

        # ------------------------------------------------------------------
        # get our new data
        # 1 from dv[target_key + '_sum']
        # 2 from m_agg_j[target_key + '_sum']
        # last win
        # ------------------------------------------------------------------

        if delta_values.get('duration') is None:
            tmp_duration = getAggDuration(agg_level[0])
        else:
            tmp_duration = float(delta_values["duration"])

        # get our M_s from our delta_values
        tmp_tmp = self.get_json_value(delta_values, target_key, [agg_suffix], None)
        if tmp_tmp is not None:
            has_data = True
            tmp_sum = float(tmp_tmp)
        if delta_values.get(target_key + '_duration') is not None:
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm) and agg_level[0] == 'H':
                tmp_duration = getAggDuration(agg_level[0])
            else:
                tmp_duration = delta_values[target_key + '_duration']

        synos = [target_key]
        if my_measure.get('syno') is not None:
            for a_syno in my_measure['syno']:
                synos.append(a_syno)

        b_value_found = False
        for a_key in synos:
            if b_value_found:
                continue
            tmp_tmp = self.get_json_value(m_agg_j, a_key, [agg_suffix], True)
            if tmp_tmp is not None:
                has_data = True
                tmp_sum = float(tmp_tmp)
                if m_agg_j.__contains__(a_key + '_duration') is True:
                    tmp_duration = float(m_agg_j[a_key + '_duration'])
                else:
                    tmp_duration = getAggDuration(agg_level[0])
                if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
                    tmp_duration = getAggDuration(agg_level[0])
                b_value_found = True

        # return if the aggregation should not be sent to upper levels
        if has_data is False:
            return

        agg_deca.dirty = True

        addJson(agg_j, target_key + agg_suffix, tmp_sum - tmp_sum_old)
        addJson(agg_j, target_key + '_duration', tmp_duration - tmp_duration_old)

        tmp_sum_new = agg_j[target_key + agg_suffix]
        tmp_duration_new = agg_j[target_key + '_duration']

        if tmp_duration_new == 0:
            # no duration, delete all keys
            delKey(agg_j, target_key + agg_suffix)
            delKey(agg_j, target_key + '_duration')
            delta_values[target_key + '_delete_me'] = True
        else:
            # Add omm values in agg_hour
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
                agg_j[target_key] = tmp_sum_new

        if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
            return

        # propagate to next level if no limitation on aggregation level
        dv_next[target_key + agg_suffix] = tmp_sum - tmp_sum_old
        dv_next[target_key + '_duration'] = tmp_duration - tmp_duration_old
        if delta_values.get('duration') is None:
            dv_next['duration'] = tmp_duration
        else:
            dv_next["duration"] = delta_values['duration']

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