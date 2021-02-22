# calculus for avg
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.classes.calcul.processMeasure import ProcessMeasure
from app.tools.aggTools import addJson, isFlagged
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
            # json data in aggMeteor object
            agg_j = agg_relative.data.j

            # measure Json pointer
            m_agg_j = {}
            if measures['data'][measure_idx].__contains__('aggregates'):
                for a_j_agg in measures['data'][measure_idx]['aggregates']:
                    if a_j_agg['level'] == agg_relative.agg_niveau:
                        m_agg_j = a_j_agg
                        break

            # get dat and duration of the mesure
            measure_duration = int(measures['data'][measure_idx]['current']['duration'])
            # measure_dat = measures['data'][measure_idx]['current']['dat']

            # source of data: json first, then delta_values
            if m_agg_j.__contains__(field_name + m_suffix + '_sum'):
                data_src = m_agg_j
            else:
                data_src = delta_values

            # check if we have a value in our data_src
            if data_src.__contains__(field_name + m_suffix + '_sum'):
                tmp_sum = float(data_src[field_name + m_suffix + '_sum'])
                addJson(agg_j, field_name + m_suffix + '_sum', tmp_sum)
                dv_next[field_name + m_suffix + '_sum'] = tmp_sum
                addJson(agg_j, field_name + m_suffix + '_duration', measure_duration)
                dv_next[field_name + '_duration'] = measure_duration
                if data_src.__contains__(field_name + m_suffix + '_avg'):
                    # json.aggregations contains M_avg, M_sum, M_duration
                    tmp_avg = float(data_src[field_name + m_suffix + '_avg'])
                    addJson(agg_j, field_name + m_suffix + '_avg', tmp_sum)
                    dv_next[field_name + m_suffix + '_avg'] = tmp_avg
                elif (isFlagged(my_measure['special'], MeasureProcessingBitMask.NoAvgField) is False):
                    # compute M_avg only in agg_j, if M_duration != 0
                    if dv_next[field_name + m_suffix + '_duration'] != 0:
                        tmp_avg = float(dv_next[field_name + m_suffix + '_sum'] / dv_next[field_name + m_suffix + '_duration'])
                        agg_j[field_name + m_suffix + '_avg'] = tmp_avg
            # else => we don't have any values to aggregate..

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
