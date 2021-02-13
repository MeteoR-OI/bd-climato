from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object
from app.tools.climConstant import AggLevel
import datetime


class poste_meteor:
    """Objet climato poste"""

    all = []    # all is global to all instances

    def __init(self, poste_id):
        """ this is only for test """
        print("poste_meteor(n) was called.... only available for testing !!!")
        if Poste.objects.filter(id=poste_id).exists():
            self.me = Poste.objects.get(id=poste_id)
        else:
            self.me = Poste()

    def __del__(self):
        """destructor need to clean up all list"""
        print("destructor: id " + str(self.id))
        for one_poste in self.all:
            if one_poste.__dict__.__contains__('me'):
                if one_poste.me.id == self.me.id:
                    self.all.remove(one_poste)

    @staticmethod
    def get(poste_id):
        """manage a singleton per poste instance, and load active exclusions"""
        tmp_poste = poste_meteor()
        for one_poste in tmp_poste.all:
            if one_poste.me.id == poste_id:
                return one_poste
        if Poste.objects.filter(id=poste_id).exists():
            tmp_poste.me = Poste.objects.get(id=poste_id)
            tmp_poste.exclus = Exclusion.objects.filter(poste_id_id=poste_id).filter(end_x__gt=datetime.datetime.now(datetime.timezone.utc)).values('type_instrument', 'value')
        else:
            tmp_poste.me = Poste()
            tmp_poste.exclus = []
        tmp_poste.all.append(tmp_poste)
        return tmp_poste

    def cas_gestion_extreme(self):
        """ in future could get the information from values in db """
        return self.me.cas_gestion_extreme

    def agg_min_extreme(self):
        """ in future could get the information from values in db """
        return self.me.agg_min_extreme

    def get_exclusion(self, type_intrument_id):
        """ retourne la premiere exclusion active pour le type instrument """
        for anExclu in self.exclus:
            if anExclu['type_instrument'] == type_intrument_id:
                return anExclu['value']
        return {}

    def get_date_fuseau(self, dt: datetime) -> datetime:
        """ retoune la datetime fuseau de la station """
        return dt + datetime.timedelta(hours=self.fuseau)

    def round_datetime_per_aggregation(dt: datetime, niveau_agg: str, delta: int = 0):
        """ round_datetime_per_aggregation

            arrondi la date, suivant le niveau d'agreggation.
            delta ajoute un nombre de heure/jour/... au resultat
            
            l'heure dans l'agregation heure est l'heure UTC

            les heures dans les agregations superieures sont calculees a partir de l'heure fuseau
        """
        try:
            if niveau_agg == "H":
                return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(hours=delta)
            elif niveau_agg == "D":
                return datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(days=delta)
            elif niveau_agg == "M":
                return datetime.datetime(dt.year, dt.month, 1, 0, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(months=delta)
            elif niveau_agg == "Y":
                return datetime.datetime(dt.year, 1, 1, 0, 0, 0, 0, datetime.timezone.utc) + datetime.timedelta(years=delta)
            elif niveau_agg == "A":
                return datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
            else:
                raise Exception("round_datetime_per_aggregation", "wrong niveau_agg: " + niveau_agg)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def get_agg(self, my_datetime_utc):
        """
        get_agg

        my_datetime_utc: date en UTC.

        return an array of aggregation to be used by our process_xxx methods
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
                tmp_dt = round_datetime_per_aggregation(my_datetime_utc, agg_niveau)
                agg_object = get_agg_object(agg_niveau)
                if agg_object.objects.filter(poste_id_id=self.me.id).filter(dat=tmp_dt).exists():
                    ret.append(agg_object.objects.filter(poste_id_id=self.me.id).filter(dat=tmp_dt).first)
                else:
                    new_val = agg_object(poste_id=self.me, dat=tmp_dt, last_rec_dat=tmp_dt, duration=0)
                    new_val.save()
                    ret.append(new_val)

            # get aggregation of day - 1 for measures that will aggregate yesteray
            tmp_dt = round_datetime_per_aggregation(my_datetime_utc, 'D', -1)
            ret.append(Agg_day.objects.filter(poste_id_id=self.me.id).filter(dat=tmp_dt).first)

            # get aggregation of day + 1 for measures that will aggregate the day after
            tmp_dt = round_datetime_per_aggregation(my_datetime_utc, 'D', +1)
            ret.append(Agg_day.objects.filter(poste_id_id=self.me.id).filter(dat=tmp_dt).first)
            return ret
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def get_obs(self, my_datetime_utc):
        """get or create an observation at a given datetime"""
        # todo : check that my_datetime_utc > previous dat + duration pour le poste_id
        # todo: put a warning somewhere if my_datetime_utc > previous dat+duration
        # todo: what is happening if the date given is at the middle of an existing period ?
        try:
            if Observation.objects.filter(poste_id_id=self.me.id).filter(dat=my_datetime_utc).exists():
                return Observation.objects.filter(poste_id_id=self.me.id).filter(dat=my_datetime_utc).first
            new_obs = Observation(poste_id=self.me, dat=my_datetime_utc, last_rec_dat=my_datetime_utc, duration=0)
            new_obs.save()
            return new_obs
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "poste id: " + str(self.me.id) + ", meteor: " + self.me.meteor
