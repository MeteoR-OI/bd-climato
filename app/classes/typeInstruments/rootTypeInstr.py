from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.typeInstrumentMeteor import TypeInstrumentMeteor
from app.classes.calcul.processMeasure import ProcessMeasure
from app.classes.measures.measureAvg import MeasureAvg
import json


class RootTypeInstrument:
    """ typeInstrument root object"""
    all_calculus = [
        {"agg": "avg", "object": MeasureAvg()},
        {"agg": "no", "object": None},
        {"agg": "sum", "object": None},    # MeasureSum()}
        {"agg": "rate", "object": None}   # MeasureRate()}
    ]

    def __init(self):
        tmpI = TypeInstrumentMeteor(self.my_type_instr_id)
        self.type_instrument = tmpI.data
        self.processJson = ProcessMeasure()

    def mapping(self):
        """return current mapping"""
        return self.mapping

    def processJson(self, poste_metier: PosteMetier, measures: json, obs_meteor: ObsMeteor, agg_Array: json, flag: bool) -> json:
        """
            process_json
        """
        try:
            result = []
            # for all measures
            for my_measure in self.mesures:
                # find the calculus object for my_mesure
                for a_calculus in self.all_calculus:
                    if a_calculus['agg'] == my_measure['agg']:
                        # for all data element in our json
                        idx = 0
                        while idx < measures.data.__len__():
                            if a_calculus['object'] is not None:
                                delta_values = a_calculus['object'].updateObsAndGetDelta(poste_metier, my_measure, measures, idx, obs_meteor, flag)
                                result.append(delta_values)
                            # todo call agg calculus
            return result

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
