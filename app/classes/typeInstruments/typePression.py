from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypePression(RootTypeInstrument):
    """Type Pression"""

    def __init__(self):
        try:
            # type_instrument_id
            self.my_type_instr_id = 3

            self.mesures = [
                {'type_i': 3, 'src_key': 'barometer', 'dataType': float, 'agg': 'avg', 'avg': True, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
                {'type_i': 3, 'src_key': 'barometer', 'dataType': float, 'agg': 'avgomm', 'avg': True, 'min': False, 'max': False, 'hour_deca': 7, 'special': 48},
                {'type_i': 3, 'src_key': 'pressure', 'dataType': float, 'agg': 'no', 'avg': False, 'min': False, 'max': False, 'hour_deca': 0, 'special': 0},
            ]
            super()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
