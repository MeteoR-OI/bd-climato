from csvFileDef import CsvFileSpec


class CsvH_974(CsvFileSpec):
    __spec = {
        'pattern': [
            r'H_974_\d{4}_\d{4}\.csv',
            r'H_974_latest-\d{4}-\d{4}\.csv'
        ],
        'mappings': [
            {'csv_field': 'DD2',       'mesure': 'wind dir',         'minmax': '{}'},
            {'csv_field': 'FF',        'mesure': 'wind 10 omm',      'minmax': '{}'},
            {'csv_field': 'FF',        'mesure': 'wind 10',          'minmax': '{"max": "FXY", "maxDir": "DXY", "maxTime": "HXY"}'},
            {'csv_field': 'FF2',       'mesure': 'wind',             'minmax': '{"max": "FXI2", "maxDir": "DXI2", "maxTime": "HXI2"}'},
            {'csv_field': 'GLO',       'mesure': 'radiation',        'minmax': '{}'},
            {'csv_field': 'PMER',      'mesure': 'barometer omm',    'minmax': '{"minTime": "PMERMIN"}'},
            {'csv_field': 'PMER',      'mesure': 'barometer',        'minmax': '{"minTime": "PMERMIN"}'},
            {'csv_field': 'PSTAT',     'mesure': 'pressure',         'minmax': '{}'},
            {'csv_field': 'RR1',       'mesure': 'rain omm',         'minmax': '{}'},
            {'csv_field': 'RR1',       'mesure': 'rain',             'minmax': '{}'},
            {'csv_field': 'T',         'mesure': 'temp omm',         'minmax': '{"min": "TN", "minTime": "HTN", "max": "TX", "maxTine": "HTX"}'},
            {'csv_field': 'T',         'mesure': 'temperature',      'minmax': '{"min": "TN", "minTime": "HTN", "max": "TX", "maxTine": "HTX"}'},
            {'csv_field': 'TD',        'mesure': 'dewpoint',         'minmax': '{}'},
            {'csv_field': 'TVEGETAUX', 'mesure': 'leaftemp1',        'minmax': '{}'},
            {'csv_field': 'U',         'mesure': 'humidity omm',     'minmax': '{"min": "UN", "minTime": "HUN", "max": "UX", "maxTine": "HUX"}'},
            {'csv_field': 'U',         'mesure': 'humidity',         'minmax': '{"min": "UN", "minTime": "HUN", "max": "UX", "maxTine": "HUX"}'},
            {'csv_field': 'UV',        'mesure': 'uv_indice',        'minmax': '{}'},
        ],
        'skip_lines': 1,
        'poste_strategies': 1,
    }

    def __init__(self):
        super().__init__()

    def getPoste(self, csv_row):
        return {
                'meteor': csv_row['NOM_USUEL'],
                'ALTI': csv_row['ALTI'],
                'LAT': csv_row['LAT'],
                'LONG': csv_row['LON'],
                'CODE': csv_row['NUM_POSTE']
        }
