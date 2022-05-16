# Worker class
# ------------
# The worker class should implement the following 4 methods:
#   work_item = class.getNextWorkItem()
#       return None -> no more work for now
#       return a work_item data, which should include enought info for other calls
#   processItem(work_item, my_span)
#       Process the work item
#   succeedWorkItem(work_item, my_span)
#       Mark the work_item as processed
#   failWorkItem(work_item, exc, my_span)
#       mark the work_item as failed (exc is the exception)
# ----------
import threading
import time
import json
from app.tools.refManager import RefManager
from app.tools.telemetry import Telemetry
from app.classes.repository.incidentMeteor import IncidentMeteor
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

    def __init__(self, name, cls, frequency: int = 120, synonym: dict = [''], run_once=False):
        self.name = name
        self.run_once = run_once
        self.ref_mgr = RefManager.GetInstance()
        try:
            self.display = str(name).replace("<class 'app.classes.workers.", "")
            self.display = self.display.split('.')[0]
            t.logInfo('worker ' + name + ' new instance')
        except Exception:
            self.display = name

        # check globally that only one instance was created for the name
        if self.ref_mgr.IncrementRef(name + '_count') > 0:
            IncidentMeteor().new('worker ' + name, 'CRITICAL', 'Multiple instance')
            t.logError('multiple instances of ' + name)
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
        self.closed = threading.Event()
        self.closed.clear()
        self.killFlag = False

        # register and start our service
        self.__register(name, cls)

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
        self.eventRunMe.set()

    # Start the service (in waitable mode)
    def Start(self):
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wrks:
                if a_worker['name'] == self.name:
                    try:
                        if a_worker['threadRunning'] is True:
                            # just return if the task already running
                            return
                        self.killFlag = False
                        self.closed = False
                        thread = threading.Thread(target=self.__runSvc, args=(a_worker,), daemon=True)
                        thread.setName(self.name)
                        if self.GetTraceFlag() is True:
                            t.logInfo('svc thread started', None, {"svc": self.display, "status": "started"})
                        thread.start()
                        a_worker['threadRunning'] = True
                        # force the thread to run once
                        time.sleep(1)
                        self.eventRunMe.set()
                        return

                    except Exception as exc:
                        a_worker['threadRunning'] = False
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
                    if a_worker['threadRunning'] is False:
                        raise Exception('workers::Stop', self.display + ' already stopped')

                    # Stop this worker first
                    self.killFlag = True
                    self.eventRunMe.set()
                    t.logInfo('Stop command received', None, {"svc": self.display, "status": "stopped"})

                    if self.run_once is False:
                        self.closed.wait(5)

                except Exception as exc:
                    t.Exception(exc, None)

                finally:
                    with WorkerRoot.wrks_lock:
                        a_worker['threadRunning'] = False

    #  add manually aork item
    def AddWorkItem(self, work_item: json):
        pass

    # Check thread list to check if service is running
    def IsRunning(self) -> bool:
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wrks:
                if a_worker['name'] == self.name:
                    return a_worker['threadRunning']
            t.logError('Service ' + self.display + " not found", None, {})

        finally:
            WorkerRoot.wrks_lock.release()

    def IsKilled(self):
        return self.killFlag

    # private methods
    # Register in WorkerRoot.wrks (global variable)
    def __register(self, name: str, cls):
        for a_worker in WorkerRoot.wrks:
            if a_worker['name'] == name:
                t.logError('task ' + self.display + name + ' already registered')
        WorkerRoot.wrks_lock.acquire()
        WorkerRoot.wrks.append({"name": name, "class": cls, 'threadRunning': False})
        WorkerRoot.wrks_lock.release()

    # Start the service, and call the service function every frequency
    def __runSvc(self, a_worker):
        trace_flag = self.GetTraceFlag()
        try:
            if trace_flag is True:
                t.logInfo('task ' + self.display + " running", None, {})

            while True:
                try:
                    trace_flag = self.GetTraceFlag()
                    if trace_flag is True:
                        t.logInfo('task ' + self.display + " waiting now", None, {"frequency": self.frequency})

                    # wait our frequency
                    self.eventRunMe.wait(self.frequency)

                    #  Stop request processing
                    if self.killFlag is True:
                        self.closed.set()
                        return

                    work_item = a_worker['class'].getNextWorkItem()
                    if work_item is None:
                        if self.run_once is True:
                            self.Stop()
                            return
                        self.eventRunMe.clear()
                        continue

                    with self.tracer.start_as_current_span("load Json") as my_span:
                        # call the service handler
                        try:
                            # my_span = self.tracer.start_as_current_span("load Json")
                            a_worker['class'].processWorkItem(work_item, my_span, self.tracer)
                            a_worker['class'].succeedWorkItem(work_item, my_span)
                            my_span._status._status_code = Telemetry.get_ok_status()

                        except Exception as exc:
                            my_span._status._status_code = Telemetry.get_error_status()
                            a_worker['class'].failWorkItem(work_item, exc, my_span)

                    self.eventRunMe.set()

                except Exception as exc:
                    t.logException(exc)

        finally:
            WorkerRoot.wrks_lock.acquire()
            a_worker['threadRunning'] = False
            WorkerRoot.wrks_lock.release()
