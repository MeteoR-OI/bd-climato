from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.observation.processJsonData import ProcessJsonData
from app.tools.aggTools import isFlagged, loadFromExclu, calcAggDate, delKey
import json


class ProcessJsonDataAvg(ProcessJsonData):
    """
        ProcessJsonDataAvg

        Computation specific to a measure type

        must load dv[M_value], and dv[first_time] when in omm mode

    """

    def loadData(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        trace_flag: bool,
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

        # b_exclu = True -> load data from exclusion, False -> normal processing
        b_exclu = loadFromExclu(exclusion, src_key)

        if measures['data'][measure_idx].__contains__('current'):
            # load our data from the measure (json)
            data_src = measures['data'][measure_idx]['current']
            if data_src.__contains__(src_key) is False:
                # no data
                return
            my_value = my_measure['dataType'](data_src[src_key])
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                my_value_dir = data_src[src_key + '_dir']
            my_dat = data_src['stop_dat']
        elif b_exclu is False:
            # no data, only aggregations, no exclusion, then m_agg_j will be processed in aggregation processing
            return

        if b_exclu is True:
            # load the value from exclusion
            data_src = exclusion
            my_value = my_measure['dataType'](exclusion[src_key])
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                my_value_dir = None
                if exclusion.__contains__(src_key + '_dir'):
                    my_value_dir = exclusion[src_key + '_dir']

        # get our duration, and save it in the obs_meteor if not set, or test if compatible
        tmp_duration = int(measures['data'][measure_idx]['current']['duration'])

        if obs_meteor.data.duration == 0:
            # need to load the duration in our observation dataRow
            obs_meteor.data.duration = tmp_duration
            # save our agg_h.start_dat for faster retrieval of observation for a given agg_h.start_dat
            obs_meteor.data.agg_start_dat = calcAggDate('H', obs_meteor.data.stop_dat, tmp_duration, True)

        # double check that the duration are compatible
        if obs_meteor.data.duration != tmp_duration:
            raise Exception('loadObsDatarow', 'incompatible durations -> in table obs: ' + str(obs_meteor.data.duration) + ', in json: ' + str(tmp_duration))

        # double check the stop_dat of the obs, is the same as the one in our json data
        if obs_meteor.data.stop_dat != my_dat:
            raise Exception('loadObsDatarow', 'incompatible dates -> in table obs: ' + str(obs_meteor.data.stop_dat) + ', in json(or exclusion): ' + str(my_dat))

        # we will save current value in obs, and propagate delta values to our aggregations
        if my_measure['avg'] is True:

            # remove current values from our aggregations
            if obs_j.__contains__(target_key):
                tmp_value_old = obs_j[target_key]
                tmp_duration_old = obs_meteor.data.duration
                tmp_sum = tmp_value_old * tmp_duration
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                    tmp_sum = tmp_value_old
                delta_values[target_key + '_sum_old'] = tmp_sum
                delta_values[target_key + '_duration_old'] = tmp_duration_old

                # in case of replacement, invalidate the value for our min/max in aggregations
                if obs_j.__contains__(target_key) and obs_j[target_key] != my_value:
                    delta_values[target_key + '_maxmin_invalid_val_max'] = obs_j[target_key]
                    delta_values[target_key + '_maxmin_invalid_val_min'] = obs_j[target_key]

            tmp_sum = my_value * tmp_duration
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                tmp_sum = my_value

            if data_src.__contains__(src_key + avg_suffix):
                # use the given _avg if any, and compute  new 'virtual' sum
                tmp_avg2 = float(data_src[src_key + avg_suffix])
                tmp_sum = tmp_avg2 * tmp_duration

            # pass delta values to our aggregations
            delta_values[target_key + '_sum'] = tmp_sum
            delta_values[target_key + '_duration'] = tmp_duration

        # save our data
        obs_j[target_key] = my_value
        delta_values[target_key] = my_value
        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and my_value_dir is not None:
            delta_values[target_key + '_dir'] = my_value_dir
            obs_j[target_key + '_dir'] = my_value_dir
        if isOmm is True:
            # save for max/min processing and omm procesing
            delta_values[target_key + '_first_time'] = my_dat

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
