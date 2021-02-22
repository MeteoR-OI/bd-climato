from app.tools.aggTools import getAggDuration
# import datetimex


def test_getAggDuration():
    dur = getAggDuration('H')
    assert dur == 60

    dur = getAggDuration('D')
    assert dur == (60 * 24)
