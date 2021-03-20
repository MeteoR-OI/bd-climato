from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeTemp(RootTypeInstrument):
    """Type Temp"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 1

        self.mesures = [
            {'type_i': 1, 'src_key': 'out_temp', 'dataType': float, 'agg': 'avg', 'avg': True, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
            {'type_i': 1, 'src_key': 'out_temp', 'dataType': float, 'agg': 'avgomm', 'avg': True, 'min': True, 'max': True, 'hour_deca': 7, 'special': 16},
            {'type_i': 1, 'src_key': 'windchill', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 0},
            {'type_i': 1, 'src_key': 'heatindex', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 0},
            {'type_i': 1, 'src_key': 'dewpoint', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
            {'type_i': 1, 'src_key': 'soiltemp', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': True, 'max': False, 'hour_deca': 0, 'special': 0}
        ]
        super()
