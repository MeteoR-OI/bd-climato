from app.classes.typeInstruments.typeTemp import TypeTemp
from app.classes.typeInstruments.typeHumidity import TypeHumidity
from app.classes.typeInstruments.typePression import TypePression
from app.classes.typeInstruments.typeRain import TypeRain
from app.classes.typeInstruments.typeWind import TypeWind
from app.classes.typeInstruments.typeSolar import TypeSolar
from app.classes.typeInstruments.typeInterieur import TypeInterieur
from app.classes.typeInstruments.typeDivers import TypeDivers


class AllTypeInstruments():
    """
        AllTypeInstruments

        Repository of all our typeInstruments
    """

    def __init__(self):
        # Tous les types connus, et le nom de la classe qui l'implemente
        self.all_instruments = [
            {'type_id': 1, 'name': 'Temp', 'object': TypeTemp()},
            {'type_id': 2, 'name': 'Humidity', 'object': TypeHumidity()},
            {'type_id': 3, 'name': 'Pression', 'object': TypePression()},
            {'type_id': 4, 'name': 'Rain', 'object': TypeRain()},
            {'type_id': 5, 'name': 'Wind', 'object': TypeWind()},
            {'type_id': 6, 'name': 'Solar', 'object': TypeSolar()},
            {'type_id': 7, 'name': 'Interieur', 'object': TypeInterieur()},
            {'type_id': 9, 'name': 'Divers', 'object': TypeDivers()},
        ]

    def get(self, type_instrument_id: int):
        """ get TypeInstrument object """
        for atype in self.all_instruments:
            if atype['type_id'] == type_instrument_id:
                return atype['object']
        raise Exception("all_instrument_meteor.get", "invalid type_instrument_id: " + str(type_instrument_id))

    def get_all_instruments(self):
        # iterator
        for an_instrument in self.all_instruments:
            yield an_instrument

    def __str__(self):
        """print myself"""
        return "TypeInstrumentAll count: " + str(self.all_instruments.__len__())
