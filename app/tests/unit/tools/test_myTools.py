# Line number should match in lines 10, 20, 30
from app.tools.myTools import logException, logInfo, logTrace
import pytest

@pytest.mark.unit
def test_logException():
    inst = Exception('test_logE', 'this is an Exception')
    log_e = logException(inst, "12345", {"a": 1}, True)
    assert log_e['span_id'] == "12345"
    assert log_e['loc'] == "test_logException::8"
    assert log_e['level'] == 'error'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_logInfo():
    log_e = logInfo("my message", "12345", {"a": 1}, True)
    assert log_e['msg'] == 'my message'
    assert log_e['span_id'] == "12345"
    assert log_e['loc'] == "test_logInfo::17"
    assert log_e['level'] == 'info'
    assert log_e["a"] == 1


@pytest.mark.unit
def test_logTrace():
    log_e = logTrace("my message", "12345", {"a": 1}, True)
    assert log_e['msg'] == 'my message'
    assert log_e['span_id'] == "12345"
    assert log_e['loc'] == "test_logTrace::27"
    assert log_e['level'] == 'trace'
    assert log_e["a"] == 1
