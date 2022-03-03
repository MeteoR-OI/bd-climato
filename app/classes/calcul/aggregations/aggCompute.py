from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.extremeTodoMeteor import ExtremeTodoMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.tools.climConstant import MeasureProcessingBitMask
from app.tools.aggTools import isFlagged, delKey, getAggDuration, getMeanAngle
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
        m_agg_j: json,
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
                m_agg_j: aggregations clause in json file, for this aggregation
                delta_values: json for delta values to include in this aggregation
                dv_next: delta_values that will be used for next level
                trace_flag
        """
        # exit if only hour agregation
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.OnlyAggregateInHour) is True and agg_decas[0].agg_niveau[0] != 'H':
            my_dv_next = {'duration': dv_next.get('duration'), 'maxminFix': []}     # do not store any data in dv_next, use a dummy variable
        else:
            my_dv_next = dv_next

        # init default
        target_key = my_measure['target_key']

        if target_key == 'rain_omm':
            target_key = 'rain_omm'

        agg_main_j = agg_decas[0].data.j
        agg_level = agg_decas[0].getLevelCode()
        m_suffix, isSum = self.get_suffix(my_measure)
        delete_measure = False

        if delta_values.get('duration') is None:
            tmp_duration = getAggDuration(agg_level[0], agg_decas[0].data.start_dat)
        else:
            tmp_duration = float(delta_values["duration"])

        # ------------------------------------------------------------------
        # get our measure data
        # 1 from dv[target_key + '_s'] and dv[target_key + '_d']
        # 2 from m_agg_j[target_key_s] and m_agg_j[target_key_d]
        # 3 from m_agg_j[target_key_avg/_sum/_rate] and compute _s/_d new values
        # last non null win
        # ------------------------------------------------------------------

        # get current values from aggregation row
        old_measure_s = 0 if agg_main_j.get(target_key + '_s') is None else agg_main_j[target_key + '_s']
        old_measure_d = 0 if agg_main_j.get(target_key + '_d') is None else agg_main_j[target_key + '_d']

        # get our M_s/M_d from our delta_values
        if delta_values.get(target_key + '_d') is None:
            has_measure = False
            measure_d = 0
        else:
            has_measure = True
            measure_d = delta_values[target_key + '_d']
        measure_s = 0 if has_measure is False else delta_values.get(target_key + '_s')

        if m_agg_j.get(target_key + '_s') is not None:
            if old_measure_d != 0:
                raise Exception('cannot have a value in <aggregations>, with exisitng data in the aggregation row. key = ' + target_key)
            has_measure = True
            measure_s = m_agg_j.get(target_key + '_s')
            measure_d = m_agg_j.get(target_key + '_d')
            if measure_d is None:
                measure_d = m_agg_j.get('default_duration')

        # get the agregated value, and recompute the _d/_s delta needed
        elif m_agg_j.get(target_key + m_suffix) is not None:
            has_measure = True
            measure_aggregated = m_agg_j.get(target_key + m_suffix)
            measure_d = tmp_duration - old_measure_d
            if measure_d is None:
                measure_d = m_agg_j.get('default_duration')
            if isSum is True:
                measure_s = measure_aggregated - old_measure_s
            else:
                measure_s = (measure_aggregated * tmp_duration) - old_measure_s

        if has_measure is True:
            if (measure_d + old_measure_d) == 0:
                # no duration, delete all keys
                delKey(agg_main_j, target_key + '_s')
                delKey(agg_main_j, target_key + '_d')
                delKey(agg_main_j, target_key + '_avg')
                delete_measure = True
            else:
                agg_main_j[target_key + '_s'] = measure_s + old_measure_s
                agg_main_j[target_key + '_d'] = measure_d + old_measure_d
                if isSum is False:
                    agg_main_j[target_key + m_suffix] = measure_s / measure_d
            # update my_dv_next for next level
            my_dv_next[target_key + '_s'] = measure_s
            my_dv_next[target_key + '_d'] = measure_d

        # ------------------------------------------------------------------
        # get our max/min data
        # 1 from dv[target_key + '_max'], _min
        #   including delete_measur
        # 2 from m_agg_j[target_key + '_max], _min
        # if need to recompute -> call add_new_maxmin_fix
        # ------------------------------------------------------------------

        idx_maxmin = 0
        for maxmin_key in ['max', 'min']:
            maxmin_suffix = '_' + maxmin_key
            idx_maxmin += 1
            agg_maxmin_j = agg_decas[idx_maxmin].data.j

            # var default value
            new_value = new_time = new_dir = None
            cur_value = cur_time = None     # cur_dir not needed

            # load current values if exist
            if agg_maxmin_j.get(target_key + maxmin_suffix) is not None:
                cur_value = agg_maxmin_j[target_key + maxmin_suffix]
                cur_time = agg_maxmin_j[target_key + maxmin_suffix + '_time']

            # # if extreme has to be calculated
            # if delete_measure is False and my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:
            #     # load delta_values
            #     if delta_values.get(target_key + maxmin_suffix) is not None:
            #         new_value = delta_values[target_key + maxmin_suffix]
            #         new_time = delta_values[target_key + maxmin_suffix + '_time']
            #         if delta_values.get(target_key + maxmin_suffix + '_dir') is not None:
            #             new_dir = delta_values[target_key + maxmin_suffix + '_dir']

            # if extreme has to be calculated
            if delete_measure is False and my_measure[maxmin_key] is True:
                # load delta_values
                if delta_values.get(target_key + maxmin_suffix) is not None:
                    new_value = delta_values[target_key + maxmin_suffix]
                    new_time = delta_values[target_key + maxmin_suffix + '_time']
                    if delta_values.get(target_key + maxmin_suffix + '_dir') is not None:
                        new_dir = delta_values[target_key + maxmin_suffix + '_dir']

                # load forced aggregated values

            # get value to challenge in delete situation
            challenge_value = challenge_time = challenge_dir = None
            for maxmin_fix in delta_values['maxminFix']:
                if challenge_value is None:
                    if maxmin_fix['key'] == target_key and maxmin_fix['type'] == maxmin_key:
                        challenge_value = maxmin_fix['value']
                        challenge_time = maxmin_fix['date']
                        challenge_dir = maxmin_fix['dir']

            if m_agg_j.get(target_key + maxmin_suffix) is not None:
                if cur_value is None:
                    IncidentMeteor.new(
                        'aggCompute',
                        'W',
                        'Impossible to use an aggregated value when obs values exist',
                        {
                            "key": target_key,
                            "maxmin": maxmin_key,
                            "level": agg_decas[0].agg_niveau,
                            "poste_id": agg_decas[0].data.poste_id,
                            "start_dat": agg_decas[0].data.start_dat,
                            "valeur_cur": cur_value,
                            "valeur_agg": challenge_value,
                            "date_cur": cur_time,
                            "date_agg": challenge_time,
                        })
                    action = 's'
                else:
                    new_value = m_agg_j[target_key + maxmin_suffix]
                    new_time = m_agg_j[target_key + maxmin_suffix + '_time']
                    if m_agg_j.get(target_key + maxmin_suffix + '_dir') is not None:
                        new_dir = m_agg_j[target_key + maxmin_suffix + '_dir']
            action = self.get_extreme_action(maxmin_key, cur_value, cur_time, new_value, new_time, challenge_value, challenge_time)

            match (action):
                case 'n':
                    agg_maxmin_j[target_key + maxmin_suffix] = new_value
                    my_dv_next[target_key + maxmin_suffix] = new_value
                    agg_maxmin_j[target_key + maxmin_suffix + '_time'] = new_time
                    my_dv_next[target_key + maxmin_suffix + '_time'] = new_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if new_dir is not None:
                            agg_maxmin_j[target_key + maxmin_suffix + '_dir'] = new_dir
                            my_dv_next[target_key + maxmin_suffix + '_dir'] = new_dir
                case 'c':
                    agg_maxmin_j[target_key + maxmin_suffix] = challenge_value
                    my_dv_next[target_key + maxmin_suffix] = challenge_value
                    agg_maxmin_j[target_key + maxmin_suffix + '_time'] = challenge_time
                    my_dv_next[target_key + maxmin_suffix + '_time'] = challenge_time
                    # propagate fix request to next level
                    my_dv_next.maxminFix.append({
                        'key': target_key,
                        'ope': 'd',
                        'type': maxmin_suffix,
                        'value': challenge_value,
                        'date': challenge_time,
                        'dir': challenge_dir,
                    })
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if challenge_dir is not None:
                            agg_maxmin_j[target_key + maxmin_suffix + '_dir'] = challenge_dir
                            my_dv_next[target_key + maxmin_suffix + '_dir'] = challenge_dir

                case 's':
                    pass

                case 'd':
                    # delete extreme data for this key
                    delKey(agg_maxmin_j, target_key + maxmin_suffix)
                    delKey(agg_maxmin_j, target_key + maxmin_suffix + '_tine')
                    delKey(agg_maxmin_j, target_key + maxmin_suffix + '_dir')
                    my_dv_next['maxminFix'].append({
                        'key': target_key,
                        'ope': 'd',
                        'type': maxmin_suffix,
                        'value': cur_value,
                        'date': cur_time,
                        'dir': agg_maxmin_j[target_key + maxmin_suffix + '_dir']
                    })

                case 'r':
                    raise Exception("not yet coded")

                case 'e':
                    raise Exception('Invalid data: key: ' + target_key + ' action returned an error')

        # ------------------------------------------------------------------
        # get our wind data
        # 1 from dv[target_key + '_dir_nb'], _sin, _cos  delta values !
        # 2 from m_agg_j[target_key + '_dir_nb], _sin, _cos absolute values !
        # last win
        # ------------------------------------------------------------------
        dv_wind_nb = dv_wind_sin = dv_wind_cos = 0
        has_wind_measure = False
        if isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind) is True:
            agg_wind_nb = agg_wind_sin = agg_wind_cos = 0
            if agg_main_j.get(target_key + '_dir_nb') is not None:
                has_wind_measure = True
                agg_wind_nb = agg_main_j[target_key + '_dir_nb']
                agg_wind_sin = agg_main_j[target_key + '_dir_sin']
                agg_wind_cos = agg_main_j[target_key + '_dir_cos']

            if delta_values.get(target_key + '_dir_nb') is not None:
                has_wind_measure = True
                dv_wind_nb = delta_values[target_key + '_dir_nb']
                dv_wind_sin = delta_values[target_key + '_dir_sin']
                dv_wind_cos = delta_values[target_key + '_dir_cos']

            if m_agg_j.get(target_key + '_dir_nb') is not None:
                has_wind_measure = True
                dv_wind_nb = dv_wind_nb - m_agg_j[target_key + '_dir_nb']
                dv_wind_sin = dv_wind_sin - m_agg_j[target_key + '_dir_sin']
                dv_wind_cos = dv_wind_cos - m_agg_j[target_key + '_dir_cos']

            if has_wind_measure is True:
                my_dv_next[target_key + '_dir_nb'] = dv_wind_nb
                my_dv_next[target_key + '_dir_sin'] = dv_wind_sin
                my_dv_next[target_key + '_dir_cos'] = dv_wind_cos

                if (dv_wind_nb + agg_wind_nb) == 0:
                    delKey(agg_main_j, target_key + '_dir')
                    delKey(agg_main_j, target_key + '_dir_nb')
                    delKey(agg_main_j, target_key + '_dir_sin')
                    delKey(agg_main_j, target_key + '_dir_cos')
                else:
                    agg_main_j[target_key + '_dir_nb'] = dv_wind_nb + agg_wind_nb
                    agg_main_j[target_key + '_dir_sin'] = dv_wind_sin + agg_wind_sin
                    agg_main_j[target_key + '_dir_cos'] = dv_wind_cos + agg_wind_cos
                    agg_main_j[target_key + '_dir'] = getMeanAngle(agg_main_j[target_key + '_dir_nb'], agg_main_j[target_key + '_dir_sin'], agg_main_j[target_key + '_dir_cos'])

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
