import pytest
from app.classes.workers.workerRoot import WorkerRoot
# import time


@pytest.mark.unit
def test_1_monitor():
    try:
        w = WorkerRoot.GetInstance(1)
        # print('workers created')
        assert w.isRunning('monitor') is True
        # print('calling KillThread')
        w.killThread('monitor')
        # print('KillThread returned')
        assert w.isRunning('monitor') is False

    except Exception as inst:
        print(inst)
