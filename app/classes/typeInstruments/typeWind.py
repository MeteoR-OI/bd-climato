from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeWind(RootTypeInstrument):
    """Type Wind"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 5

        self.measures = [
            {'type_i': 5, 'src_key': 'wind_i', 'dataType': float, 'agg': 'avg', 'avg': True, 'calcAvg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 2},
            {'type_i': 5, 'src_key': 'wind', 'dataType': float, 'agg': 'avg', 'avg': True, 'calcAvg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 2},
            {'type_i': 5, 'src_key': 'win10', 'dataType': float, 'agg': 'avg', 'avg': True, 'calcAvg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 2},
        ]
        super()
