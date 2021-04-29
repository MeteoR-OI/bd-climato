# Line number should match in lines 10, 20, 30
from app.tools.jsonPlus import JsonPlus
from app.tools.myTools import CopyJson, logException, logInfo, logTrace
import pytest


@pytest.mark.unit
def test_logException():
    inst = Exception('test_logE', 'this is an Exception')
    log_e = logException(inst, "12345", {"a": 1}, True)
    assert log_e['span_id'] == "12345"
    assert log_e['loc'] == "test_logException::10"
    assert log_e['level'] == 'error'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_logInfo():
    log_e = logInfo("my message", "12345", {"a": 1}, True)
    assert log_e['msg'] == 'my message'
    assert log_e['span_id'] == "12345"
    assert log_e['loc'] == "test_logInfo::19"
    assert log_e['level'] == 'info'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_logTrace():
    log_e = logTrace("my message", "12345", {"a": 1}, True)
    assert log_e['msg'] == 'my message'
    assert log_e['span_id'] == "12345"
    assert log_e['loc'] == "test_logTrace::29"
    assert log_e['level'] == 'trace'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_copyJson():
    src = {"n": 12, "s": "abc", "j": {"b": 23, "c": [1, 2, 3], "d": {"e": 45}}, "a": ["a", "b", "c"]}
    dest = {}
    CopyJson(src, dest)
    print(JsonPlus().dumps(dest))
