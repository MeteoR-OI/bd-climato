import pytest
from app.tools.jsonPlus import JsonPlus
import datetime

jp = JsonPlus()
z = jp.json_test()


@pytest.mark.unit
def test_load_json_from_string():
    # load a json, with date as a str
    jj = jp.loads(z)
    # all dates are datetime after loads
    ret = isinstance(jj['data'][0]['current']['dat'], datetime.datetime)
    assert ret


@pytest.mark.unit
def test_dumps_loads():
    jj = jp.loads(z)
    jj2 = jp.loads(jp.dumps(jj))
    ret = jp.dumps(jj2) == jp.dumps(jj)
    assert ret


@pytest.mark.unit
def test_serialize():
    jj = jp.loads(z)
    jp.serialize(jj)
    ret = isinstance(jj['data'][0]['current']['dat'], str)
    assert ret


@pytest.mark.unit
def test_deserialize():
    jj = jp.loads(z)
    jp.serialize(jj)
    jp.deserialize(jj)
    ret = isinstance(jj['data'][0]['current']['dat'], datetime.datetime)
    assert ret
