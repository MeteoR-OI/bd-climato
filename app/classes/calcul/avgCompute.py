from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.processMeasure import ProcessMeasure
from app.tools.aggTools import addJson, isFlagged, getAggDuration, loadFromExclu, calcAggDate, delKey
import json


class AvgCompute(ProcessMeasure):
    """
        AvgCompute

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """

    def loadObservationDatarow(
        self, my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        isOmm: bool = False,
        avg_suffix: str = '_avg',
    ):
        """
            loadObservationDatarow

            load Observation dataRow from json measures
            load delta_values from json mesures

            isOmm: only to load more info in case of omm/avg
        """
        obs_j = obs_meteor.data.j

        # save aggregations in obs for future recomputation if required
        if measures['data'][measure_idx].__contains__('aggregations'):
            obs_j['aggregations'] = measures['data'][measure_idx]['aggregations']

        # b_exclu = True -> load data from exclusion, False -> normal processing
        b_exclu = loadFromExclu(exclusion, src_key)

        if measures['data'][measure_idx].__contains__('current'):
            # load our data from the measure (json)
            data_src = measures['data'][measure_idx]['current']
            if data_src.__contains__(src_key) is False:
                # no data
                return
            my_value = my_measure['dataType'](data_src[src_key])
            my_dat = data_src['dat']
        elif b_exclu is False:
            # no data, only aggregations, no exclusion, then m_agg_j will be processed in aggregation processing
            return

        if b_exclu is True:
            # load the value from exclusion
            data_src = exclusion
            my_value = my_measure['dataType'](exclusion[src_key])

        # get our duration, and save it in the obs_meteor if not set, or test if compatible
        tmp_duration = int(measures['data'][measure_idx]['current']['duration'])

        if obs_meteor.data.duration == 0:
            # need to load the duration in our observation dataRow
            obs_meteor.data.duration = tmp_duration
            # save our agg_h.start_dat for faster retrieval of observation for a giben agg_h.start_dat
            obs_meteor.data.start_dat = calcAggDate('H', obs_meteor.data.dat, tmp_duration)
        elif obs_meteor.data.duration != tmp_duration:
            raise Exception('loadObsDatarow', 'incompatible durations -> in table obs: ' + str(obs_meteor.data.duration) + ', in json: ' + str(tmp_duration))

        # we will save current value in obs, and propagate delta values to our aggregations
        if my_measure['avg'] is True:
            # remove current values from our aggregations
            if obs_j.__contains__(target_key + '_sum'):
                delta_values[target_key + '_sum_old'] = obs_j[target_key + '_sum']
                delta_values[target_key + '_duration_old'] = obs_j[target_key + '_duration']

            tmp_sum = my_value * tmp_duration
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                tmp_sum = my_value
            tmp_avg = tmp_sum / tmp_duration

            if data_src.__contains__(src_key + avg_suffix):
                # use the given _avg if any, and compute  new 'virtual' sum
                tmp_avg2 = float(data_src[src_key + avg_suffix])
                tmp_sum = tmp_avg2 * tmp_duration

            # update our avg fields in obs
            obs_j[target_key + '_sum'] = tmp_sum
            obs_j[target_key + '_duration'] = tmp_duration
            obs_j[target_key + avg_suffix] = tmp_avg
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                obs_j[target_key + '_dir'] = int(data_src[src_key + "_dir"])

            # pass delta values to our aggregations
            delta_values[target_key + '_sum'] = tmp_sum
            delta_values[target_key + '_duration'] = tmp_duration

        # in case of replacement, invalidate the value for our min/max in aggregations
        if obs_j.__contains__(target_key) and obs_j[target_key] != my_value:
            delta_values[target_key + '_maxmin_invalid_val_max'] = obs_j[target_key]
            delta_values[target_key + '_maxmin_invalid_val_min'] = obs_j[target_key]

        # save our data
        obs_j[target_key] = my_value
        delta_values[target_key] = my_value
        if isOmm is True:
            # save for max/min processing and omm procesing
            delta_values[target_key + '_first_time'] = my_dat

        obs_j['dv'] = delta_values

    def getDeltaFromObservation(self, my_measure: json, obs_meteor: ObsMeteor, json_key: str, delta_values: json) -> json:
        """
            getDeltaFromObs

            susbtract M_sum and M_duration
        """
        # todo: load max/min
        obs_j = obs_meteor.data.j

        # use the value in obs_meteor
        if obs_j.__contains__(json_key + '_sum'):
            delta_values[json_key + '_sum'] = obs_j[json_key + '_sum'] * -1
            delKey(obs_j, json_key + '_sum')

        if obs_j.__contains__(json_key + '_duration'):
            delta_values[json_key + '_duration'] = obs_j[json_key + '_sum'] * -1
            delKey(obs_j, json_key + '_duration')

    def loadAggregationDatarows(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        current_agg: AggMeteor,
        json_key: str,
        delta_values: json,
        dv_next: json,
        avg_suffix: str = '_avg',
    ):
        """
            loadAggregationDatarows

            Load one aggretation value from delta_values, update dv_next

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
        # if we get no data, return
        if delta_values.__contains__(json_key) is False:
            return

        # for tracing, save inputed delta_values in dv
        agg_j, m_agg_j = self.savedv_and_get_agg_magg(current_agg, delta_values, measures, measure_idx)

        if my_measure['avg'] is True:
            tmp_sum = tmp_duration = None

            # load old values
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
                tmp_duration = m_agg_j[json_key + '_duration']

            # we got a forced avg in the aggregation part of our json.
            # avg can be given without a sum, or a duration...
            if m_agg_j.__contains__(json_key + avg_suffix):
                tmp_avg = float(m_agg_j[json_key + avg_suffix])
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
                dv_next = {"extremesFix": [], "maxminFix": []}
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

        # return if the aggregation should not be sent to upper levels
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
            dv_next = {"extremesFix": [], "maxminFix": []}

    def savedv_and_get_agg_magg(self, current_agg: AggMeteor, delta_values: json, measures: json, measure_idx: int):
        """
            savedv_and_get_agg_magg

            save delta_values in agg_j['dv']

            return agg json, and m_agg json
        """
        agg_j = current_agg.data.j
        if agg_j.__contains__('dv') is False:
            agg_j['dv'] = {}
        for akey in delta_values.items():
            agg_j['dv'][akey[0]] = delta_values[akey[0]]

        # get aggregation values in measures
        m_agg_j = {}
        if measures.__contains__('data') and measures['data'][measure_idx].__contains__('aggregations'):
            for a_j_agg in measures['data'][measure_idx]['aggregations']:
                if a_j_agg['level'] == current_agg.data.level:
                    m_agg_j = a_j_agg
                    break
        return agg_j, m_agg_j
