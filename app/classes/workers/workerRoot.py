# Worker class
# ------------
#   wait on eventRunMe(frequency)
#       if killFlag -> exit
#       loop until queueRun.empty is True:
#           param = queueRun.get()
#           call svc func(param)
#       eventRunMe.clear()
#       loop
# ----------
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
    wrks = []
    wrks_lock = threading.Lock()
    instances = {}
    all_syn = []
    trace_flag = []

    def __init__(self, name, fct, frequency: int = 120, synonym: dict = ['']):
        self.name = name
        self.ref_mgr = RefManager.GetInstance()
        try:
            self.display = str(name).replace("<class 'app.classes.workers.", "")
            self.display = self.display.split('.')[0]
        except Exception:
            self.display = name

        # check globally that only one instance was created for the name
        if self.ref_mgr.IncrementRef(name + '_count') > 0:
            raise Exception(name, 'Multiple instances called')

        self.tracer = Telemetry.Start('svc ' + self.display, __name__)
        self.frequency = frequency
        self.synonym = synonym
        WorkerRoot.all_syn.append({"s": synonym, "svc": name, "name": self.display, "instance": self})

        WorkerRoot.trace_flag.append({"s": name, "trace_flag": False})

        # save a default kill frequency on a global space
        self.ref_mgr.SetRefIfNotExist("worker_kill_frequency", 15)

        # event to notify when a thread is exited
        self.eventRunMe = threading.Event()
        self.eventRunMe.clear()
        self.queueRun = queue.Queue()
        self.killFlag = False

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
        for a_trc in WorkerRoot.trace_flag:
            if a_trc['s'] == self.name:
                return a_trc['trace_flag']
        return None

    def SetTraceFlag(self, trace_flag: bool):
        for a_trc in WorkerRoot.trace_flag:
            if a_trc['s'] == self.name:
                a_trc['trace_flag'] = trace_flag
                if trace_flag:
                    t.logInfo(
                        'task ' + self.display + ' setTraceFlag',
                        None,
                        {'traceFlag': trace_flag}
                    )
                return
        raise Exception('workerRoot::SetTraceFlag', 'service ' + self.display + ' not found')

    # Call the service function with a set of parameter
    def RunMe(self, params: json = {}):
        if self.IsRunning() is False:
            raise Exception('service ' + self.display + ' is stopped')
        self.queueRun.put(params)
        self.eventRunMe.set()

    # Start the service (in waitable mode)
    def Start(self):
        try:
            if self.IsRunning() is True:
                return
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wrks:
                if a_worker['name'] == self.name:
                    try:
                        if a_worker['run'] is True:
                            # just return if the task already running
                            return
                        self.killFlag = False
                        thread = threading.Thread(target=self.__runSvc, args=(a_worker,), daemon=True)
                        thread.setName(self.name)
                        if self.GetTraceFlag() is True:
                            t.logInfo('svc thread started', None, {"svc": self.display, "status": "started"})
                        thread.start()
                        a_worker['run'] = True
                        # force the thread to run once
                        time.sleep(1)
                        self.queueRun.put({})
                        self.eventRunMe.set()
                        return

                    except Exception as exc:
                        a_worker['run'] = False
                        t.logError('Start ' + self.display + ": Exception", None, {"exception": str(exc)})
                        raise exc

        finally:
            WorkerRoot.wrks_lock.release()

    # Stop the service (send a kill request)
    def Stop(self):
        if self.IsRunning() is False:
            return
        for a_worker in WorkerRoot.wrks:
            if a_worker['name'] == self.name:
                try:
                    if a_worker['run'] is False:
                        raise Exception('workers::Stop', self.display + ' already stopped')

                    # Stop this worker first
                    self.killFlag = True
                    self.eventRunMe.set()
                    t.logInfo('Stop command received', None, {"svc": self.display, "status": "stopped"})

                    # Notify service handler
                    try:
                        a_worker['fct']({"param": {"StopMe": True}})
                    except Exception as exc:
                        with self.tracer.start_as_current_span(self.display, True) as my_span:
                            my_span.record_exception(exc)
                    #  Bye
                    return

                except Exception as exc:
                    t.logError('Stop ' + self.display + ": Exception", None, {"exception": str(exc)})
                    raise exc

                finally:
                    with WorkerRoot.wrks_lock:
                        a_worker['run'] = False

    # Check thread list to check if service is running
    def IsRunning(self) -> bool:
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wrks:
                if a_worker['name'] == self.name:
                    return a_worker['run']
            t.LogError('Service ' + self.display + " not found", None, {})

        finally:
            WorkerRoot.wrks_lock.release()

    # private methods
    # Register in WorkerRoot.wrks (global variable)
    def __register(self, name: str, fct):
        for a_worker in WorkerRoot.wrks:
            if a_worker['name'] == name:
                t.logError('task ' + self.display + name + ' already registered')
        WorkerRoot.wrks_lock.acquire()
        WorkerRoot.wrks.append({"name": name, "fct": fct, 'run': False, 'killMe': threading.Event()})
        WorkerRoot.wrks_lock.release()

    # Start the service, and call the service function every frequency
    def __runSvc(self, a_worker):
        trace_flag = self.GetTraceFlag()
        try:
            if trace_flag is True:
                t.LogDebug('task ' + self.display + " running", None, {})

            while True:
                try:
                    trace_flag = self.GetTraceFlag()
                    if trace_flag is True:
                        t.LogDebug('task ' + self.display + " waiting now", None, {"frequency": self.frequency})

                    # wait our frequency
                    self.eventRunMe.wait(self.frequency)

                    #  Stop request processing
                    if self.killFlag is True:
                        return

                    # Loop on queue messages
                    call_params = {"param": {}}
                    while self.queueRun.empty() is False:

                        # get our param
                        call_params["param"] = self.queueRun.get(False)
                        if call_params['param'].get('trace_flag') is not None:
                            trace_flag = call_params['param']['trace_flag']
                            self.SetTraceFlag(trace_flag)
                            t.LogDebug('task ' + self.display + " Run " + self.display, None)

                        # old bug...
                        if call_params['param'] is None or call_params == []:
                            call_params['param'] = {}
                        call_params["param"]["trace_flag"] = trace_flag

                        # call the service handler
                        try:
                            a_worker['fct'](call_params)
                        except Exception as exc:
                            with self.tracer.start_as_current_span(self.display, trace_flag) as my_span:
                                my_span.record_exception(exc)

                    self.eventRunMe.clear()

                except Exception as exc:
                    with self.tracer.start_as_current_span(self.display, trace_flag) as my_span:
                        my_span.record_exception(exc)

        finally:
            WorkerRoot.wrks_lock.acquire()
            a_worker['run'] = False
            WorkerRoot.wrks_lock.release()
