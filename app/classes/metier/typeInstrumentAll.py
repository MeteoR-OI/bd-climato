from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.metier.posteMetier import PosteMetier
from app.classes.typeInstruments import rootTypeInstr, typeTemp, typeHumidity, typePression, typeRain, typeWind, typeSolar, typeInterieur, typeDivers
import json


class TypeInstrumentAll():
    """
        TypeInstrumentRepository

        Objet climato type_instrument
    """

    # Tous les types connus, et le nom de la classe qui l'implemente
    all_instruments = [
        {'type_id': 1, 'name': 'Temp', 'object': typeTemp},
        {'type_id': 2, 'name': 'Humidity', 'object': typeHumidity},
        {'type_id': 3, 'name': 'Pression', 'object': typePression},
        {'type_id': 4, 'name': 'Rain', 'object': typeRain},
        {'type_id': 5, 'name': 'Wind', 'object': typeWind},
        {'type_id': 6, 'name': 'Solar', 'object': typeSolar},
        {'type_id': 7, 'name': 'Interieur', 'object': typeInterieur},
        {'type_id': 9, 'name': 'Divers', 'object': typeDivers},
    ]

    def get(self, type_instrument_id: int) -> rootTypeInstr:
        """ get TypeInstrument object """
        for atype in self.all_instruments:
            if atype['type_id'] == type_instrument_id:
                return atype.object
        raise Exception("all_instrument_meteor.get", "invalid type_instrument_id: " + str(type_instrument_id))

    def process_json(self, poste_metier: PosteMetier, measures: json, obs_meteor: ObsMeteor, agg_array: json, flag: bool) -> json:
        """process observation data for all our TypeInstrument"""
        try:
            result = []
            # for all type_instruments
            for an_intrument in self.all_instruments:
                delta_values = an_intrument['object']().processJson(poste_metier, measures, obs_meteor, agg_array, flag)
                result.append(delta_values)
            return result

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        """print myself"""
        return "TypeInstrumentAll count: " + str(self.all_instruments.__len__())
