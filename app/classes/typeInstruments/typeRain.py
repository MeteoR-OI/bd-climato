from rootTypeInstr import root_type_instr


class type_rain(root_type_instr):

    def __init(self):
        self.mapping = [
            # key: key string in json
            # field: db column name
            # avg -> compute "field"_sum, "field"_duration, et si besoin "field"_avg
            # max -> load "field"_max & "field"_max_time from json. if null -> will be computed in aggregation
            # min -> load "field"_min & "field"_min_time from json. if null -> will be computed in aggregation
            # special: special processing (like "field"_dir)
            {'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'special': 0},
            {'key': 'windchill', 'field': 'windchill', 'avg': False, 'min': False, 'max': False, 'special': 0},
            {'key': 'heatindex', 'field': 'heatindex', 'avg': False, 'min': False, 'max': True, 'special': 0},
            {'key': 'dewpoint', 'field': 'dewpoint', 'avg': False, 'min': True, 'max': True, 'special': 0},
            {'key': 'soiTemp', 'field': 'soil_temp', 'avg': False, 'min': True, 'max': False, 'special': 0}
        ]
