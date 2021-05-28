from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeRain(RootTypeInstrument):
    """Type Rain"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 4

        self.measures = [
            {'type_i': 4, 'src_key': 'rain', 'target_key': 'rain', 'agg': 'sum', 'measureType': 'inst', 'min': False, 'max': False},
            {'type_i': 4, 'src_key': 'rain', 'agg': 'sumomm', 'measureType': 'inst', 'min': False, 'hour_deca': 7},
            {'type_i': 4, 'src_key': 'rain_rate', 'agg': 'rate', 'measureType': 'inst', 'min': False},
        ]
        super().__init__()
