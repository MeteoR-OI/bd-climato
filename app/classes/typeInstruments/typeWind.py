from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeWind(RootTypeInstrument):
    """Type Wind"""

    def __init__(self):
        try:
            # type_instrument_id
            self.my_type_instr_id = 5

            self.mesures = [
                {'type_i': 5, 'src_key': 'wind_i', 'dataType': float, 'agg': 'avg', 'avg': True, 'calcAvg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 0},
                {'type_i': 5, 'src_key': 'wind', 'dataType': float, 'agg': 'avgomm', 'avg': True, 'calcAvg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 16},
                {'type_i': 5, 'src_key': 'win10', 'dataType': float, 'agg': 'avg', 'avg': True, 'calcAvg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 0},
            ]
            super()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
