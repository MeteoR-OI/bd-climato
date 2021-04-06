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
            agg_j[json_key + '_omm_time'] = m_stop_date
            agg_j[json_key + '_sum'] = tmp_sum
            agg_j[json_key + '_duration'] = tmp_duration
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False:
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
                delKey(agg_j, json_key + '_omm_time')
                delKey(agg_j, json_key)
                delta_values[json_key + '_delete_me'] = True
            else:
                # compute the new _avg
                if isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False:
                    agg_j[json_key + '_avg'] = tmp_sum_new / tmp_duration_new

        # if tmp_sum_old != 0 and tmp_sum != tmp_sum_old:
        #     # mark as potential candidate for max/min regeneration
        #     delta_values[json_key + '_check_maxmin'] = True

        # propagate to next level if no limitation on aggregation level
        dv_next[json_key + '_sum'] = tmp_sum
        dv_next[json_key + '_duration'] = tmp_duration
        dv_next[json_key] = delta_values[json_key]

    # def loadMaxMinInAllAggregations(self, my_measure: json, measures: json, measure_idx: int, agg_deca, json_key: str, exclusion: json, delta_values: json, dv_next: json):
    #     """
    #         loadMaxMinInAggregation

    #         update agg_xx max/min
    #         update delta_values
    #     """
    #     # save our dv, and get agg_j, m_agg_j
    #     m_agg_j = self.get_agg_magg(agg_deca, delta_values, measures, measure_idx)
    #     agg_j = agg_deca.data.j

    #     for maxmin_suffix in ['_max', '_min']:
    #         maxmin_key = maxmin_suffix.split('_')[1]

    #         if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:

    #             if delta_values.__contains__(json_key + '_delete_me') is True:
    #                 # measure was deleted previously
    #                 if agg_j.__contains__(json_key + maxmin_suffix):
    #                     # need to invalidate this value for next level
    #                     invalid_value = agg_j[json_key + maxmin_suffix]
    #                     dv_next[json_key + maxmin_suffix + '_invalidate'] = invalid_value
    #                     self.add_new_maxmin_fix(json_key, maxmin_key, agg_deca.data.start_dat, delta_values, agg_deca)
    #                 delKey(agg_j, json_key + maxmin_suffix)
    #                 delKey(agg_j, json_key + maxmin_suffix + '_time')
    #                 delKey(agg_j, json_key + maxmin_suffix + '_omm_time')
    #                 continue

    #             current_maxmin = None

    #             if delta_values.__contains__(json_key + maxmin_suffix) is True:
    #                 # load from delta_values
    #                 current_maxmin = my_measure['dataType'](delta_values[json_key + maxmin_suffix])
    #                 current_maxmin_time = delta_values[json_key + maxmin_suffix + '_time']
    #                 if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
    #                     current_maxmin_dir = None
    #                     if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
    #                         current_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

    #             if m_agg_j.__contains__(json_key + maxmin_suffix):
    #                 # load and use measure maxmin if given
    #                 current_maxmin = my_measure['dataType'](m_agg_j[json_key + maxmin_suffix])
    #                 current_maxmin_time = m_agg_j[json_key + maxmin_suffix + '_time']
    #                 if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
    #                     current_maxmin_dir = None
    #                     if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
    #                         current_maxmin_dir = int(m_agg_j[json_key + maxmin_suffix + '_dir'])

    #             if current_maxmin is None:
    #                 # no values
    #                 continue

    #             b_change_maxmin = False
    #             # load current data from our aggregation
    #             if agg_j.__contains__(json_key + maxmin_suffix):
    #                 agg_maxmin = agg_j[json_key + maxmin_suffix]

    #                 # check if max/min value has to be replaced because omm changed
    #                 if delta_values.__contains__(json_key + maxmin_suffix + '_invalidate') and agg_maxmin == delta_values[json_key + maxmin_suffix + '_invalidate']:
    #                     # run a regeneration of our maxmin
    #                     dv_next[json_key + maxmin_suffix + '_invalidate'] = agg_maxmin
    #                     self.add_new_maxmin_fix(json_key, maxmin_key, agg_deca.data.start_dat, delta_values, agg_deca)
    #                     b_change_maxmin = True
    #             else:
    #                 b_change_maxmin = True
    #                 # force the usage of tmp_maxmin
    #                 if maxmin_suffix == '_min':
    #                     agg_maxmin = current_maxmin + 1
    #                 else:
    #                     agg_maxmin = current_maxmin - 1

    #             # do we need to change our maxmin
    #             if agg_deca.agg_niveau != 'H':
    #                 if (maxmin_suffix == '_max' and agg_maxmin < current_maxmin) or (maxmin_suffix == '_min' and agg_maxmin > current_maxmin):
    #                     b_change_maxmin = True

    #             if b_change_maxmin is True:
    #                 # we need to change the omm value
    #                 agg_j[json_key + maxmin_suffix] = current_maxmin
    #                 dv_next[json_key + maxmin_suffix] = current_maxmin
    #                 agg_j[json_key + maxmin_suffix + '_time'] = current_maxmin_time
    #                 dv_next[json_key + maxmin_suffix + '_time'] = current_maxmin_time
    #                 if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
    #                     if current_maxmin_dir is not None:
    #                         agg_j[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir
    #                         dv_next[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir
