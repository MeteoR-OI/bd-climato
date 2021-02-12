from app.models import Poste, Observation, Agg_hour, Agg_day, Agg_month, Agg_year, Agg_global, Exclusion, TypeInstrument   #

from app.classes.typeInstruments import typeTemp
import json

# from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object

# Tous les types connus, et le nom de la classe qui l'implemente
mapping = [
    {'type_id': 1, 'name': 'Temp', 'object': typeTemp()},
]

# modif
class all_instruments_meteor:
    """Objet climato type_instrument """

    # def __init(self):

    def get(self, type_instrument_id):
        """ get TypeInstrument object """
        for aType in self.mapping:
            if aType['type_id'] == type_instrument_id:
                return aType.object
        raise Exception("all_instrument_meteor.get", "invalid type_instrument_id: " + str(type_instrument_id))

    def process_observation(self, json_obs: json, obs_dataset: Observation, flag: bool):
        """process observation data for all our TypeInstrument"""
        for aType in self.mapping:
            aType['objects'].process_observation(json_obs, obs_dataset, flag)

    def process_aggregation(self, json_obs: json, agg_all_dataset, flag: bool):
        """process aggregation data for all our TypeInstrument"""
        for aType in self.mapping:
            aType['objects'].process_aggregation(json_obs, agg_all_dataset, flag)

    def process_extreme(self, json_obs: json, agg_all_dataset, flag: bool):
        """process aggregation data for all our TypeInstrument"""
        for aType in self.mapping:
            aType['objects'].process_extreme(json_obs, agg_all_dataset, flag)

    def __str__(self):
        """print myself"""
        return "Type_instrument count: " + str(self.mapping.__len__())
