from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
# from app.classes.measures.measureAvg import RootMeasure
from app.tools.aggTools import isFlagged
import json


class avgCompute():
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
