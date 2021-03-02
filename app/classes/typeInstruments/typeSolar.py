from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeSolar(RootTypeInstrument):
    """Type Solar"""

    def __init__(self):
        try:
            # type_instrument_id
            self.my_type_instr_id = 6

            self.mesures = [
                # type_i : type_instrument_id
                # key: key string in json
                # field: db column name only if different. No value -> use key name
                # agg: Type aggregation: avg, ommAvg, rate, sun, no
                # avg -> compute "field"_sum, "field"_duration, et si besoin "field"_avg
                # max -> load "field"_max & "field"_max_time from json. if null -> will be computed in aggregation
                # min -> load "field"_min & "field"_min_time from json. if null -> will be computed in aggregation
                # hour_deca -> heure de debut d'agregation jour :
                #                                     99 -> local (utilise le timezone de la station),
                #                                      0 -> TU
                #                                      n -> decallage de n heures par rapport a heure locale
                #                                     -n -> decalage de n heures par rapport a heure GMT
                # special: special processing (like "field"_dir)
                {'type_i': 6, 'src_key': 'uv_indice', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 0},
                {'type_i': 6, 'src_key': 'radiation', 'dataType': float, 'agg': 'avg', 'avg': True, 'min': False, 'max': True, 'hour_deca': 0, 'special': 16},
                {'type_i': 6, 'src_key': 'etp', 'dataType': float, 'agg': 'sum', 'avg': False, 'min': True, 'max': False, 'hour_deca': 0, 'special': 1 + 8}
            ]
            super()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
