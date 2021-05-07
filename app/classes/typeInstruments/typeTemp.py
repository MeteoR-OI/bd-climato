from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeTemp(RootTypeInstrument):
    """Type Temp"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 1

        self.measures = [
            {'type_i': 1, 'src_key': 'out_temp', 'agg': 'avg'},
            {'type_i': 1, 'src_key': 'out_temp', 'agg': 'avgomm', 'measureType': 'inst', 'deca_min': -5, 'deca_max': 7},
            {'type_i': 1, 'src_key': 'out_temp2', 'agg': 'sum'},
            {'type_i': 1, 'src_key': 'windchill', 'agg': 'no', 'max': False},
            {'type_i': 1, 'src_key': 'heatindex', 'agg': 'no', 'min': False},
            {'type_i': 1, 'src_key': 'dewpoint', 'agg': 'no'},
            {'type_i': 1, 'src_key': 'soiltemp', 'agg': 'no', 'max': False}
        ]
        super().__init__()
