from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.processMeasure import ProcessMeasure
from app.tools.aggTools import isFlagged
import json


class avgCompute(ProcessMeasure):
    """
        avgCompute

        Computation specific to a measure type

    """

    def loadObsGetDelta(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, field_name: str, m_suffix: str, exclusion: json, flag: bool) -> json:
        """ generate deltaValues from ObsMeteor.data """
        try:
            delta_values = {'extremes': []}
            b_set_val = True        # a value is forced in exclusion
            b_set_null = False      # the measure is invalidated
            b_omm_case = False
            obs_j = obs_meteor.data.j
            factor = 1
            if flag is False:
                factor = -1

            # get the exclusion value if specified, and not the string 'null'
            if exclusion.__contains__(field_name) is True and exclusion[field_name] != 'value':
                # exclusion[field_name] = 'null' or value_to_force
                b_set_val = False
                if exclusion[field_name] == 'null':
                    b_set_null = True

            m_suffix = ''
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.IsOmmMeasure)):
                m_suffix = '_omm'
                b_omm_case = True

            # in exclusion + nullify return an empty json
            if b_set_null:
                return delta_values

            if b_set_val:
                if measures['data'][measure_idx].__contains__('current'):
                    data_src = measures['data'][measure_idx]['current']
                else:
                    data_src = {}
                    b_omm_case = False
            else:
                data_src = exclusion
                b_omm_case = False

            if data_src.__contains__(field_name):
                # add Measure to ObsMeteor
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.DoNotProcessTwiceInObs)) is False:
                    obs_j[field_name + m_suffix] = data_src[field_name] * factor
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        obs_j[field_name + m_suffix + '_dir'] = data_src[field_name + "_dir"]
                # add M_sum/M_duration to delta_values
                tmp_duration = data_src['duration'] * factor
                delta_values[field_name + m_suffix + '_sum'] = data_src[field_name] * tmp_duration * factor
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                    delta_values[field_name + m_suffix + '_sum'] = data_src[field_name] * factor
                delta_values[field_name + m_suffix + '_duration'] = tmp_duration * factor
                if data_src.__contains__(field_name + m_suffix + '_avg'):
                    delta_values[field_name + m_suffix + '_avg'] = data_src[field_name + m_suffix + '_avg']
                    obs_j[field_name + m_suffix + '_avg'] = data_src[field_name + m_suffix + '_avg']

                if b_omm_case:
                    obs_j[field_name + '_mesure'] = data_src[field_name] * factor
                    obs_j[field_name + '_first_time'] = data_src['dat']
                    delta_values[field_name + m_suffix + '_mesure'] = data_src[field_name] * factor
                    delta_values[field_name + m_suffix + 'first_time'] = data_src['dat']

            return delta_values

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    # agregation calculus to split
    # try:
    #     key_name = my_measure['key']
    #     # load field if defined in json
    #     field_name = key_name
    #     if my_measure.__contains__('field'):
    #         field_name = my_measure['field']
    #     gs = GetterSetter()
    #     jsonp = JsonPlus()
    #     for anAgg in AggLevel:
    #         """loop for all aggregations in ascending level"""
    #         delta_values_next = {}
    #         agg_ds = getAggObject(anAgg)()
    #         agg_j = {}

    #         if measures['data'][measure_idx].__contains__('aggregates'):
    #             for a_j_agg in measures['data'][measure_idx]['aggregates']:
    #                 if a_j_agg['level'] == anAgg:
    #                     agg_j = a_j_agg
    #                     break

    #         # get exclusion
    #         exclusion = poste_metier.exclusion(my_measure['type_i'])

    #         # do nothing if exclusion is nullify
    #         if exclusion.__contains__(field_name) is True and exclusion[field_name] == 'null':
    #             return delta_values

    #         tmp_duration = int(measures['data'][measure_idx]['current']['duration'])

    #         if gs.has(agg_j, field_name + '_sum'):
    #             tmp_sum = float(gs.get(agg_j, [field_name + '_sum']))
    #             gs.add(agg_ds, tmp_sum, field_name + '_sum')
    #             gs.set(delta_values_next, tmp_sum, field_name + '_sum')
    #             gs.add(agg_ds, tmp_duration, field_name + '_duration')
    #             gs.set(delta_values_next, tmp_duration,
    #                    field_name + '_duration')
    #             if gs.has(agg_j, field_name + '_avg'):
    #                 # json.aggregations contains M_avg, M_sum, M_duration
    #                 tmp_avg = float(gs.get(agg_j, [field_name + '_avg']))
    #                 gs.set(agg_ds, tmp_avg, field_name + '_avg')
    #                 gs.set(delta_values_next, tmp_avg, field_name + '_avg')
    #             elif (isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False):
    #                 # compute M_avg if required
    #                 tmp_avg = float(gs.get(delta_values_next, [
    #                                 field_name + '_sum']) / gs.get(delta_values_next, [field_name + '_duration']))
    #                 gs.set(agg_ds, tmp_avg, field_name + '_avg')
    #                 gs.set(delta_values_next, tmp_avg, field_name + '_avg')
    #         elif gs.has(delta_values, field_name + '_sum'):
    #             tmp_sum = float(gs.get(delta_values, field_name + '_sum'))
    #             gs.add(agg_ds, tmp_sum, field_name + '_sum')
    #             gs.set(delta_values_next, tmp_sum, field_name + '_sum')
    #             gs.add(agg_ds, tmp_duration, field_name + '_duration')
    #             gs.set(delta_values_next, tmp_duration,
    #                    field_name + '_duration')
    #             if gs.has(delta_values, field_name + '_avg'):
    #                 # get our values to agregate from delta_values
    #                 tmp_avg = float(
    #                     gs.get(delta_values, [field_name + '_avg']))
    #                 gs.set(agg_ds, tmp_avg, field_name + '_avg')
    #                 gs.set(delta_values_next, tmp_avg, field_name + '_avg')
    #         # else => we don't have any values to aggregate..

    #         if gs.has(agg_j, field_name + '_max'):
    #             if gs.is_max(agg_ds, gs.get(agg_j, field_name + '_max'), field_name + '_max'):
    #                 tmp_max = float(gs.get(agg_j, [field_name + '_max']))
    #                 gs.set(agg_ds, tmp_max, field_name + '_max')
    #                 gs.set(delta_values_next, tmp_max, field_name + '_max')
    #                 tmp_max_time = jsonp.dumps(gs.get(agg_j, [field_name + '_max_time']))
    #                 gs.set(agg_ds, tmp_max_time, field_name + '_max_time')
    #                 gs.set(delta_values_next, tmp_max_time, field_name + '_max_time')
    #                 if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
    #                     tmp_dir = gs.get(agg_j, [field_name + '_max_dir'])
    #                     gs.set(agg_ds, tmp_dir, field_name + '_max_dir')
    #                     gs.set(delta_values_next, tmp_dir, field_name + '_max_dir')
    #         else:
    #             if gs.has(delta_values, field_name + '_max'):
    #                 tmp_max = gs.get(delta_values, field_name + '_max')
    #                 if gs.is_max(agg_ds, tmp_max, field_name + '_max'):
    #                     tmp_max = float(
    #                         gs.get(delta_values, field_name + '_max'))
    #                     gs.set(agg_ds, tmp_max, field_name + '_max')
    #                     gs.set(delta_values_next, tmp_max, field_name + '_max')
    #                     tmp_max_time = jsonp.dumps(gs.get(delta_values, field_name + '_max_time'))
    #                     gs.set(agg_ds, tmp_max_time, field_name + '_max_time')
    #                     gs.set(delta_values_next, tmp_max_time, field_name + '_max_time')
    #                     if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
    #                         tmp_dir = gs.get(agg_j, field_name + '_max_dir')
    #                         gs.set(agg_ds, tmp_dir, field_name + '_max_dir')
    #                         gs.set(delta_values_next, tmp_dir, field_name + '_max_dir')

    #         # we give our new delta_values to the next level
    #         delta_values = delta_values_next
    #     return delta_values

    # except Exception as inst:
    #     print(type(inst))    # the exception instance
    #     print(inst.args)     # arguments stored in .args
    #     print(inst)          # __str__ allows args to be printed directly
