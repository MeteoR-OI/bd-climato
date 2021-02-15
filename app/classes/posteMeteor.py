from app.models import Poste
from app.tools.climConstant import AggLevel
import datetime
from dateutil.relativedelta import relativedelta
import json
from app.classes.obsMeteor import ObsMeteor
from app.classes.aggMeteor import AggMeteor
from app.classes.ExcluMeteor import ExcluMeteor


class PosteMeteor:
    """
        PosteMeteor

        gere les objets Poste metier en memoire, une seule instance en memoire
        (singleton par instance d'objet)

        p=PosteMeteor.get(1) -> recuperer le poste id = 1

    """

    all = []    # all is global to all instances

    # def __del__(self):
    #     """destructor need to clean up all list"""
    #     try:
    #         print("destructor: id " + str(self.me.id))
    #         for one_poste in self.all:
    #             if one_poste.__dict__.__contains__('me'):
    #                 if one_poste.me.id == self.me.id:
    #                     self.all.remove(one_poste)
    #     except Exception as inst:
    #         print(type(inst))    # the exception instance
    #         print(inst.args)     # arguments stored in .args
    #         print(inst)          # __str__ allows args to be printed directly,

    @staticmethod
    def get(poste_id: int):
        """manage a singleton per poste instance, and load active exclusions"""
        tmp_poste = PosteMeteor()
        for one_poste in tmp_poste.all:
            if one_poste.me.id == poste_id:
                return one_poste
        if Poste.objects.filter(id=poste_id).exists():
            tmp_poste.me = Poste.objects.get(id=poste_id)
            tmp_poste.exclus = ExcluMeteor.getAllForAPoste(tmp_poste.me.id)
        else:
            tmp_poste.me = Poste()
            tmp_poste.exclus = []
        tmp_poste.all.append(tmp_poste)
        return tmp_poste

    def save(self):
        """ save Poste """
        try:
            self.me.save()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def cas_gestion_extreme(self):
        """ in future could get the information from values in db """
        return self.me.cas_gestion_extreme

    def agg_min_extreme(self):
        """ in future could get the information from values in db """
        return self.me.agg_min_extreme

    def exclusion(self, type_intrument_id) -> json:
        """ retourne la premiere exclusion active pour le type instrument """
        for anExclu in self.exclus:
            if anExclu['type_instrument'] == type_intrument_id:
                return anExclu['value']
        return {}

    def date_fuseau(self, dt: datetime) -> datetime:
        """ retoune la datetime fuseau de la station """
        return dt + datetime.timedelta(hours=self.me.fuseau)

    def round_datetime_per_aggregation(self, dt: datetime, niveau_agg: str, delta: int = 0):
        """ round_datetime_per_aggregation

            arrondi la date, suivant le niveau d'agreggation.
            delta ajoute un nombre de heure/jour/... au resultat

            l'heure pour le niveau d'agregation heure est basée sur l'heure UTC

            les heures dans les agregations superieures sont calculees a partir
            de l'heure fuseau
        """
        try:
            if niveau_agg == "H":
                return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(hours=delta)

            # on passe sur la date/heure fuseau
            d_loc = self.date_fuseau(dt)
            if niveau_agg == "D":
                return datetime.datetime(d_loc.year, d_loc.month, d_loc.day, 0, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(days=delta)
            elif niveau_agg == "M":
                return datetime.datetime(d_loc.year, d_loc.month, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(months=delta)
            elif niveau_agg == "Y":
                return datetime.datetime(d_loc.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + relativedelta(years=delta)
            elif niveau_agg == "A":
                return datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
            else:
                raise Exception("round_datetime_per_aggregation",
                                "wrong niveau_agg: " + niveau_agg)

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
                tmp_dt = self.round_datetime_per_aggregation(my_datetime_utc, agg_niveau)
                ret.append(AggMeteor(self.me, agg_niveau, tmp_dt))

            # get aggregation of day - 1 for measures that will aggregate yesteray
            tmp_dt = self.round_datetime_per_aggregation(my_datetime_utc, 'D', -1)
            ret.append(AggMeteor(self.me, 'D', tmp_dt))

            # get aggregation of day + 1 for measures that will aggregate the day after
            tmp_dt = self.round_datetime_per_aggregation(my_datetime_utc, 'D', +1)
            ret.append(AggMeteor(self.me, 'D', tmp_dt))
 
            return ret
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def observation(self, my_datetime_utc: datetime) -> ObsMeteor:
        """get or create an observation at a given datetime"""
        try:
            return ObsMeteor(self.me, my_datetime_utc)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "PosteMeteor id: " + str(self.me.id) + ", meteor: " + self.me.meteor + ", #exclu: " + str(self.exclus.__len__())
