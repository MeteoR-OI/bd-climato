from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.processMeasure import ProcessMeasure
from app.tools.aggTools import addJson, isFlagged, getAggDuration, shouldNullify, loadFromExclu, calcAggDate
import json


class avgCompute(ProcessMeasure):
    """
        avgCompute

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
        flag: bool,
        isOmm: bool = False,
    ):
        """ 
            loadObservationDatarow

            load Observation dataRow from json measures
            load delta_values from json mesures

            isOmm: only to load more info in case of omm/avg
        """
        if flag is False:
            # self.getDeltaFromObservation(my_measure, obs_meteor, target_key, delta_values)
            raise Exception("avgOmmCompute::loadObs", "flag = False not coded yet")
            return

        b_set_null = shouldNullify(exclusion, src_key)
        b_exclu = loadFromExclu(exclusion, src_key)
        # we can have:  b_exclu  |  b_set_null
        #                False   |     xxx   -> load from measure
        #                True    |    False  -> load from exclusion
        #                True    |    True   -> nullify our measure -> return
        if b_exclu is True and b_set_null is True:
            return

        obs_j = obs_meteor.data.j

        # save aggregations in obs for future recomputation if required
        if measures['data'][measure_idx].__contains__('aggregations'):
            obs_j['aggregations'] = measures['data'][measure_idx]['aggregations']

        if measures['data'][measure_idx].__contains__('current'):
            # load our data from the measure (json)
            data_src = measures['data'][measure_idx]['current']
            if data_src.__contains__(src_key) is False:
                return
            my_value = my_measure['dataType'](data_src[src_key])
            my_dat = data_src['dat']
        elif b_exclu is False:
            # no data, only aggregations, no exclusion, then exit will be processed in aggregation processing
            return

        if b_exclu:
            # load the value from exclusion
            data_src = exclusion
            my_value = my_measure['dataType'](exclusion[src_key])

        if isOmm is True:
            # save for max/min processing and omm procesing
            delta_values[target_key + '_value'] = my_value
            delta_values['first_time'] = my_dat

        # get our duration, and save it in the obs_meteor if not set, or test if compatible
        tmp_duration = int(measures['data'][measure_idx]['current']['duration'])

        if obs_meteor.data.duration == 0:
            # need to load the duration in our observation dataRow
            obs_meteor.data.duration = tmp_duration
            # save our agg_h.start_dat for faster retrieval of observation for a giben agg_h.start_dat
            obs_meteor.data.start_dat = calcAggDate('H', obs_meteor.data.dat, tmp_duration)
        elif obs_meteor.data.duration != tmp_duration:
            raise Exception('loadObsDatarow', 'incompatible durations -> in table obs: ' + str(obs_meteor.data.duration) + ', in json: ' + str(tmp_duration))

        # save value
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.DoNotProcessTwiceInObs) is False:
            obs_j[target_key] = my_value
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                obs_j[target_key + '_dir'] = int(data_src[src_key + "_dir"])

        # add M_sum/M_duration/M_avg to delta_values if avg is required
        # we have to agregate avg as well, if an upper agregation does not have all measures
        if my_measure['avg'] is True:
            tmp_sum = my_value * tmp_duration
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                tmp_sum = my_value
            delta_values[target_key + '_sum'] = tmp_sum
            delta_values[target_key + '_duration'] = tmp_duration
            tmp_avg = tmp_sum / tmp_duration

        if data_src.__contains__(src_key + '_avg'):
            # use the given _avg if any, and compute  new 'virtual' sum
            tmp_avg2 = float(data_src[src_key + '_avg'])
            # if avg are differents, remove the _sum to not have aggregated value to be computed on measure value
            if delta_values.__contains__(target_key + '_sum') and abs(tmp_avg - tmp_avg2) > 0.1:
                delta_values[target_key + '_sum'] = tmp_avg2 * tmp_duration

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
            del obs_j[json_key + '_sum']

        if obs_j.__contains__(json_key + '_duration'):
            delta_values[json_key + '_duration'] = obs_j[json_key + '_sum'] * -1
            del obs_j[json_key + '_duration']

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

        # if we get no data, return
        if delta_values.__contains__(json_key + '_sum') is False:
            tmp_sum = tmp_duration = 0
            if delta_values.__contains__(json_key + '_avg') is False:
                return
        else:
            # get our data
            tmp_sum = float(delta_values[json_key + '_sum'])
            tmp_duration = float(delta_values[json_key + '_duration'])

        # we got a forced avg in the aggregation part of our json.
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

        # add the _sum and _duration in our aggregation
        addJson(agg_j, json_key + '_sum', tmp_sum)
        addJson(agg_j, json_key + '_duration', tmp_duration)
        # compute _avg if required
        tmp_sum_new = tmp_duration_new = 0
        if my_measure['avg'] is True:
            tmp_sum_new = agg_j[json_key + '_sum']
            tmp_duration_new = agg_j[json_key + '_duration']
            agg_j[json_key + '_avg'] = tmp_sum_new / tmp_duration_new

        # return if the aggregation should not be sent to upper levels
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
            return

        # propagate to next level if no limitation on aggregation level
        dv_next[json_key + '_sum'] = tmp_sum
        dv_next[json_key + '_duration'] = tmp_duration
