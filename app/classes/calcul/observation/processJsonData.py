from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.tools.aggTools import isFlagged
from app.tools.aggTools import loadFromExclu, calcAggDate
import json
import datetime


class ProcessJsonData():
    """
        ProcessJsonData

        Computation specific to a measure type

        calculus v3

    """

    def loadInObs(self, poste_metier, my_measure: json, json_file_data: json, measure_idx: int, m_agg_j: json, obs_meteor: ObsMeteor, delta_values: json, trace_flag: bool = False):
        """
            processObservation

            load json data in Observation table

            load max/min

            return the delta_values to be added in all aggregations

            some methods are implemented here, some in the inherited class
        """

        # load field if defined in json
        src_key = my_measure['src_key']
        target_key = my_measure['target_key']

        # get exclusion, and return if value is nullified
        exclusion = poste_metier.exclusion(my_measure['type_i'])
        # to check later...
        # if shouldNullify(exclusion, src_key) is True:
        #     return

        my_values = {}
        if target_key == "rain_rate":
            target_key = "rain_rate"

        self.loadValuesFromCurrent(my_measure, json_file_data, measure_idx, src_key, target_key, exclusion, my_values, obs_meteor.data.stop_dat, trace_flag)

        if my_values.__len__() == 0 and m_agg_j.__len__() == 0:
            return

        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.NotAllowedInCurrent) is True):
            return

        # load Json data in dv

        # update duration & agg_start_dat in obs if needed
        if obs_meteor.data.duration == 0 and my_values.__len__() > 1:
            tmp_duration = delta_values.get(target_key + '_du')
            obs_meteor.data.duration = tmp_duration
            # compute our agg_h.start_dat for faster retrieval of observation for a given agg_h.start_dat
            obs_meteor.data.agg_start_dat = calcAggDate('H', obs_meteor.data.stop_dat, tmp_duration, True)

            # double check that the duration are compatible
            if obs_meteor.data.duration != tmp_duration:
                raise Exception('loadObsDatarow', 'incompatible durations -> in table obs: ' + str(obs_meteor.data.duration) + ', in json: ' + str(tmp_duration))

        # load data from dv to obs
        self.loadDataInObs(my_measure, obs_meteor, target_key, delta_values, my_values, trace_flag)

        # check maxmin that need to be regenated later
        self.checkMaxMinToRegenerate(my_measure, obs_meteor, target_key, delta_values, my_values, trace_flag)

        # load Max/Min in obs, and in dv
        self.loadMaxMinInObs(my_measure, obs_meteor, target_key, delta_values, my_values, trace_flag)
        return

    # ----------------------------------------------------------
    # private or methods common to multiple inherited instances
    # ----------------------------------------------------------
    def loadValuesFromCurrent(
        self,
        my_measure: json,
        json_file_data: json,
        measure_idx: int,
        src_key: str,
        target_key: str,
        exclusion: json,
        my_values: json,
        trace_flag: bool,
    ):
        if my_measure.__contains__('xyz') is False:
            # just to satisfy our parser... Will always fail
            raise Exception('loadDataInDV', 'should be in virtual func')

    def _loadValuesFromCurrent(
        self,
        my_measure: json,
        json_file_data: json,
        measure_idx: int,
        src_key: str,
        target_key: str,
        exclusion: json,
        my_values: json,
        key_suffix: str,
        stop_dat: datetime,
        trace_flag: bool,
    ):
        """
            Load ou values in delta_value for value passing to loadDataInObs, and loadMaxMinInObsInObservation
        """
        # b_exclu = True -> load data from exclusion, False -> normal processing
        b_exclu = loadFromExclu(exclusion, src_key)

        my_value_instant = my_value_avg = None
        my_value_dir = None

        if my_measure['target_key'] == 'barometer':
            measure_type = 3

        measure_type = 3
        if my_measure.__contains__('measureType'):
            if my_measure['measureType'] == 'avg':
                measure_type = 1
            elif my_measure['measureType'] == 'inst':
                measure_type = 2
            elif my_measure['measureType'] != 'both':
                raise Exception('processJsonDataAvg::loadDataInObs', 'invalid measureType: ' + my_measure['measureType'] + ' for ' + src_key)

        if b_exclu is False:
            # load our data from the measure (json)
            data_src = json_file_data['data'][measure_idx].get('current')
        else:
            data_src = exclusion

        all_src_keys = [my_measure['src_key']]
        if my_measure.get('syno') is not None:
            for a_syno in my_measure['syno']:
                all_src_keys.append(a_syno)
        value_found = False
        for a_srckey in all_src_keys:
            if value_found:
                continue
            if data_src is not None:
                if data_src.__contains__(a_srckey) and (measure_type & 2) == 2:
                    my_value_instant = self.get_json_value(data_src, a_srckey, [], True)
                    value_found = True
                if data_src.__contains__(a_srckey + key_suffix) and (measure_type & 1) == 1:
                    my_value_avg = self.get_json_value(data_src, a_srckey + key_suffix, [], True)
                    value_found = True
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                    if data_src.__contains__(a_srckey + '_dir'):
                        my_value_dir = data_src[a_srckey + '_dir']
                    elif data_src.__contains__(a_srckey + key_suffix + '_dir'):
                        my_value_dir = data_src[a_srckey + '_dir']

        # init value instantaneout and avg
        # measure_type         I      1      I      2      I      3
        # measure_avg (ma)     I ma, then mi I     None    I ma, then mi
        # measure_instant (mi) I     None    I mi, then ma I mi, then ma

        if measure_type == 1:
            if my_value_avg is None:
                my_value_avg = my_value_instant
            if measure_type == 1:
                my_value_instant = None
        if measure_type == 2:
            if my_value_instant is None:
                my_value_instant = my_value_avg
            if measure_type == 2:
                my_value_avg = None
        if measure_type == 3:
            if my_value_avg is None:
                my_value_avg = my_value_instant
            if my_value_instant is None:
                my_value_instant = my_value_avg

        if my_value_avg is not None:
            my_values[target_key + '_a'] = my_value_avg
        if my_value_instant is not None:
            my_values[target_key + '_i'] = my_value_instant
        if my_value_dir is not None:
            my_values[target_key + '_di'] = my_value_dir
        tmp_duration = int(json_file_data['data'][measure_idx]['current']['duration'])
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            tmp_duration = 60
        if tmp_duration != 0:
            my_values[target_key + '_du'] = tmp_duration

        # load max/min from json
        for maxmin_key in ['max', 'min']:
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                maxmin_suffix = '_' + maxmin_key
                if data_src is not None and data_src.get(src_key + maxmin_suffix) is not None:
                    my_values[target_key + maxmin_suffix] = data_src[src_key + maxmin_suffix]
                    my_values[target_key + maxmin_suffix + '_time'] = data_src[src_key + maxmin_suffix + '_time']
                    if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if data_src is not None and data_src.get(src_key + maxmin_suffix + '_dir') is not None:
                            my_values[target_key + maxmin_suffix + '_dir'] = data_src[src_key + maxmin_suffix + '_dir']
                else:
                    if my_value_avg is not None or my_value_instant is not None:
                        my_values[target_key + maxmin_suffix] = my_value_instant if my_value_instant is not None else my_value_avg
                        if data_src is not None and data_src.get(src_key + maxmin_suffix + "_time") is not None:
                            my_values[target_key + maxmin_suffix + '_time'] = data_src[src_key + maxmin_suffix + '_time']
                        else:
                            my_values[target_key + maxmin_suffix + '_time'] = stop_dat

    def loadDataInObs(
        self,
        my_measure: json,
        obs_meteor: ObsMeteor,
        target_key: str,
        delta_values: json,
        trace_flag: bool,
    ):
        if my_measure.__contains__('xyz') is False:
            # just to satisfy our parser... Will always fail
            raise Exception('loadDataInDV', 'should be in virtual func')

    def checkMaxMinToRegenerate(
        self,
        my_measure: json,
        obs_meteor: ObsMeteor,
        target_key: str,
        delta_values: json,
        my_values: json,
        tracing_flag: bool = False,
    ):
        obs_j = obs_meteor.data.j

        for maxmin_suffix in ['_max', '_min']:
            if obs_j.get(target_key + maxmin_suffix) is not None:
                my_old_maxmin_value = obs_j[target_key + maxmin_suffix]
                my_values[target_key + '_check' + maxmin_suffix] = my_old_maxmin_value

    def loadMaxMinInObs(
        self,
        my_measure: json,
        obs_meteor: ObsMeteor,
        target_key: str,
        delta_values: json,
        my_values: json,
        trace_flag: bool = False,
    ):
        """
            loadMaxMinInObsInObservation

            load in obs max/min value if present
            update delta_values

            calculus v2
        """
        obs_j = obs_meteor.data.j

        b_is_max = True
        for maxmin_key in ['max', 'min']:
            # is max or min needed for this measure
            maxmin_suffix = '_' + maxmin_key
            # if target_key == "rain_rate":
            #     target_key = "rain_rate"
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                # propagate the check request
                if my_values.get(target_key + '_check' + maxmin_suffix) is not None:
                    obs_j[target_key + '_check' + maxmin_suffix] = my_values[target_key + '_check' + maxmin_suffix]

                if my_values.get(target_key + maxmin_suffix) is not None:
                    my_maxmin_value = my_values[target_key + maxmin_suffix]
                    my_maxmin_date = my_values[target_key + maxmin_suffix + '_time']
                    obs_j[target_key + maxmin_suffix] = my_maxmin_value
                    obs_j[target_key + maxmin_suffix + '_time'] = my_maxmin_date
                    delta_values[target_key + maxmin_suffix] = my_maxmin_value
                    delta_values[target_key + maxmin_suffix + '_time'] = my_maxmin_date
                    if my_values.get(target_key + maxmin_suffix + '_dir') is not None:
                        my_wind_dir = my_values[target_key + maxmin_suffix + '_dir']
                        obs_j[target_key + maxmin_suffix + '_dir'] = my_wind_dir
                        delta_values[target_key + maxmin_suffix + '_dir'] = my_wind_dir

            b_is_max = not(b_is_max)

    def get_json_value(self, j: json, key: str, suffix_list: list, key_preffix_first: bool):
        key_list = []
        if key_preffix_first is not None and key_preffix_first is False:
            key_list.append(key)
        for a_suffix in suffix_list:
            key_list.append(a_suffix)
        if key_preffix_first is not None and key_preffix_first is True:
            key_list.append(key)

        for a_key in key_list:
            if j.get(a_key) is not None:
                return j[a_key]
        return None
