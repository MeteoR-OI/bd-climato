import threading
import time
from app.tools.refManager import RefManager


class WorkerRoot:
    """
        Background workers
    """
    wkrs = []
    wrks_lock = threading.Lock()
    instances = {}

    def __init__(self, name, fct):
        self.name = name
        self.ref_mgr = RefManager.GetInstance()

        # check globally that only one instance was created for the name
        if self.ref_mgr.IncrementRef(name + '_count') > 0:
            raise Exception(name, 'Multiple instances called')

        # save a default kill frequency on a global space
        self.ref_mgr.SetRefIfNotExist("worker_kill_frequency", 30)

        # event to notify when a thread is exited
        self.eventKill = threading.Event()
        self.eventRun = threading.Event()

        # register and start our service
        self.__register(name, fct)
        self.Start()

    @staticmethod
    def GetInstance(myClass):
        # return the instance
        ref_mgr = RefManager.GetInstance()
        if ref_mgr.GetRef('Svc' + str(myClass)) is None:
            ref_mgr.AddRef('Svc' + str(myClass), myClass())
        return ref_mgr.GetRef('Svc' + str(myClass))

    def RunIt(self):
        self.eventRun.set()

    def Start(self):
        try:
            WorkerRoot.wrks_lock.acquire()
            for a_worker in WorkerRoot.wkrs:
                if a_worker['name'] == self.name:
                    if a_worker['run'] is True:
                        raise Exception('workers::Start', self.name + ' already running')
                    thread = threading.Thread(target=self.__runSvc, args=(a_worker,), daemon=True)
                    thread.setName(self.name)
                    # print("thread " + name + " started")
                    thread.start()
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
                        raise Exception('workers::Stop', self.name + ' already stopped')
                    self.eventKill.set()
                    a_worker['run'] = False
                    time.sleep(self.ref_mgr.GetRef("worker_kill_frequency"))
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
                        print(self.name + " has a wring status: " + str(a_worker['run']) + ' instead of ' + str(thread_found))
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
                raise Exception('Workers:register', name + ' already registered')
        WorkerRoot.wrks_lock.acquire()
        WorkerRoot.wkrs.append({"name": name, "fct": fct, 'run': False, 'killMe': threading.Event()})
        WorkerRoot.wrks_lock.release()

    def __runSvc(self, a_worker):
        # print("......monitor thread started")
        try:
            while True:
                try:
                    evt = self.eventRun.wait(self.ref_mgr.GetRef("worker_kill_frequency"))
                    if evt is False:
                        # check the kill flag for ourself
                        if self.eventKill.isSet() is True:
                            return
                        continue
                    # we have something to process
                    a_worker['fct']()
                except Exception as exc:
                    print(exc)
        finally:
            WorkerRoot.wrks_lock.acquire()
            a_worker['run'] = False
            WorkerRoot.wrks_lock.release()
