import datetime
import json
import threading
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.excluMeteor import ExcluMeteor
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.typeInstruments.allTtypes import AllTypeInstruments
from app.tools.aggTools import calcAggDate, getAggLevels


class PosteMetier(PosteMeteor):
    """
        PosteMeteor

        Add obs/agg/exclu info to PosteMeteor
    """

    def __init__(self, poste_id: int, start_date: datetime = datetime.datetime.now(datetime.timezone.utc)):
        """ load our instance from db, load exclusions at date_histo """
        super().__init__(poste_id)
        self.exclus = ExcluMeteor.getAllForAPoste(self.data.id, start_date)
        self.lock_event = threading.Event()
        # self.analysis_date = start_date

    def lock(self):
        """
            lock

            lock le poste Metier pour serialiser les ajouts d'observation, ou calcul des agregations

            Les calculs obs, et aggregation se passent avec toutes les données en memoire, donc il est important
            de serialiser la periode lecture/update de ces donnees.

            Cela doit se faire par poste, donc gerer les locks a ce niveau est la meilleure (et plus simple a coder) approche
        """
        self.lock_event.set()

    def unlock(self):
        if self.lock_event.is_set():
            self.lock_event.clear()

    def exclusion(self, type_intrument_id) -> json:
        """ retourne la premiere exclusion active pour le type instrument """
        for anExclu in self.exclus:
            if anExclu['type_instrument'] == type_intrument_id:
                return anExclu['value']
        return None

    def getAllForAPoste(self, start_dat: datetime = datetime.datetime.now(datetime.timezone.utc)) -> json:
        return ExcluMeteor.getAllForAPoste(self.data.id, start_dat)

    def aggregations(self, start_date_utc: datetime, is_measure_date: bool = False, is_tmp: bool = None) -> json:
        """
            get_agg

            my_start_date_utc: date en UTC
                aggregation start_dat, or obs.stop_date
            return an array of aggregations needed by our calculus function

            load empty agg_xxxx if does not exist
        """
        # determine all dates needed to process the measure at the given date
        my_start_date_utc = start_date_utc
        if is_measure_date is True:
            my_start_date_utc = calcAggDate('H', start_date_utc, 0, True)
        # m_duration = self.data.du
        needed_dates = [my_start_date_utc]
        calculated_deca = {'d0': True}
        ti_all = AllTypeInstruments()
        for an_instru in ti_all.get_all_instruments():
            for a_measure in an_instru['object'].measures:
                for deca_type in ['hour_deca', 'deca_max', 'deca_min']:
                    if a_measure.get(deca_type) is not None:
                        hour_deca = int(a_measure[deca_type])
                        if calculated_deca.get('d' + str(hour_deca)) is None:
                            calculated_deca['d' + str(hour_deca)] = True
                            deca_duration = datetime.timedelta(hours=int(hour_deca))
                            needed_dates.append(my_start_date_utc - deca_duration)

        # now load the needed aggregations
        ret = []
        for a_needed_date in needed_dates:
            tmp_dt = a_needed_date
            b_need_to_sum_duration = False
            if str(a_needed_date) == str(my_start_date_utc):
                b_need_to_sum_duration = True
            for agg_niveau in getAggLevels(is_tmp):
                # is_measure_date only used in agg_hour
                tmp_dt = calcAggDate(agg_niveau, tmp_dt, 0, False)
                already_loaded = False
                for a_ret in ret:
                    if a_ret.data.start_dat == tmp_dt and a_ret.agg_niveau == agg_niveau:
                        already_loaded = True
                        break
                if already_loaded is False:
                    ret.append(AggMeteor(self.data.id, agg_niveau, tmp_dt, False, b_need_to_sum_duration))
        return ret

    def observation(self, my_stop_date_utc: datetime, is_tmp: bool = None) -> ObsMeteor:
        """get or create an observation at a given datetime"""
        return ObsMeteor(self.data.id, my_stop_date_utc, is_tmp)

    def __str__(self):
        """print myself"""
        super().__str__()
        return "....PosteXMeteor, #exclu: " + str(self.exclus.__len__())
