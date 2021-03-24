from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeInterieur(RootTypeInstrument):
    """Type Interieur"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 7

        self.measures = [
            {'type_i': 7, 'src_key': 'in_temp', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
            {'type_i': 7, 'src_key': 'in_humidity', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
        ]
        super()
