import threading
import time
from app.tools.refManager import RefManager


class Workers:
    """
        Background workers
    """
    wkrs = []
    wrks_lock = threading.Lock()
    instances = {}

    def __init__(self, name, fct):
        self.name = name
        # check globally that only one instance was created for the name
        if Workers.instances.__contains__(name) is False:
            Workers.instances[name] = 0
        if Workers.instances[name] > 0:
            raise Exception(name, 'Multiple instances called')
        Workers.instances[name] += 1

        # save a default kill frequency on a global space
        self.ref_mgr = RefManager.GetInstance()
        if self.ref_mgr.GetRef("worker_kill_frequency") is None:
            self.ref_mgr.AddRef("worker_kill_frequency", 30)

        # event to notify when a thread is exited
        self.eventExit = threading.Event()
        self.eventRun = threading.Event()

        # start our monitoring system if not started
        if self.IsRegistered("monitor") is False:
            self.Register("monitor", self.__monitorTask)
            self.Start("monitor")

        # register and start our service
        self.Register(name, fct)
        self.Start(name)

    @staticmethod
    def GetInstance(name):
        # return the instance
        ref_mgr = RefManager.GetInstance()
        if ref_mgr.GetRef('Svc' + name) is None:
            ref_mgr.AddRef('Svc' + name, Workers.CreateInstance())
        return ref_mgr.GetRef('Svc' + name)

    def GetExitEvent(self):
        return self.eventExit

    def RunSvcOnce(self):
        ref_mgr = RefManager.GetInstance()
        ref_mgr.GetRef('Event' + self.name).set()

    def Register(self, name: str, fct):
        for a_worker in Workers.wkrs:
            if a_worker['name'] == name:
                raise Exception('Workers:register', 'name already registered')
        thread_kill_event = threading.Event()
        Workers.wrks_lock.acquire()
        Workers.wkrs.append({"name": name, "fct": fct, 'run': False, 'killMe': thread_kill_event})
        Workers.wrks_lock.release()

    def IsRegistered(self, name: str):
        # used mainly for our monitor task
        for a_worker in Workers.wkrs:
            if a_worker['name'] == name:
                return True
        return False

    def LaunchThread(self, name: str):
        lock_relased = False
        try:
            Workers.wrks_lock.acquire()
            for a_worker in Workers.wkrs:
                if a_worker['name'] == name:
                    a_worker['run'] = True
                    Workers.wrks_lock.release()
                    lock_relased = True
                    a_worker['fct'](a_worker['killMe'], self.thread_event)
        finally:
            if lock_relased is False:
                Workers.wrks_lock.release()
            self.thread_event.set()

    def killThread(self, name: str, bWait: bool = True):
        lock_relased = False
        try:
            Workers.wrks_lock.acquire()
            for a_worker in Workers.wkrs:
                if a_worker['name'] == name:
                    lock_relased = True
                    # print('++++ killThred ' + name + " releasing the event")
                    Workers.wrks_lock.release()
                    a_worker['killMe'].set()
                    # we need to wait the kill_frequency to be sure that we received the event
                    if bWait is True:
                        time.sleep(self.ref_mgr.GetRef("worker_kill_frequency") + 1)
                    # print("+++++ killThread exiting")
        finally:
            if lock_relased is False:
                Workers.wrks_lock.release()

    def Start(self, name: str):
        try:
            for a_worker in Workers.wkrs:
                if a_worker['name'] == name:
                    if a_worker['run'] is True:
                        raise Exception('workers::start', 'already running')
                    thread = threading.Thread(target=self.LaunchThread, args=(a_worker['name'],), daemon=True)
                    thread.setName(name)
                    # print("thread " + name + " started")
                    thread.Start()
                    # force the thread to start
                    time.sleep(1)
        finally:
            pass

    def isRunning(self, name: str) -> bool:
        try:
            Workers.wrks_lock.acquire()
            for a_worker in Workers.wkrs:
                # if a_worker['run'] is True:
                #     print("isRunning: True")
                # else:
                #     print("isRunning: False")
                return a_worker['run']
            return False
        finally:
            Workers.wrks_lock.release()

    def join(self, name: str):
        try:
            Workers.wrks_lock.acquire()
            for a_thread in threading.enumerate():
                for a_worker in Workers.wkrs:
                    if a_worker['name'] == a_thread.getName():
                        a_thread.join()
                        return
            raise Exception('workers::join', 'thread ' + name + ' not found')
        finally:
            Workers.wrks_lock.release()

    def __monitorTask(self, kill_me: threading.Event, stop_event: threading.Event):
        try:
            # print("......monitor thread started")
            while True:
                evt = self.thread_event.wait(self.ref_mgr.GetRef("worker_kill_frequency"))
                if evt is False:
                    # check the kill flag for ourself
                    if kill_me.isSet() is False:
                        # print('......monitor: not killed return to wait')
                        continue
                    # we need to update ourself, because we are the monitor
                    Workers.wrks_lock.acquire()
                    for a_worker in Workers.wkrs:
                        if a_worker['name'] == 'monitor':
                            a_worker['run'] = False
                            # print("......monitor: thread " + a_worker['name'] + ' was stopped')
                            break
                    Workers.wrks_lock.release()
                    return
                # print("......monitor: thread_event signaled")
                # thread_event was set
                Workers.wrks_lock.acquire()
                for a_thread in threading.enumerate():
                    for a_worker in Workers.wkrs:
                        if a_worker['name'] == a_thread.getName():
                            if a_thread.is_alive() is False:
                                # print("......monitor: thread " + a_worker['name'] + ' was stopped')
                                a_worker['run'] = False
                Workers.wrks_lock.release()
                self.thread_event.clear()

        finally:
            stop_event.set()



# class T2:
#     statix = 'TT'
#     nb_instance = {}
#     def __init__(self, name):
#         T2.statix='T2'
#         if T2.nb_instance.__contains__(name) is False:
#             T2.nb_instance[name] = 0
#         T2.nb_instance[name] += 1
#         print(name + ' instances: ' + str(T2.nb_instance[name]))
#     @staticmethod
#     def GetStatix():
#         return T2.statix
#     @staticmethod
#     def GetName():
#         return T2.name

# class T3(T2):
#     def __init__(self, name: str = 'T3'):
#         super(T3, self).__init__(name)
#         print(name + ' instances: ' + str(T2.nb_instance[name]))
#         T3.MyName="my name is T3"
#         T2.name = T3.MyName

# class T4(T2):
#     def __init__(self, name: str = 'T4'):
#         super(T4, self).__init__(name)
#         print(name + ' instances: ' + str(T2.nb_instance[name]))
#         T3.MyName="my name is T4"
#         T2.name = T3.MyName
