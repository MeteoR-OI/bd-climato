from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument
from app.tools.climConstant import MeasureProcessingBitMask


class TypeWind(RootTypeInstrument):
    """Type Wind"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 5

        self.measures = [
            {'type_i': 5, 'src_key': 'wind_inst', 'measureType': 'inst', 'agg': 'avg', 'calcAvg': False, 'min': False, 'max': False, 'special': MeasureProcessingBitMask.MeasureIsWind},
            {'type_i': 5, 'src_key': 'wind',      'measureType': 'avg',  'agg': 'avg', 'min': False, 'special': MeasureProcessingBitMask.MeasureIsWind},
            # {'type_i': 5, 'src_key': 'gust',      'measureType': 'avg',  'agg': 'no', 'calcAvg': False, 'min': False, 'special': MeasureProcessingBitMask.MeasureIsWind},
            {'type_i': 5, 'src_key': 'win10',     'measureType': 'avg',  'agg': 'avg', 'calcAvg': False, 'min': False, 'max': False, 'special': MeasureProcessingBitMask.MeasureIsWind},
            {'type_i': 5, 'src_key': 'win10',     'measureType': 'avg',  'agg': 'avgomm', 'calcAvg': False, 'min': False, 'special': MeasureProcessingBitMask.MeasureIsWind},
        ]
        super().__init__()
