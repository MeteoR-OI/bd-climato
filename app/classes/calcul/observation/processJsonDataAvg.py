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
        json_file_data: json,
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

        my_value_instant = my_value_avg = None
        my_value_dir = None
        obs_stop_dat = obs_meteor.data.stop_dat

        measure_type = 3
        if my_measure.__contains__('measureType'):
            if my_measure['measureType'] == 'avg':
                measure_type = 1
            elif my_measure['measureType'] == 'inst':
                measure_type = 2
            elif my_measure['measureType'] != 'both':
                raise Exception('processJsonDataAvg::loadData', 'invalid measureType: ' + my_measure['measureType'] + ' for ' + src_key)

        if b_exclu is False:
            # load our data from the measure (json)
            data_src = json_file_data['data'][measure_idx]['current']
            if data_src.__contains__(src_key) and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                my_value_instant = my_measure['dataType'](data_src[src_key])
            if data_src.__contains__(src_key + '_avg') and (measure_type & 1) == 1:
                my_value_avg = my_measure['dataType'](data_src[src_key + '_avg'])
            # get synonym [field]_sum for sum fields, if no [field] is given
            if my_value_avg is None and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                if data_src.__contains__(src_key + '_sum'):
                    my_value_avg = my_measure['dataType'](data_src[src_key + '_sum'])
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and data_src.__contains__(src_key + '_dir'):
                my_value_dir = data_src[src_key + '_dir']
        else:
            # load the value from exclusion
            data_src = exclusion
            if exclusion.__contains__(src_key):
                my_value_instant = my_measure['dataType'](exclusion[src_key])
            if exclusion.__contains__(src_key + '_avg'):
                my_value_avg = my_measure['dataType'](exclusion[src_key + '_avg'])
            if my_value_avg == 'null' or my_value_instant == 'null':
                return
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and exclusion.__contains__(src_key + '_dir'):
                my_value_dir = exclusion[src_key + '_dir']

        # init value instantanee et avg
        if my_value_avg is None:
            if my_value_instant is None:
                # no data
                return
            my_value_avg = my_value_instant
        elif my_value_instant is None:
            my_value_instant = my_value_avg

        # get our duration, and save it in the obs_meteor if not set, or test if compatible
        tmp_duration = int(json_file_data['data'][measure_idx]['current']['duration'])

        if obs_meteor.data.duration == 0:
            # need to load the duration in our observation dataRow
            obs_meteor.data.duration = tmp_duration
            # save our agg_h.start_dat for faster retrieval of observation for a given agg_h.start_dat
            obs_meteor.data.agg_start_dat = calcAggDate('H', obs_meteor.data.stop_dat, tmp_duration, True)

        # double check that the duration are compatible
        if obs_meteor.data.duration != tmp_duration:
            raise Exception('loadObsDatarow', 'incompatible durations -> in table obs: ' + str(obs_meteor.data.duration) + ', in json: ' + str(tmp_duration))

        # double check the stop_dat of the obs, is the same as the one in our json data
        if obs_meteor.data.stop_dat != obs_stop_dat:
            raise Exception('loadObsDatarow', 'incompatible dates -> in table obs: ' + str(obs_meteor.data.stop_dat) + ', in json(or exclusion): ' + str(obs_stop_dat))

        # we will save current value in obs, and propagate delta values to our aggregations
        # remove current values from our aggregations
        tmp_sum_avg_old = tmp_duration_old = 0
        if obs_j.__contains__(target_key):  # in obs only _avg are stored
            tmp_value_old_avg = obs_j[target_key]
            tmp_duration_old = obs_meteor.data.duration
            tmp_sum_avg_old = tmp_value_old_avg * tmp_duration
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                tmp_sum_avg = tmp_value_old_avg
            delta_values[target_key + '_sum_old'] = tmp_sum_avg_old
            delta_values[target_key + '_duration_old'] = tmp_duration_old

            # in case of replacement, invalidate the value for our min/max in aggregations
            if tmp_value_old_avg != my_value_avg:
                delta_values[target_key + '_invalidate_max'] = tmp_value_old_avg
                delta_values[target_key + '_invalidate_min'] = tmp_value_old_avg

        tmp_sum_avg = my_value_avg * tmp_duration
        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
            tmp_sum_avg = my_value_avg

        # pass delta values to our aggregations
        delta_values[target_key + '_sum'] = tmp_sum_avg
        delta_values[target_key + '_duration'] = tmp_duration

        # save our data (avg)
        obs_j[target_key] = my_value_instant
        obs_j[target_key + '_avg'] = my_value_avg
        delta_values[target_key] = my_value_avg
        delta_values[target_key + '_i'] = my_value_instant
        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and my_value_dir is not None:
            delta_values[target_key + '_dir'] = my_value_dir
            obs_j[target_key + '_dir'] = my_value_dir
        if isOmm is True:
            # save for max/min processing and omm procesing
            delta_values[target_key + '_time'] = obs_stop_dat

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
