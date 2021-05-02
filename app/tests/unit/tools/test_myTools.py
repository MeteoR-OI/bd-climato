# Line number should match in lines 10, 20, 30
from app.tools.myTools import CopyJson, LogException, logInfo, logTrace
import pytest


@pytest.mark.unit
def test_LogException():
    inst = Exception('test_logE', 'this is an Exception')
    log_e = LogException(inst, None, {"a": 1}, True)
    assert log_e['loc'] == "test_LogException::9"
    assert log_e['level'] == 'error'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_logInfo():
    log_e = logInfo("my message", None, {"a": 1}, True)
    assert log_e['msg'] == 'my message'
    assert log_e['loc'] == "test_logInfo::17"
    assert log_e['level'] == 'info'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_logTrace():
    log_e = logTrace("my message", None, {"a": 1}, True)
    assert log_e['msg'] == 'my message'
    assert log_e['loc'] == "test_logTrace::26"
    assert log_e['level'] == 'trace'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_copyJson():
    src = {"n": 12, "s": "abc", "j": {"b": 23, "c": [1, 2, 3], "d": {"e": 45}}, "a": ["a", "b", "c"]}
    dest = {}
    CopyJson(src, dest)
    assert src["a"].__len__() == dest["a"].__len__()
    assert src["j"]["b"] == dest["j"]["b"]
    assert src["n"] == dest["n"]
    assert src["s"] == dest["s"]
