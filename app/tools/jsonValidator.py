import json
import datetime
# from app.tools.jsonPlus import JsonPlus


def check(j: json) -> str:
    idx = 0
    val_to_add = []
    while idx < j['data'].__len__():
        new_val = {}
        if j['data'][idx].__contains__('current') is False:
            return 'no current key in j.data[' + str(idx) + ']'
        a_current = j['data'][idx]['current']

        if a_current.__contains__('duration') is False:
            return 'no duration in j.data[' + str(idx) + '].current'

        if a_current.__contains__('stop_dat') is False:
            if a_current.__contains__('start_dat') is False:
                return 'no start and stop_dat in j.data[' + str(idx) + '].current'
            measure_duration = datetime.timedelta(minutes=int(a_current['duration']))
            new_val['stop_dat'] = a_current['start_dat'] + measure_duration

        if a_current.__contains__('start_dat') is False:
            measure_duration = datetime.timedelta(minutes=int(a_current['duration']))
            new_val['start_dat'] = a_current['stop_dat'] - measure_duration

        # print('idx: ' + str(idx) + ', ' + str(a_current['stop_dat']))

        half_duration = datetime.timedelta(minutes=int(a_current['duration'])/2)
        half_period = a_current['stop_dat'] - half_duration
        for key in a_current.__iter__():
            if str(key).endswith('_max') or str(key).endswith('_min'):
                if a_current.__contains__(key + '_time') is False:
                    new_val[key + '_time'] = half_period
        val_to_add.append(new_val)
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
