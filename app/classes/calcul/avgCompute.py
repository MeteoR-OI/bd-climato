# calculus for avg
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.processMeasure import ProcessMeasure
from app.tools.aggTools import addJson, isFlagged, getAggDuration
import json


class avgCompute(ProcessMeasure):
    """
        avgCompute

        Computation specific to a measure type

    """

    def loadObsGetDelta(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, field_name: str, m_suffix: str, exclusion: json, delta_values: json, flag: bool):
        """ generate deltaValues from ObsMeteor.data """
        try:
            b_exclu = False        # a value is forced in exclusion
            b_set_null = False      # the measure is invalidated
            b_omm_case = isFlagged(my_measure['special'], MeasureProcessingBitMask.IsOmmMeasure)
            obs_j = obs_meteor.data.j
            factor = 1
            if flag is False:
                factor = -1

            # if exclusion[field] == 'value' -> load our measure data
            if exclusion.__contains__(field_name) is True and exclusion[field_name] != 'value':
                # exclusion[field_name] = 'null' or value_to_force
                b_exclu = True
                if exclusion[field_name] == 'null':
                    b_set_null = True
            # we can have:  b_exclu  |  b_set_null
            #                False   |     xxx   -> load from measure
            #                True    |    False  -> load from exclusion
            #                True    |    True   -> delete any existing values, delta_values -> negative values

            # in exclusion + substract all existing values
            if b_set_null:
                self.getDeltaFromObs(my_measure, obs_meteor, field_name, m_suffix, exclusion, delta_values)
                return

            # save aggregations in obs for future recomputation if required
            if measures['data'][measure_idx].__contains__('aggregations'):
                obs_j['aggregations'] = measures['data'][measure_idx]['aggregations']

            if b_exclu:
                # load the value from exclusion
                data_src = exclusion
                b_omm_case = False
                my_value = my_measure['dataType'](exclusion[field_name] * factor)
            else:
                if measures['data'][measure_idx].__contains__('current'):
                    # load our data from the measure (json)
                    data_src = measures['data'][measure_idx]['current']
                    if data_src.__contains__(field_name + m_suffix) is False:
                        return
                    my_value = my_measure['dataType'](data_src[field_name + m_suffix] * factor)
                else:
                    # no data, only aggregations, then exit will be processed in aggregation processing
                    return

            # get our duration, and save it in the obs_meteor if not set, or test if compatible
            tmp_duration = int(measures['data'][measure_idx]['current']['duration']) * factor
            if obs_meteor.data.duration == 0:
                obs_meteor.data.duration = tmp_duration
            elif obs_meteor.data.duration != tmp_duration and flag is True:     # don't care for a delete
                raise Exception('loadObsGetDelta', 'incompatible duration -> obs: ' + str(obs_meteor.data.duration) + ', json: ' + str(tmp_duration))

            # save value
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.DoNotProcessTwiceInObs) is False:
                obs_j[field_name + m_suffix] = my_value
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                    obs_j[field_name + m_suffix + '_dir'] = int(data_src[field_name + m_suffix + "_dir"])

            # add M_sum/M_duration/M_avg to delta_values if avg is required
            # we have to agregate avg as well, if an upper agregation does not have all measures
            if my_measure['avg'] is True:
                tmp_sum = my_value * tmp_duration * factor
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                    tmp_sum = my_value * factor
                delta_values[field_name + m_suffix + '_sum'] = tmp_sum
                delta_values[field_name + m_suffix + '_duration'] = tmp_duration
                tmp_avg = tmp_sum / tmp_duration   # always positive

            if data_src.__contains__(field_name + m_suffix + '_avg'):
                tmp_avg2 = float(data_src[field_name + m_suffix + '_avg'])      # positive
                # if avg are differents, remove the _sum to not have aggregated value to be computed on measure value
                if delta_values.__contains__(field_name + m_suffix + '_sum') and abs(tmp_avg - tmp_avg2) > 0.1:
                    del delta_values[field_name + m_suffix + '_sum']

            if b_omm_case:
                delta_values[field_name + m_suffix + '_mesure'] = my_value * factor
                delta_values[field_name + m_suffix + 'first_time'] = data_src['dat']
            obs_j['dv'] = delta_values

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def loadAggGetDelta(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        agg_relative: AggMeteor,
        field_name: str,
        m_suffix: str,
        delta_values: json,
        dv_next: json,
        flag: bool,
    ):
        """
            loadAggGetDelta

            Load one aggretation value form delta_values, update dv_next

            parameters:
                my_measure: measure definition
                mesures: json data used as input
                mesure_idx: indice in the data section
                agg_j_relative: our aggregation to update
                field_name + m_suffix : field name
                delta_value: json for forced values
                dv_next: delta_values for next level
                flag: True=insert, False=delete
        """
        try:
            # factor = 1
            if flag is False:
                # factor = -1
                raise Exception('loadAggGetDelta', 'flag = False -> not coded yet')

            # json data in aggMeteor object
            agg_j = agg_relative.data.j
            if agg_j.__contains__('dv') is False:
                agg_j['dv'] = {}
            for akey in delta_values.items():
                agg_j['dv'][akey[0]] = delta_values[akey[0]]

            # measure Json pointer
            m_agg_j = {}
            b_has_measures = False
            if measures.__contains__('data'):
                b_has_measures = True
            if b_has_measures is True and measures['data'][measure_idx].__contains__('aggregations'):
                for a_j_agg in measures['data'][measure_idx]['aggregations']:
                    if a_j_agg['level'] == agg_relative.data.level:
                        m_agg_j = a_j_agg
                        break

            if isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField):
                return

            # if we get a sum, save it in current aggregation, and for next level
            if delta_values.__contains__(field_name + m_suffix + '_sum') is False:
                tmp_sum = tmp_duration = 0
            else:
                tmp_sum = float(delta_values[field_name + m_suffix + '_sum'])
                tmp_duration = float(delta_values[field_name + m_suffix + '_duration'])
                tmp_avg = tmp_sum / tmp_duration

            # we got a forced avg in the json.
            if m_agg_j.__contains__(field_name + m_suffix + '_avg'):
                tmp_avg = float(m_agg_j[field_name + m_suffix + '_avg'])
                if m_agg_j.__contains__(field_name + m_suffix + '_duration'):
                    tmp_duration = m_agg_j[field_name + m_suffix + '_duration']
                else:
                    # use the duration of the json if one is given
                    if measures['data'][measure_idx].__contains__('current'):
                        tmp_duration = measures['data'][measure_idx]['current']['duration']
                    else:
                        # no duration given, then we use the full duration of the agregation
                        tmp_duration = getAggDuration(agg_relative.data.level)
                tmp_sum = tmp_avg * tmp_duration

            if tmp_duration == 0:
                # just a safety measure
                return

            addJson(agg_j, field_name + m_suffix + '_sum', tmp_sum)
            addJson(agg_j, field_name + m_suffix + '_duration', tmp_duration)
            agg_j[field_name + m_suffix + '_avg'] = tmp_avg

            # return if the aggregation should not be sent to upper levels
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True:
                return

            # propagate to next level if no limitation on aggregation level
            dv_next[field_name + m_suffix + '_sum'] = tmp_sum
            dv_next[field_name + m_suffix + '_avg_sum'] = tmp_sum
            dv_next[field_name + m_suffix + '_duration'] = tmp_duration

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
