from enum import Enum
from app.models import Code_QA

class CsvOvpf:
    class RowId(Enum):
        DATE = 0
        TIME = 1
        RR1 = 2
        QRR1 = 3

    pattern = [
        r'^.*.csv$',
    ]
    duration = 1440
    poste_strategy = 1
    separator = ' '
    skip_lines = 0
    move_file = False
    fix_obs_last_date = True
    mappings = [
        {'csv_field': 'RR1',       'csv_idx': RowId.RR1.value, 'qa_idx': None,       'mesure': 'rain_utc',         'minmax': {},      "convert": {}},
    ]
    qa_mapping = [ ]

    def getArchiveDir(self, file_name):
        return '/'


# RR1	HAUTEUR DE PRECIPITATIONS JOURNALIER	MILLIMETRES ET 1/10