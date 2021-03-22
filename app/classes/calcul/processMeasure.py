from app.classes.repository.obsMeteor import ObsMeteor
from app.tools.climConstant import AggLevel, MeasureProcessingBitMask
from app.tools.aggTools import isFlagged, delKey
from app.tools.aggTools import shouldNullify
from app.tools.aggTools import calcAggDate
import json
import datetime


class ProcessMeasure():
    """
        ProcessMeasure

        Computation specific to a measure type

    """
    # p should be called with o.dat in case of delete !
    # {'type_i': 1, 'src_key': 'out_temp', 'target_key': 'out_temp', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
    def processObservation(
        self,
        poste_metier,
        my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        delta_values: json,
        trace_flag: bool = False,
    ):
        """
            getProcessObject

            generate deltaValues and load Observation

            calculation methods are implemented as virtual in the xxxCompute module
        """
        # load field if defined in json
        src_key, target_key = self.get_src_key(my_measure)

        # get exclusion, and return if value is nullified
        exclusion = poste_metier.exclusion(my_measure['type_i'])
        if shouldNullify(exclusion, src_key) is True:
            return

        # load obs record, and get the delta_values added
        # should load dv[M_value], and dv[first_time] when in omm mode
        self.loadObservationDatarow(
            my_measure,
            measures,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            exclusion,
            delta_values,
            trace_flag,
        )

        # load Max/Min and update delta_values
        self.loadMaxMinInObservation(
            my_measure,
            measures,
            measure_idx,
            obs_meteor,
            src_key,
            target_key,
            exclusion,
            delta_values,
            trace_flag,
        )

        # save our delta_values if in trace mode
        if trace_flag is True:
            j_obs = obs_meteor.data.j
            if j_obs.__contains__('dv') is False:
                j_obs['dv'] = {}
            for akey in delta_values.items():
                j_obs['dv'][akey[0]] = delta_values[akey[0]]
        return

    def processAggregations(
        self,
        poste_metier,
        my_measure: json,
        measures: json,
        measure_idx: int,
        aggregations: list,
        delta_values: json,
        trace_flag: bool = False,
    ):
        """ update all aggregation from the delta data, and aggregations key on json, return a list of extremes to recompute """

        # load field if defined in json
        src_key, target_key = self.get_src_key(my_measure)

        # get exclusion, and return if value is nullified
        exclusion = poste_metier.exclusion(my_measure['type_i'])
        if shouldNullify(exclusion, src_key) is True:
            return

        # load the current aggregations array for our anAgg
        deca_hour = 0
        if my_measure.__contains__('hour_deca') is True:
            deca_hour = my_measure['hour_deca']

        measure_dat = calcAggDate('H', measures['data'][measure_idx]['current']['stop_dat'], deca_hour, True)

        for anAgg in AggLevel:
            measure_dat = calcAggDate(anAgg, measure_dat, 0, False)

            """loop for all aggregations in ascending level"""
            dv_next = {"maxminFix": []}

            # load our array of current aggregation, plus prev/next for agg_day only
            agg_deca = None
            for my_agg in aggregations:
                if my_agg.agg_niveau == anAgg and my_agg.data.start_dat == measure_dat:
                    agg_deca = my_agg
                    break

            if agg_deca is None:
                raise Exception('processAggregations', 'aggregation not loaded')

            # load data in our aggregation
            self.loadAggregationDatarows(
                my_measure,
                measures,
                measure_idx,
                agg_deca,
                target_key,
                delta_values,
                dv_next,
            )

            # get our extreme values
            self.loadMaxMinInAggregation(
                my_measure,
                measures,
                measure_idx,
                agg_deca,
                target_key,
                exclusion,
                delta_values,
                dv_next,
            )
            # save our delta_values if in trace mode
            if trace_flag is True:
                j_agg = agg_deca[0].data.j
                if j_agg.__contains__('dv') is False:
                    j_agg['dv'] = {}
                for akey in delta_values.items():
                    j_agg['dv'][akey[0]] = delta_values[akey[0]]

            # we will pass our new delta_values to the next level
            delta_values = dv_next
        return

    def recomputeExtremes():
        print('to do')

    # ----------------------------------------------------
    # private or methods common to multiple sub-instances
    # ----------------------------------------------------
    def loadMaxMinInObservation(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        b_use_rate: bool = False,
    ):
        """
            loadMaxMinInObservation

            load in obs max/min value if present
            update delta_values
        """
        obs_j = obs_meteor.data.j
        if delta_values.__contains__(target_key) is False:
            # no value processed
            return

        half_period_len = datetime.timedelta(minutes=float(measures['data'][measure_idx]['current']['duration'] / 2))
        half_period_time = measures['data'][measure_idx]['current']['stop_dat'] - half_period_len
        data_src = {}
        if measures['data'][measure_idx].__contains__('current'):
            data_src = measures['data'][measure_idx]['current']

        for maxmin_suffix in ['_max', '_min']:
            # is max or min needed for this measure
            maxmin_key = maxmin_suffix.split('_')[1]
            if b_use_rate:
                maxmin_suffix = '_rate' + maxmin_suffix
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                maxmin_time = half_period_time

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
                elif delta_values.__contains__(target_key):
                    # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                    if b_use_rate:
                        # pour les "rate" on prend l'avg (qui est un rate)
                        delta_values[target_key + maxmin_suffix] = delta_values[target_key + '_sum']
                    else:
                        # sinon on prend la valeur de la mesure
                        delta_values[target_key + maxmin_suffix] = delta_values[target_key]
                    delta_values[target_key + maxmin_suffix + '_time'] = maxmin_time

    def loadMaxMinInAggregation(
        self, my_measure: json,
        measures: json,
        measure_idx: int,
        my_aggreg,
        json_key: str,
        exclusion: json,
        delta_values: json,
        dv_next: json,
        b_use_rate: bool = False,
    ):
        """
            loadMaxMinInObservation

            load in obs max/min  i our aggregation value if present
            update dv_next for nest level
        """
        # save our dv, and get agg_j, m_agg_j
        m_agg_j = self.get_agg_magg(my_aggreg, delta_values, measures, measure_idx)
        agg_j = my_aggreg.data.j

        for maxmin_suffix in ['_max', '_min']:
            maxmin_key = maxmin_suffix.split('_')[1]
            if b_use_rate:
                maxmin_suffix = '_rate' + maxmin_suffix

            if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:

                if m_agg_j.__contains__(json_key + '_delete_me') is True:
                    # measure was deleted previously
                    delKey(m_agg_j, json_key + maxmin_suffix + '_max')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_max_time')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_min')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_min_time')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_first_time')
                    continue

                # if the max-min is required in measure definition
                current_maxmin = None

                if delta_values.__contains__(json_key + maxmin_suffix) is True:
                    # load from delta_values
                    current_maxmin = my_measure['dataType'](delta_values[json_key + maxmin_suffix])
                    current_maxmin_time = delta_values[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        current_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

                if m_agg_j.__contains__(json_key + maxmin_suffix):
                    # load and use json measure maxmin if given in aggregation key
                    current_maxmin = my_measure['dataType'](m_agg_j[json_key + maxmin_suffix])
                    current_maxmin_time = m_agg_j[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        current_maxmin_dir = None
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(m_agg_j[json_key + maxmin_suffix + '_dir'])

                if current_maxmin is None:
                    # no values
                    continue

                # load current data from our aggregation
                if agg_j.__contains__(json_key + maxmin_suffix):
                    agg_maxmin = agg_j[json_key + maxmin_suffix]
                else:
                    # force the usage of current_maxmin
                    if maxmin_suffix == '_min':
                        agg_maxmin = current_maxmin + 1
                    else:
                        agg_maxmin = current_maxmin - 1

                b_change_maxmin = False
                if delta_values.__contains__(json_key + '_maxmin_invalid_val' + maxmin_suffix) and agg_maxmin == delta_values[json_key + '_maxmin_invalid_val' + maxmin_suffix]:
                    self.add_new_maxmin_fix(json_key, maxmin_key, my_aggreg.data.start_dat, delta_values, my_aggreg)
                    dv_next[json_key + '_maxmin_invalid_val' + maxmin_suffix] = agg_maxmin
                    b_change_maxmin = True
                # compare the measure data and current maxmin
                if maxmin_suffix == '_max' and agg_maxmin < current_maxmin:
                    b_change_maxmin = True
                if maxmin_suffix == '_min' and agg_maxmin > current_maxmin:
                    b_change_maxmin = True

                if b_change_maxmin:
                    agg_j[json_key + maxmin_suffix] = current_maxmin
                    dv_next[json_key + maxmin_suffix] = current_maxmin
                    agg_j[json_key + maxmin_suffix + '_time'] = current_maxmin_time
                    dv_next[json_key + maxmin_suffix + '_time'] = current_maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if current_maxmin_dir is not None:
                            agg_j[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir
                            dv_next[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir

    def get_src_key(self, my_measure: json):
        """ return the target key name """
        src_key = my_measure['src_key']
        target_key = src_key
        if my_measure.__contains__('target_key'):
            target_key = my_measure['target_key']
        elif isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            target_key += '_omm'
        return (src_key, target_key)

    def add_new_maxmin_fix(self, json_key: str, maxmin_key: str, measure_date: datetime, delta_values: json, my_aggreg):
        delta_values['maxminFix'].append({
            "posteId": my_aggreg.data.poste_id_id,
            "startDat": my_aggreg.data.start_dat,
            "level": my_aggreg.agg_niveau,
            "maxmin": maxmin_key,
            "key": json_key,
            "valeur": my_aggreg.data.j[json_key + '_' + maxmin_key],
            "dat": measure_date,
        })
