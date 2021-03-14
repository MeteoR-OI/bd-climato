from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.avgCompute import avgCompute
from app.tools.aggTools import addJson, isFlagged, getAggDuration, delKey
import json


class avgOmmCompute(avgCompute):
    """
        avgOmmCompute

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

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
    ):
        """ generate deltaValues from ObsMeteor.data """
        super(avgOmmCompute, self).loadObservationDatarow(
            my_measure,
            measures,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            exclusion,
            delta_values,
            True,
        )
        # we will invalidate only if our omm value is changed
        delKey(delta_values, target_key + '_maxmin_invalid_val_max')
        delKey(delta_values, target_key + '_maxmin_invalid_val_min')

    def loadAggregationDatarows(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        current_agg: AggMeteor,
        json_key: str,
        delta_values: json,
        dv_next: json,
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
        # if we get no data, return
        if delta_values.__contains__(json_key) is False:
            return

        # for tracing, save inputed delta_values in dv
        agg_j, m_agg_j = self.savedv_and_get_agg_magg(current_agg, delta_values, measures, measure_idx)

        tmp_sum = tmp_duration = None

        # load old values
        tmp_sum_old = tmp_duration_old = 0
        if agg_j.__contains__(json_key + '_sum'):
            tmp_sum_old = agg_j[json_key + '_sum']
            tmp_duration_old = agg_j[json_key + '_duration']

        # get our new data
        if delta_values.__contains__(json_key + '_sum'):
            tmp_sum = float(delta_values[json_key + '_sum'])
            tmp_duration = float(delta_values[json_key + '_duration'])

        # if we got a forced sum/duration
        if m_agg_j.__contains__(json_key + '_sum'):
            tmp_sum = m_agg_j[json_key + '_sum']
            tmp_duration = m_agg_j[json_key + '_duration']

        # we got a forced avg in the aggregation part of our json.
        # avg can be given without a sum, or a duration...
        if m_agg_j.__contains__(json_key + '_avg'):
            tmp_avg = float(m_agg_j[json_key + '_avg'])
            if m_agg_j.__contains__(json_key + '_duration'):
                tmp_duration = m_agg_j[json_key + '_duration']
            else:
                if measures['data'][measure_idx].__contains__('current'):
                    # use the duration of the meaure json if one is given
                    tmp_duration = measures['data'][measure_idx]['current']['duration']
                else:
                    # no duration given, don't use the one in delta_values
                    # use the full duration of the agregation
                    tmp_duration = getAggDuration(m_agg_j.djson)
            tmp_sum = tmp_avg * tmp_duration

        # specific omm processing
        if current_agg.agg_niveau == 'H':
            tmp_first_dt = delta_values[json_key + '_first_time']
            if agg_j.__contains__(json_key + '_first_time'):
                tmp_first_dt = agg_j[json_key + '_first_time']

            if tmp_first_dt < delta_values[json_key + '_first_time']:
                # no change in our current omm values
                return

            # save in our agg_h_sum, _duration _first_time
            tmp_val = tmp_sum / tmp_duration
            tmp_sum = tmp_val * 60
            tmp_duration = 60
            agg_j[json_key + '_first_time'] = delta_values[json_key + '_first_time']
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

            # return if the aggregation should not be sent to upper levels
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
                return

            # propagate the delta
            tmp_sum = tmp_sum - tmp_sum_old
            tmp_duration = tmp_duration - tmp_duration_old
        else:
            addJson(agg_j, json_key + '_sum', tmp_sum)
            addJson(agg_j, json_key + '_duration', tmp_duration)

            tmp_duration_new = agg_j[json_key + '_duration']
            if tmp_duration_new == 0:
                # no duration, delete all keys
                delKey(agg_j, json_key + '_sum')
                delKey(agg_j, json_key + '_duration')
                delKey(agg_j, json_key + '_avg')
                delKey(agg_j, json_key)
                agg_j[json_key + '_delete_me'] = True
                dv_next = {"extremesFix": [], "maxminFix": []}
            else:
                # compute the new _avg
                tmp_sum_new = agg_j[json_key + '_sum']
                tmp_duration_new = agg_j[json_key + '_duration']
                if isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False:
                    agg_j[json_key + '_avg'] = tmp_sum_new / tmp_duration_new

        if tmp_sum_old != 0 and tmp_sum != tmp_sum_old:
            # mark as potential candidate for max/min regeneration
            delta_values[json_key + '_check_maxmin'] = True

        # propagate to next level if no limitation on aggregation level
        dv_next[json_key + '_sum'] = tmp_sum
        dv_next[json_key + '_duration'] = tmp_duration
        dv_next[json_key] = delta_values[json_key]

    def loadMaxMinInAggregation(self, my_measure: json, measures: json, measure_idx: int, my_aggreg, json_key: str, exclusion: json, delta_values: json, dv_next: json):
        """
            loadMaxMinInAggregation

            update agg_xx max/min
            update delta_values
        """
        # save our dv, and get agg_j, m_agg_j
        agg_j, m_agg_j = self.savedv_and_get_agg_magg(my_aggreg, delta_values, measures, measure_idx)

        for maxmin_suffix in ['_max', '_min']:
            maxmin_key = maxmin_suffix.split('_')[1]

            if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:

                if agg_j.__contains__(json_key + '_delete_me') is True:
                    # measure was deleted previously
                    delKey(agg_j, json_key + maxmin_suffix + '_max')
                    delKey(agg_j, json_key + maxmin_suffix + '_max_time')
                    delKey(agg_j, json_key + maxmin_suffix + '_min')
                    delKey(agg_j, json_key + maxmin_suffix + '_min_time')
                    delKey(agg_j, json_key + maxmin_suffix + '_first_time')
                    continue

                current_maxmin = None

                if delta_values.__contains__(json_key + maxmin_suffix) is True:
                    # load from delta_values
                    current_maxmin = my_measure['dataType'](delta_values[json_key + maxmin_suffix])
                    current_maxmin_time = delta_values[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        current_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

                if m_agg_j.__contains__(json_key + maxmin_suffix):
                    # load and use measure maxmin if given
                    current_maxmin = my_measure['dataType'](m_agg_j[json_key + maxmin_suffix])
                    current_maxmin_time = m_agg_j[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        current_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(m_agg_j[json_key + maxmin_suffix + '_dir'])

                if current_maxmin is None:
                    # no values
                    continue

                b_change_maxmin = False
                # load current data from our aggregation
                if agg_j.__contains__(json_key + maxmin_suffix):
                    agg_maxmin = agg_j[json_key + maxmin_suffix]

                    # check if max/min value has to be replaced because omm changed
                    if delta_values.__contains__(json_key + '_maxmin_invalid_val' + maxmin_suffix) and agg_maxmin == delta_values[json_key + '_maxmin_invalid_val' + maxmin_suffix]:
                        # run a regeneration of our maxmin
                        dv_next[json_key + '_maxmin_invalid_val' + maxmin_suffix] = agg_maxmin
                        self.add_new_maxmin_fix(json_key, maxmin_key, my_aggreg.data.start_dat, delta_values, my_aggreg)
                        b_change_maxmin = True
                else:
                    b_change_maxmin = True
                    # force the usage of tmp_maxmin
                    if maxmin_suffix == '_min':
                        agg_maxmin = current_maxmin + 1
                    else:
                        agg_maxmin = current_maxmin - 1

                # do we need to change our maxmin
                if my_aggreg.data.level != 'H':
                    if (maxmin_suffix == '_max' and agg_maxmin < current_maxmin) or (maxmin_suffix == '_min' and agg_maxmin > current_maxmin):
                        b_change_maxmin = True

                if b_change_maxmin is True:
                    # we need to change the omm value
                    agg_j[json_key + maxmin_suffix] = current_maxmin
                    dv_next[json_key + maxmin_suffix] = current_maxmin
                    agg_j[json_key + maxmin_suffix + '_time'] = current_maxmin_time
                    dv_next[json_key + maxmin_suffix + '_time'] = current_maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if current_maxmin_dir is not None:
                            agg_j[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir
                            dv_next[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir
