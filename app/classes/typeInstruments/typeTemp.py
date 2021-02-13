from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeTemp(RootTypeInstrument):
    """Type Temp"""
    def __init(self):
        # type_instrument_id
        self.my_type_instr_id = 1

        self.mapping = [
            # key: key string in json
            # field: db column name
            # avg -> compute "field"_sum, "field"_duration, et si besoin "field"_avg
            # max -> load "field"_max & "field"_max_time from json. if null -> will be computed in aggregation
            # min -> load "field"_min & "field"_min_time from json. if null -> will be computed in aggregation
            # hour_deca -> heure de debut d'agregation jour :
            #                                     99 -> local (utilise le timezone de la station),
            #                                      0 -> TU
            #                                      n -> decallage de n heures par rapport a heure locale
            #                                     -n -> decalage de n heures par rapport a heure GMT
            # special: special processing (like "field"_dir)
            {'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
            {'key': 'temp_out', 'field': 'temp_out_non_gmt', 'avg': True, 'min': True, 'max': True, 'hour_deca': 7, 'special': 0},
            {'key': 'windchill', 'field': 'windchill', 'avg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 0},
            {'key': 'heatindex', 'field': 'heatindex', 'avg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 0},
            {'key': 'dewpoint', 'field': 'dewpoint', 'avg': False, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
            {'key': 'soilTemp', 'field': 'soil_temp', 'avg': False, 'min': True, 'max': False, 'hour_deca': 0, 'special': 0}
        ]
