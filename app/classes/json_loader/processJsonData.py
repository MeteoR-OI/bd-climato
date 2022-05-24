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

    def loadOneMeasureInObs(
            self,
            poste_metier,
            obs_meteor: ObsMeteor,
            my_measure: json,
            one_data_item: json,
            default_duration: int,
            json_is_obs: bool):
        """
            loadOneMeasureInObs

            load Json values in obs table
        """

        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.NotAllowedInCurrent) is True):
            return

        # load local variables
        target_key = my_measure['target_key']
        obs_data_j = obs_meteor.data.j[obs_meteor.data.j.__len__() - 1]
        data_src = self.get_data_src(poste_metier, my_measure, one_data_item)
        if data_src is None:
            return
        measure_duration = data_src[target_key + '_d'] if data_src.get(target_key + '_d') is not None else default_duration
        is_rounded_hour = is_in_rounded_hour(obs_meteor.data.stop_dat, measure_duration)

        # get our values from our data_src (my_omm_value just used for omm_sum calculus, if the measure is omm)
        my_value_inst, my_value_agg, my_value_dir, my_omm_value = self.get_measure_values(json_is_obs, my_measure, data_src)

        # update obj.j
        self.update_obs(my_measure, my_value_inst, my_value_agg, my_value_dir, my_omm_value, measure_duration, obs_data_j, is_rounded_hour)

        # update max/min in obs
        for maxmin_key in ['max', 'min']:
            self.load_maxmin(my_measure, maxmin_key, data_src, my_value_inst, my_value_agg, my_value_dir, obs_data_j, obs_meteor.data.stop_dat)

        return

    def loadDeltaValues(
        self,
        my_measure: json,
        obs_meteor: ObsMeteor,
        obs_data_idx: int,
        delta_values: json,
        remove_data: bool,
        period_start: str,
        period_end: str,
    ):
        """
            loadDeltaValues

            build delta_values array from obs.j
            delta_values is used to propagate measures in all aggregation levels
            Code will be similar to build delta_values from agg_xxx.j
        """
        obs_j = obs_meteor.data.j[obs_data_idx]
        obs_j_xtreme = obs_meteor.data.j_xtreme[obs_data_idx]
        target_key = my_measure['target_key']
        factor_sign = 1 if remove_data is False else -1
        my_value_sum = None

        my_value_duration = obs_j.get(target_key + '_d')
        if my_value_duration is not None:
            delta_values[target_key + '_d'] = my_value_duration * factor_sign
            my_value_sum = obs_j.get(target_key + '_s')
            if my_value_sum is not None:
                delta_values[target_key + '_s'] = my_value_sum * factor_sign

        if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind):
            my_value_dir = obs_j.get(target_key + '_dir')
            if my_value_dir is not None:
                delta_values[target_key + '_dir_nb'] = factor_sign
                delta_values[target_key + '_dir_sin'] = obs_j.get(target_key + '_dir_sin') * factor_sign
                delta_values[target_key + '_dir_cos'] = obs_j.get(target_key + '_dir_cos') * factor_sign

        for maxmin_key in ['max', 'min']:
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                maxmin_suffix = '_' + maxmin_key
                new_maxmin_val = new_maxmin_time = new_maxmin_dir = None

                # get data from obj.j colum
                if obs_j.get(target_key + maxmin_suffix) is not None:
                    new_maxmin_val = obs_j[target_key + maxmin_suffix]
                    new_maxmin_time = obs_j[target_key + maxmin_suffix + '_time']
                    if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if obs_j.get(target_key + maxmin_suffix + '_dir') is not None:
                            new_maxmin_dir = obs_j[target_key + maxmin_suffix + '_dir']

                if obs_j_xtreme.get(target_key + maxmin_suffix) is not None:
                    tmp_maxmin_val = obs_j_xtreme[target_key + maxmin_suffix]
                    tmp_maxmin_time = obs_j_xtreme[target_key + maxmin_suffix + '_time']
                    if self.is_extreme_in_range(maxmin_key, tmp_maxmin_time, period_start, period_end) is True:
                        if ((new_maxmin_val is None) or
                                (maxmin_suffix == 'max' and tmp_maxmin_val > new_maxmin_val) or
                                (maxmin_suffix == 'min' and tmp_maxmin_val < new_maxmin_val)):
                            new_maxmin_val = tmp_maxmin_val
                            new_maxmin_time = tmp_maxmin_time
                            if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                                if obs_j_xtreme.get(target_key + maxmin_suffix + '_dir') is not None:
                                    new_maxmin_dir = obs_j_xtreme[target_key + maxmin_suffix + '_dir']

                if new_maxmin_val is not None:
                    if remove_data is False:
                        delta_values[target_key + maxmin_suffix] = new_maxmin_val
                        delta_values[target_key + maxmin_suffix + '_time'] = new_maxmin_time
                        if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and new_maxmin_dir is not None:
                            delta_values[target_key + maxmin_suffix + '_dir'] = new_maxmin_dir
                        continue
                    else:
                        delta_values['maxminFix'].append({
                            'key': target_key,
                            'ope': 'd',
                            'type': maxmin_suffix,
                            'value': new_maxmin_val,
                            'date': new_maxmin_time,
                            'dir': new_maxmin_dir,
                        })
        return

    def get_data_src(self, poste_metier, my_measure, one_data_item):
        # get our data_src
        exclusion = poste_metier.exclusion(my_measure['type_i'])
        #  loadFromExclu(exclusion, src_key) should return True, False or None (nullify this measure)
        return exclusion if loadFromExclu(exclusion, my_measure['src_key']) is True else one_data_item.get('valeurs')

    def is_extreme_in_range(self, maxmin_key, str, x_dat: str, period_start: str, period_end: str):
        """ is_extreme_in_range """
        if x_dat > period_end or x_dat < period_start:
            return False
        return True

    def get_suffix_measure(self, my_measure):
        match my_measure['agg']:
            case 'avg' | 'avgomm' | 'rate' | 'rateomm':
                key_suffix = '_avg'
            case 'sum' | 'sumomm':
                key_suffix = '_sum'
            case 'no':
                key_suffix = ''
            case _:
                raise Exception("unknown agg field in measure: " + json.dumps(my_measure))
        return key_suffix

    def get_weewx_aggregated_values(self, key_name, my_measure, data_srv):
        match my_measure['agg']:
            case 'avg' | 'avgomm' | 'rate' | 'rateomm':
                key_suffix = '_avg'
            case 'sum' | 'sumomm':
                key_suffix = '_sum'
            case 'no':
                key_suffix = ''
            case _:
                raise Exception("unknown agg field in measure: " + json.dumps(my_measure))
        return key_suffix

    def get_measure_type(self, my_measure):
        b_load_agg = b_load_inst = True
        if my_measure.__contains__('measureType'):
            if my_measure['measureType'] == 'avg':
                b_load_inst = False
            elif my_measure['measureType'] == 'inst':
                b_load_agg = False
            elif my_measure['measureType'] != 'both':
                raise Exception('processJsonDataAvg::loadDeltaValues', 'invalid measureType: ' + my_measure['measureType'] + ' for ' + my_measure['src_key'])
        return b_load_inst, b_load_agg

    def get_all_keys_for_a_measure(self, my_measure):
        all_src_keys = [my_measure['src_key']]
        if my_measure.get('syno') is not None:
            for a_syno in my_measure['syno']:
                all_src_keys.append(a_syno)
        return all_src_keys

    def get_measure_values(self, json_is_obs, my_measure, data_src):
        all_synonym_keys = self.get_all_keys_for_a_measure(my_measure)
        if json_is_obs:
            return self.get_measure_values_obs_data(my_measure, data_src, all_synonym_keys)
        else:
            return self.get_measure_values_agg_data(my_measure, data_src, all_synonym_keys)

    def get_measure_values_obs_data(self, my_measure, data_src, all_synonym_keys):
        """
            get_measure_values_obs_data

            load our values from data_src
            get values depending on measure_type policy
        """
        # lookup in json data for src_keys, and all syno
        key_suffix = self.get_suffix_measure(my_measure)
        value_found = False
        b_load_inst, b_load_agg = self.get_measure_type(my_measure)
        my_value_inst = my_value_agg = my_value_dir = my_omm_value = None

        for a_srckey in all_synonym_keys:
            if value_found:
                continue

            # load instant value if allowed and if found
            if b_load_inst is True and data_src.__contains__(a_srckey):
                my_value_inst = data_src[a_srckey]
                my_omm_value = data_src.get(a_srckey + '_omm')
                value_found = True
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and data_src.get(a_srckey + '_dir') is not None:
                    my_value_dir = data_src[a_srckey + '_dir']

            # load pre-aggregated value if allowed and if found
            if b_load_agg and data_src.__contains__(a_srckey + key_suffix):
                my_value_agg = data_src[a_srckey + key_suffix]
                if my_omm_value is None:
                    my_omm_value = data_src.get(a_srckey + '_omm')
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

        # load omm_value from inst/agg measure (depending on measure type) if <key>_omm not in data_src
        if b_load_inst is True:
            if my_omm_value is None:
                my_omm_value = my_value_inst
        if b_load_agg is True:
            if my_omm_value is None:
                my_omm_value = my_value_agg

        return my_value_inst, my_value_agg, my_value_dir, my_omm_value

    def update_obs(self, my_measure, my_value_inst, my_value_agg, my_value_dir, my_omm_value, measure_duration, obs_data_j, is_rounded_hour):
        target_key = my_measure['target_key']

        if measure_duration != 0 and (my_value_agg is not None or my_value_inst is not None):
            match my_measure['agg']:
                case 'avg' | 'rate':
                    obs_data_j[target_key + '_s'] = my_value_agg * measure_duration
                    obs_data_j[target_key + '_d'] = measure_duration
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        updateWindData(obs_data_j, target_key, my_value_dir)
                case 'sum':
                    obs_data_j[target_key + '_s'] = my_value_agg
                    obs_data_j[target_key + '_d'] = measure_duration
                case 'avgomm' | 'rateomm':
                    if is_rounded_hour is True:
                        measure_duration = 60
                        obs_data_j[target_key + '_s'] = my_omm_value * measure_duration
                        obs_data_j[target_key + '_d'] = measure_duration
                        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                            updateWindData(obs_data_j, target_key + '', my_value_dir)
                case 'sumomm':
                    obs_data_j[target_key + '_s'] = my_omm_value
                    obs_data_j[target_key + '_d'] = measure_duration
                case 'no':
                    pass
                case _:
                    raise Exception("unknown agg field in measure: " + json.dumps(my_measure))

    def load_maxmin(self, my_measure, maxmin_key, data_src, my_value_inst, my_value_agg, my_value_dir, obs_data_j, my_stop_dat):
        target_key = my_measure['target_key']
        src_key = my_measure['src_key']

        # load max/min from json
        if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
            maxmin_suffix = '_' + maxmin_key
            if data_src.get(src_key + maxmin_suffix) is not None:
                obs_data_j[target_key + maxmin_suffix] = data_src[src_key + maxmin_suffix]
                obs_data_j[target_key + maxmin_suffix + '_time'] = data_src[src_key + maxmin_suffix + '_time']
                if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                    if data_src.get(src_key + maxmin_suffix + '_dir') is not None:
                        obs_data_j[target_key + maxmin_suffix + '_dir'] = data_src[src_key + maxmin_suffix + '_dir']
            else:
                if my_value_agg is not None or my_value_inst is not None:
                    obs_data_j[target_key + maxmin_suffix] = my_value_inst if my_value_inst is not None else my_value_agg
                    obs_data_j[target_key + maxmin_suffix + '_time'] = str(my_stop_dat)
                    if maxmin_key == 'max' and (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if my_value_dir is not None:
                            obs_data_j[target_key + maxmin_suffix + '_dir'] = my_value_dir
