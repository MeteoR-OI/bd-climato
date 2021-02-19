import datetime
from app.classes.posteMeteor import PosteMeteor
from app.classes.obsMeteor import ObsMeteor
from app.tools.climConstant import AggLevel, MeasureProcessingBitMask
# from app.classes.measures.measureAvg import RootMeasure
from app.tools.agg_tools import is_flagged
import json
from app.tools.getterSetter import GetterSetter


class MeasureAvg():
    """
        MeasureAvg

        Computation specific to a measure type

    """

    # p should be called with o.dat in case of delete !
    # {'type_i': 1, 'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def update_obs_and_get_delta(self, poste_meteor: PosteMeteor, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, flag: bool) -> json:
        """ generate deltaValues from ObsMeteor.data """
        try:
            # deltaValues returned for aggregation processing
            delta_values = {}
            key_name = my_measure['key']
            # load field if defined in json
            field_name = key_name
            if my_measure.__contains__('field'):
                field_name = my_measure['field']

            # get exclusion
            exclusion = poste_meteor.exclusion(my_measure['type_i'])

            b_set_val = True
            b_set_null = False
            # get the exclusion value if specified, and not the string 'null'
            if exclusion.__contains__(field_name) is True and exclusion[field_name] != 'value':
                b_set_val = False    # exclusion[field_name] = 'null' or value_to_force
                if exclusion[field_name] == 'null':
                    b_set_null = True

            # no processing if measure is nullified by an exclusion
            if b_set_null is True:
                return delta_values

            m_suffix = ''
            if (is_flagged(my_measure['special'], MeasureProcessingBitMask.IsOmmMeasure)):
                m_suffix = '_omm'

            # in delete situation, generate the delta_values from the obs dataset
            if flag is False:
                if obs_meteor.__contains__(field_name + m_suffix):
                    if b_set_val:
                        if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                            delta_values[field_name + m_suffix + '_sum'] = obs_meteor.data.__setattr__(field_name, -1)
                        else:
                            delta_values[field_name + m_suffix + '_sum'] = obs_meteor.data.__setattr__(field_name, -1 * obs_meteor.data['duration'])
                        delta_values[field_name + m_suffix + '_duration'] = obs_meteor.data['duration'] * -1
                    elif b_set_null is False:
                        if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                            delta_values[field_name + m_suffix + '_sum'] = exclusion[field_name] * -1
                        else:
                            delta_values[field_name + m_suffix + '_sum'] = exclusion[field_name] * -1 * obs_meteor.data['duration']
                        delta_values[field_name + m_suffix + '_duration'] = obs_meteor.data['duration'] * -1
                return delta_values

            # process our measure
            if measures['data'][measure_idx].__contains__('current') and measures['data'][measure_idx]['current'].__contains__(field_name):
                if b_set_val:
                    # add Measure to ObsMeteor
                    if (is_flagged(my_measure['special'], MeasureProcessingBitMask.DoNotProcessTwiceInObs)) is False:
                        obs_meteor.data.__setattr__(field_name, measures['data'][measure_idx]['current'][field_name])
                        if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                            obs_meteor.data.__setattr__(field_name + '_dir', measures['data'][measure_idx]['current'][field_name+"_dir"])
                    # add Measure to delta_values
                    if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                        delta_values[field_name + '_sum'] = measures['data'][measure_idx]['current'][field_name]
                    else:
                        delta_values[field_name + '_sum'] = measures['data'][measure_idx]['current'][field_name] * measures['data'][measure_idx]['current']['duration']
                    delta_values[field_name + '_duration'] = measures['data'][measure_idx]['current']['duration']
                else:
                    # add exclusion to ObsMeteor
                    if (is_flagged(my_measure['special'], MeasureProcessingBitMask.DoNotProcessTwiceInObs)) is False:
                        obs_meteor.data.__setattr__(field_name, exclusion[field_name])
                        if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                            # if wind is forced, then win_dir should be forced (probably not a real situation....)
                            obs_meteor.data.__setattr__(field_name + '_dir', exclusion[field_name + "_dir"])
                    # add Exclusion to delta_values
                    if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                        delta_values[field_name + '_sum'] = exclusion[field_name]
                    else:
                        delta_values[field_name + '_sum'] = exclusion[field_name] * measures['data'][measure_idx]['current']['duration']
                    delta_values[field_name + '_duration'] = measures['data'][measure_idx]['current']['duration']

            # datetime de la demie-periode
            half_period_time = measures['data'][measure_idx]['current']['dat'] + datetime.timedelta(seconds=int(measures['data'][measure_idx]['current']['duration'] / 2))

            # store M_max for the next upper aggregation
            if measures['data'][measure_idx]['current'].__contains__(field_name + '_max'):
                # on a le max dans le json
                obs_meteor.data.__setattr__(field_name + '_max', measures['data'][measure_idx]['current'][field_name + '_max'])
                obs_meteor.data.__setattr__(field_name + '_max_time', measures['data'][measure_idx]['current'][field_name + '_max_time'])
                delta_values[field_name + '_max'] = measures['data'][measure_idx]['current'][field_name + '_max']
                delta_values[field_name + '_max_time'] = measures['data'][measure_idx]['current'][field_name + '_max_time']
                if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                    """ save Wind_max_dir """
                    obs_meteor.data.__setattr__(field_name + '_max_dir', measures['data'][measure_idx]['current'][field_name + '_max_dir'])
            else:
                # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                delta_values[field_name + '_max'] = obs_meteor.data.__getattribute__(field_name)
                delta_values[field_name + '_max_time'] = half_period_time

            # store M_min for the next upper aggregation
            if measures['data'][measure_idx]['current'].__contains__(field_name + '_min'):
                # on a le min dans le json
                obs_meteor.data.__setattr__(field_name + '_min', measures['data'][measure_idx]['current'][field_name + '_min'])
                obs_meteor.data.__setattr__(field_name + '_min_time', measures['data'][measure_idx]['current'][field_name + '_min_time'])
                delta_values[field_name + '_min'] = measures['data'][measure_idx]['current'][field_name + '_min']
                delta_values[field_name + '_min_time'] = measures['data'][measure_idx]['current'][field_name + '_min_time']
                if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                    """ save Wind_min_dir """
                    obs_meteor.data.__setattr__(field_name + '_min_dir', measures['data'][measure_idx]['current'][field_name + '_min_dir'])
            else:
                # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                delta_values[field_name + '_min'] = obs_meteor.data.__getattribute__(field_name)
                delta_values[field_name + '_min_time'] = half_period_time

            return delta_values

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    # {'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def update_aggs(self, poste_meteor: PosteMeteor, my_measure: json, measures: json, measure_idx: int, aggregations: list, delta_values: json, flag: bool) -> json:
        """ update all aggregation from the delta data, and aggregations key on json, return a list of extremes to recompute """

        try:
            extremes_todo = []
            agg_niveau_idx = 0
            field_name = my_measure['field']
            gs = GetterSetter()
            for anAgg in AggLevel:
                """loop for all aggregations in ascending level"""
                delta_values_next = {}
                agg_ds = aggregations[agg_niveau_idx]
                agg_j = {}
                if anAgg == 'H':
                    data_src = agg_ds.data
                else:
                    data_src = delta_values

                if measures['data'][measure_idx].__contains__('aggregates'):
                    for a_j_agg in measures['data'][measure_idx]['aggregates']:
                        if a_j_agg['level'] == anAgg:
                            agg_j = a_j_agg
                            break

                # get exclusion
                exclusion = poste_meteor.exclusion(my_measure['type_i'])

                # do nothing if exclusion is nullify
                if exclusion.__contains__(field_name) is True and exclusion[field_name] == 'null':
                    return delta_values

                tmp_duration = int(measures['data'][measure_idx]['current']['duration'])

                if gs.has(agg_j, field_name + '_sum'):
                    tmp_sum = float(gs.get(agg_j, [field_name + '_sum']))
                    gs.add(agg_ds.data, tmp_sum, field_name + '_sum')
                    gs.set(delta_values_next, tmp_sum, field_name + '_sum')
                    gs.add(agg_ds.data, tmp_duration, field_name + '_duration')
                    gs.set(delta_values_next, tmp_duration, field_name + '_duration')
                    if gs.has(agg_j, field_name + '_avg'):
                        # json.aggregations contains M_avg, M_sum, M_duration
                        tmp_avg = float(gs.get(agg_j, [field_name + '_avg']))
                        gs.set(agg_ds.data, tmp_avg, field_name + '_avg')
                        gs.set(delta_values_next, tmp_avg, field_name + '_avg')
                    elif (is_flagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False):
                        # compute M_avg if required
                        tmp_avg = float(gs.get(delta_values_next, [field_name + '_sum']) / gs.get(delta_values_next, [field_name + '_duration']))
                        gs.set(agg_ds.data, tmp_avg, field_name + '_avg')
                        gs.set(delta_values_next, tmp_avg, field_name + '_avg')
                elif gs.has(data_src, field_name + '_sum'):
                    tmp_sum = float(gs.get(data_src, field_name + '_sum'))
                    gs.add(agg_ds.data, tmp_sum, field_name + '_sum')
                    gs.set(delta_values_next, tmp_sum, field_name + '_sum')
                    gs.add(agg_ds.data, tmp_duration, field_name + '_duration')
                    gs.set(delta_values_next, tmp_duration, field_name + '_duration')
                    if gs.has(data_src, field_name + '_avg'):
                        # get our values to agregate from data_src
                        tmp_avg = float(gs.get(data_src, [field_name + '_avg']))
                        gs.set(agg_ds.data, tmp_avg, field_name + '_avg')
                        gs.set(delta_values_next, tmp_avg, field_name + '_avg')
                # else => we don't have any values to aggregate..

# toto: process max/min

                # we give our new delta_values to the next level
                delta_values = delta_values_next

            return extremes_todo

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
