from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeRain(RootTypeInstrument):
    """Type Rain"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 4

        self.measures = [
            {'type_i': 4, 'src_key': 'rain', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 1},
            {'type_i': 4, 'src_key': 'rain', 'dataType': float, 'agg': 'avgomm', 'avg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 17},
            {'type_i': 4, 'src_key': 'rain_rate', 'dataType': float, 'agg': 'rate', 'avg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 0},
        ]
        super()
