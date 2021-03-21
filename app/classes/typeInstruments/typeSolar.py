from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeSolar(RootTypeInstrument):
    """Type Solar"""

    def __init__(self):
        try:
            # type_instrument_id
            self.my_type_instr_id = 6

            self.mesures = [
                {'type_i': 6, 'src_key': 'uv_indice', 'dataType': float, 'agg': 'avg', 'avg': False, 'min': False, 'max': True, 'hour_deca': 0, 'special': 0},
                {'type_i': 6, 'src_key': 'radiation', 'dataType': float, 'agg': 'avgomm', 'avg': True, 'min': False, 'max': True, 'hour_deca': 0, 'special': 16},
                {'type_i': 6, 'src_key': 'etp', 'dataType': float, 'agg': 'sum', 'avg': False, 'min': True, 'max': False, 'hour_deca': 0, 'special': 1 + 8}
            ]
            super()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
