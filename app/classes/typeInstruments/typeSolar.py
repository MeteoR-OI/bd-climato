from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument
from app.tools.climConstant import MeasureProcessingBitMask


class TypeSolar(RootTypeInstrument):
    """Type Solar"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 6

        self.measures = [
            {'type_i': 6, 'src_key': 'uv_indice', 'agg': 'no', 'min': False},
            {'type_i': 6, 'src_key': 'radiation', 'target_key': 'radiation', 'agg': 'sum', 'min': False, 'max': False},
            {'type_i': 6, 'src_key': 'etp',       'agg': 'sum', 'min': False, 'max': False, 'special': MeasureProcessingBitMask.NotAllowedInCurrent}
        ]
        super().__init__()
