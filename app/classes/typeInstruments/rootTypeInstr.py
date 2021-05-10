from app.classes.repository.typeInstrumentMeteor import TypeInstrumentMeteor
from app.tools.climConstant import MeasureProcessingBitMask

# --------------------------------------
# Measure Definitions & default values -
# --------------------------------------
# type_i : type_instrument_id

# src_key: key string in measures json (coming from the station)

# syno: list of accepted synonyms
#     M_sum is automatically added for sum type of aggregation
#     M_rate ...

# target_key: json key name only if different. Used in obs and all aggregations
#      M_omm is used for omm measure, when no target is defined

# measureType: default = both
#   avg -> only use the average value ([field]_avg)
#   inst -> only use the instantaneous value ie [field]

# agg: Type aggregation: avg, avgomm, rate
#   avg: classic average (sum(value * duration)/duration)
#   avgomm: classic average, but use the last measure of the hour as the value for the full hour
#   sum : only sum up the value
#   sumomm: omm value based on a sum
#   rate: same as avg, only differ in max/min calculation
#   no : no aggregation, only process max/min
#   there is no rateomm, neither noomm. if there is a need, just ask

# calcAvg: Optionnel, defaut=True, can we compute avg if not given in aggregation json
#    calcAvg=False -> use only data coming from json file
#    calcAvg=True  -> use in first data coming from json file, if not present use the current value of the measure

# max -> compute max. Default is True

# min -> compute min. Default is True

# hour_deca -> Hours substracted/added to the time of the measure when computing the hour aggregation datetime (default is 0)

# deca_min -> Hours substracted/added to the time for the processing of min values (default is hour_deca)

# deca_max -> Hours substracted/added to the time for the processing of max values (default is hour_deca)

# special: special processing:
#   MeasureIsWind(1) : Measure is wind (need to save the xxx_dir)
#   OnlyAggregateInHour: calculus will be limited to agg_hour
#   NotAllowedInCurrent: the value can only be specified in aggregations/validation key


class RootTypeInstrument:
    def __init__(self):
        tmpI = TypeInstrumentMeteor(self.my_type_instr_id)
        self.type_instrument = tmpI.data
        # force some default parameters
        for a_measure in self.measures:
            if a_measure.get('agg') is None:
                raise Exception('RootTypeInstrument', 'no <agg> key defined for ' + a_measure.get('src_key'))
            for default_param in [('special', 0), ('hour_deca', 0), ('calcAvg', True), ('max', True), ('min', True), ('dataType', float), ('measureType', 'both')]:
                if a_measure.get(default_param[0]) is None:
                    a_measure[default_param[0]] = default_param[1]

            # # add combo target_key first
            # if 'sumomm' in str(a_measure['agg']):
            #     if a_measure.get('target_key') is None:
            #         a_measure['target_key'] = a_measure['src_key'] + '_sum_omm'

            # mark the measure when it is an omm measure
            if 'omm' in str(a_measure['agg']):
                a_measure['special'] |= MeasureProcessingBitMask.MeasureIsOmm
                a_measure['measure_type'] = 'inst'
                if a_measure.get('target_key') is None:
                    a_measure['target_key'] = a_measure['src_key'] + '_omm'

            # add _rate suffix for sum type of aggregation
            if 'rate' in str(a_measure['agg']):
                rate_key = a_measure['src_key'] + '_rate'
                if '_rate_rate' in rate_key:
                    rate_key = a_measure['src_key']
                if a_measure.get('syno') is None:
                    a_measure['syno'] = []
                if rate_key in a_measure['syno'] is False:
                    a_measure['syno'].append(rate_key)
                if a_measure.get('target_key') is None:
                    a_measure['target_key'] = a_measure['src_key']
                a_measure['agg'] = str(a_measure['agg']).replace('rate', 'avg')

            # add _sum suffix for sum type of aggregation
            if 'sum' in str(a_measure['agg']):
                sum_key = a_measure['src_key'] + '_sum'
                if '_sum_sum' in sum_key:
                    sum_key = a_measure['src_key']
                if a_measure.get('syno') is None:
                    a_measure['syno'] = []
                if (sum_key in a_measure['syno']) is False:
                    a_measure['syno'].append(sum_key)
                if a_measure.get('target_key') is None:
                    a_measure['target_key'] = a_measure['src_key']

            for default_param in [('deca_max', a_measure['hour_deca']), ('deca_max', a_measure['hour_deca']), ('target_key', a_measure['src_key'])]:
                if a_measure.get(default_param[0]) is None:
                    a_measure[default_param[0]] = default_param[1]

    def get_all_measures(self):
        # iterator
        for a_measure in self.measures:
            yield a_measure

    def __str__(self):
        return "TypeInstrument, id: " + str(self.my_type_instr_id)
