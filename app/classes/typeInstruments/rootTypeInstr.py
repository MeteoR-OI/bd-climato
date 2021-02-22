from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.typeInstrumentMeteor import TypeInstrumentMeteor
from app.classes.calcul.processMeasure import ProcessMeasure
import json


class RootTypeInstrument:
    """ typeInstrument root object"""

    def __init(self):
        tmpI = TypeInstrumentMeteor(self.my_type_instr_id)
        self.type_instrument = tmpI.data
        self.process_json = ProcessMeasure()

    def mapping(self):
        """return current mapping"""
        return self.mapping

    def process_json(self, poste_meteor: PosteMetier, measures: json, measure_idx: int, obs_meteor: ObsMeteor, agg_Array: json, flag: bool) -> json:
        """
            process_json
        """
        try:
            for amesure in self.mesures:
                process_obj = self.getProcessObject(amesure['agg'])
                # begin ttx
                process_obj.process_json.update_obs_and_get_delta(
                    poste_meteor,
                    amesure,
                    measures,
                    measure_idx,
                    obs_meteor,
                    flag)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
