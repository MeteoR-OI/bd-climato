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

    def loadObsGetDelta(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, field_name: str, m_suffix: str, exclusion: json, delta_values: json, flag: bool) -> json:
        """ generate deltaValues from ObsMeteor.data """
        try:
            b_set_val = True        # a value is forced in exclusion
            b_set_null = False      # the measure is invalidated
            b_omm_case = isFlagged(my_measure['special'], MeasureProcessingBitMask.IsOmmMeasure)
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
                my_value = my_measure['dataType'](data_src[field_name] * factor)
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.DoNotProcessTwiceInObs)) is False:
                    obs_j[field_name + m_suffix] = my_value
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        obs_j[field_name + m_suffix + '_dir'] = int(data_src[field_name + "_dir"])
                # add M_sum/M_duration to delta_values
                tmp_duration = int(measures['data'][measure_idx]['current']['duration'])
                delta_values[field_name + m_suffix + '_sum'] = my_value * tmp_duration * factor
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                    delta_values[field_name + m_suffix + '_sum'] = my_value * factor
                delta_values[field_name + m_suffix + '_duration'] = tmp_duration * factor
                if data_src.__contains__(field_name + m_suffix + '_avg'):
                    tmp_avg = float(data_src[field_name + m_suffix + '_avg'])/tmp_duration
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                        tmp_avg = float(data_src[field_name + m_suffix + '_avg'])
                    delta_values[field_name + m_suffix + '_avg'] = tmp_avg
                    obs_j[field_name + m_suffix + '_avg'] = tmp_avg
                if b_omm_case:
                    obs_j[field_name + '_mesure'] = my_value * factor
                    obs_j[field_name + '_first_time'] = data_src['dat']
                    delta_values[field_name + m_suffix + '_mesure'] = my_value * factor
                    delta_values[field_name + m_suffix + 'first_time'] = data_src['dat']
            return delta_values

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
            factor = 1
            if flag is False:
                factor = -1

            # json data in aggMeteor object
            agg_j = agg_relative.data.j

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

            # update aggregation and dv_next
            # look to 'calcul aggregation.xls' in tab 'delta vs agg'
            if m_agg_j.__contains__(field_name + m_suffix + '_sum'):
                tmp_sum = float(m_agg_j[field_name + m_suffix + '_sum'] * factor)
                addJson(agg_j, field_name + m_suffix + '_sum', tmp_sum)
                dv_next[field_name + m_suffix + '_sum'] = tmp_sum
                tmp_duration = int(m_agg_j[field_name + m_suffix + '_duration'] * factor)
                addJson(agg_j, field_name + m_suffix + '_duration', tmp_duration)
                dv_next[field_name + '_duration'] = tmp_duration
                if m_agg_j.__contains__(field_name + m_suffix + '_avg'):
                    tmp_avg = float(m_agg_j[field_name + m_suffix + '_avg'])
                    agg_j[field_name + m_suffix + '_avg'] = tmp_avg
                    dv_next[field_name + m_suffix + '_avg'] = tmp_avg
                else:
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False):
                        tmp_avg = float(tmp_sum / tmp_duration)
                        addJson(agg_j, field_name + m_suffix + '_avg', tmp_avg)
            else:
                if delta_values.__contains__(field_name + m_suffix + '_sum'):
                    tmp_sum = float(delta_values[field_name + m_suffix + '_sum'])
                    addJson(agg_j, field_name + m_suffix + '_sum', tmp_sum)
                    dv_next[field_name + m_suffix + '_sum'] = tmp_sum
                    tmp_duration = float(delta_values[field_name + m_suffix + '_duration'])
                    addJson(agg_j, field_name + m_suffix + '_duration', tmp_duration)
                    dv_next[field_name + '_duration'] = tmp_duration
                if m_agg_j.__contains__(field_name + m_suffix + '_avg'):
                    tmp_avg = float(m_agg_j[field_name + m_suffix + '_avg'])
                    agg_j[field_name + m_suffix + '_avg'] = tmp_avg
                    dv_next[field_name + m_suffix + '_avg'] = tmp_avg
                else:
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False):
                        if delta_values.__contains__(field_name + m_suffix + '_avg'):
                            tmp_avg = delta_values[field_name + m_suffix + '_avg']
                            agg_j[field_name + m_suffix + '_avg'] = tmp_avg
                            dv_next[field_name + m_suffix + '_avg'] = tmp_avg
                        else:
                            if agg_j.__contains__(field_name + m_suffix + '_sum'):
                                tmp_avg = float(int(agg_j[field_name + m_suffix + '_sum']) / int(agg_j[field_name + m_suffix + '_duration']))
                                if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum):
                                    tmp_avg = float(agg_j[field_name + m_agg_j + '_sum'])
                                agg_j[field_name + m_suffix + '_avg'] = tmp_avg

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
