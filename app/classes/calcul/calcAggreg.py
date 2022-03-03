from app.classes.calcul.aggregations.aggCompute import AggCompute
from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.refManager import RefManager
from app.tools.aggTools import calcAggDate, getAggLevels
from app.tools.telemetry import Telemetry
import app.tools.myTools as t
from django.db import transaction
import json
import datetime


class CalcAggreg():
    """ Aggregate data from new inserted observation rows """

    def __init__(self):
        self.tracer = Telemetry.Start("calculus", __name__)
        self.agg_compute = AggCompute()

    def ComputAggregFromSvc(self, data: json, is_killed):
        """entry point called from worker"""
        self.stopRequested = False

        # load params
        if data is None or data.get("param") is None or data["param"] == {}:
            t.LogError("wrong data")
        params = data["param"]

        # Stop request
        if params.get("StopMe") is True:
            self.stopRequested = True
            return

        # load parameters (global trace, then params.trace_flag)
        if RefManager.GetInstance().GetRef("calcAgg_trace_flag") is None:
            trace_flag = False
        else:
            trace_flag = RefManager.GetInstance().GetRef("calcAgg_trace_flag")
        if params.get("trace_flag") is not None:
            trace_flag = params["trace_flag"]

        # load other params
        ret = []

        # run now
        try:
            ret = self.CalcAggregControler(False, trace_flag, is_killed)
            return ret

        except Exception as inst:
            t.LogCritical(inst)

    def CalcAggregControler(self, is_tmp_called: bool, trace_flag: bool, is_killed):
        """ CalcAggregControler function """

        while self.stopRequested is False:
            if is_killed() is True:
                return

            # get first aggTodo
            a_todo = AggTodoMeteor.popOne(False)
            if a_todo is None:
                a_todo = AggTodoMeteor.popOne(True)
                if a_todo is None:
                    # no more data to update, return to sleep
                    return
            my_span = self.tracer.start_as_current_span("Calc agg", trace_flag)

            try:
                self.__processTodo(a_todo, False)

            except Exception as exc:
                IncidentMeteor.new(
                    "calc_agg",
                    "Exception",
                    str(exc),
                    {
                        'meteor': a_todo.obs.poste.meteor,
                        'obs_id': a_todo.data.id,
                        'stopDat': str(a_todo.obs.stop_dat),
                    })
                my_span.record_exception(exc)
                a_todo.ReportError(exc)
                a_todo.save()

            finally:
                my_span.end()

    @transaction.atomic
    def __processTodo(self, a_todo, is_tmp: bool = False):
        """ Aggregate data from an agg_todo """

        time_start = datetime.datetime.now()
        all_instr = AllTypeInstruments()
        if RefManager.GetInstance().GetRef("calcAggreg_trace_flag") is None:
            trace_flag = False
        else:
            trace_flag = RefManager.GetInstance().GetRef("calcAggreg_trace_flag")

        json_type = a_todo.data.json_type
        is_json_obs = True if json_type in ["O", "C"] else False

        my_span = self.tracer.start_as_current_span("Calc agg", trace_flag)
        my_span.set_attribute("obsId", a_todo.data.id)
        my_span.set_attribute("stopDat", str(a_todo.obs.stop_dat))
        my_span.set_attribute("meteor", a_todo.obs.poste.meteor)

        # retrieve posteMetier and needed aggregations
        with self.tracer.start_span("finding needed aggregations", trace_flag) as span_load_data:
            m_stop_dat = a_todo.obs.stop_dat
            a_start_dat = a_todo.obs.agg_start_dat
            poste_metier = PosteMetier(a_todo.obs.poste_id, a_start_dat)

            poste_metier.lock()
            aggregations = poste_metier.aggregations(a_todo.data.id, m_stop_dat, True, False, json_type)
            span_load_data.set_attribute("items", aggregations.__len__())

        try:
            idx_dv = 0
            while idx_dv < a_todo.data.j.__len__():
                # load dv/m_agg_j variable, add duration to the main aggregations
                if is_json_obs is True:
                    delta_values = a_todo.data.j[idx_dv]
                    m_agg_j = {}
                    tmp_duration = delta_values["duration"]
                    for an_agg in aggregations:
                        # add duration in main aggregations (the one with no deca...)
                        new_dursum = an_agg.add_duration(tmp_duration)
                        if new_dursum > 0:
                            my_span.set_attribute('duration_agg' + an_agg.agg_niveau + '_' + str(an_agg.data.start_dat), new_dursum)
                else:
                    delta_values = {}
                    m_agg_j = a_todo.data.j[idx_dv]
                    tmp_duration = m_agg_j["duration"]

                    mini_duration = m_agg_j.get['level'] if not None else '?'
                    b_first_level_passed = False
                    for an_agg in aggregations:
                        if b_first_level_passed is False:
                            b_first_level_passed = (mini_duration == an_agg.agg_niveau)
                        if b_first_level_passed is True:
                            an_agg.add_duration(tmp_duration)
                            span_load_data.set_attribute('duration_agg' + an_agg.agg_niveau + '_' + str(an_agg.data.start_dat), tmp_duration)

                # loop on each level
                for anAgg in getAggLevels(False):
                    with self.tracer.start_span("level " + anAgg, trace_flag) as span_lvl:
                        span_lvl.set_attribute("idx_dv", idx_dv)
                        b_insert_start_dat = True
                        # adjust start date, depending on the aggregation level

                        # dv_next is the delta_values for next level
                        dv_next = {"maxminFix": [], "duration": tmp_duration}

                        # for all type_instruments
                        for an_instrument in all_instr.get_all_instruments():
                            # for all measures
                            for my_measure in an_instrument["object"].get_all_measures():
                                # load the needed aggregation for this measure
                                agg_decas = self.load_aggregations_in_array(my_measure, anAgg, aggregations, m_stop_dat)
                                if my_measure['agg'] == 'sumomm':
                                    agg_decas = self.load_aggregations_in_array(my_measure, anAgg, aggregations, m_stop_dat)

                                if b_insert_start_dat:
                                    b_insert_start_dat = False
                                    span_lvl.set_attribute("startDat", str(agg_decas[0].data.start_dat))

                                # find the calculus object for my_mesure
                                self.agg_compute.loadDVDataInAggregation(my_measure, agg_decas, m_agg_j, delta_values, dv_next, trace_flag)

                                # get our extreme values
                                # self.agg_compute.loadDVMaxMinInAggregation(my_measure, m_stop_dat, agg_decas, m_agg_j, delta_values, dv_next, trace_flag)

                        # loop to the next AggLevel
                        delta_values = dv_next
                idx_dv += 1

            # save our aggregations for this delta_values
            with self.tracer.start_span("saveData", trace_flag):
                for an_agg in aggregations:
                    an_agg.save()

                a_todo.data.status = 999
                a_todo.save()
                # a_todo.delete()

                # we're done
                duration = datetime.datetime.now() - time_start
                dur_millisec = round(duration.total_seconds() * 1000)
                t.logInfo(
                    "Aggregation computed",
                    my_span,
                    {
                        "obsId": a_todo.obs.id,
                        "meteor": a_todo.obs.poste.meteor,
                        "queueLength": AggTodoMeteor.count(),
                        "timeExec": dur_millisec,
                    },
                )
        finally:
            poste_metier.unlock()

    def load_aggregations_in_array(self, my_measure, anAgg: str, aggregations, m_stop_dat: datetime):
        """load array of aggregations for calculus:
        [0] -> main_deca for data
        [1] -> max_deca
        [2] -> min_deca
        """
        agg_decas = []
        deca_hours = []

        # data always aggregated @ hour_deca
        deca_hours.append(my_measure["hour_deca"])
        # aggregation for max values
        deca_hours.append(my_measure["deca_max"])
        # aggregation for min values
        deca_hours.append(my_measure["deca_min"])

        old_deca = 999
        for deca_hour in deca_hours:
            if deca_hour == old_deca:
                # use last pushed data if deca_hour is the same
                agg_decas.append(agg_decas[-1])
            else:
                # compute new start_dat
                old_deca = deca_hour
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
