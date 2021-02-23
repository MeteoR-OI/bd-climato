# import sys
# with open('/tmp/python-sys-path.txt', 'w') as outfile:
#     print("** PATH **: " + str(sys.path))
import pytest
from app.tools.aggTools import getAggDuration, addJson


def test_getAggDuration():
    assert getAggDuration('H') == 60
    # assert getAggDuration('D') == (60 * 24)


def test_addJson():
    jj = {}
    addJson(jj, 'a', 12)
    assert jj['a'] == 12

    addJson(jj, 'a', -2)
    assert jj['a'] == 10
