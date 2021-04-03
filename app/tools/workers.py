import threading
import time
from app.tools.refManager import RefManager


class Workers:
    """
        Background workers
    """
    wkrs = []
    wrks_lock = threading.Lock()

    def __init__(self, kill_freq: int = 30):
        # save our kill frequency on a global space
        self.ref_mgr = RefManager.GetInstance()
        self.ref_mgr.AddRef("worker_kill_frequency", kill_freq)

        # event to notify when a thread is stopped
        self.thread_event = threading.Event()

        # start our monitoring system
        self.register("monitor", self.monitor)
        self.start("monitor")

    def monitor(self, kill_me: threading.Event):
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
            # self.thread_event.set()
            pass

    def register(self, name: str, fct):
        for a_worker in Workers.wkrs:
            if a_worker['name'] == name:
                raise Exception('Workers:register', 'name already registered')
        thread_kill_event = threading.Event()
        Workers.wrks_lock.acquire()
        Workers.wkrs.append({"name": name, "fct": fct, 'run': False, 'killMe': thread_kill_event})
        Workers.wrks_lock.release()

    def LaunchThread(self, name: str):
        lock_relased = False
        try:
            Workers.wrks_lock.acquire()
            for a_worker in Workers.wkrs:
                if a_worker['name'] == name:
                    a_worker['run'] = True
                    Workers.wrks_lock.release()
                    lock_relased = True
                    a_worker['fct'](a_worker['killMe'])
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

    def start(self, name: str):
        try:
            for a_worker in Workers.wkrs:
                if a_worker['name'] == name:
                    if a_worker['run'] is True:
                        raise Exception('workers::start', 'already running')
                    thread = threading.Thread(target=self.LaunchThread, args=(a_worker['name'],), daemon=True)
                    thread.setName(name)
                    # print("thread " + name + " started")
                    thread.start()
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
