from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeDivers(RootTypeInstrument):
    """Type Divers"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 9

        self.measures = [
            {'type_i': 9, 'src_key': 'rx',      'agg': 'avg'},
            {'type_i': 9, 'src_key': 'voltage', 'agg': 'avg'},
        ]
        super().__init__()
