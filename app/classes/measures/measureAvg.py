import datetime
from app.classes.posteMeteor import PosteMeteor
from app.classes.obsMeteor import ObsMeteor
from app.tools.climConstant import AggLevel, MeasureProcessingBitMask
# from app.classes.measures.measureAvg import RootMeasure
from app.tools.agg_tools import is_flagged
import json


class MeasureAvg():
    """
        MeasureAvg

        Computation specific to a measure type

    """
    # {'type_i': 1, 'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def compute(self, measure_def: json, measures: json, obs_meteor: ObsMeteor, agg_array, agg_niveau: AggLevel, flag: bool):
        """
            compute: process new measure

            measure_def: from typeInstruments
            measures: json with new data. Should have the key dat, duration
            obs_meteor
            flag: True new data, False, data to delete
        """

    # {'type_i': 1, 'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def update_obs_and_get_delta(self, poste_meteor: PosteMeteor, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, flag: bool) -> json:
        """ generate deltaValues from ObsMeteor.data """
        try:
            # deltaValues returned for aggregation processing
            delta_values = {}
            field_name = my_measure['field']

            # get exclusion
            exclusion = poste_meteor.exclusion(my_measure['type_i'])
            # todo: no exclusion for now
            exclusion = {}

            b_set_val = True
            b_set_null = False
            # get the exclusion value if specified, and not the string 'null'
            if exclusion.__contains__(field_name) is True and exclusion[field_name] != 'value':
                b_set_val = False    # exclusion[field_name] = 'null' or value_to_force
                if exclusion[field_name] == 'null':
                    b_set_null = True

            # in delete situation, generate the delta_values from the obs dataset
            if flag is False:
                if obs_meteor.__contains__(field_name):
                    if b_set_val:
                        if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                            delta_values[field_name + '_sum'] = obs_meteor.data.__setattr__(field_name, -1)
                        else:
                            delta_values[field_name + '_sum'] = obs_meteor.data.__setattr__(field_name, -1 * obs_meteor.data['duration'])
                        delta_values[field_name + '_duration'] = obs_meteor.data['duration'] * -1
                    elif b_set_null is False:
                        if (is_flagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                            delta_values[field_name + '_sum'] = exclusion[field_name] * -1
                        else:
                            delta_values[field_name + '_sum'] = exclusion[field_name] * -1 * obs_meteor.data['duration']
                        delta_values[field_name + '_duration'] = obs_meteor.data['duration'] * -1
                return delta_values

            # no processing if measure is nullified by an exclusion
            if b_set_null is True:
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
    def update_aggs(self, poste_meteor: PosteMeteor, measure_def: json, measures: json, measure_idx: int, aggregations: list, delta_values: json, flag: bool) -> json:
        """ update all aggregation from the delta data, and aggregations key on json, return a list of extremes to recompute """

        extremes_todo = []
        agg_niveau_idx = 0
        # for anAgg in AggLevel:
        #     """loop for all aggregations in ascending level"""
        #     agg_ds = aggregations[agg_niveau_idx]
        #     agg_j = {}
            # if measures['data'][measure_idx]['current'].__contains__()
        return extremes_todo
