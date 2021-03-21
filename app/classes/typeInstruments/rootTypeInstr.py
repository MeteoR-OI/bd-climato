from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.typeInstrumentMeteor import TypeInstrumentMeteor
from app.classes.calcul.avgCompute import AvgCompute
from app.classes.calcul.avgOmmCompute import AvgOmmCompute
from app.classes.calcul.rateCompute import RateCompute
import json

# ---------------------
# Measure Definitions -
# ---------------------
# type_i : type_instrument_id
# src_key: key string in measures json (coming from the station)
# target_key: json key name only if different. Used in obs and all aggregations
# agg: Type aggregation: avg, ommAvg, rate
# avg -> compute "field"_sum, "field"_duration, et si besoin "field"_avg
#        field_sum is value * duration if MeasureIsSum is not set
# calcAvg: Optionnel, defaut=True, can we compute avg if not given in aggregation json
# max -> load "field"_max & "field"_max_time from json. if null -> will be computed in aggregation
# min -> load "field"_min & "field"_min_time from json. if null -> will be computed in aggregation
# hour_deca -> Hours substracted/added to the time of the measure when computing the hour aggregation datetime
# special: special processing:
#   Standard(0) : no specific processing
#   MeasureIsSum(1) : Measure is a sum (no need to multiplu by duration)
#   MeasureIsWind(2) : Measure is wind (need to save the xxx_dir)
#   OnlyAggregateInHour(4)
#   NoAvgField(8) : Compute xx_sum and xx_duration but not xxx_avg
#   MeasureIsOmm(16) : This flag is set when agg == 'ommAvg', no need to use it


class RootTypeInstrument:
    """ typeInstrument root object"""
    all_calculus = [
        {"agg": "avg", "object": AvgCompute()},
        {"agg": "avgomm", "object": AvgOmmCompute()},
        # {"agg": "no", "object": None},
        # {"agg": "sum", "object": None},    # sumCompute()}
        {"agg": "rate", "object": RateCompute()}    # rateCompute()}
    ]

    def __init(self):
        tmpI = TypeInstrumentMeteor(self.my_type_instr_id)
        self.type_instrument = tmpI.data

    def mapping(self):
        """return current mapping"""
        return self.mapping

    def processJson(
        self,
        poste_metier,
        measures: json,
        measure_idx: int,
        obs_meteor: ObsMeteor,
        agg_array: json,
        delta_values: json,
        trace_flag: bool = False,
    ) -> json:
        """
            processJson
        """
        try:
            # for all measures
            for my_measure in self.measures:
                # find the calculus object for my_mesure
                for a_calculus in self.all_calculus:
                    if a_calculus['agg'] == my_measure['agg']:
                        if a_calculus['object'] is not None:
                            # load our json in obs row
                            a_calculus['object'].processObservation(poste_metier, my_measure, measures, measure_idx, obs_meteor, delta_values, trace_flag)
                            # load our json in all aggregation rows
                            a_calculus['object'].processAggregations(poste_metier, my_measure, measures, measure_idx, agg_array, delta_values, trace_flag)
                            # process xtremes
                            # todo call agg calculus
                        break
            return

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,

    def __str__(self):
        return "TypeInstrument, id: " + str(self.my_type_instr_id)
