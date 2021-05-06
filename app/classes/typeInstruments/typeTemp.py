from app.classes.typeInstruments.rootTypeInstr import RootTypeInstrument


class TypeTemp(RootTypeInstrument):
    """Type Temp"""

    def __init__(self):
        # type_instrument_id
        self.my_type_instr_id = 1

        self.measures = [
        {
            'type_i': 1,
            'src_key': 'out_temp',
            'dataType': float,
            'agg': 'avg',
            'avg': True,
            'min': True,
            'max': True,
            'hour_deca': 0,
            'special': 0,
        },
        {
            'type_i': 1,
            'src_key': 'out_temp',
            'dataType': float,
            'agg': 'avgomm',
            'measureType': 'inst',
            'avg': True,
            'min': True,
            'deca_min': -5,
            'max': True,
            'deca_max': 7,
            'hour_deca': 0,
            'special': 0,
        },
        {
            'type_i': 1,
            'src_key': 'out_temp2',
            'syno': ['out_temp2_sum'],
            'dataType': float,
            'agg': 'sum',
            'avg': True,
            'min': True,
            'max': True,
            'hour_deca': 0,
            'special': 0,
        },
        {
            'type_i': 1,
            'src_key': 'windchill',
            'dataType': float,
            'agg': 'avg',
            'avg': False,
            'min': True,
            'max': False,
            'hour_deca': 0,
            'special': 0,
        },
        {
            'type_i': 1,
            'src_key': 'heatindex',
            'dataType': float,
            'agg': 'avg',
            'avg': False,
            'min': False,
            'max': True,
            'hour_deca': 0,
            'special': 0,
        },
        {
            'type_i': 1,
            'src_key': 'dewpoint',
            'dataType': float,
            'agg': 'avg',
            'avg': False,
            'min': True,
            'max': True,
            'hour_deca': 0,
            'special': 0,
        },
        {
            'type_i': 1,
            'src_key': 'soiltemp',
            'dataType': float,
            'agg': 'avg',
            'avg': False,
            'min': True,
            'max': False,
            'hour_deca': 0,
            'special': 0,
        }
        ]
        super().__init__()
