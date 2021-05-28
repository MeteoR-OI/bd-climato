from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypePression(RootTypeInstrument):
    """Type Pression"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 3

        self.measures = [
            {'type_i': 3, 'src_key': 'barometer', 'agg': 'avg'},
            {'type_i': 3, 'src_key': 'barometer', 'agg': 'avgomm'},
            {'type_i': 3, 'src_key': 'pressure', 'agg': 'no'},
        ]
        super().__init__()
