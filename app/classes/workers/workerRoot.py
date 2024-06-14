# Worker class
# ------------
# The worker class should implement the following 4 methods:
#   work_item = class.getNextWorkItem()
#       return None -> no more work for now
#       return a work_item data, which should include enought info for other calls
#   processItem(work_item)
#       Process the work item
#   succeedWorkItem(work_item)
#       Mark the work_item as processed
#   failWorkItem(work_item, exc)
#       mark the work_item as failed (exc is the exception)
# ----------
import threading
import time
import json
from app.tools.refManager import RefManager
from app.classes.repository.incidentMeteor import IncidentMeteor
import app.tools.myTools as t
from datetime import datetime


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
            self.display = '{0}'.format(name).replace("<class 'app.classes.workers.", "")
            self.display = self.display.split('.')[0]
            t.logInfo('worker ' + self.display + ' new instance', {"svc": self.display})
        except Exception:
            self.display = name

        self.ref_mgr.AddRef("Inst_" + self.display, svc_instance)
        # check globally that only one instance was created for the name
        if self.ref_mgr.IncrementRef("Svc_" + name) > 1:
            IncidentMeteor().new('worker ' + name, 'CRITICAL', 'Multiple instance')
            raise Exception(name, 'Multiple instances of ' + name + ' called')

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
        if ref_mgr.GetRef('{0}'.format(myClass)) is None:
            ref_mgr.AddRef('{0}'.format(myClass), myClass())
        return ref_mgr.GetRef('{0}'.format(myClass))

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
                        t.logInfo('svc thread started', {"svc": self.display, "status": "started"})
                        thread.start()
                        a_worker['threadRunning'] = True
                        # force the thread to run once
                        time.sleep(1)
                        return

                    except Exception as exc:
                        a_worker['threadRunning'] = False
                        # t.logError('Start', self.display + ": Exception", {"svc": self.display, "exception": '{0}'.format(exc)})
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
                    t.logInfo('Stop command received', {"svc": self.display, "status": "stopped"})

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
                    info = a_worker['class'].addNewWorkItem(work_item)
                    t.logInfo(self.display + " new item in queue - " + info, {"svc": self.display, "info": info})

                except Exception as exc:
                    t.logException(exc, None)

                finally:
                    pass

    # Check thread list to check if service is running
    def IsRunning(self) -> bool:
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wrks:
                if a_worker['name'] == self.name:
                    return a_worker['threadRunning']
            t.logError('workerRoot::IsRunning', 'Service ' + self.display + " not found", {"svc": self.display})

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
                t.logInfo('task ' + self.display + " running", {})

            while True:
                in_use = False
                try:
                    trace_flag = self.GetTraceFlag()
                    if trace_flag is True:
                        t.logInfo('task ' + self.display + " waiting now", {"frequency": self.frequency})

                    # wait our frequency
                    self.eventRunMe.wait(self.frequency)

                    #  Stop request processing
                    if self.killFlag is True:
                        if trace_flag is True:
                            t.logInfo('task ' + self.display + " killed", {})
                        self.closed.set()
                        return

                    if in_use is True:
                        if trace_flag is True:
                            t.logInfo('task ' + self.display + " in use, continue", {})
                        continue

                    # work_item should have the key: spanID, and info, plus info for the service itself
                    work_item = a_worker['class'].getNextWorkItem()
                    if work_item is None:
                        if self.run_once is True:
                            if trace_flag is True:
                                t.logInfo('task ' + self.display + " queue empty, stop", {})
                            self.Stop()
                            return
                        self.eventRunMe.clear()
                        continue

                    # safe check...
                    if work_item.get("info") is None:
                        work_item['info'] = self.display
                    if work_item.get("meteor") is None:
                        work_item['meteor'] = "?"

                    # call the service handler
                    try:
                        start_ts = datetime.now()
                        in_use = True
                        a_worker['class'].processWorkItem(work_item)
                        a_worker['class'].succeedWorkItem(work_item)
                        t.logInfo("item processed ok", {
                            "svc": self.display,
                            "info": work_item['info'],
                            "duration": datetime.now() - start_ts,
                        })

                    except Exception as exc:
                        t.logException(exc, {"svc": self.display, "info": work_item.get('info')})
                        a_worker['class'].failWorkItem(work_item, exc)

                    finally:
                        in_use = False

                    self.eventRunMe.set()

                except Exception as exc:
                    in_use = False
                    t.logException(exc)
                    print('#$##$#$#$##$# in workerRoot')
                    print('Exception in ' + self.display + '=>' + '{0}'.format(exc))
                    print('#$##$#$#$##$#')

        finally:
            WorkerRoot.wrks_lock.acquire()
            a_worker['threadRunning'] = False
            WorkerRoot.wrks_lock.release()
