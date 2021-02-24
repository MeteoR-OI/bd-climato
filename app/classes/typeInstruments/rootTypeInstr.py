from app.classes.metier.posteMetier import PosteMetier
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.typeInstrumentMeteor import TypeInstrumentMeteor
from app.classes.calcul.avgCompute import avgCompute
import json


class RootTypeInstrument:
    """ typeInstrument root object"""
    all_calculus = [
        {"agg": "avg", "object": avgCompute()},
        {"agg": "no", "object": None},
        {"agg": "sum", "object": None},    # sumCompute()}
        {"agg": "rate", "object": None}    # rateCompute()}
    ]

    def __init(self):
        tmpI = TypeInstrumentMeteor(self.my_type_instr_id)
        self.type_instrument = tmpI.data

    def mapping(self):
        """return current mapping"""
        return self.mapping

    def processJson(self, poste_metier: PosteMetier, measures: json, measure_idx: int, obs_meteor: ObsMeteor, agg_array: json, delta_values: json, flag: bool) -> json:
        """
            processJson
        """
        try:
            # for all measures
            for my_measure in self.mesures:
                # find the calculus object for my_mesure
                for a_calculus in self.all_calculus:
                    if a_calculus['agg'] == my_measure['agg']:
                        if a_calculus['object'] is not None:
                            # load our json in obs row
                            a_calculus['object'].updateObsAndGetDelta(poste_metier, my_measure, measures, measure_idx, obs_meteor, delta_values, flag)
                            # load our json in all aggregation rows
                            xtreme_values = a_calculus['object'].updateAggAndGetDeltaVal(poste_metier, my_measure, measures, measure_idx, agg_array, delta_values, flag)

                            # process xtremes
                        # todo call agg calculus
            return delta_values

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        return "TypeInstrument, id: " + str(self.my_type_instr_id)
