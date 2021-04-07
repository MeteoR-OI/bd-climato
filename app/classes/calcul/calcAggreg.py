from app.classes.calcul.allCalculus import AllCalculus
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.refManager import RefManager
from django.db import transaction


class CalcAggreg(AllCalculus):
    """
        CalcAggreg

        Handle all the update of our aggregation, after a change in observation table
    """

    def ComputeAggreg(self):
        """
            ComputeAggreg

            called  by the daemon service

            send the delta values to all aggregations related to our measure
        """
        while True:
            a_todo = AggTodoMeteor.popOne()
            if a_todo is None:
                # no more data to update, return to sleep
                return
            try:
                self.__processTodo(a_todo)
            except Exception as exc:
                # our transaction should ebe rolledback here
                a_todo.ReportError(exc)

    @transaction.atomic
    def __processTodo(self, a_todo):
        """
            __processTodo

            Process an agg_todo
        """
        all_instr = AllTypeInstruments()

        # retrieve data we will need
        m_stop_dat = a_todo.data.obs_id.stop_dat
        a_start_dat = a_todo.data.obs_id.agg_start_dat
        poste_metier = PosteMetier(a_todo.data.obs_id.poste_id_id, a_start_dat)
        aggregations = poste_metier.aggregations(m_stop_dat, True)
        delta_values = a_todo.data.j_dv
        j_dv_agg = a_todo.data.obs_id.j_agg
        if RefManager.GetInstance().GetRef("trace_flag") is None:
            trace_flag = False
        else:
            trace_flag = RefManager.GetInstance().GetRef("trace_flag")

        # mark all aggregation as clean. only dirty aggregation will be saved
        for an_agg in aggregations:
            an_agg.dirty = False

        # for all type_instruments
        for an_intrument in all_instr.get_all_instruments():
            # for all measures
            for my_measure in an_intrument['object'].get_all_measures():
                # find the calculus object for my_mesure
                for a_calculus in self.all_calculus:
                    if a_calculus['agg'] == my_measure['agg']:
                        if a_calculus['calc_obs'] is not None:
                            # load our json in obs row
                            a_calculus['calc_agg'].loadAggregations(m_stop_dat, my_measure, j_dv_agg, aggregations, delta_values, trace_flag)
                        break
        for an_agg in aggregations:
            if an_agg.dirty is True:
                an_agg.save()
        a_todo.delete()
