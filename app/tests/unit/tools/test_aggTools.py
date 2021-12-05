import datetime
from app.tools.aggTools import addJson, calcAggDate
from app.tools.dateTools import str_to_date
import pytest


# @pytest.mark.unit
# def test_getAggDuration():
#     assert int(getAggDuration('H')) == int(60)
#     assert int(getAggDuration('D')) == int(1440)
#     assert int(getAggDuration('M')) == int(43920)
#     assert int(getAggDuration('Y')) == int(525960)


@pytest.mark.unit
def test_addJson():
    jj = {}
    addJson(jj, 'a', 12)
    assert jj['a'] == 12

    addJson(jj, 'a', -2)
    assert jj['a'] == 10


@pytest.mark.unit
def test_calcRealAggHourDate():
    # check that our constants matchs our computation made in Excel

    results = [
        {'t': 5,   'h': '2020-12-31 22:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00', 'y': '2020-01-01 00:00:00+04:00'},
        {'t': 10,  'h': '2020-12-31 22:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00', 'y': '2020-01-01 00:00:00+04:00'},
        {'t': 70,  'h': '2020-12-31 23:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00', 'y': '2020-01-01 00:00:00+04:00'},
        {'t': 75,  'h': '2020-12-31 23:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00', 'y': '2020-01-01 00:00:00+04:00'},
        {'t': 80,  'h': '2021-01-01 00:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00', 'y': '2021-01-01 00:00:00+04:00'},
        {'t': 85,  'h': '2021-01-01 00:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00', 'y': '2021-01-01 00:00:00+04:00'},
        {'t': 90,  'h': '2021-01-01 00:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00', 'y': '2021-01-01 00:00:00+04:00'},
        {'t': 135,  'h': '2021-01-01 00:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00', 'y': '2021-01-01 00:00:00+04:00'},
        {'t': 140, 'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00', 'y': '2021-01-01 00:00:00+04:00'}
    ]

    dt = str_to_date('2020-12-31T22:45:00')
    sum_duration = 0
    for result in results:
        # compute the delta of duration
        duration = int(result['t']) - sum_duration

        # sum the duration to allow to compute delta_duration
        sum_duration += duration

        # we got an end date in our json
        end_date = dt + datetime.timedelta(minutes=int(result['t']))

        # compute aggregation dates
        aggh_dt = calcAggDate('H', end_date, 0, True)
        aggd_dt = calcAggDate('D', end_date, 0, True)
        aggd_dt2 = calcAggDate('D', aggh_dt, 0)
        aggm_dt = calcAggDate('M', end_date, 0, True)
        aggm_dt2 = calcAggDate('M', aggh_dt, 0)
        aggy_dt = calcAggDate('Y', end_date, 0, True)
        aggy_dt2 = calcAggDate('Y', aggh_dt, 0)

        # check result, and print duration in order to know where is our error...
        assert 't' + str(sum_duration) + '->' + str(aggh_dt) == 't' + str(sum_duration) + '->' + result['h']
        assert 't' + str(sum_duration) + '->' + str(aggd_dt) == 't' + str(sum_duration) + '->' + result['d']
        assert 't' + str(sum_duration) + '->' + str(aggd_dt2) == 't' + str(sum_duration) + '->' + result['d']
        assert 't' + str(sum_duration) + '->' + str(aggm_dt) == 't' + str(sum_duration) + '->' + result['m']
        assert 't' + str(sum_duration) + '->' + str(aggm_dt2) == 't' + str(sum_duration) + '->' + result['m']
        assert 't' + str(sum_duration) + '->' + str(aggy_dt) == 't' + str(sum_duration) + '->' + result['y']
        assert 't' + str(sum_duration) + '->' + str(aggy_dt2) == 't' + str(sum_duration) + '->' + result['y']
