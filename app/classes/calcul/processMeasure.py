import datetime
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import AggLevel, MeasureProcessingBitMask
from app.tools.aggTools import isFlagged
from app.tools.aggTools import getRightAggregation
import json


class ProcessMeasure():
    """
        ProcessMeasure

        Computation specific to a measure type

    """
    # p should be called with o.dat in case of delete !
    # {'type_i': 1, 'key': 'out_temp', 'field': 'out_temp', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def updateObsAndGetDelta(self, poste_metier: PosteMetier, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, flag: bool) -> json:
        """
            getProcessObject

            generate deltaValues and load Observation
                flag=True => from our json data
                flag=False => from the obs data

            calculation methods are implemented as virtual in the xxxCompute module
        """
        try:
            # deltaValues returned for aggregation processing
            delta_values = {'extremes': []}
            key_name = my_measure['key']
            # load field if defined in json
            field_name = key_name
            if my_measure.__contains__('field'):
                field_name = my_measure['field']

            # get exclusion for the measure type
            exclusion = poste_metier.exclusion(my_measure['type_i'])

            b_set_null = False      # the measure is invalidated

            # get the exclusion value if specified, and not the string 'null'
            if exclusion.__contains__(field_name) is True and exclusion[field_name] == 'null':
                b_set_null = True

            # no processing if measure is nullified by an exclusion
            if b_set_null is True:
                return delta_values

            m_suffix = ''
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.IsOmmMeasure)):
                m_suffix = '_omm'

            # in delete situation, generate the delta_values from the obs dataset
            if flag is False:
                return self.getDeltaFromObs(my_measure, obs_meteor, field_name, m_suffix, exclusion)

            # load obs record, and get the delta_values added
            delta_values = self.loadObsGetDelta(my_measure, measures, measure_idx, obs_meteor, field_name, m_suffix, exclusion, flag)

            # load Max/Min and update delta_values
            self.loadMaxMin(my_measure, measures, measure_idx, obs_meteor, field_name, exclusion, delta_values, flag)

            return delta_values

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    # {'key': 'out_temp', 'field': 'out_temp', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def updateAggAndGetDeltaVal(self, poste_metier: PosteMetier, my_measure: json, measures: json, measure_idx: int, aggregations: list, delta_values: json, flag: bool) -> json:
        """ update all aggregation from the delta data, and aggregations key on json, return a list of extremes to recompute """
        try:
            key_name = my_measure['key']
            # load field if defined in json
            field_name = key_name
            if my_measure.__contains__('field'):
                field_name = my_measure['field']

            m_suffix = ''
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.IsOmmMeasure)):
                m_suffix = '_omm'

            for anAgg in AggLevel:
                """loop for all aggregations in ascending level"""
                dv_next = {}

                # array of aggregations, current, and prev/next for agg_day only
                all_agg = []
                for anAgg in aggregations:
                    if anAgg.agg_niveau == anAgg:
                        all_agg.append(anAgg)
                        if anAgg == "D":
                            all_agg.append(aggregations[5])
                            all_agg.append(aggregations[6])

                # get the rigth aggregation with hour_deca
                measure_dat = measures['data'][measure_idx]['current']['dat']
                agg_active = getRightAggregation(anAgg, measure_dat, my_measure['hour_deca'], all_agg)

                # get exclusion
                exclusion = poste_metier.exclusion(my_measure['type_i'])

                # do nothing if exclusion is nullify
                if exclusion.__contains__(field_name) is True and exclusion[field_name] == 'null':
                    return delta_values

                # load data in our aggregation
                self.loadAggGetDelta(my_measure, measures, measure_idx, agg_active, field_name, m_suffix, delta_values, dv_next, flag)

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
            return delta_values

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly

    def recomputeExtremes():
        print('to do')

    # -------------------------
    # private or virtal methods
    # --------------------------
    def getDeltaFromObs(self, my_measure: json, obs_meteor: ObsMeteor, field_name: str, m_suffix: str, exclusion: json) -> json:
        """
            getDeltaFromObs

            get delta_values from current Obs
            Always in substracting mode, because this is called only in delete obs situation
        """
        try:
            delta_values = {'extremes': []}
            b_set_val = True        # a value is forced in exclusion
            b_set_null = False      # the measure is invalidated
            obs_j = obs_meteor.data.j

            # get the exclusion value if specified, and not the string 'null'
            if exclusion.__contains__(field_name) is True and exclusion[field_name] != 'value':
                # exclusion[field_name] = 'null' or value_to_force
                b_set_val = False
                if exclusion[field_name] == 'null':
                    b_set_null = True

            if b_set_null is False:
                if b_set_val:
                    # value forced from exclusion
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                        delta_values[field_name + m_suffix + '_sum'] = exclusion[field_name] * -1
                    else:
                        delta_values[field_name + m_suffix + '_sum'] = exclusion[field_name] * obs_meteor.data['duration'] * -1
                    delta_values[field_name + m_suffix + '_duration'] = obs_meteor.data['duration'] * -1
                elif obs_j.__contains__(field_name + m_suffix):
                    # use the value in obs_meteor
                    if b_set_val:
                        if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsSum)):
                            delta_values[field_name + m_suffix + '_sum'] = obs_j[field_name] * -1
                        else:
                            delta_values[field_name + m_suffix + '_sum'] = obs_j[field_name] * obs_meteor.data['duration'] * -1
                        delta_values[field_name + m_suffix + '_duration'] = obs_meteor.data['duration'] * -1
            return delta_values

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly

    def loadObsGetDelta(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, field_name: str, exclusion: json, flag: bool) -> json:
        raise Exception("loadObsGetDelta", "not allowed in parent class")

    def loadMaxMin(self, my_measure: json, measures: json, measure_idx: int, obs_meteor: ObsMeteor, field_name: str, exclusion: json, delta_values: json, flag: bool) -> json:
        """
            loadMaxMin

            load in obs max/min value if present
            update delta_values
        """
        try:
            b_set_val = True        # a value is forced in exclusion
            b_set_null = False      # the measure is invalidated
            obs_j = obs_meteor.data.j

            # get the exclusion value if specified, and not the string 'null'
            if exclusion.__contains__(field_name) is True and exclusion[field_name] != 'value':
                # exclusion[field_name] = 'null' or value_to_force
                b_set_val = False
                if exclusion[field_name] == 'null':
                    b_set_null = True

            m_suffix = ''
            if (isFlagged(my_measure['special'], MeasureProcessingBitMask.IsOmmMeasure)):
                m_suffix = '_omm'

            if b_set_val:
                if measures['data'][measure_idx].__contains__('current'):
                    data_src = measures['data'][measure_idx]['current']
                else:
                    data_src = {}
            else:
                data_src = exclusion

            # in exclusion + nullify return an empty json
            if b_set_null:
                return delta_values

            half_period_time = measures['data'][measure_idx]['current']['dat'] + datetime.timedelta(seconds=int(measures['data'][measure_idx]['current']['duration'] / 2))

            for my_avg in ['_max', '_min']:
                # is there a M_max/M_min in the data_src ?
                if data_src.__contains__(field_name + m_suffix + my_avg):
                    # found, then load in in obs and delta_values
                    obs_j[field_name + m_suffix + my_avg] = data_src[field_name + m_suffix + my_avg]
                    obs_j[field_name + m_suffix + my_avg + '_time'] = data_src[field_name + m_suffix + my_avg + '_time']
                    delta_values[field_name + m_suffix + my_avg] = data_src[field_name + m_suffix + my_avg]
                    delta_values[field_name + m_suffix + my_avg + '_time'] = data_src[field_name + m_suffix + my_avg + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and my_avg == '_max':
                        """ save Wind_max_dir """
                        obs_j[field_name + m_suffix + my_avg + '_dir'] = data_src[field_name + m_suffix + my_avg + '_dir']
                elif obs_j.__contains__(field_name + m_suffix):
                    # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                    delta_values[field_name + m_suffix + my_avg] = obs_j[field_name + m_suffix]
                    delta_values[field_name + m_suffix + my_avg + '_time'] = half_period_time

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly
