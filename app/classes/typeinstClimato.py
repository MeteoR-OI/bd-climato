from app.models import TypeInstrument   #
# from app.tools.agg_tools import round_datetime_per_aggregation, get_agg_object

# Tous les types connus, et le nom de la classe qui l'implemente
INSTRUMENT_CODED = (
    (1, "type_rain")
)

class type_instrument_meteor:
    """Objet climato type_instrument """

    all = []    # all is global to all instances

    def __init(self, type_instrument_id):
        """ this is only for test """
        print("type_instrument_meteor(n) was called.... only available for testing !!!")
        if TypeInstrument.objects.filter(id=type_instrument_id).exists():
            self.me = TypeInstrument.objects.get(id=type_instrument_id)
            INSTRUMENT_CODED.__getitem__(1)
        else:
            raise Exception("type_instrument.__init", "type inconnu: " + str(type_instrument_id))

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
        if TypeInstrument.objects.filter(id=type_instrument_id).exists():
            tmp_instr.me = TypeInstrument.objects.get(id=type_instrument_id)
        else:
            raise Exception("type_instrument.get_cached", "type inconnu: " + str(type_instrument_id))
        tmp_instr.all.append(tmp_instr)
        return tmp_instr

    def process_observation(self, json_obs, obs_dataset, flag):
        """process observation data into obs_dataset. flag is True for insert, False for delete"""

    def process_aggregation(self, json_obs, agg_all_dataset, flag):
        """process observation data into al aggregation dataset. flag is True for insert, False for delete"""

    def __str__(self):
        """print myself"""
        return "Type_instrument id: " + str(self.me.id) + ", meteor: " + self.me.name
