from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.avgCompute import avgCompute
from app.tools.aggTools import addJson, isFlagged, getAggDuration
import datetime
import json


class avgOmmCompute(avgCompute):
    """
        avgOmmCompute

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """

    def loadObservationDatarow(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, src_key: str, target_key: str, exclusion: json, delta_values: json, flag: bool):
        """ generate deltaValues from ObsMeteor.data """
        super(avgOmmCompute, self).loadObservationDatarow(my_measure, measures, measure_idx, obs_meteor, src_key, target_key, exclusion, delta_values, flag, True)

    def loadAggregationDatarows(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        agg_relative: AggMeteor,
        json_key: str,
        delta_values: json,
        dv_next: json,
        flag: bool,
    ):
        """
            loadAggGetDelta

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
        if flag is False:
            raise Exception('loadAggGetDelta', 'flag = False -> not coded yet')

        if isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField):
            return

        # for tracing, save inputed delta_values in dv
        agg_j = agg_relative.data.j
        if agg_j.__contains__('dv') is False:
            agg_j['dv'] = {}
        for akey in delta_values.items():
            agg_j['dv'][akey[0]] = delta_values[akey[0]]

        # get aggregation values in measures
        m_agg_j = {}
        if measures.__contains__('data') and measures['data'][measure_idx].__contains__('aggregations'):
            for a_j_agg in measures['data'][measure_idx]['aggregations']:
                if a_j_agg['level'] == agg_relative.data.level:
                    m_agg_j = a_j_agg
                    break

        # if we get a sum, save it in current aggregation, and for next level
        if delta_values.__contains__(json_key + '_sum') is False:
            tmp_sum = tmp_duration = 0
            if delta_values.__contains__(json_key + '_avg') is False:
                return
        else:
            tmp_sum = float(delta_values[json_key + '_sum'])
            tmp_duration = float(delta_values[json_key + '_duration'])

        # we got a forced avg in the json.
        if m_agg_j.__contains__(json_key + '_avg'):
            tmp_avg = float(m_agg_j[json_key + '_avg'])
            if m_agg_j.__contains__(json_key + '_duration'):
                tmp_duration = m_agg_j[json_key + '_duration']
            else:
                # use the duration of the json if one is given
                if measures['data'][measure_idx].__contains__('current'):
                    tmp_duration = measures['data'][measure_idx]['current']['duration']
                else:
                    # no duration given, then we use the full duration of the agregation
                    tmp_duration = getAggDuration(agg_relative.data.level)
            tmp_sum = tmp_avg * tmp_duration

        # load old values
        tmp_sum_old = tmp_duration_old = 0
        if agg_j.__contains__(json_key + '_sum'):
            tmp_sum_old = agg_j[json_key + '_sum']
            tmp_duration_old = agg_j[json_key + '_duration']

        if agg_relative.agg_niveau == 'H':
            tmp_first_dt = None
            # save ou first_time, and fix agg_j values
            if agg_j.__contains__(json_key + '_first_time'):
                tmp_first_dt = agg_j[json_key + '_first_time']
            if tmp_first_dt is not None and delta_values['first_time'] > tmp_first_dt:
                # no change in our current omm values
                return

            if agg_j.__contains__(json_key + '_first_time'):
                # mark as potential candidate for max/min regeneration
                delta_values[json_key + '_regenerate'] = True
            tmp_sum = tmp_sum / tmp_duration * 60
            tmp_duration = 60
            # save our values in agg_h
            agg_j[json_key + '_first_time'] = delta_values['first_time']
            agg_j[json_key + '_sum'] = tmp_sum
            agg_j[json_key + '_duration'] = tmp_duration

            # return if the aggregation should not be sent to upper levels
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
                return

            # propagate the delta
            tmp_sum = tmp_sum - tmp_sum_old
            tmp_duration = tmp_duration - tmp_duration_old
        else:
            addJson(agg_j, json_key + '_sum', tmp_sum)
            addJson(agg_j, json_key + '_duration', tmp_duration)

        # compute M_avg if required
        tmp_sum_new = tmp_duration_new = 0
        if my_measure['avg'] is True:
            tmp_sum_new = agg_j[json_key + '_sum']
            tmp_duration_new = agg_j[json_key + '_duration']
            if tmp_duration_new != 0:
                agg_j[json_key + '_avg'] = tmp_sum_new / tmp_duration_new

        # propagate to next level if no limitation on aggregation level
        dv_next[json_key + '_sum'] = tmp_sum
        dv_next[json_key + '_duration'] = tmp_duration

    def loadMaxMinInAggregation(self, my_measure: json, measures: json, measure_idx: int, my_aggreg, json_key: str, exclusion: json, delta_values: json, dv_next: json, flag: bool):
        """
            loadMaxMinFromMeasures

            load in obs max/min value if present
            update delta_values
        """
        am_i_omm = isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm)
        agg_j = my_aggreg.data.j
        # get aggregation values in measures
        m_agg_j = {}
        if measures.__contains__('data') and measures['data'][measure_idx].__contains__('aggregations'):
            for a_j_agg in measures['data'][measure_idx]['aggregations']:
                if a_j_agg['level'] == my_aggreg.data.level:
                    m_agg_j = a_j_agg
                    break

        for maxmin_suffix in ['_max', '_min']:
            maxmin_key = maxmin_suffix.split('_')[1]

            if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:
                tmp_maxmin = None

                if delta_values.__contains__(json_key + maxmin_suffix) is True:
                    # load from delta_values
                    tmp_maxmin = my_measure['dataType'](delta_values[json_key + maxmin_suffix])
                    tmp_maxmin_time = delta_values[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        tmp_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            tmp_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

                if m_agg_j.__contains__(json_key + maxmin_suffix):
                    # load and use measure maxmin if given
                    tmp_maxmin = my_measure['dataType'](m_agg_j[json_key + maxmin_suffix])
                    tmp_maxmin_time = m_agg_j[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        tmp_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            tmp_maxmin_dir = int(m_agg_j[json_key + maxmin_suffix + '_dir'])

                if tmp_maxmin is None:
                    # no data in dv, neither on aggregation
                    if delta_values.__contains__(json_key) is False or am_i_omm is True:
                        # can't compute without a data
                        continue
                    tmp_maxmin_time = measures['data'][measure_idx]['current']['dat'] + datetime.timedelta(minutes=float(measures['data'][measure_idx]['current']['duration'] / 2))
                    tmp_maxmin = my_measure['dataType'](delta_values[json_key])
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        tmp_maxmin_dir = None

                # load current data from our aggregation
                if agg_j.__contains__(json_key + maxmin_suffix):
                    current_maxmin = agg_j[json_key + maxmin_suffix]
                else:
                    if maxmin_suffix == '_min':
                        current_maxmin = tmp_maxmin + 1
                    else:
                        current_maxmin = tmp_maxmin - 1
                # push regenerate data
                if delta_values.__contains__(json_key + '_regenerate') and delta_values.__contains__(json_key + maxmin_suffix):
                    tmp_mm_dt = delta_values[json_key + maxmin_suffix + '_time']
                    if tmp_mm_dt == tmp_maxmin_time:
                        new_fix = {
                            "posteId": my_aggreg.data.poste_id_id,
                            "startDat": my_aggreg.data.start_dat,
                            "level": my_aggreg.data.level,
                            "maxmin": maxmin_key,
                            "key": json_key,
                            "valeur": delta_values[json_key + maxmin_suffix],
                            "dat": tmp_mm_dt
                        }
                        delta_values['maxminFix'].append(new_fix)

                # compare the measure data and current maxmin
                b_loadValue = False
                # we got a max greater than our current max
                if maxmin_suffix == '_max' and tmp_maxmin > current_maxmin:
                    b_loadValue = True
                # we got a min smaller than our current min
                if maxmin_suffix == '_min'and tmp_maxmin < current_maxmin:
                        b_loadValue = True
                # for omm if there is a max/min for agg_day, force the value
                if am_i_omm is True and my_aggreg.data.level == 'D':
                    b_loadValue = True

                if b_loadValue:
                    agg_j[json_key + maxmin_suffix] = tmp_maxmin
                    dv_next[json_key + maxmin_suffix] = tmp_maxmin
                    agg_j[json_key + maxmin_suffix + '_time'] = tmp_maxmin_time
                    dv_next[json_key + maxmin_suffix + '_time'] = tmp_maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if tmp_maxmin_dir is not None:
                            agg_j[json_key + maxmin_suffix + '_dir'] = tmp_maxmin_dir
                            dv_next[json_key + maxmin_suffix + '_dir'] = tmp_maxmin_dir
