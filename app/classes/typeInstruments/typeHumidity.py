from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeHumidity(RootTypeInstrument):
    """Type Humidity"""

    def __init__(self):
        try:
            # type_instrument_id
            self.my_type_instr_id = 2

            self.mesures = [
                {'type_i': 2, 'src_key': 'humidity', 'dataType': int, 'agg': 'avg', 'avg': True, 'min': True, 'max': True, 'hour_deca': 0, 'special': 0},
            ]
            super()

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
