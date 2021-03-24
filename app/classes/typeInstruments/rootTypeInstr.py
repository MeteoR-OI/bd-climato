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
# agg: Type aggregation: avg, avgomm, rate
#   avg: classic average
#   avgomm: classic average, but use the last measure of the hour as the value for the full hour
#   rate: same as avg, only differ in max/min calculation
# avg -> compute "field"_sum, "field"_duration, et si besoin "field"_avg
#        field_sum is value * duration
#        if MeasureIsSum is set, then field_sum is the value of the measure
# calcAvg: Optionnel, defaut=True, can we compute avg if not given in aggregation json
#    calcAvg=False -> use only data coming from json file
#    calcAvg=True  -> use in first data coming from json file, if not present use the current value of the measure
# max -> compute max. Default is False
# min -> compute min. Default is False
#    computation:
#       load measure_value from json
#       Overload with "field"_max/min in json/current
#       Overload with json/aggregations."field"_max/min
#       take this value, and compare with current max/min in agregation. Replace if it is better
# hour_deca -> Hours substracted/added to the time of the measure when computing the hour aggregation datetime
# special: special processing:
#   Standard(0) : no specific processing
#   MeasureIsSum(1) : Measure is a sum (no need to multiplu by duration)
#   MeasureIsWind(2) : Measure is wind (need to save the xxx_dir)
#   OnlyAggregateInHour(4)
#   NoAvgField(8) : Compute xx_sum and xx_duration but not xxx_avg
#   MeasureIsOmm(16) : This flag is set by the app when agg == 'ommAvg', no need to use it


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

    def __str__(self):
        return "TypeInstrument, id: " + str(self.my_type_instr_id)
