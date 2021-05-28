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

    def loadDVMaxMinInAggregation(
        self,
        my_measure: json,
        m_stop_date: datetime,
        agg_decas: AggMeteor,
        m_agg_j: json,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
    ):
        """
            loadDVMaxMinInAggregation

            load in all aggregations max/min
            update dv_next for nest level
        """
        target_key = my_measure['target_key']
        idx_maxmin = 1
        for maxmin_suffix in ['_max', '_min']:
            agg_j = agg_decas[idx_maxmin].data.j
            agg_decas[idx_maxmin].dirty = True
            idx_maxmin += 1

            maxmin_key = maxmin_suffix.split('_')[1]

            if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:
                new_calulated_maxmin = None
                new_calulated_maxmin_dir = None

                if target_key == "wind" and maxmin_key == 'max':
                    target_key = "wind"

                # check if measure was deleted
                if delta_values.__contains__(target_key + '_delete_me') is True:
                    # measure was deleted previously
                    if agg_j.__contains__(target_key + maxmin_suffix):
                        # need to invalidate this value for next level
                        invalid_value = agg_j[target_key + maxmin_suffix]
                        dv_next[target_key + maxmin_suffix + '_invalidate'] = invalid_value
                        dv_next[target_key + '_check' + maxmin_suffix] = agg_j[target_key + maxmin_suffix]
                    delKey(agg_j, target_key + maxmin_suffix)
                    delKey(agg_j, target_key + maxmin_suffix + '_time')
                    continue

                # get the current max/min (the last load win)
                # - load current value form delta_values
                # - load current max/min from delta_values if given
                # - load from "aggregations" clause in the json data file if given
                if delta_values.__contains__(target_key):
                    new_calulated_maxmin = my_measure['dataType'](delta_values[target_key])
                    new_calulated_maxmin_time = m_stop_date
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if delta_values.__contains__(target_key + maxmin_suffix + '_dir') is True:
                            new_calulated_maxmin_dir = float(delta_values[target_key + maxmin_suffix + '_dir'])

                if delta_values.__contains__(target_key + maxmin_suffix) is True:
                    new_calulated_maxmin = my_measure['dataType'](delta_values[target_key + maxmin_suffix])
                    new_calulated_maxmin_time = delta_values[target_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if m_agg_j.__contains__(target_key + maxmin_suffix + '_dir') is True:
                            new_calulated_maxmin_dir = float(delta_values[target_key + maxmin_suffix + '_dir'])

                if m_agg_j.__contains__(target_key + maxmin_suffix):
                    new_calulated_maxmin = my_measure['dataType'](m_agg_j[target_key + maxmin_suffix])
                    new_calulated_maxmin_time = m_agg_j[target_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if m_agg_j.__contains__(target_key + maxmin_suffix + '_dir') is True:
                            new_calulated_maxmin_dir = float(m_agg_j[target_key + maxmin_suffix + '_dir'])

                if new_calulated_maxmin is None:
                    # should never occurs...
                    continue

                # load current max/min value from our aggregation
                agg_maxmin = None
                if agg_j.__contains__(target_key + maxmin_suffix):
                    agg_maxmin = agg_j[target_key + maxmin_suffix]

                """
                invalidation decision tree for [field]_max

                new_calulated_maxmin  +   agg_maxmin  +  former_maxmin_value +  action
                basic
                    10                +               +           No          +  update
                    10                +       5       +           No          +  update
                    10                +       10      +           No          +  pass
                    10                +       15      +           No          +  pass

                check_maxmin flag
                    10                +       5       +           5           +  update -> auto
                    10                +       10      +           10          +  pass -> auto
                    10                +       15      +           15          +  recompute
                """
                if delta_values.__contains__(target_key + '_check' + maxmin_suffix):
                    if agg_maxmin is None:
                        raise Exception('loadDVMaxMinInAggregation', 'Invalidate and no data in aggregation...')
                    former_maxmin_value = delta_values[target_key + '_check' + maxmin_suffix]
                    if maxmin_suffix == '_max':
                        if agg_maxmin > former_maxmin_value:
                            agg_maxmin = None
                            dv_next[target_key + '_check' + maxmin_suffix] = former_maxmin_value
                            self.add_new_maxmin_fix(target_key, maxmin_key, my_measure['deca' + maxmin_suffix], agg_decas[idx_maxmin], delta_values)
                    else:
                        if agg_maxmin < former_maxmin_value:
                            agg_maxmin = None
                            dv_next[target_key + '_check' + maxmin_suffix] = former_maxmin_value
                            self.add_new_maxmin_fix(target_key, maxmin_key, my_measure['deca' + maxmin_suffix], agg_decas[idx_maxmin], delta_values)

                if agg_maxmin is None:
                    # force the update i agg_deca for our new_calulated_maxmin
                    if maxmin_suffix == '_min':
                        agg_maxmin = new_calulated_maxmin + 1
                    else:
                        agg_maxmin = new_calulated_maxmin - 1

                b_change_maxmin = False
                if (target_key == "wind"):
                    print('testing: agg_' + agg_decas[idx_maxmin].agg_niveau + ': ' + str(agg_maxmin) + ', new_calc: ' + str(new_calulated_maxmin) + ', equal? ' + str(agg_maxmin == new_calulated_maxmin))
                    if agg_j.__contains__(target_key + maxmin_suffix + '_time'):
                        print("  wind_max: old_time=> " + str(agg_j[target_key + maxmin_suffix + '_time']) + ", new=> " + str(new_calulated_maxmin_time))
                        print("  agg: id: " + str(agg_decas[idx_maxmin].data.id) + ', level: ' + agg_decas[idx_maxmin].agg_niveau + ', start_dat: ' + str(agg_decas[idx_maxmin].data.start_dat))
                    else:
                        print("  wind_max: old_time=> ** no data **, new=> " + str(new_calulated_maxmin_time))
                        print("  agg: id: " + str(agg_decas[idx_maxmin].data.id) + ', level: ' + agg_decas[idx_maxmin].agg_niveau + ', start_dat: ' + str(agg_decas[idx_maxmin].data.start_dat))
                # compare the measure data and current maxmin
                if maxmin_suffix == '_max' and agg_maxmin < new_calulated_maxmin:
                    if (target_key == "wind"):
                        print('   *** agg < new_calc')
                    b_change_maxmin = True
                if maxmin_suffix == '_max' and agg_maxmin == new_calulated_maxmin and str(agg_j[target_key + maxmin_suffix + '_time']) < str(new_calulated_maxmin_time):
                    if (target_key == "wind"):
                        print('   *** max agg_time < new_calc_time -> yes')
                    b_change_maxmin = True
                if maxmin_suffix == '_max' and agg_maxmin == new_calulated_maxmin and str(agg_j[target_key + maxmin_suffix + '_time']) > str(new_calulated_maxmin_time):
                    if (target_key == "wind"):
                        print('   *** max agg_time > new_calc_time -> NO')
                if maxmin_suffix == '_min' and agg_maxmin > new_calulated_maxmin:
                    b_change_maxmin = True
                if maxmin_suffix == '_min' and agg_maxmin == new_calulated_maxmin and str(agg_j[target_key + maxmin_suffix + '_time']) < str(new_calulated_maxmin_time):
                    b_change_maxmin = True

                if b_change_maxmin:
                    agg_j[target_key + maxmin_suffix] = new_calulated_maxmin
                    dv_next[target_key + maxmin_suffix] = new_calulated_maxmin
                    agg_j[target_key + maxmin_suffix + '_time'] = new_calulated_maxmin_time
                    dv_next[target_key + maxmin_suffix + '_time'] = new_calulated_maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if new_calulated_maxmin_dir is not None:
                            agg_j[target_key + maxmin_suffix + '_dir'] = new_calulated_maxmin_dir
                            dv_next[target_key + maxmin_suffix + '_dir'] = new_calulated_maxmin_dir
                else:
                    if (target_key == "wind"):
                        print('   *** skipped')

    def add_new_maxmin_fix(self, target_key: str, maxmin_key: str, deca: int, agg_deca: AggMeteor, delta_values: json):
        # calculus v1
        max_min_fix = {
            "deca": deca,
            "key": target_key,
            "level": agg_deca.agg_niveau,
            "maxmin": maxmin_key,
            "poste_id": agg_deca.data.poste_id_id,
            "start_dat": agg_deca.data.start_dat,
            "valeur": agg_deca.data.j[target_key + '_' + maxmin_key],
        }
        delta_values['maxminFix'].append(max_min_fix)
        # write an extreme_todo record
        e_todo = ExtremeTodoMeteor(agg_deca.data.poste_id_id, agg_deca.agg_niveau, agg_deca.data.start_dat, maxmin_key)
        e_todo.data.j_invalid = max_min_fix
        e_todo.save()

    def get_json_value(self, j: json, key: str, suffix_list: list, key_preffix_first: bool):
        key_list = []
        if key_preffix_first is not None and key_preffix_first is False:
            key_list.append(key)
        for a_suffix in suffix_list:
            key_list.append(key + a_suffix)
        if key_preffix_first is not None and key_preffix_first is True:
            key_list.append(key)

        for a_key in key_list:
            if j.get(a_key) is not None:
                return j[a_key]
        return None
