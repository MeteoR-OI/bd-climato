import pytest
from app.tools.jsonPlus import JsonPlus
import datetime

jp = JsonPlus()
z = """
        {
            "meteor" : "BBF015",
            "info" : {
                "blabla": "blabla"
            },
            "data":
            [
                {
                    "current":
                        {
                            "dat" : "2021-02-11T13:09:30",
                            "duration" : 5,
                            "out_temp" : 29.5,
                            "out_temp_max": 30.1,
                            "out_temp_max_time": "2021-02-11T13:09:32"
                        },
                    "aggregations": [
                        {
                            "level" : "H",
                            "out_temp_avg" : 32.75
                        },
                        {
                            "level" : "D",
                            "rain_rate_avg" : 1.23
                        }
                    ]
                },
                {
                    "current" :
                        {
                            "dat" : "2021-02-11T13:09:40",
                            "duration" : 5,
                            "out_temp" : 30
                        },
                    "aggregations" : [
                        {
                            "level" : "H",
                            "out_temp_avg" : 33
                        },
                        {
                            "level" : "D",
                            "rain_rate_avg" : 1.23
                        }
                    ]
                }
            ]
        }
    """


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
