from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeHumidity(RootTypeInstrument):
    """Type Humidity"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 2

        self.measures = [
            {'type_i': 2, 'src_key': 'humidity', 'dataType': int, 'agg': 'avg'},
            {'type_i': 2, 'src_key': 'humidity', 'dataType': int, 'agg': 'avgomm'}
        ]
        super().__init__()
