from app.classes.obsMeteor import ObsMeteor
from app.classes.posteMeteor import PosteMeteor
from app.classes.aggMeteor import AggMeteor
from app.classes.typeInstruments import rootTypeInstr, typeTemp

import json

# from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object

# Tous les types connus, et le nom de la classe qui l'implemente
all_instruments = [
    {'type_id': 1, 'name': 'Temp', 'object': typeTemp()},
]


class TypeInstrumentRepository():
    """
        TypeInstrumentRepository
    
        Objet climato type_instrument
    """

    # def __init(self):

    def get(self, type_instrument_id: int) -> rootTypeInstr:
        """ get TypeInstrument object """
        for atype in self.all_instruments:
            if atype['type_id'] == type_instrument_id:
                return atype.object
        raise Exception("all_instrument_meteor.get", "invalid type_instrument_id: " + str(type_instrument_id))

    def process_json(self, poste_meteor: PosteMeteor, measures: json, measure_idx: int, obs_meteor: ObsMeteor, agg_array: json, flag: bool) -> json:
        """process observation data for all our TypeInstrument"""
        try:
            for an_intrument in self.all_instruments:
                an_intrument['objects'].process_json(poste_meteor, measures, measure_idx, obs_meteor, agg_array, flag)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "Type_instrument count: " + str(self.all_instruments.__len__())
