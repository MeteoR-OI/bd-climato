from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.tools.aggTools import isFlagged
from app.tools.aggTools import shouldNullify
import json


class ProcessJsonData():
    """
        ProcessJsonData

        Computation specific to a measure type

        calculus v2

    """

    def loadInObs(self, poste_metier, my_measure: json, json_file_data: json, measure_idx: int, obs_meteor: ObsMeteor, delta_values: json, trace_flag: bool = False):
        """
            processObservation

            load json data in Observation table

            load max/min

            return the delta_values to be added in all aggregations

            some methods are implemented here, some in the inherited class
        """

        # load field if defined in json
        src_key, target_key = self.get_src_key(my_measure)

        # get exclusion, and return if value is nullified
        exclusion = poste_metier.exclusion(my_measure['type_i'])
        if shouldNullify(exclusion, src_key) is True:
            return

        # load obs record, and get the delta_values
        self.loadData(my_measure, json_file_data, measure_idx, obs_meteor, src_key, target_key, exclusion, delta_values, trace_flag)

        # load Max/Min and update delta_values
        self.loadMaxMin(my_measure, json_file_data, measure_idx, obs_meteor, src_key, target_key, exclusion, delta_values, trace_flag)
        return

    # ----------------------------------------------------------
    # private or methods common to multiple inherited instances
    # ----------------------------------------------------------
    def loadMaxMin(
        self,
        my_measure: json,
        json_file_data: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        tracing_flag: bool = False,
        b_use_rate: bool = False,
    ):
        """
            loadMaxMinInObservation

            load in obs max/min value if present
            update delta_values

            calculus v2
        """
        obs_j = obs_meteor.data.j
        if delta_values.__contains__(target_key) is False:
            # no value processed
            return

        m_stop_dat = json_file_data['data'][measure_idx]['stop_dat']
        data_src = {}
        if json_file_data['data'][measure_idx].__contains__('current'):
            data_src = json_file_data['data'][measure_idx]['current']

        for maxmin_sufx in ['_max', '_min']:
            # is max or min needed for this measure
            maxmin_key = maxmin_sufx.split('_')[1]
            maxmin_suffix = maxmin_sufx
            if b_use_rate:
                maxmin_suffix = '_rate' + maxmin_sufx
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                maxmin_time = m_stop_dat

                # is there a M_max/M_min in the data_src ?
                if data_src.__contains__(src_key + maxmin_suffix):
                    # found, then load in in obs and delta_values
                    my_maxmin_value = my_measure['dataType'](data_src[src_key + maxmin_suffix])
                    obs_j[target_key + maxmin_suffix] = my_maxmin_value
                    if data_src.__contains__(src_key + maxmin_suffix + '_time'):
                        maxmin_time = data_src[src_key + maxmin_suffix + '_time']
                    obs_j[target_key + maxmin_suffix + '_time'] = maxmin_time
                    delta_values[target_key + maxmin_suffix] = my_maxmin_value
                    delta_values[target_key + maxmin_suffix + '_time'] = maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and maxmin_suffix == '_max':
                        """ save Wind_max_dir """
                        if data_src.__contains__(src_key + maxmin_suffix + '_dir') is True:
                            my_wind_dir = int(data_src[src_key + maxmin_suffix + '_dir'])
                            obs_j[target_key + maxmin_suffix + '_dir'] = my_wind_dir
                            delta_values[target_key + maxmin_suffix + '_dir'] = my_wind_dir
                elif delta_values.__contains__(target_key + '_i'):
                    # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                    if b_use_rate:
                        # pour les "rate" on prend l'avg (qui est un rate)
                        delta_values[target_key + maxmin_suffix] = delta_values[target_key + '_sum']
                    else:
                        # sinon on prend la valeur de la mesure
                        delta_values[target_key + maxmin_suffix] = delta_values[target_key + '_i']
                    delta_values[target_key + maxmin_suffix + '_time'] = maxmin_time

    def get_src_key(self, my_measure: json):
        """
            return the target key name

            calculus v1
            calculus v2
        """
        src_key = my_measure['src_key']
        target_key = src_key
        if my_measure.__contains__('target_key'):
            target_key = my_measure['target_key']
        elif isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            target_key += '_omm'
        return (src_key, target_key)
