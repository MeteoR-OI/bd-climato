from app.models import Poste
from app.tools.climConstant import AggLevel
import datetime
from app.tools.agg_tools import calc_agg_date
import json
from app.classes.obsMeteor import ObsMeteor
from app.classes.aggMeteor import AggMeteor
from app.classes.ExcluMeteor import ExcluMeteor


class PosteMeteor:
    """
        PosteMeteor

        objets Poste metier

        p1=PosteMeteor(1) -> recupere le poste id = 1 + exclusions actuelles
        p2=PosteMeteor(1, my_date) -> recupere le poste id = 1 et exclusions a la date de my_date
    """

    def __init__(self, poste_id: int, date_histo=datetime.datetime.now(datetime.timezone.utc)):
        """ load our instance from db, load exclusions at date_histo """
        if Poste.objects.filter(id=poste_id).exists():
            self.data = Poste.objects.get(id=poste_id)
            self.exclus = ExcluMeteor.getAllForAPoste(self.data, date_histo)
        else:
            self.data = Poste()
            self.exclus = []

    def save(self):
        """ save Poste """
        try:
            self.data.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def cas_gestion_extreme(self):
        """ in future could get the information from values in db """
        return self.data.cas_gestion_extreme

    def agg_min_extreme(self):
        """ in future could get the information from values in db """
        return self.data.agg_min_extreme

    def exclusion(self, type_intrument_id) -> json:
        """ retourne la premiere exclusion active pour le type instrument """
        for anExclu in self.exclus:
            if anExclu['type_instrument'] == type_intrument_id:
                return anExclu['value']
        return {}

    def date_fuseau(self, dt: datetime) -> datetime:
        """ retoune la datetime fuseau de la station """
        return dt + datetime.timedelta(hours=self.data.fuseau)

    def round_datetime_per_aggregation(self, dt: datetime, niveau_agg: str, delta: int = 0):
        """ round_datetime_per_aggregation

            retourne la date/heure du debut d'agregation pour le poste

            l'heure pour le niveau d'agregation heure est basée sur l'heure UTC

            les heures dans les agregations superieures sont calculees a partir
            de l'heure fuseau
        """
        try:
            if niveau_agg == "H":
                return calc_agg_date(niveau_agg, dt)

            # on passe sur la date/heure fuseau
            d_loc = self.date_fuseau(dt)
            return calc_agg_date(niveau_agg, d_loc)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def aggregations(self, my_datetime_utc: datetime):
        """
        get_agg

        my_datetime_utc: date en UTC.

        return an array of AggMeteor to be used by our process_xxx methods
            [0] -> Agg_hour
            [1] -> Agg_day
            [2] -> Agg_month
            [3] -> Agg-year
            [4] -> Agg_all
            [5] -> Agg_day for day - 1
            [6] -> Agg_day for day + 1

        create them if needed
        """
        try:
            ret = []
            # push aggregations of all levels for the given date
            for agg_niveau in AggLevel:
                tmp_dt = self.round_datetime_per_aggregation(
                    my_datetime_utc, agg_niveau)
                ret.append(AggMeteor(self.data, agg_niveau, tmp_dt))

            # get aggregation of day - 1 for measures that will aggregate yesteray
            tmp_dt = self.round_datetime_per_aggregation(
                my_datetime_utc, 'D', -1)
            ret.append(AggMeteor(self.data, 'D', tmp_dt))

            # get aggregation of day + 1 for measures that will aggregate the day after
            tmp_dt = self.round_datetime_per_aggregation(
                my_datetime_utc, 'D', +1)
            ret.append(AggMeteor(self.data, 'D', tmp_dt))

            return ret
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def observation(self, my_datetime_utc: datetime) -> ObsMeteor:
        """get or create an observation at a given datetime"""
        try:
            return ObsMeteor(self.data, my_datetime_utc)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "PosteMeteor id: " + str(self.data.id) + ", meteor: " + self.data.meteor + ", #exclu: " + str(self.exclus.__len__())
