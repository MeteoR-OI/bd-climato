# import sys
# with open('/tmp/python-sys-path.txt', 'w') as outfile:
#     print("** PATH **: " + str(sys.path))
import pytest
from app.tools.aggTools import getAggDuration, addJson


def test_getAggDuration():
    assert int(getAggDuration('H')) == int(60)
    assert int(getAggDuration('D')) == int(1440)
    assert int(getAggDuration('M')) == int(43920)
    assert int(getAggDuration('Y')) == int(525960)


def test_addJson():
    jj = {}
    addJson(jj, 'a', 12)
    assert jj['a'] == 12

    addJson(jj, 'a', -2)
    assert jj['a'] == 10
