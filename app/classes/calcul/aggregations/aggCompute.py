from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.extremeTodoMeteor import ExtremeTodoMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.tools.aggTools import isFlagged, delKey
import json
import datetime


class AggCompute():
    """
        ProcessAggreg

        Computation specific to a measure type
    """

    def loadAggregations(
        self,
        m_stop_date: datetime,
        my_measure: json,
        delta_values: json,
        agg_deca: AggMeteor,
        m_agg_j: json,
        dv_next: json,
        trace_flag: bool = False,
    ):

        # load data in our aggregation
        self.loadDVInAllAggregations(
            my_measure,
            m_stop_date,
            agg_deca,
            m_agg_j,
            delta_values,
            dv_next,
            trace_flag,
        )

        # get our extreme values
        self.loadMaxMinInAllAggregations(
            my_measure,
            m_stop_date,
            agg_deca,
            m_agg_j,
            delta_values,
            dv_next,
            trace_flag,
        )
        # save our delta_values if in trace mode
        if trace_flag is True:
            j_dv_agg = agg_deca[0].data.j
            if j_dv_agg.__contains__('dv') is False:
                j_dv_agg['dv'] = {}
            for akey in delta_values.items():
                j_dv_agg['dv'][akey[0]] = delta_values[akey[0]]
        return

    # ----------------------------------------------------
    # private or methods common to multiple sub-instances
    # ----------------------------------------------------
    def loadMaxMinInAllAggregations(
        self,
        my_measure: json,
        m_stop_date: datetime,
        agg_deca: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        b_use_rate: bool = False,
    ):
        """
            loadMaxMinInAllAggregations

            load in all aggregations max/min
            update dv_next for nest level
        """
        json_key = self.get_json_key(my_measure)
        agg_j = agg_deca.data.j

        for maxmin_suffix in ['_max', '_min']:
            maxmin_key = maxmin_suffix.split('_')[1]
            if b_use_rate:
                maxmin_suffix = '_rate' + maxmin_suffix

            if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:
                current_maxmin = None
                current_maxmin_dir = None

                # check if measure was deleted
                if delta_values.__contains__(json_key + '_delete_me') is True:
                    # measure was deleted previously
                    if agg_j.__contains__(json_key + maxmin_suffix):
                        # need to invalidate this value for next level
                        invalid_value = agg_j[json_key + maxmin_suffix]
                        dv_next[json_key + maxmin_suffix + '_invalidate'] = invalid_value
                    delKey(agg_j, json_key + maxmin_suffix)
                    delKey(agg_j, json_key + maxmin_suffix + '_time')
                    continue

                # get the current max/min (the last load win)
                # - load current value form delta_values
                # - load current max/min from delta_values if given
                # - load from "aggregations" clause in the json data file if given
                if delta_values.__contains__(json_key):
                    current_maxmin = my_measure['dataType'](delta_values[json_key])
                    current_maxmin_time = m_stop_date
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if delta_values.__contains__(json_key + '_dir') is True:
                            current_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

                if delta_values.__contains__(json_key + maxmin_suffix) is True:
                    current_maxmin = my_measure['dataType'](delta_values[json_key + maxmin_suffix])
                    current_maxmin_time = delta_values[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

                if m_agg_j.__contains__(json_key + maxmin_suffix):
                    current_maxmin = my_measure['dataType'](m_agg_j[json_key + maxmin_suffix])
                    current_maxmin_time = m_agg_j[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(m_agg_j[json_key + maxmin_suffix + '_dir'])

                if current_maxmin is None:
                    # should never occurs...
                    continue

                # load current max/min value from our aggregation
                agg_maxmin = None
                if agg_j.__contains__(json_key + maxmin_suffix):
                    agg_maxmin = agg_j[json_key + maxmin_suffix]

                """
                invalidation decision tree for [field]_max

                current_maxmin  +   agg_maxmin  +  invalid_maxmin_value +   action
                basic
                    10          +               +           No          +       update
                    10          +       5       +           No          +       update
                    10          +       15      +           No          +       pass

                invalidate value
                    10          +       5       +           5           +       update -> auto

                    10          +       10      +           10          +       pass -> auto

                    10          +       15      +           11          +       pass -> auto
                    10          +       15      +           15          +       recompute
                """
                if delta_values.__contains__(json_key + '_invalidate' + maxmin_suffix):
                    if agg_maxmin is None:
                        raise Exception('loadMaxMinInAllAggregations', 'Invalidate and no data in aggregation...')
                    invalid_maxmin_value = delta_values[json_key + '_invalidate' + maxmin_suffix]
                    if maxmin_suffix == '_max':
                        if agg_maxmin == invalid_maxmin_value and current_maxmin < agg_maxmin:
                            agg_maxmin = None
                            dv_next[json_key + '_invalidate' + maxmin_suffix] = invalid_maxmin_value
                            self.add_new_maxmin_fix(json_key, maxmin_key, agg_deca, delta_values)
                    else:
                        if agg_maxmin == invalid_maxmin_value and current_maxmin > agg_maxmin:
                            agg_maxmin = None
                            dv_next[json_key + '_invalidate' + maxmin_suffix] = invalid_maxmin_value
                            self.add_new_maxmin_fix(json_key, maxmin_key, agg_deca, delta_values)

                if agg_maxmin is None:
                    # force the update i agg_deca for our current_maxmin
                    if maxmin_suffix == '_min':
                        agg_maxmin = current_maxmin + 1
                    else:
                        agg_maxmin = current_maxmin - 1

                b_change_maxmin = False
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

    def add_new_maxmin_fix(self, json_key: str, maxmin_key: str, agg_deca: AggMeteor, delta_values: json):
        # calculus v1
        max_min_fix = {
            "poste_id": agg_deca.data.poste_id_id,
            "stop_dat": agg_deca.data.poste_id.stop_dat,
            "level": agg_deca.agg_niveau,
            "maxmin": maxmin_key,
            "key": json_key,
            "valeur": agg_deca.data.j[json_key + '_' + maxmin_key],
            "start_dat": agg_deca.data.start_dat,
        }
        delta_values['maxminFix'].append(max_min_fix)
        # write an extreme_todo record
        e_todo = ExtremeTodoMeteor(agg_deca.data.poste_id_id, agg_deca.agg_niveau, agg_deca.data.start_dat, maxmin_key)
        e_todo.data.j_invalid = max_min_fix
        e_todo.save()

    def get_json_key(self, my_measure: json):
        """
            return the target key name
        """
        target_key = my_measure['src_key']
        if my_measure.__contains__('target_key'):
            target_key = my_measure['target_key']
        elif isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            target_key += '_omm'
        return target_key

    def loadDVInAllAggregations(
        self,
        my_measure: json,
        m_stop_date: datetime,
        agg_deca: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
        avg_suffix: str = '_rate',
    ):
        pass
