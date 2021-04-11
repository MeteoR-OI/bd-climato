from app.classes.calcul.allCalculus import AllCalculus
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.refManager import RefManager
from app.tools.climConstant import AggLevel
from app.tools.aggTools import calcAggDate
from django.db import transaction
import json


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
        if RefManager.GetInstance().GetRef("trace_flag") is None:
            trace_flag = False
        else:
            trace_flag = RefManager.GetInstance().GetRef("trace_flag")

        # retrieve data we will need
        m_stop_dat = a_todo.data.obs_id.stop_dat
        a_start_dat = a_todo.data.obs_id.agg_start_dat
        poste_metier = PosteMetier(a_todo.data.obs_id.poste_id_id, a_start_dat)

        try:
            poste_metier.lock()
            aggregations = poste_metier.aggregations(m_stop_dat, True)
            for delta_values in a_todo.data.j_dv:
                # mark all aggregation as clean. only dirty aggregation will be saved
                for an_agg in aggregations:
                    an_agg.dirty = False

                for anAgg in AggLevel:
                    # adjust start date, depending on the aggregation level

                    # dv_next is the delta_values for next level
                    dv_next = {"maxminFix": []}

                    # for all type_instruments
                    for an_intrument in all_instr.get_all_instruments():

                        # for all measures
                        for my_measure in an_intrument['object'].get_all_measures():

                            # get our deca_hour
                            deca_hour = 0
                            if my_measure.__contains__('hour_deca') is True:
                                deca_hour = my_measure['hour_deca']
                            a_start_dat_level = calcAggDate(anAgg, m_stop_dat, deca_hour, True)

                            # load the needed aggregation for this measure
                            agg_deca = None
                            for my_agg in aggregations:
                                if my_agg.agg_niveau == anAgg and my_agg.data.start_dat == a_start_dat_level:
                                    agg_deca = my_agg
                                    break
                            if agg_deca is None:
                                raise Exception('aggCompute::loadAggregations', 'aggregation not loaded ' + anAgg + ", " + str(a_start_dat_level))

                            m_agg_j = self.get_agg_magg(anAgg, a_todo.data.obs_id.j_agg)

                            # find the calculus object for my_mesure
                            for a_calculus in self.all_calculus:
                                if a_calculus['agg'] == my_measure['agg']:
                                    if a_calculus['calc_obs'] is not None:

                                        # load our json in obs row
                                        a_calculus['calc_agg'].loadAggregations(m_stop_dat, my_measure, delta_values, agg_deca, m_agg_j, dv_next, trace_flag)
                                    break

                    # loop to the next AggLevel
                    delta_values = dv_next

                # save our aggregations for this delta_values
                for an_agg in aggregations:
                    if an_agg.dirty is True:
                        an_agg.save()

            # we're done
            print("a_todo " + str (a_todo.data.id) + ' processed. on queue: ' + str(a_todo.count()))
            a_todo.delete()
        finally:
            poste_metier.unlock()

    def get_agg_magg(self, agg_level: str, j_agg: json):
        """
            get_agg_magg
        """
        # get aggregation values in measures
        m_agg_j = {}
        if j_agg != {}:
            for a_j_agg in j_agg:
                if a_j_agg.__contains__('level') and a_j_agg['level'] == agg_level:
                    m_agg_j = a_j_agg
                    break
        return m_agg_j
