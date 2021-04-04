from app.classes.calcul.aggregations.svcAggreg import SvcAggreg
from app.classes.calcul.calculus import Calculus
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.aggTools import calcAggDate
from app.tools.jsonPlus import JsonPlus
from app.tools.jsonValidator import checkJson
from app.tools.refManager import RefManager
from app.tools.workers import Workers
from django.db import transaction
import threading


class CalcAggreg(Calculus):

    def __init__(self):
        super(CalcAggreg, self).__init__()
        self.name = 'SvcAggreg'
        if Workers.nb_instances != 0:
            raise Exception(self.name, 'Call Workers.GetInstance()')
        Workers.nb_instances += 1

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

    def startAgg_ttx(self):
        """ set the event object, that will start the SvcAggreg process """

        # be sure that SvcAggreg is running
        SvcAggreg.GetInstance()
        # set our event
        RefManager().GetRef('EventSvcAggreg').set()

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
                self.ComputeAggreg()
        except Exception as exc:
            print(exc)
        finally:
            stop_event.set()

    @transaction.atomic
    def ComputeAggreg(self):
        """
            ComputeAggreg

            send the delta values to all our measures
        """
        a_todo = AggTodoMeteor.popOne()
        if a_todo is None:
            return

        all_instr = AllTypeInstruments()
        # retrieve data we will need
        m_stop_dat = a_todo.data.obs_id.stop_dat
        a_start_dat = a_todo.data.obs_id.agg_start_dat
        poste_metier = PosteMetier(a_todo.data.obs_id.poste_id_id, a_start_dat)
        aggregations = poste_metier.aggregations(m_stop_dat, True)
        delta_values = a_todo.data.j_dv

        # for all type_instruments
        for an_intrument in all_instr.get_all_instruments():
            # for all measures
            for my_measure in an_intrument['object'].get_all_measures():
                # find the calculus object for my_mesure
                for a_calculus in self.all_calculus:
                    if a_calculus['agg'] == my_measure['agg']:
                        if a_calculus['calc_obs'] is not None:
                            # load our json in obs row
                            a_calculus['calc_agg'].
                            loadInObs(poste_metier, my_measure, m_j, measure_idx, obs_meteor, delta_values, trace_flag)
                        break
