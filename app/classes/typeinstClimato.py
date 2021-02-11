from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #

from app.classes.typeInstruments import type_rain
import json

# from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object

# Tous les types connus, et le nom de la classe qui l'implemente
mapping = [
    {'type_id': 1, 'object': type_rain()},
]


class type_instrument_meteor:
    """Objet climato type_instrument """

    all = []    # all is global to all instances

    def __init(self, type_instrument_id):
        """ this is only for test """
        print("type_instrument_meteor(n) was called.... only available for testing !!!")
        if INSTRUMENT_CODED.__contains__(type_instrument_id) is False:
            raise Exception("type_instrument.__init", "type non supported: " + str(type_instrument_id))

        self.me = TypeInstrument.objects.get(id=type_instrument_id)
        self.obj = globals()['typeInstruments.' + INSTRUMENT_CODED.__getitem__(1)]

    def __del__(self):
        """destructor need to clean up all list"""
        for one_instr in self.all:
            if one_instr.me.id == self.me.id:
                self.all.remove(one_instr)

    @staticmethod
    def get_cached(type_instrument_id):
        """manage a singleton per type_instrument instance"""
        tmp_instr = type_instrument_meteor()
        for one_instr in tmp_instr.all:
            if one_instr.me.id == type_instrument_id:
                return one_instr

        if INSTRUMENT_CODED.__contains__(type_instrument_id) is False:
            raise Exception("type_instrument.__init", "type non supported: " + str(type_instrument_id))

        tmp_instr.me = TypeInstrument.objects.get(id=type_instrument_id)
        tmp_instr.obj = INSTRUMENT_CODED.__getitem__(type_instrument_id)]
        return tmp_instr

    def process_observation(self, json_obs: json, obs_dataset: Observation, flag: bool):
        """process observation data into obs_dataset. flag is True for insert, False for delete"""
        return self.obj.process_observation(json_obs, self.me, obs_dataset, flag)

    def process_aggregation(self, json_obs: json, agg_all_dataset, flag: bool):
        """process observation data into al aggregation dataset. flag is True for insert, False for delete"""
        return self.obj.process_aggregation(json_obs, self.me, agg_all_dataset, flag)

    def __str__(self):
        """print myself"""
        return "Type_instrument id: " + str(self.me.id) + ", meteor: " + self.me.name
