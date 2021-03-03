import datetime
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import AggLevel, MeasureProcessingBitMask
from app.tools.aggTools import isFlagged
from app.tools.aggTools import getRightAggregation, shouldNullify
import json


class ProcessMeasure():
    """
        ProcessMeasure

        Computation specific to a measure type

    """
    # p should be called with o.dat in case of delete !
    # {'type_i': 1, 'src_key': 'out_temp', 'target_key': 'out_temp', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def processObservation(self, poste_metier: PosteMetier, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, delta_values: json, flag: bool):
        """
            getProcessObject

            generate deltaValues and load Observation
                flag=True => from our json data
                flag=False => from the obs data

            calculation methods are implemented as virtual in the xxxCompute module
        """
        # load field if defined in json
        src_key = my_measure['src_key']
        target_key = src_key
        if my_measure.__contains__('target_key'):
            target_key = my_measure['target_key']
        elif isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            target_key += '_omm'

        # get exclusion for the measure type
        exclusion = poste_metier.exclusion(my_measure['type_i'])

        # load obs record, and get the delta_values added
        # should load dv[M_value], and dv[first_time] when in omm mode
        self.loadObservationDatarow(my_measure, measures, measure_idx, obs_meteor, src_key, target_key, exclusion, delta_values, flag)

        # load Max/Min and update delta_values
        self.loadMaxMinFromMeasures(my_measure, measures, measure_idx, obs_meteor, src_key, target_key, exclusion, delta_values, flag)

        return

    def processAggregations(self, poste_metier: PosteMetier, my_measure: json, measures: json, measure_idx: int, aggregations: list, delta_values: json, flag: bool):
        """ update all aggregation from the delta data, and aggregations key on json, return a list of extremes to recompute """
        # be sure that we have an extremesFix key
        if delta_values.__contains__("extremesFix") is False:
            delta_values['extremesFix'] = []

        src_key = my_measure['src_key']
        target_key = src_key
        if my_measure.__contains__('target_key'):
            target_key = my_measure['target_key']
        elif isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            target_key += '_omm'

        # get exclusion
        exclusion = poste_metier.exclusion(my_measure['type_i'])
        # do nothing if exclusion is nullify
        if shouldNullify(exclusion, src_key) is True:
            return

        measure_dat = measures['data'][measure_idx]['current']['dat']

        for anAgg in AggLevel:
            """loop for all aggregations in ascending level"""
            dv_next = {}

            # load an array of aggregations, current, and prev/next for agg_day only
            all_agg = []
            for my_agg in aggregations:
                if my_agg.data.level == anAgg:
                    all_agg.append(my_agg)
                    if anAgg == "D":
                        all_agg.append(aggregations[5])
                        all_agg.append(aggregations[6])
                    break

            # get the rigth aggregation with hour_deca (only for day)
            agg_deca = getRightAggregation(anAgg, measure_dat, my_measure['hour_deca'], all_agg)
            all_agg = []

            # load data in our aggregation
            self.loadAggregationDatarows(my_measure, measures, measure_idx, agg_deca, target_key, delta_values, dv_next, flag)

            self.loadMaxMinInAggregation(my_measure, measures, measure_idx, agg_deca, target_key, exclusion, delta_values, dv_next, flag)

            # we give our new delta_values to the next level
            delta_values = dv_next
        return

    def recomputeExtremes():
        print('to do')

    # -------------------------
    # private or virtal methods
    # --------------------------
    def loadObservationDatarow(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, src_key: str, target_key: str, exclusion: json, delta_values: json, flag: bool):
        raise Exception("loadObservationDatarow", "not allowed in parent class")

    def getDeltaFromObs(self, my_measure: json, obs_meteor: ObsMeteor, json_key: str, delta_values: json):
        raise Exception("getDeltaFromObs", "not allowed in parent class")

    def loadAggregationDatarows(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        agg_relative,
        json_key: str,
        delta_values: json,
        dv_next: json,
        flag: bool,
    ):
        raise Exception("loadAggregationDatarows", "not allowed in parent class")

    def loadMaxMinFromMeasures(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, src_key: str, target_key: str, exclusion: json, delta_values: json, flag: bool):
        """
            loadMaxMinFromMeasures

            load in obs max/min value if present
            update delta_values
        """
        obs_j = obs_meteor.data.j
        if delta_values.__contains__(target_key + '_value') is False:
            # no value processed
            return

        half_period_time = measures['data'][measure_idx]['current']['dat'] + datetime.timedelta(minutes=float(measures['data'][measure_idx]['current']['duration'] / 2))
        data_src = {}
        if measures['data'][measure_idx].__contains__('current'):
            data_src = measures['data'][measure_idx]['current']

        for maxmin_suffix in ['_max', '_min']:
            # is max or min needed for this measure
            maxmin_key = maxmin_suffix.split('_')[1]
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                # is there a M_max/M_min in the data_src ?
                if data_src.__contains__(src_key + maxmin_suffix):
                    # found, then load in in obs and delta_values
                    my_maxmin_value = my_measure['dataType'](data_src[src_key + maxmin_suffix])
                    obs_j[target_key + maxmin_suffix] = my_maxmin_value
                    if data_src.__contains__(src_key + maxmin_suffix + '_time'):
                        my_avg_time = data_src[src_key + maxmin_suffix + '_time']
                    else:
                        my_avg_time = half_period_time
                    obs_j[target_key + maxmin_suffix + '_time'] = my_avg_time
                    delta_values[target_key + maxmin_suffix] = my_maxmin_value
                    delta_values[target_key + maxmin_suffix + '_time'] = my_avg_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and maxmin_suffix == '_max':
                        """ save Wind_max_dir """
                        if data_src.__contains__(src_key + maxmin_suffix + '_dir') is True:
                            my_wind_dir = int(data_src[src_key + maxmin_suffix + '_dir'])
                            obs_j[target_key + maxmin_suffix + '_dir'] = my_wind_dir
                            delta_values[target_key + maxmin_suffix + '_dir'] = my_wind_dir
                elif data_src.__contains__(src_key):
                    # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                    delta_values[target_key + maxmin_suffix] = my_measure['dataType'](data_src[src_key])
                    delta_values[target_key + maxmin_suffix + '_time'] = half_period_time

    def loadMaxMinInAggregation(self, my_measure: json, measures: json, measure_idx: int, my_aggreg, json_key: str, exclusion: json, delta_values: json, dv_next: json, flag: bool):
        """
            loadMaxMinFromMeasures

            load in obs max/min value if present
            update delta_values
        """
        agg_j = my_aggreg.data.j
        # get aggregation values in measures
        m_agg_j = {}
        if measures.__contains__('data') and measures['data'][measure_idx].__contains__('aggregations'):
            for a_j_agg in measures['data'][measure_idx]['aggregations']:
                if a_j_agg['level'] == my_aggreg.data.level:
                    m_agg_j = a_j_agg
                    break

        for maxmin_suffix in ['_max', '_min']:
            maxmin_key = maxmin_suffix.split('_')[1]

            if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:
                tmp_maxmin = None

                if delta_values.__contains__(json_key + maxmin_suffix) is True:
                    # load from delta_values
                    tmp_maxmin = my_measure['dataType'](delta_values[json_key + maxmin_suffix])
                    tmp_maxmin_time = delta_values[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        tmp_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            tmp_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

                if m_agg_j.__contains__(json_key + maxmin_suffix):
                    # load and use measure maxmin if given
                    tmp_maxmin = my_measure['dataType'](m_agg_j[json_key + maxmin_suffix])
                    tmp_maxmin_time = m_agg_j[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        tmp_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            tmp_maxmin_dir = int(m_agg_j[json_key + maxmin_suffix + '_dir'])

                if tmp_maxmin is None:
                    # no data in dv, neither on aggregation
                    if delta_values.__contains__(json_key) is False:
                        # can't compute without a data
                        return
                    tmp_maxmin_time = measures['data'][measure_idx]['current']['dat'] + datetime.timedelta(minutes=float(measures['data'][measure_idx]['current']['duration'] / 2))
                    tmp_maxmin = my_measure['dataType'](delta_values[json_key])
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        tmp_maxmin_dir = None

                # load current data from our aggregation
                if agg_j.__contains__(json_key + maxmin_suffix):
                    current_maxmin = agg_j[json_key + maxmin_suffix]
                else:
                    if maxmin_suffix == '_min':
                        current_maxmin = tmp_maxmin + 1
                    else:
                        current_maxmin = tmp_maxmin - 1

                # compare the measure data and current maxmin
                if (maxmin_suffix == '_max' and tmp_maxmin > current_maxmin) or (maxmin_suffix == '_min' and tmp_maxmin < current_maxmin):
                    agg_j[json_key + maxmin_suffix] = tmp_maxmin
                    dv_next[json_key + maxmin_suffix] = tmp_maxmin
                    agg_j[json_key + maxmin_suffix + '_time'] = tmp_maxmin_time
                    dv_next[json_key + maxmin_suffix + '_time'] = tmp_maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if tmp_maxmin_dir is not None:
                            agg_j[json_key + maxmin_suffix + '_dir'] = tmp_maxmin_dir
                            dv_next[json_key + maxmin_suffix + '_dir'] = tmp_maxmin_dir
