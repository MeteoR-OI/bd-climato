from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggTodoMeteor import AggTodoMeteor
from app.tools.climConstant import AggLevel, MeasureProcessingBitMask
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.aggTools import isFlagged, delKey, shouldNullify, calcAggDate
from app.tools.workers import Workers
from app.tools.refManager import RefManager
from django.db import transaction
import json
import datetime
import threading


class ProcessAggreg():
    """
        ProcessAggreg

        Computation specific to a measure type

        calculus v2

        select_for_update(skip_locked=True)
        select id, priority, status from agg_todo order by priority, id limit 1 for update  SKIP LOCKED
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
        name = 'ProcessAggreg'
        ref_mgr = RefManager.GetInstance()
        if ref_mgr.GetRef('Svc' + name) is None:
            ref_mgr.AddRef('Svc' + name, ProcessAggreg(name))
        return ref_mgr.GetRef('Svc' + name)

    def start(self, kill_me: threading.Event, stop_event: threading.Event):
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
                self.runMe()
        except Exception as exc:
            print(exc)
        finally:
            stop_event.set()

    def ComputeAggreg(a_todo: AggTodoMeteor):
        """
            ComputeAggreg

            send the delta values to all our measures
        """
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
                            a_calculus['calc_obs'].loadInObs(poste_metier, my_measure, m_j, measure_idx, obs_meteor, delta_values, trace_flag)
                        break


    # def processAggregations(
    #     self,
    #     poste_metier,
    #     my_measure: json,
    #     measures: json,
    #     measure_idx: int,
    #     aggregations: list,
    #     delta_values: json,
    #     trace_flag: bool = False,
    # ):


        # load the current aggregations array for our anAgg
        deca_hour = 0
        if my_measure.__contains__('hour_deca') is True:
            deca_hour = my_measure['hour_deca']

        measure_dat = calcAggDate('H', measures['data'][measure_idx]['current']['stop_dat'], deca_hour, True)

        for anAgg in AggLevel:
            measure_dat = calcAggDate(anAgg, measure_dat, 0, False)

            """loop for all aggregations in ascending level"""
            dv_next = {"maxminFix": []}

            # load our array of current aggregation, plus prev/next for agg_day only
            agg_deca = None
            for my_agg in aggregations:
                if my_agg.agg_niveau == anAgg and my_agg.data.start_dat == measure_dat:
                    agg_deca = my_agg
                    break

            if agg_deca is None:
                raise Exception('processAggregations', 'aggregation not loaded')

            # load data in our aggregation
            self.loadAggregationDatarows(
                my_measure,
                measures,
                measure_idx,
                agg_deca,
                target_key,
                delta_values,
                dv_next,
            )

            # get our extreme values
            self.loadMaxMinInAggregation(
                my_measure,
                measures,
                measure_idx,
                agg_deca,
                target_key,
                exclusion,
                delta_values,
                dv_next,
            )
            # save our delta_values if in trace mode
            if trace_flag is True:
                j_agg = agg_deca[0].data.j
                if j_agg.__contains__('dv') is False:
                    j_agg['dv'] = {}
                for akey in delta_values.items():
                    j_agg['dv'][akey[0]] = delta_values[akey[0]]

            # we will pass our new delta_values to the next level
            delta_values = dv_next
        return

    def recomputeExtremes():
        # calculus v1
        print('to do')

    # ----------------------------------------------------
    # private or methods common to multiple sub-instances
    # ----------------------------------------------------
    def loadMaxMinInObservation(
        self,
        my_measure: json,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        src_key: str,
        target_key: str,
        exclusion: json,
        delta_values: json,
        b_use_rate: bool = False,
    ):
        """
            loadMaxMinInObservation

            load in obs max/min value if present
            update delta_values

            calculus v2
        """
        obs_j = obs_meteor.data.j
        if delta_values.__contains__(target_key) is False:
            # no value processed
            return

        last_measure_time = measures['data'][measure_idx]['current']['stop_dat']
        data_src = {}
        if measures['data'][measure_idx].__contains__('current'):
            data_src = measures['data'][measure_idx]['current']

        for maxmin_sufx in ['_max', '_min']:
            # is max or min needed for this measure
            maxmin_key = maxmin_sufx.split('_')[1]
            maxmin_suffix = maxmin_sufx
            if b_use_rate:
                maxmin_suffix = '_rate' + maxmin_sufx
            if my_measure.__contains__(maxmin_key) is True and my_measure[maxmin_key] is True:
                maxmin_time = last_measure_time

                # is there a M_max/M_min in the data_src ?
                if data_src.__contains__(src_key + maxmin_suffix):
                    # found, then load in in obs and delta_values
                    my_maxmin_value = my_measure['dataType'](data_src[src_key + maxmin_suffix])
                    obs_j[target_key + maxmin_suffix] = my_maxmin_value
                    if data_src.__contains__(src_key + maxmin_suffix + '_time'):
                        maxmin_time = data_src[src_key + maxmin_suffix + '_time']
                    obs_j[target_key + maxmin_suffix + '_time'] = maxmin_time
                    delta_values[target_key + maxmin_suffix] = my_maxmin_value
                    delta_values[target_key + maxmin_suffix + '_time'] = maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)) and maxmin_suffix == '_max':
                        """ save Wind_max_dir """
                        if data_src.__contains__(src_key + maxmin_suffix + '_dir') is True:
                            my_wind_dir = int(data_src[src_key + maxmin_suffix + '_dir'])
                            obs_j[target_key + maxmin_suffix + '_dir'] = my_wind_dir
                            delta_values[target_key + maxmin_suffix + '_dir'] = my_wind_dir
                elif delta_values.__contains__(target_key):
                    # on prend la valeur reportee, et le milieu de l'heure de la periode de la donnee elementaire
                    if b_use_rate:
                        # pour les "rate" on prend l'avg (qui est un rate)
                        delta_values[target_key + maxmin_suffix] = delta_values[target_key + '_sum']
                    else:
                        # sinon on prend la valeur de la mesure
                        delta_values[target_key + maxmin_suffix] = delta_values[target_key]
                    delta_values[target_key + maxmin_suffix + '_time'] = maxmin_time

    def loadMaxMinInAggregation(
        self, my_measure: json,
        measures: json,
        measure_idx: int,
        my_aggreg,
        json_key: str,
        exclusion: json,
        delta_values: json,
        dv_next: json,
        b_use_rate: bool = False,
    ):
        """
            loadMaxMinInObservation

            load in obs max/min  i our aggregation value if present
            update dv_next for nest level

            calculus v1
        """
        # save our dv, and get agg_j, m_agg_j
        m_agg_j = self.get_agg_magg(my_aggreg, delta_values, measures, measure_idx)
        agg_j = my_aggreg.data.j

        for maxmin_suffix in ['_max', '_min']:
            maxmin_key = maxmin_suffix.split('_')[1]
            if b_use_rate:
                maxmin_suffix = '_rate' + maxmin_suffix

            if my_measure.__contains__(maxmin_key) and my_measure[maxmin_key] is True:

                if m_agg_j.__contains__(json_key + '_delete_me') is True:
                    # measure was deleted previously
                    delKey(m_agg_j, json_key + maxmin_suffix + '_max')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_max_time')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_min')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_min_time')
                    delKey(m_agg_j, json_key + maxmin_suffix + '_first_time')
                    continue

                if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                    current_maxmin_dir = None

                # if the max-min is required in measure definition
                current_maxmin = None
                if delta_values.__contains__(json_key):
                    current_maxmin = my_measure['dataType'](delta_values[json_key])
                    current_maxmin_time = measures['data'][measure_idx]['current']['stop_dat']

                if delta_values.__contains__(json_key + maxmin_suffix) is True:
                    # load from delta_values
                    current_maxmin = my_measure['dataType'](delta_values[json_key + maxmin_suffix])
                    current_maxmin_time = delta_values[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(delta_values[json_key + maxmin_suffix + '_dir'])

                if m_agg_j.__contains__(json_key + maxmin_suffix):
                    # load and use json measure maxmin if given in aggregation key
                    current_maxmin = my_measure['dataType'](m_agg_j[json_key + maxmin_suffix])
                    current_maxmin_time = m_agg_j[json_key + maxmin_suffix + '_time']
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if m_agg_j.__contains__(json_key + maxmin_suffix + '_dir') is True:
                            current_maxmin_dir = int(m_agg_j[json_key + maxmin_suffix + '_dir'])

                if current_maxmin is None:
                    # no values
                    continue

                # load current data from our aggregation
                if agg_j.__contains__(json_key + maxmin_suffix):
                    agg_maxmin = agg_j[json_key + maxmin_suffix]
                else:
                    # force the usage of current_maxmin
                    if maxmin_suffix == '_min':
                        agg_maxmin = current_maxmin + 1
                    else:
                        agg_maxmin = current_maxmin - 1

                b_change_maxmin = False
                if delta_values.__contains__(json_key + '_maxmin_invalid_val' + maxmin_suffix) and agg_maxmin == delta_values[json_key + '_maxmin_invalid_val' + maxmin_suffix]:
                    self.add_new_maxmin_fix(json_key, maxmin_key, my_aggreg.data.start_dat, delta_values, my_aggreg)
                    dv_next[json_key + '_maxmin_invalid_val' + maxmin_suffix] = agg_maxmin
                    b_change_maxmin = True
                # compare the measure data and current maxmin
                if maxmin_suffix == '_max' and agg_maxmin < current_maxmin:
                    b_change_maxmin = True
                if maxmin_suffix == '_min' and agg_maxmin > current_maxmin:
                    b_change_maxmin = True

                if b_change_maxmin:
                    agg_j[json_key + maxmin_suffix] = current_maxmin
                    dv_next[json_key + maxmin_suffix] = current_maxmin
                    agg_j[json_key + maxmin_suffix + '_time'] = current_maxmin_time
                    dv_next[json_key + maxmin_suffix + '_time'] = current_maxmin_time
                    if (isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsWind)):
                        if current_maxmin_dir is not None:
                            agg_j[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir
                            dv_next[json_key + maxmin_suffix + '_dir'] = current_maxmin_dir

    def get_src_key(self, my_measure: json):
        """
            return the target key name

            calculus v1
            calculus v2
        """
        src_key = my_measure['src_key']
        target_key = src_key
        if my_measure.__contains__('target_key'):
            target_key = my_measure['target_key']
        elif isFlagged(my_measure['special'], MeasureProcessingBitMask.MeasureIsOmm):
            target_key += '_omm'
        return (src_key, target_key)

    def add_new_maxmin_fix(self, json_key: str, maxmin_key: str, measure_date: datetime, delta_values: json, my_aggreg):
        # calculus v1
        delta_values['maxminFix'].append({
            "posteId": my_aggreg.data.poste_id_id,
            "startDat": my_aggreg.data.start_dat,
            "level": my_aggreg.agg_niveau,
            "maxmin": maxmin_key,
            "key": json_key,
            "valeur": my_aggreg.data.j[json_key + '_' + maxmin_key],
            "dat": measure_date,
        })
