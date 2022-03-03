from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.extremeTodoMeteor import ExtremeTodoMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.tools.aggTools import isFlagged, delKey, getMeanAngle
import json


class AggCompute():
    """
        ProcessAggreg

        Computation specific to a measure type
    """

    def loadDVDataInAggregation(
        self,
        my_measure: json,
        agg_decas: AggMeteor,
        delta_values: json,
        dv_next: json,
        trace_flag: bool = False,
    ):
        """
            loadDVDataInAggregation

            Load one aggretation level with values from delta_values, update my_dv_next

            parameters:
                my_measure: measure definition
                agg_decas[0]: aggregation row
                delta_values: values to include in this aggregation
                dv_next: delta_values that will have to be propagated into next level
                trace_flag
        """
        # exit if only hour agregation
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True and agg_decas[0].agg_niveau[0] != 'H':
            my_dv_next = {'duration': dv_next.get('duration'), 'maxminFix': []}     # do not store any data in dv_next, use a dummy variable
        else:
            my_dv_next = dv_next

        # init default
        target_key = my_measure['target_key']

        agg_main_j = agg_decas[0].data.j
        # agg_level = agg_decas[0].getLevelCode()
        m_suffix, isSum = self.get_suffix(my_measure)

        # get current values from aggregation row
        old_measure_s = 0 if agg_main_j.get(target_key + '_s') is None else agg_main_j[target_key + '_s']
        old_measure_d = 0 if agg_main_j.get(target_key + '_d') is None else agg_main_j[target_key + '_d']
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind) is True:
            old_wind_dir_nb = old_wind_dir_cos = old_wind_dir_sin = 0
            if agg_main_j.get(target_key + '_dir_nb') is not None:
                old_wind_dir_nb = agg_main_j[target_key + '_dir_nb']
                old_wind_dir_sin = agg_main_j[target_key + '_dir_sin']
                old_wind_dir_cos = agg_main_j[target_key + '_dir_cos']

        # get our M_s/M_d from our delta_values
        if delta_values.get(target_key + '_d') is not None:
            measure_d = delta_values[target_key + '_d']
            measure_s = delta_values[target_key + '_s']
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind) is True:
                measure_wind_dir_nb = measure_wind_dir_cos = measure_wind_dir_sin = 0
                if delta_values.get(target_key + '_dir_nb') is not None:
                    measure_wind_dir_nb = delta_values[target_key + '_dir_nb']
                    measure_wind_dir_sin = delta_values[target_key + '_dir_sin']
                    measure_wind_dir_cos = delta_values[target_key + '_dir_cos']

            # do we need to remove the measure ?
            if (measure_d + old_measure_d) == 0:
                # no duration, delete all keys
                delKey(agg_main_j, target_key + '_s')
                delKey(agg_main_j, target_key + '_d')
                delKey(agg_main_j, target_key + '_avg')
                delKey(agg_main_j, target_key + '_dir')
                delKey(agg_main_j, target_key + '_dir_nb')
                delKey(agg_main_j, target_key + '_dir_sin')
                delKey(agg_main_j, target_key + '_dir_cos')
            else:
                agg_main_j[target_key + '_s'] = measure_s + old_measure_s
                agg_main_j[target_key + '_d'] = measure_d + old_measure_d
                if isSum is False:
                    agg_main_j[target_key + m_suffix] = measure_s / measure_d
                if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind) is True:
                    agg_main_j[target_key + '_dir_nb'] = old_wind_dir_nb + measure_wind_dir_nb
                    agg_main_j[target_key + '_dir_sin'] = old_wind_dir_sin + measure_wind_dir_sin
                    agg_main_j[target_key + '_dir_cos'] = old_wind_dir_cos + measure_wind_dir_cos
                    agg_main_j[target_key + '_dir'] = getMeanAngle(agg_main_j[target_key + '_dir_nb'], agg_main_j[target_key + '_dir_sin'], agg_main_j[target_key + '_dir_cos'])

            # update my_dv_next for next level
            my_dv_next[target_key + '_s'] = measure_s
            my_dv_next[target_key + '_d'] = measure_d
            if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind) is True:
                my_dv_next[target_key + '_dir_nb'] = measure_wind_dir_nb
                my_dv_next[target_key + '_dir_sin'] = measure_wind_dir_sin
                my_dv_next[target_key + '_dir_cos'] = measure_wind_dir_cos

        # get our max/min data
        idx_maxmin_in_agg_decas = 0
        for maxmin_key in ['max', 'min']:
            maxmin_suffix = '_' + maxmin_key

            # get the right aggregation for the max/min
            idx_maxmin_in_agg_decas += 1
            agg_maxmin_j = agg_decas[idx_maxmin_in_agg_decas].data.j

            # get value to challenge in delete situation
            challenge_value = challenge_time = challenge_dir = None
            for maxmin_fix in delta_values['maxminFix']:
                if challenge_value is None:
                    if maxmin_fix['key'] == target_key and maxmin_fix['type'] == maxmin_key:
                        challenge_value = maxmin_fix['value']
                        challenge_time = maxmin_fix['date']
                        challenge_dir = maxmin_fix.get('dir')

            # decide how to handle maxmin values
            action = self.get_extreme_action(
                maxmin_key,
                agg_maxmin_j.get(target_key + maxmin_suffix),
                agg_maxmin_j.get(target_key + maxmin_suffix + '_time'),
                delta_values.get(target_key + maxmin_suffix),
                delta_values.get(target_key + maxmin_suffix + '_time'),
                challenge_value,
                challenge_time,
            )

            match (action):
                case 'n':
                    # update with new values
                    agg_maxmin_j[target_key + maxmin_suffix] = delta_values.get(target_key + maxmin_suffix)
                    my_dv_next[target_key + maxmin_suffix] = delta_values.get(target_key + maxmin_suffix)
                    agg_maxmin_j[target_key + maxmin_suffix + '_time'] = delta_values.get(target_key + maxmin_suffix + '_time')
                    my_dv_next[target_key + maxmin_suffix + '_time'] = delta_values.get(target_key + maxmin_suffix + '_time')
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if delta_values.get(target_key + maxmin_suffix + '_dir') is not None:
                            agg_maxmin_j[target_key + maxmin_suffix + '_dir'] = delta_values.get(target_key + maxmin_suffix + '_dir')
                            my_dv_next[target_key + maxmin_suffix + '_dir'] = delta_values.get(target_key + maxmin_suffix + '_dir')

                case 'c':
                    # update with challenge data
                    agg_maxmin_j[target_key + maxmin_suffix] = challenge_value
                    my_dv_next[target_key + maxmin_suffix] = challenge_value
                    agg_maxmin_j[target_key + maxmin_suffix + '_time'] = challenge_time
                    my_dv_next[target_key + maxmin_suffix + '_time'] = challenge_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and challenge_dir is not None:
                        agg_maxmin_j[target_key + maxmin_suffix + '_dir'] = challenge_dir
                        my_dv_next[target_key + maxmin_suffix + '_dir'] = challenge_dir

                case 's':
                    # skip - keep current values or None
                    pass

                case 'd':
                    # delete extreme data
                    delKey(agg_maxmin_j, target_key + maxmin_suffix)
                    delKey(agg_maxmin_j, target_key + maxmin_suffix + '_tine')
                    delKey(agg_maxmin_j, target_key + maxmin_suffix + '_dir')

                    # add a challenge entry for the next level
                    my_dv_next['maxminFix'].append({
                        'key': target_key,
                        'ope': 'd',
                        'type': maxmin_suffix,
                        'value': agg_maxmin_j.get(target_key + maxmin_suffix),
                        'date': agg_maxmin_j.get(target_key + maxmin_suffix + '_time'),
                        'dir': agg_maxmin_j[target_key + maxmin_suffix + '_dir']
                    })

                case 'r':
                    raise Exception("not yet coded")

                case 'e':
                    raise Exception('Invalid data: key: ' + target_key + ' action returned an error')

    def add_new_recompute(self, target_key: str, maxmin_key: str, agg_deca: AggMeteor, valeur: float, ttime: str, dir: str):
        max_min_fix = {
            "key": target_key,
            "maxmin": maxmin_key,
            "level": agg_deca.agg_niveau,
            "poste_id": agg_deca.data.poste_id,
            "start_dat": agg_deca.data.start_dat,
            "valeur": valeur,
            "date": ttime,
            "dir": dir,
        }
        # write an extreme_todo record
        e_todo = ExtremeTodoMeteor(agg_deca.data.poste_id, agg_deca.agg_niveau, agg_deca.data.start_dat, maxmin_key)
        e_todo.data.j_recompute = max_min_fix
        e_todo.save()

    def get_extreme_action(self, maxmin_key: str, cur_value: float, cur_time: str, new_value: float, new_time: str, chal_value: float, chal_time: str):
        """
            get_extreme_action

            return:
                s (skip = keep current)
                n (use new_xxx)
                c (use chal_xxx)
                d (delete)
                r (recompute)
                e (error)
        """
        comp_func = less_than
        if maxmin_key == 'max':
            comp_func = greather_than

        #   cur_value +  new_value + compu_f + chal_value +
        #      None   +     None   +         +    None     +  's'
        if chal_value == new_value and new_value == cur_value and cur_value is None:
            return 's'

        # more often situation: no challenge data
        #   cur_value    +  new_value + compu_f + chal_value +
        #    Not None    +     None   +         +    None     +  skip
        #      None      +      10    +         +    None     +  update new
        #        5       +      10    +   -1    +    None     +  update new
        #       10       +      10    +    0    +    None     +  cur_time < new_time -> upate new, sinon skip
        #       15       +      10    +    1    +    None     +  skip
        if chal_value is None:
            if cur_value is None:
                return "n"
            elif new_value is None:
                return 's'
            match (comp_func(cur_value, new_value)):
                case -1:
                    return "n"
                case 0:
                    if new_time > cur_time:
                        return "n"
                    return "s"
                case 1:
                    return "s"

        #   cur_value    + new_value + compu_f +   chal_value   +
        #      None      +    None   +         +       10       +  Error
        #        5       +    None   +   -1    +       10       +  Error
        #       10       +    None   +    0    +       10       +  check dates: is chal_time == cur_time -> recompute sinon skip
        #       15       +    None   +    1    +       10       +  skip
        if new_value is None:
            if cur_value is None:
                return 'e'
            match (comp_func(cur_value, chal_value)):
                case -1:
                    return "e"
                case 0:
                    if chal_time == cur_time:
                        return 'r'
                    return "s"
                case 1:
                    return "s"

        # cur_value +  new_value + chal_value + compu_f +
        #    None   +     10     +      5     +         +  Error

        # cur_value < new_value
        #      5    +     10     +      5     +         +  update new_xxx
        #      5    +     10     +     10     +         +  si chal_time > new_time -> update chal_xxx sinon update new_xxx
        #      5    +     10     +     15     +         +  update chal_xxx

        # cur_value == new_value
        #    10    +     10     +      5     +         +  si new_time > cur_time -> update new sinon skip
        #    10    +     10     +     10     +         +  si new_time > cur_time ->
        #                                              +     si chal_time > new_time -> update chal sinon update new
        #                                              +  sinon chal_time > cur_time -> update chal sinon skip
        #    10    +     10     +     15     +         +  update chal

        # cur_value > new_value
        #    15    +     10     +      5     +         +  skip
        #    15    +     10     +     15     +         +  si chal_time > cur_date -> update chal_xxx sinon skip
        #    15    +     10     +     20     +         +  Error

        # cur_time +  new_time + compu_f +   chal_value
        #       10      +     10     +    0    +         10       +  check dates -> update or pass

        if cur_value is None:
            return 'e'
        match (comp_func(cur_value, new_value)):
            case -1:
                match(comp_func(new_value, chal_value)):
                    case -1:
                        return "n"
                    case 0:
                        if chal_time > new_time:
                            return "c"
                        else:
                            return "n"
                    case 1:
                        return "c"
            case 0:
                match(comp_func(new_value, chal_value)):
                    case -1:
                        if new_time > cur_time:
                            return "n"
                        else:
                            return "s"
                    case 0:
                        if new_time > cur_time:
                            if chal_time > new_time:
                                return "c"
                            else:
                                return "n"
                        else:
                            if chal_time > cur_time:
                                return "c"
                            else:
                                return "s"
                    case 1:
                        return "c"
            case 1:
                match(comp_func(cur_value, chal_value)):
                    case -1:
                        return "s"
                    case 0:
                        if chal_time > cur_time:
                            return "c"
                        else:
                            return "s"
                    case 1:
                        return "e"

        raise Exception('get_extreme_action: action not found...')

    def get_suffix(self, my_measure):
        # isAvg = isRate = False
        isSum = False
        match(my_measure['agg']):
            case 'avg' | 'avgomm':
                # isAvg = True
                m_suffix = '_avg'
            case 'sum' | 'sumomm':
                isSum = True
                m_suffix = '_sum'
            case 'rate' | 'rateomm':
                # isRate = True
                m_suffix = '_rate'
            case 'no':
                m_suffix = ''
            case '_':
                raise Exception('invalid [agg] value: ' + str(my_measure['agg']))
        return m_suffix, isSum


def less_than(a, b) -> int:
    if a == b:
        return 0
    if a < b:
        return 1
    return -1


def greather_than(a, b) -> bool:
    if a == b:
        return 0
    if a > b:
        return 1
    return -1
