from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #
from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object
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

    def convert_relative_hour(self, mesure_dt: datetime, hour_deca: int):
        """retourne le numero de l'heure relative pour une certaine mesure (hour_deca est une propriete de la mesure)"""
        local_delta_hour = hour_deca
        if hour_deca <= 0:
            return mesure_dt.datetime.hour - hour_deca
        elif hour_deca == 99:
            hour_deca = 0
        # todo
        # transform time to TU time
        # return hour + hour_deca
        return local_delta_hour

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

    def get_agg(self, my_datetime):
        """return an array of aggregation per hour/day/month/year/all for the given datetime. create them if needed"""
        try:
            ret = []
            for agg_niveau in ['H', 'D', 'M', 'Y', 'A']:
                tmp_dt = round_datetime_per_aggregation(my_datetime, agg_niveau)
                agg_object = get_agg_object(agg_niveau)
                if agg_object.objects.filter(poste_id_id=self.me.id).filter(dat=tmp_dt).exists():
                    ret.append(agg_object.objects.filter(poste_id_id=self.me.id).filter(dat=tmp_dt).first)
                else:
                    new_val = agg_object(poste_id=self.me, dat=tmp_dt, last_rec_dat=tmp_dt, duration=0)
                    new_val.save()
                    ret.append(new_val)
            return ret
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def get_obs(self, my_datetime):
        """get or create an observation at a given datetime"""
        # todo : check that my_datetime > previous dat + duration pour le poste_id
        # todo: put a warning somewhere if my_datetime > previous dat+duration
        try:
            if Observation.objects.filter(poste_id_id=self.me.id).filter(dat=my_datetime).exists():
                return Observation.objects.filter(poste_id_id=self.me.id).filter(dat=my_datetime).first
            new_obs = Observation(poste_id=self.me, dat=my_datetime, last_rec_dat=my_datetime, duration=0)
            new_obs.save()
            return new_obs
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "poste id: " + str(self.me.id) + ", meteor: " + self.me.meteor
