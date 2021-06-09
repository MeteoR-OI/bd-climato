from app.classes.calcul.allCalculus import AllCalculus
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.refManager import RefManager
from app.tools.aggTools import calcAggDate, getAggLevels
from app.tools.telemetry import Telemetry
import app.tools.myTools as t
from django.db import transaction
import json
import datetime


class CalcAggreg(AllCalculus):
    """
    CalcAggreg

    Handle all the update of our aggregation, after a change in observation table
    """

    def __init__(self):
        self.tracer = Telemetry.Start("calculus", __name__)

    def ComputAggregFromSvc(self, data: json):
        """entry point from worker"""

        if data is None or data.get("param") is None or data["param"] == {}:
            t.LogError("wrong data")
        params = data["param"]
        trace_flag = False
        if params.get("trace_flag") is not None:
            trace_flag = params["trace_flag"]
        try:
            # load our parameters
            is_tmp = False
            ret = []
            if params.get("is_tmp") is not None:
                is_tmp = params["is_tmp"]
            ret = self._computeAggreg(is_tmp, trace_flag)
            return ret

        except Exception as inst:
            t.LogCritical(inst)

    def ComputeAggregCall(self, is_tmp: bool = False, trace_flag: bool = False):
        self._computeAggreg(is_tmp, trace_flag)

    def _computeAggreg(self, is_tmp_called: bool, trace_flag: bool):
        """
        _computeAggreg

        called  by the daemon service

        send the delta values to all aggregations related to our measure
        """
        while True:
            is_tmp = is_tmp_called
            a_todo = AggTodoMeteor.popOne(is_tmp)
            if a_todo is None:
                is_tmp = not is_tmp
                a_todo = AggTodoMeteor.popOne(is_tmp)
                if a_todo is None:
                    # no more data to update, return to sleep
                    return

            try:
                self.__processTodo(a_todo, is_tmp)
            except Exception as exc:
                a_todo.ReportError(exc)
                a_todo.save()

    @transaction.atomic
    def __processTodo(self, a_todo, is_tmp: bool = False):
        """
        __processTodo

        Process an agg_todo
        """
        time_start = datetime.datetime.now()
        all_instr = AllTypeInstruments()
        if RefManager.GetInstance().GetRef("svcAggreg_trace_flag") is None:
            trace_flag = False
        else:
            trace_flag = RefManager.GetInstance().GetRef("svcAggreg_trace_flag")

        span_name = "Calc agg"
        if is_tmp is True:
            span_name += "_tmp"
        with self.tracer.start_as_current_span(span_name, trace_flag) as my_span:
            my_span.set_attribute("obsId", a_todo.data.obs_id_id)
            my_span.set_attribute("stopDat", str(a_todo.data.obs_id.stop_dat))
            my_span.set_attribute("meteor", a_todo.data.obs_id.poste_id.meteor)
            my_span.set_attribute("isTmp", is_tmp)
            # retrieve data we will need
            span_load_data = self.tracer.start_span("load Aggreg", trace_flag)
            m_stop_dat = a_todo.data.obs_id.stop_dat
            a_start_dat = a_todo.data.obs_id.agg_start_dat
            poste_metier = PosteMetier(a_todo.data.obs_id.poste_id_id, a_start_dat)
            poste_metier.lock()
            aggregations = poste_metier.aggregations(m_stop_dat, True, is_tmp)
            span_load_data.set_attribute("items", aggregations.__len__())
            span_load_data.end()
            try:
                idx_delta_value = -1
                for an_agg in aggregations:
                    # mark all aggregation as clean. only dirty aggregation will be saved
                    an_agg.dirty = False

                for delta_values in a_todo.data.j_dv:
                    idx_delta_value += 1

                    for an_agg in aggregations:
                        # add duration in all new aggregations
                        an_agg.add_duration(delta_values["duration"])

                    for anAgg in getAggLevels(is_tmp):
                        with self.tracer.start_span("level " + anAgg, trace_flag) as span_lvl:
                            b_insert_start_dat = True
                            if idx_delta_value > 0:
                                span_lvl.set_attribute("deltaValueIdx", idx_delta_value)
                            # adjust start date, depending on the aggregation level

                            # dv_next is the delta_values for next level
                            dv_next = {"maxminFix": []}

                            # for all type_instruments
                            for an_intrument in all_instr.get_all_instruments():
                                # for all measures
                                for my_measure in an_intrument["object"].get_all_measures():
                                    # load the needed aggregation for this measure
                                    agg_decas = self.load_aggregations_in_array(my_measure, anAgg, aggregations, m_stop_dat)

                                    m_agg_j = self.get_agg_magg(anAgg, a_todo.data.obs_id.j_agg)

                                    if b_insert_start_dat:
                                        b_insert_start_dat = False
                                        span_lvl.set_attribute("startDat", str(agg_decas[0].data.start_dat))

                                    # find the calculus object for my_mesure
                                    for a_calculus in self.all_calculus:
                                        if a_calculus["agg"] == my_measure["agg"]:
                                            if a_calculus["calc_agg"] is not None:
                                                # load data in our aggregation
                                                a_calculus["calc_agg"].loadDVDataInAggregation(my_measure, m_stop_dat, agg_decas[0], m_agg_j, delta_values, dv_next, trace_flag)

                                                # get our extreme values
                                                a_calculus["calc_agg"].loadDVMaxMinInAggregation(my_measure, m_stop_dat, agg_decas, m_agg_j, delta_values, dv_next, trace_flag)
                                            break

                            # loop to the next AggLevel
                            delta_values = dv_next

                # save our aggregations for this delta_values
                with self.tracer.start_span("saveData", trace_flag):
                    for an_agg in aggregations:
                        if an_agg.dirty is True:
                            an_agg.save()

                    # a_todo.data.status = 999
                    # a_todo.save()
                    a_todo.delete()

                    # we're done
                    duration = datetime.datetime.now() - time_start
                    dur_millisec = duration.seconds * 1000
                    if dur_millisec < 10000:
                        dur_millisec = duration.microseconds / 1000
                    t.logInfo(
                        "Aggregation computed",
                        my_span,
                        {
                            "obsId": a_todo.data.obs_id_id,
                            "meteor": a_todo.data.obs_id.poste_id.meteor,
                            "queueLength": a_todo.count(),
                            "timeExec": dur_millisec,
                        },
                    )
            finally:
                poste_metier.unlock()

    def load_aggregations_in_array(self, my_measure, anAgg: str, aggregations, m_stop_dat: datetime):
        """load array of aggregations for calculus:
        [0] -> main_deca for data
        [1] -> min_deca
        [2] -> max_deca
        """
        agg_decas = []
        deca_hours = []

        if my_measure.get('target_key') == 'rain_omm':
            agg_decas = []

        if my_measure.get("hour_deca") is None or anAgg[0] != 'H':
            deca_hours.append(0)
            main_deca = 0
        else:
            main_deca = my_measure["hour_deca"]
            deca_hours.append(main_deca)

        if my_measure.get("deca_max") is None or anAgg[0] != 'H':
            deca_hours.append(main_deca)
        else:
            deca_hours.append(my_measure["deca_max"])

        if my_measure.get("deca_min") is None or anAgg[0] != 'H':
            deca_hours.append(main_deca)
        else:
            deca_hours.append(my_measure["deca_min"])

        for deca_hour in deca_hours:
            a_start_dat_level = calcAggDate(anAgg, m_stop_dat, deca_hour, True)

            # load the needed aggregation for this measure
            b_found = False
            for my_agg in aggregations:
                if (
                    my_agg.agg_niveau == anAgg
                    and my_agg.data.start_dat == a_start_dat_level
                ):
                    agg_decas.append(my_agg)
                    b_found = True
                    break
            if b_found is False:
                raise Exception(
                    "aggCompute::loadAggregations",
                    "aggregation not loaded deca: "
                    + str(deca_hour)
                    + ", date: "
                    + str(a_start_dat_level),
                )

        return agg_decas

    def get_agg_magg(self, agg_level: str, j_agg: json):
        """
        get_agg_magg
        """
        # get aggregation values in measures
        m_agg_j = {}
        if j_agg != {}:
            for a_j_agg in j_agg:
                if (
                    a_j_agg.__contains__("level")
                    and a_j_agg["level"][0] == agg_level[0]
                ):
                    t.CopyJson(a_j_agg, m_agg_j)
        return m_agg_j
