import threading
import time
import queue
import json
from app.tools.refManager import RefManager
from app.tools.telemetry import Telemetry
import app.tools.myTools as t


class WorkerRoot:
    """
        Background workers
    """
    wkrs = []
    wrks_lock = threading.Lock()
    instances = {}
    all_syn = []
    trace_flag = []

    def __init__(self, name, fct, frequency: int = 120, synonym: dict = ['']):
        self.name = name
        try:
            self.display = str(name).replace("<class 'app.classes.workers.", "")
            self.display = self.display.split('.')[0]
        except Exception:
            self.display = name
        self.tracer = Telemetry.Start('task ' + self.display, 'task ' + self.display)
        self.synonym = synonym
        WorkerRoot.all_syn.append({"s": synonym, "svc": name, "name": self.display, "instance": self})
        WorkerRoot.trace_flag.append({"s": name, "trace_flag": False})
        self.frequency = frequency
        self.ref_mgr = RefManager.GetInstance()

        # check globally that only one instance was created for the name
        if self.ref_mgr.IncrementRef(name + '_count') > 0:
            raise Exception(name, 'Multiple instances called')

        # save a default kill frequency on a global space
        self.ref_mgr.SetRefIfNotExist("worker_kill_frequency", 15)

        # event to notify when a thread is exited
        self.eventKill = threading.Event()
        self.queueRun = queue.Queue()

        # register and start our service
        self.__register(name, fct)

    @staticmethod
    def GetInstance(myClass):
        # return the instance
        ref_mgr = RefManager.GetInstance()
        if ref_mgr.GetRef('Svc' + str(myClass)) is None:
            ref_mgr.AddRef('Svc' + str(myClass), myClass())
        return ref_mgr.GetRef('Svc' + str(myClass))

    @staticmethod
    def GetSynonym():
        # return the instance
        return WorkerRoot.all_syn

    def GetTraceFlag(self) -> bool:
        all_trc = WorkerRoot.trace_flag
        for a_trc in all_trc:
            if a_trc['s'] == self.name:
                return a_trc['trace_flag']
        return None

    def SetTraceFlag(self, trace_flag: bool):
        all_trc = WorkerRoot.trace_flag
        for a_trc in all_trc:
            if a_trc['s'] == self.name:
                a_trc['trace_flag'] = trace_flag
                t.logInfo(
                    'task ' + self.name + ' setTraceFlag',
                    None,
                    {'trace_flag': trace_flag}
                )
                return
        raise Exception('workerRoot::SetTraceFlag', 'service ' + self.display + ' not found')

    def RunIt(self, params: json = {}):
        self.queueRun.put(params)

    def Start(self):
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wkrs:
                if a_worker['name'] == self.name:
                    if a_worker['run'] is True:
                        raise Exception('workers::Start', self.display + ' already running')
                    thread = threading.Thread(target=self.__runSvc, args=(a_worker,), daemon=True)
                    thread.setName(self.name)
                    if self.GetTraceFlag() is True:
                        t.logInfo('task ' + self.display + ' kthread started', None, {"status": "started"})
                    thread.start()
                    a_worker['run'] = True
                    # force the thread to start
                    time.sleep(1)
        finally:
            WorkerRoot.wrks_lock.release()

    def Stop(self):
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wkrs:
                if a_worker['name'] == self.name:
                    if a_worker['run'] is False:
                        raise Exception('workers::Stop', self.display + ' already stopped')
                    self.eventKill.set()
                    t.logInfo('task ' + self.display + ' kill event sent. Task should be stopped', None, {"status": "stopped"})
                    a_worker['run'] = False
                    # time.sleep(self.ref_mgr.GetRef("worker_kill_frequency"))
        finally:
            WorkerRoot.wrks_lock.release()

    def IsRunning(self) -> bool:
        try:
            thread_found = False
            for a_thread in threading.enumerate():
                if a_thread.getName() == self.name:
                    thread_found = True
            # update our internal array
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wkrs:
                if a_worker['name'] == self.name:
                    if a_worker['run'] != thread_found:
                        t.logError(
                            'task ' + self.display + ": wrong status",
                            None,
                            {"status.worker": str(a_worker['run']), "status.thread": str(thread_found)},
                        )
                        a_worker['run'] = thread_found
            return thread_found
        finally:
            WorkerRoot.wrks_lock.release()

    def WaitToFinish(self):
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_thread in threading.enumerate():
                if a_thread.getName() == self.name:
                    for a_worker in WorkerRoot.wkrs:
                        if a_worker['name'] == self.name:
                            a_thread.join()
        finally:
            WorkerRoot.wrks_lock.release()

    # private methods
    def __register(self, name: str, fct):
        for a_worker in WorkerRoot.wkrs:
            if a_worker['name'] == name:
                t.logError('task ' + self.display + name + ' already registered')
        WorkerRoot.wrks_lock.acquire()
        WorkerRoot.wkrs.append({"name": name, "fct": fct, 'run': False, 'killMe': threading.Event()})
        WorkerRoot.wrks_lock.release()

    def __runSvc(self, a_worker):
        trace_flag = self.GetTraceFlag()
        try:
            used_fequency = self.frequency
            check_exit = self.ref_mgr.GetRef("worker_kill_frequency")
            if trace_flag is True:
                t.logTrace('task ' + self.display + " running", None, {"check_time_out": check_exit})

            while True:
                try:
                    trace_flag = self.GetTraceFlag()
                    if trace_flag is True:
                        t.logTrace('task ' + self.display + " waiting now", None, {"freq": self.frequency, "freq.used": used_fequency})
                    trace_flag = self.GetTraceFlag()
                    call_params = {
                        "t": self.tracer,
                        "p": [],
                        "tf": trace_flag}
                    try:
                        call_params["p"] = self.queueRun.get(True, check_exit)
                        if trace_flag is True:
                            t.logTrace('task ' + self.display + " Queue released", None)
                        used_fequency -= check_exit
                        used_fequency = self.frequency
                        a_worker['fct'](call_params)
                    except queue.Empty:
                        if self.eventKill.isSet() is True:
                            t.logInfo('task ' + self.display + ' kill event received, exiting')
                            return
                        used_fequency -= check_exit
                        continue
                except Exception as exc:
                    t.LogException(exc)
        finally:
            WorkerRoot.wrks_lock.acquire()
            a_worker['run'] = False
            WorkerRoot.wrks_lock.release()
