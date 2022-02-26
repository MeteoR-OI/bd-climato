from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.tools.aggTools import isFlagged, loadFromExclu, updateWindData
from app.tools.dateTools import is_in_rounded_hour
import json
# import datetime


class ProcessJsonData():
    """
        ProcessJsonData

        Computation specific to a measure type

        calculus v3

    """

    def loadJsonInObs(
            self,
            poste_metier,
            obs_meteor: ObsMeteor,
            my_measure: json,
            json_file_data: json,
            json_data_idx: int,
            trace_flag: bool = False):
        """ loadJsonInObs: load Json values in obs table """

        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.NotAllowedInCurrent) is True):
            return

        # load local variables
        src_key = my_measure['src_key']
        target_key = my_measure['target_key']

        if ('barometer' in src_key):
            src_key = src_key

        obs_values = obs_meteor.data.j[obs_meteor.data.j.__len__() - 1]
        match my_measure['agg']:
            case 'avg' | 'avgomm' | 'rate' | 'rateomm':
                key_suffix = '_avg'
            case 'sum' | 'sumomm':
                key_suffix = '_sum'
            case 'no':
                key_suffix = ''
            case _:
                raise Exception("unknown agg field in measure: " + json.dumps(my_measure))

        # get exclusion, and return if value is nullified
        exclusion = poste_metier.exclusion(my_measure['type_i'])
        # todo later...
        # if shouldNullify(exclusion, src_key) is True:
        #     return

        # b_exclu = True -> load data from exclusion, False -> normal processing
        b_exclu = loadFromExclu(exclusion, src_key)

        # get data_src
        data_src = exclusion if b_exclu is True else json_file_data['data'][json_data_idx].get('current')
        if data_src is None:
            return

        # load aggregated/instantaneous values
        my_value_inst = my_value_agg = my_value_dir = None
        b_load_inst = b_load_agg = True

        if my_measure.__contains__('measureType'):
            if my_measure['measureType'] == 'avg':
                b_load_inst = False
            elif my_measure['measureType'] == 'inst':
                b_load_agg = False
            elif my_measure['measureType'] != 'both':
                raise Exception('processJsonDataAvg::loadDeltaValues', 'invalid measureType: ' + my_measure['measureType'] + ' for ' + src_key)

        # lookup in json data for src_keys, and all syno
        all_src_keys = [my_measure['src_key']]
        if my_measure.get('syno') is not None:
            for a_syno in my_measure['syno']:
                all_src_keys.append(a_syno)
        value_found = False
        for a_srckey in all_src_keys:
            if value_found:
                continue

            # load instant value if allowed and if found
            if b_load_inst is True and data_src.__contains__(a_srckey):
                my_value_inst = data_src[a_srckey]
                value_found = True
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and data_src.get(a_srckey + '_dir') is not None:
                    my_value_dir = data_src[a_srckey + '_dir']
            # load pre-aggregated value if allowed and if found
            if b_load_agg and data_src.__contains__(a_srckey + key_suffix):
                my_value_agg = data_src[a_srckey + key_suffix]
                value_found = True
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and data_src.get(a_srckey + key_suffix + '_dir') is not None:
                    my_value_dir = data_src[a_srckey + key_suffix + '_dir']
                elif (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and data_src.get(a_srckey + '_dir') is not None:
                    my_value_dir = data_src[a_srckey + '_dir']

        # init value instantaneous and avg (aggregated)
        # measure_type         I  Aggregated I Instantaneous I     Both
        # ---------------------I-------------I---------------I--------------
        # measure_avg (ma)     I ma, then mi I      None     I ma, then mi
        # measure_instant (mi) I     None    I  mi, then ma  I mi, then ma
        # ---------------------I-------------I---------------I--------------

        if b_load_agg is True:
            if my_value_agg is None:
                my_value_agg = my_value_inst
            if b_load_inst is False:
                my_value_inst = None
        if b_load_inst is True:
            if my_value_inst is None:
                my_value_inst = my_value_agg
            if b_load_agg is False:
                my_value_agg = None

        tmp_duration = 0
        if data_src.get(target_key + '_d') is not None:
            # Overload if specified in the data_src json
            tmp_duration = data_src[target_key + '_d']
        else:
            # Use the data duration
            tmp_duration = int(json_file_data['data'][json_data_idx]['current']['duration'])

        if tmp_duration != 0 and (my_value_agg is not None or my_value_inst is not None):
            match my_measure['agg']:
                case 'avg' | 'rate':
                    obs_values[target_key + '_s'] = my_value_agg * tmp_duration
                    obs_values[target_key + '_d'] = tmp_duration
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        updateWindData(obs_values, target_key, my_value_dir)
                case 'sum':
                    obs_values[target_key + '_s'] = my_value_agg
                    obs_values[target_key + '_d'] = tmp_duration
                case 'avgomm' | 'rateomm':
                    if is_in_rounded_hour(obs_meteor.data.stop_dat, tmp_duration):
                        tmp_duration = 60
                        if data_src.get(src_key + '_omm') is not None:
                            obs_values[target_key + '_s'] = data_src[src_key + '_omm'] * tmp_duration
                            obs_values[target_key + '_d'] = tmp_duration
                        else:
                            if b_load_inst is True:
                                obs_values[target_key + '_s'] = my_value_inst * tmp_duration
                            else:
                                # for wind10 which use an aggregted value for the omm
                                obs_values[target_key + '_s'] = my_value_agg * tmp_duration
                            obs_values[target_key + '_d'] = tmp_duration
                        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                            updateWindData(obs_values, target_key + '', my_value_dir)
                case 'sumomm':
                    if data_src.get(src_key + '_omm') is not None:
                        obs_values[target_key + '_s'] = data_src[src_key + '_omm']
                        obs_values[target_key + '_d'] = tmp_duration
                    else:
                        obs_values[target_key + '_s'] = my_value_inst
                        obs_values[target_key + '_d'] = tmp_duration
                case 'no':
                    pass
                case _:
                    raise Exception("unknown agg field in measure: " + json.dumps(my_measure))

        # load max/min from json
        for maxmin_key in ['max', 'min']:
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                maxmin_suffix = '_' + maxmin_key
                if data_src.get(src_key + maxmin_suffix) is not None:
                    obs_values[target_key + maxmin_suffix] = data_src[src_key + maxmin_suffix]
                    obs_values[target_key + maxmin_suffix + '_time'] = data_src[src_key + maxmin_suffix + '_time']
                    if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if data_src.get(src_key + maxmin_suffix + '_dir') is not None:
                            obs_values[target_key + maxmin_suffix + '_dir'] = data_src[src_key + maxmin_suffix + '_dir']
                else:
                    if my_value_agg is not None or my_value_inst is not None:
                        obs_values[target_key + maxmin_suffix] = my_value_inst if my_value_inst is not None else my_value_agg
                        obs_values[target_key + maxmin_suffix + '_time'] = str(obs_meteor.data.stop_dat)
                        if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                            if my_value_dir is not None:
                                obs_values[target_key + maxmin_suffix + '_dir'] = my_value_dir
        return

    def loadDeltaValues(
        self,
        my_measure: json,
        obs_meteor: ObsMeteor,
        data_idx: int,
        delta_values: json,
        remove_data: bool,
        trace_flag: bool,
    ):
        """
            loadDeltaValues

            build delta_values array from obs.j
            delta_values is used to propagate measures in all aggregation levels
            Code will be similar to build delta_values from agg_xxx.j
        """
        obs_j = obs_meteor.data.j[data_idx]
        target_key = my_measure['target_key']

        my_value_sum = obs_j.get(target_key + '_s')
        if my_value_sum is not None:
            delta_values[target_key + '_s'] = my_value_sum if remove_data is False else my_value_sum * -1
        my_value_duration = obs_j.get(target_key + '_d')
        if my_value_duration is not None:
            delta_values[target_key + '_d'] = my_value_duration if remove_data is False else my_value_duration * -1

        if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind):
            my_value_dir = obs_j.get(target_key + '_dir')
            if my_value_dir is not None:
                if remove_data is False:
                    delta_values[target_key + '_dir_nb'] = 1
                    delta_values[target_key + '_dir_sin'] = obs_j.get(target_key + '_dir_sin')
                    delta_values[target_key + '_dir_cos'] = obs_j.get(target_key + '_dir_cos')
                else:
                    delta_values[target_key + '_dir_nb'] = -1
                    delta_values[target_key + '_dir_sin'] = obs_j.get(target_key + '_dir_sin') * -1
                    delta_values[target_key + '_dir_cos'] = obs_j.get(target_key + '_dir_cos') * -1

        for maxmin_key in ['max', 'min']:
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                maxmin_suffix = '_' + maxmin_key
                if obs_j.get(target_key + maxmin_suffix) is not None:
                    if remove_data is False:
                        delta_values[target_key + maxmin_suffix] = obs_j[target_key + maxmin_suffix]
                        delta_values[target_key + maxmin_suffix + '_time'] = obs_j[target_key + maxmin_suffix + '_time']
                        if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                            if obs_j.get(target_key + maxmin_suffix + '_dir') is not None:
                                delta_values[target_key + maxmin_suffix + '_dir'] = obs_j[target_key + maxmin_suffix + '_dir']
                    else:
                        delta_values['maxminFix'].append({
                            'key': target_key,
                            'ope': 'd',
                            'type': maxmin_suffix,
                            'value': obs_j[target_key + maxmin_suffix],
                            'date': obs_j[target_key + maxmin_suffix + '_time'],
                            'dir': obs_j.get(target_key + maxmin_suffix + '_dir'),
                        })
        return
