from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeInterieur(RootTypeInstrument):
    """Type Interieur"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 7

        self.measures = [
            {'type_i': 7, 'src_key': 'in_temp', 'agg': 'avg', 'min': False, 'max': False},
            {'type_i': 7, 'src_key': 'in_humidity', 'agg': 'avg', 'min': False, 'max': False},
        ]
        super().__init__()
