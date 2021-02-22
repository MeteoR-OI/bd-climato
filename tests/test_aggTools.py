from app.tools.aggTools import getAggDuration
from app.tools.aggTools import addJson


def test_getAggDuration():
    dur = getAggDuration('H')
    assert dur == 60

    dur = getAggDuration('D')
    assert dur == (60 * 24)


def test_addJson():
    jj = {}
    addJson(jj, 'a', 12)
    assert jj['a'] == 12

    addJson(jj, 'a', -2)
    assert jj['a'] == 10
