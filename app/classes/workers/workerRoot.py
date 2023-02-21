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

    def __init__(self, svc_instance, name, cls, frequency: int = 120, synonym: dict = [''], run_once=False):
        self.name = name
        self.run_once = run_once
        self.ref_mgr = RefManager.GetInstance()
        try:
            self.display = str(name).replace("<class 'app.classes.workers.", "")
            self.display = self.display.split('.')[0]
            t.logInfo('worker ' + name + ' new instance')
        except Exception:
            self.display = name

        self.ref_mgr.AddRef("Inst_" + self.display, svc_instance)
        # check globally that only one instance was created for the name
        if self.ref_mgr.IncrementRef("Svc_" + name) > 1:
            IncidentMeteor().new('worker ' + name, 'CRITICAL', 'Multiple instance')
            t.logError('WorkerRoot::__init__', 'multiple instances of ' + name, None, {"svc": self.display})
            raise Exception(name, 'Multiple instances called')

        self.tracer = Telemetry.Start('svc ' + self.display, __name__)
        self.frequency = frequency
        self.synonym = synonym
        WorkerRoot.all_syn.append({"s": synonym, "svc": name, "name": self.display, "instance": self})

        WorkerRoot.trace_flag.append({"s": name, "trace_flag": False})

        # save a default kill frequency on a global space
        self.ref_mgr.SetRefIfNotExist(name, cls)
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
        if ref_mgr.GetRef(str(myClass)) is None:
            ref_mgr.AddRef(str(myClass), myClass())
        return ref_mgr.GetRef(str(myClass))

    @staticmethod
    def GetSynonym():
        # return the instance
        return WorkerRoot.all_syn

    def GetTraceFlag(self) -> bool:
        for a_trc in WorkerRoot.trace_flag:
            if a_trc['s'] == self.name:
                return a_trc['trace_flag']
        return None

    def GetDisplayName(self):
        return self.display

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
    def RunMe(self, params: json = None):
        if self.IsRunning() is False:
            self.Start()
        if params is not None:
            self.AddWorkItem(params)
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
                        self.closed.clear()
                        self.eventRunMe.clear()
                        thread = threading.Thread(target=self.__runSvc, args=(a_worker,), daemon=True)
                        thread.setName(self.name)
                        t.logInfo('svc thread started', None, {"svc": self.display, "status": "started"})
                        thread.start()
                        a_worker['threadRunning'] = True
                        # force the thread to run once
                        time.sleep(1)
                        return

                    except Exception as exc:
                        a_worker['threadRunning'] = False
                        t.logError('Start', self.display + ": Exception", None, {"svc": self.display, "exception": str(exc)}, {"svc": self.display})
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
        if self.IsRunning() is False:
            self.Start()
        for a_worker in WorkerRoot.wrks:
            if a_worker['name'] == self.name:
                try:
                    a_worker['class'].addNewWorkItem(work_item)

                except Exception as exc:
                    t.Exception(exc, None)

                finally:
                    pass

    # Check thread list to check if service is running
    def IsRunning(self) -> bool:
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wrks:
                if a_worker['name'] == self.name:
                    return a_worker['threadRunning']
            t.logError('workerRoot::IsRunning', 'Service ' + self.display + " not found", None, {"svc": self.display})

        finally:
            WorkerRoot.wrks_lock.release()

    def IsKilled(self):
        return self.killFlag

    # private methods
    # Register in WorkerRoot.wrks (global variable)
    def __register(self, name: str, cls):
        for a_worker in WorkerRoot.wrks:
            if a_worker['name'] == name:
                t.logError('workerRoot::__register', 'task ' + self.display + name + ' already registered', {"svc": self.display})
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
                in_use = False
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

                    if in_use is True:
                        continue

                    # work_item should have the key: spanID, and info, plus info for the service itself
                    work_item = a_worker['class'].getNextWorkItem()
                    if work_item is None:
                        if self.run_once is True:
                            self.Stop()
                            return
                        self.eventRunMe.clear()
                        continue

                    # safe check...
                    if work_item.get("spanID") is None:
                        work_item['spanID'] = self.display
                    if work_item.get("info") is None:
                        work_item['info'] = self.display
                    if work_item.get("meteor") is None:
                        work_item['meteor'] = "?"

                    with self.tracer.start_as_current_span(work_item['spanID']) as my_span:
                        my_span.set_attribute("job", "django")  # for link jaeger -> loki
                        my_span.set_attribute("info", work_item['info'])
                        my_span.set_attribute("meteor", work_item['meteor'])
                        # call the service handler
                        try:
                            in_use = True
                            a_worker['class'].processWorkItem(work_item, my_span)
                            my_span._status._status_code = Telemetry.get_ok_status()
                            a_worker['class'].succeedWorkItem(work_item, my_span)
                            t.logInfo("work item processed ok", my_span, {
                                "svc": self.display,
                                "info": work_item['info'],
                                "meteor": work_item['meteor'],
                            })

                        except Exception as exc:
                            my_span._status._status_code = Telemetry.get_error_status()
                            t.logException(exc, my_span, {"svc": self.display, "work_item": work_item})
                            a_worker['class'].failWorkItem(work_item, exc, my_span)

                        finally:
                            in_use = False

                    self.eventRunMe.set()

                except Exception as exc:
                    in_use = False
                    t.logException(exc)
                    print('#$##$#$#$##$#')
                    print('Exception in ' + self.display + '=>' + str(exc))
                    print('#$##$#$#$##$#')

        finally:
            WorkerRoot.wrks_lock.acquire()
            a_worker['threadRunning'] = False
            WorkerRoot.wrks_lock.release()
