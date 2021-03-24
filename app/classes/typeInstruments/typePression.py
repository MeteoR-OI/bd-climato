from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypePression(RootTypeInstrument):
    """Type Pression"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 3

        self.measures = [
            {'type_i': 3, 'src_key': 'barometer', 'dataType': float, 'agg': 'avg', 'avg': True, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
            {'type_i': 3, 'src_key': 'barometer', 'dataType': float, 'agg': 'avgomm', 'avg': True, 'min': False, 'max': False, 'hour_deca': 7, 'special': 48},
            {'type_i': 3, 'src_key': 'pressure', 'dataType': float, 'agg': 'no', 'avg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 0},
        ]
        super()
