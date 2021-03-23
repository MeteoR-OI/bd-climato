# import sys
# with open('/tmp/python-sys-path.txt', 'w') as outfile:
#     print("** PATH **: " + str(sys.path))
import datetime
from app.tools.aggTools import getAggDuration, addJson, calcAggDate
from app.tools.climConstant import ComputationParam
from app.tools.dateTools import str_to_date
import pytest


@pytest.mark.unit
def test_getAggDuration():
    assert int(getAggDuration('H')) == int(60)
    assert int(getAggDuration('D')) == int(1440)
    assert int(getAggDuration('M')) == int(43920)
    assert int(getAggDuration('Y')) == int(525960)


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
    assert ComputationParam.AddHourToMeasureInAggHour == 1

    results = [
        # feuille Excel lignes 36-55, columns: D, G, H, I, J
        {'t': 5,   'h': '2020-12-31 23:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 10,  'h': '2020-12-31 23:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 15,  'h': '2020-12-31 23:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 20,  'h': '2021-01-01 00:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 25,  'h': '2021-01-01 00:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 30,  'h': '2021-01-01 00:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 60,  'h': '2021-01-01 00:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 65,  'h': '2021-01-01 00:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 70,  'h': '2021-01-01 00:00:00+04:00', 'd': '2020-12-31 00:00:00+04:00', 'm': '2020-12-01 00:00:00+04:00'},
        {'t': 75,  'h': '2021-01-01 00:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 80,  'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 85,  'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 90,  'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 95,  'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 100, 'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 105, 'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 110, 'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 115, 'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 120, 'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
        {'t': 125, 'h': '2021-01-01 01:00:00+04:00', 'd': '2021-01-01 00:00:00+04:00', 'm': '2021-01-01 00:00:00+04:00'},
    ]

    dt = str_to_date('2020-12-31T22:45:00')
    sum_duration = 0
    for result in results:
        # compute the delta of duration
        duration = int(result['t']) - sum_duration
        # we got an end date in our json
        end_date = dt + datetime.timedelta(minutes=int(result['t']))

        # compute aggregation dates
        aggh_dt = calcAggDate('H', end_date, 0, True)
        aggd_dt = calcAggDate('D', end_date, 0)
        aggm_dt = calcAggDate('M', end_date, 0)

        # sum the duration to allow to compute delta_duration
        sum_duration += duration

        # check result, and print duration in order to know where is our error...
        assert 't' + str(sum_duration) + '->' + str(aggh_dt) == 't' + str(sum_duration) + '->' + result['h']
        assert 't' + str(sum_duration) + '->' + str(aggd_dt) == 't' + str(sum_duration) + '->' + result['d']
        assert 't' + str(sum_duration) + '->' + str(aggm_dt) == 't' + str(sum_duration) + '->' + result['m']
