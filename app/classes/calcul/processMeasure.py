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
        self.loadMaxMin(my_measure, measures, measure_idx, obs_meteor, src_key, target_key, exclusion, delta_values, flag)

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

            # todo: process max/min

            # if gs.has(data_src, field_name + '_max'):
            #     if gs.is_max(agg_ds, gs.get(data_src, field_name + '_max'), field_name + '_max'):
            #         tmp_max = float(gs.get(data_src, [field_name + '_max']))
            #         gs.set(agg_ds, tmp_max, field_name + '_max')
            #         gs.set(dv_next, tmp_max, field_name + '_max')
            #         tmp_max_time = jsonp.dumps(gs.get(data_src, [field_name + '_max_time']))
            #         gs.set(agg_ds, tmp_max_time, field_name + '_max_time')
            #         gs.set(dv_next, tmp_max_time, field_name + '_max_time')
            #         if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
            #             tmp_dir = gs.get(data_src, [field_name + '_max_dir'])
            #             gs.set(agg_ds, tmp_dir, field_name + '_max_dir')
            #             gs.set(dv_next, tmp_dir, field_name + '_max_dir')
            # else:
            #     if gs.has(delta_values, field_name + '_max'):
            #         tmp_max = gs.get(delta_values, field_name + '_max')
            #         if gs.is_max(agg_ds, tmp_max, field_name + '_max'):
            #             tmp_max = float(
            #                 gs.get(delta_values, field_name + '_max'))
            #             gs.set(agg_ds, tmp_max, field_name + '_max')
            #             gs.set(dv_next, tmp_max, field_name + '_max')
            #             tmp_max_time = jsonp.dumps(gs.get(delta_values, field_name + '_max_time'))
            #             gs.set(agg_ds, tmp_max_time, field_name + '_max_time')
            #             gs.set(dv_next, tmp_max_time, field_name + '_max_time')
            #             if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
            #                 tmp_dir = gs.get(data_src, field_name + '_max_dir')
            #                 gs.set(agg_ds, tmp_dir, field_name + '_max_dir')
            #                 gs.set(dv_next, tmp_dir, field_name + '_max_dir')

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

    def loadMaxMin(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, src_key: str, target_key: str, exclusion: json, delta_values: json, flag: bool):
        """
            loadMaxMin

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
            # is there a M_max/M_min in the data_src ?
            if data_src.__contains__(src_key + maxmin_suffix):
                # found, then load in in obs and delta_values
                my_avg_value = float(data_src[src_key + maxmin_suffix])
                obs_j[target_key + maxmin_suffix] = my_avg_value
                if data_src.__contains__(src_key + maxmin_suffix + '_time'):
                    my_avg_time = data_src[src_key + maxmin_suffix + '_time']
                else:
                    my_avg_time = half_period_time
                obs_j[target_key + maxmin_suffix + '_time'] = my_avg_time
                delta_values[target_key + maxmin_suffix] = my_avg_value
                delta_values[target_key + maxmin_suffix + '_time'] = my_avg_time
                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and maxmin_suffix == '_max':
                    """ save Wind_max_dir """
                    obs_j[target_key + maxmin_suffix + '_dir'] = int(data_src[src_key + maxmin_suffix + '_dir'])
            elif obs_j.__contains__(target_key + '_value'):
                # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                delta_values[target_key + maxmin_suffix] = my_measure['dataType'](target_key + '_value')
                delta_values[target_key + maxmin_suffix + '_time'] = half_period_time
