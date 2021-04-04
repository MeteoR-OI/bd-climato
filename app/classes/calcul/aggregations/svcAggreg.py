from app.tools.workers import Workers
from app.tools.refManager import RefManager
from app.classes.calcul.calculus import ComputeAggreg
import threading


class SvcAggreg():
    """
        SvcAggreg

        Service for Aggregation Computations

        calculus v2
    """

    def __init__(self, name: str):
        if Workers.nb_instances != 0:
            raise Exception(name, 'Call Workers.GetInstance()')
        Workers.nb_instances += 1
        self.name = name
        self.ref_mgr = RefManager.GetInstance()
        self.ref_mgr.AddRef("Event" + self.name, threading.Event())
 
    @staticmethod
    def GetInstance(kill_freq: int = 30):
        # return the instance
        name = 'SvcAggreg'
        ref_mgr = RefManager.GetInstance()
        if ref_mgr.GetRef('Svc' + name) is None:
            ref_mgr.AddRef('Svc' + name, SvcAggreg(name))
        return ref_mgr.GetRef('Svc' + name)

    def startMe(self, kill_me: threading.Event, stop_event: threading.Event):
        try:
            # print("......monitor thread started")
            my_event = self.ref_mgr.GetRef('Event' + self.name)
            while True:
                evt = my_event.wait(self.ref_mgr.GetRef("worker_kill_frequency"))
                if evt is False:
                    # check the kill flag for ourself
                    if kill_me.isSet() is True:
                        return
                    continue
                # we have something to process
                ComputeAggreg()
        except Exception as exc:
            print(exc)
        finally:
            stop_event.set()
