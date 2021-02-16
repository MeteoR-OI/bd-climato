import datetime
from app.classes.posteMeteor import PosteMeteor
from app.classes.obsMeteor import ObsMeteor
from app.tools.climConstant import AggLevel, MeasureProcessingBitMask
from app.tools.agg_tools import is_flagged
import json


class RootMeasure:
    """
        RootMeasure

        Computation specific to a measure type

    """
    # {'type_i': 1, 'key': 'temp_out', 'field': 'temp_out', 'avg': True, 'Min': True, 'max': True, 'hour_deca': 0, 'special': 0},
