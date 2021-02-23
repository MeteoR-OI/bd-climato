from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.typeInstrumentMeteor import TypeInstrumentMeteor
from app.classes.calcul.processMeasure import ProcessMeasure
from app.classes.metier.processAll import ProcessAll
import json


class RootTypeInstrument:
    """ typeInstrument root object"""

    def __init(self):
        tmpI = TypeInstrumentMeteor(self.my_type_instr_id)
        self.type_instrument = tmpI.data
        self.processJson = ProcessMeasure()

    def mapping(self):
        """return current mapping"""
        return self.mapping

    def processJson(self, poste_meteor: PosteMetier, measures: json, measure_idx: int, obs_meteor: ObsMeteor, agg_Array: json, flag: bool) -> json:
        """
            process_json
        """
        try:
            for amesure in self.mesures:
                process_obj = ProcessAll().get(amesure['agg'])
                # begin ttx
                process_obj.updateObsAndGetDelta(
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
