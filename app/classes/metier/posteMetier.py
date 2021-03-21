from app.tools.climConstant import AggLevel
import datetime
import json
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.aggMeteor import AggMeteor
from app.classes.repository.excluMeteor import ExcluMeteor
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.metier.typeInstrumentAll import TypeInstrumentAll
from app.tools.aggTools import calcAggDate


class PosteMetier(PosteMeteor):
    """
        PosteMeteor

        Add obs/agg/exclu info to PosteMeteor
    """

    def __init__(self, poste_id: int, start_date: datetime = datetime.datetime.now(datetime.timezone.utc)):
        """ load our instance from db, load exclusions at date_histo """
        super().__init__(poste_id)
        self.exclus = ExcluMeteor.getAllForAPoste(self.data.id, start_date)
        self.analysis_date = start_date

    def exclusion(self, type_intrument_id) -> json:
        """ retourne la premiere exclusion active pour le type instrument """
        for anExclu in self.exclus:
            if anExclu['type_instrument'] == type_intrument_id:
                return anExclu['value']
        return None

    def getAllForAPoste(self, start_dat: datetime = datetime.datetime.now(datetime.timezone.utc)) -> json:
        return ExcluMeteor.getAllForAPoste(self.data.id, start_dat)

    def aggregations(self, my_start_date_utc: datetime, is_measure_date: bool = False) -> json:
        """
            get_agg

            my_start_date_utc: date en UTC.
            return an array of aggregations needed by our calculus function

            load empty agg_xxxx if does not exist
        """
        # determine all dates needed to process the measure at the given date
        needed_dates = [my_start_date_utc]
        calculated_deca = {"d0": True}
        ti_all = TypeInstrumentAll()
        for an_instru in ti_all.all_instruments:
            for a_measure in an_instru['object'].measures:
                if a_measure.__contains__('hour_deca') and calculated_deca.__contains__('d' + str(a_measure['hour_deca'])) is False:
                    hour_deca = a_measure['hour_deca']
                    # set the deca as computed
                    calculated_deca['d' + str(hour_deca)] = True
                    deca_duration = datetime.timedelta(hours=int(hour_deca))
                    needed_dates.append(my_start_date_utc + deca_duration)

        # now load the needed aggregations
        ret = []
        for a_needed_date in needed_dates:
            tmp_dt = calcAggDate('H', a_needed_date, 0, True)
            for agg_niveau in AggLevel:
                # is_measure_date only used in agg_hour
                tmp_dt = calcAggDate(agg_niveau, tmp_dt, 0, False)
                already_loaded = False
                for a_ret in ret:
                    if a_ret.data.start_dat == tmp_dt:
                        already_loaded = True
                        break
                if already_loaded is False:
                    ret.append(AggMeteor(self.data.id, agg_niveau, tmp_dt))
        return ret

    def observation(self, my_stop_date_utc: datetime) -> ObsMeteor:
        """get or create an observation at a given datetime"""
        try:
            return ObsMeteor(self.data.id, my_stop_date_utc)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        super()
        return "....PosteXMeteor, #exclu: " + str(self.exclus.__len__())
