from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeHumidity(RootTypeInstrument):
    """Type Humidity"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 2

        self.measures = [
            {'type_i': 2, 'src_key': 'humidity', 'dataType': int, 'agg': 'avg', 'avg': True, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
        ]
        super()
