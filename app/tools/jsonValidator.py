import json
import datetime
from app.classes.repository.posteMeteor import PosteMeteor
# from app.tools.jsonPlus import JsonPlus


def checkJson(j: json) -> str:
    idx = 0
    val_to_add = []
    if j.__contains__('meteor') is False or j['meteor'].__len__() == 0:
        return 'missing or invalid code meteor'

    pid = PosteMeteor.getPosteIdByMeteor(j['meteor'])
    if pid is None:
        return('code meteor inconnu: ' + j['meteor'])
    j['poste_id'] = pid

    while idx < j['data'].__len__():
        new_val = {}
        if j['data'][idx].__contains__('current') is False:
            return 'no current key in j.data[' + str(idx) + ']'
        a_current = j['data'][idx]['current']

        if a_current.__contains__('duration') is False:
            return 'no duration in j.data[' + str(idx) + '].current'
        measure_duration = a_current['duration']

        if a_current.__contains__('stop_dat') is False:
            if a_current.__contains__('start_dat') is False:
                return 'no start and stop_dat in j.data[' + str(idx) + '].current'
            measure_duration = datetime.timedelta(minutes=int(a_current['duration']))
            new_val['stop_dat'] = a_current['start_dat'] + measure_duration

        if a_current.__contains__('start_dat') is False:
            measure_duration = datetime.timedelta(minutes=int(a_current['duration']))
            new_val['start_dat'] = a_current['stop_dat'] - measure_duration

        # print('idx: ' + str(idx) + ', ' + str(a_current['stop_dat']))

        for key in a_current.__iter__():
            if str(key).endswith('_max') or str(key).endswith('_min'):
                if a_current.__contains__(key + '_time') is False:
                    new_val[key + '_time'] = a_current['stop_dat']
                    val_to_add.append(new_val)
            if str(key).endswith('_sum') and a_current.__contains(key[:-4] + '_duration') is False:
                new_val[key[:-4] + '_duration'] = measure_duration
                val_to_add.append(new_val)

        if j['data'][idx].__contains__('aggregations'):
            all_aggreg = j['data'][idx]['aggregations']
            idx2 = 0
            while idx2 < all_aggreg.__len__():
                a_aggreg = j['data'][idx]['aggregations'][idx2]
                if a_aggreg.__contains__('level') is False:
                    return 'no level in data[' + str(idx) + '].aggregations[' + str(idx2) + ']'
                lvl = a_aggreg['level']
                if lvl != 'H' and lvl != 'D' and lvl != 'M' and lvl != 'Y' and lvl != 'A':
                    return lvl + ' is invalid level in data[' + str(idx) + '].aggregations[' + str(idx2) + ']'

                idx2 += 1
        idx += 1

    # print('check step2')
    idx = 0
    # print(JsonPlus().dumps(val_to_add))
    while idx < val_to_add.__len__():
        my_val = val_to_add[idx]
        my_current = j['data'][idx]['current']
        for key in my_val.__iter__():
            my_current[key] = my_val[key]
        idx += 1
    return None
