from app.classes.csv_loader.csvFileDef import CsvFileSpec
from app.tools.dateTools import str_to_datetime
from enum import Enum


class RowsId(Enum):
    NUM_POSTE = 0


class CSV_MeteoFR(CsvFileSpec):

    def __init__(self):
        super().__init__({
                'pattern': [
                    r'H_974_\d{4}-\d{4}\.csv',
                    r'H_974_previous-\d{4}-\d{4}\.csv',
                    r'H_974_latest-\d{4}-\d{4}\.csv'
                ],
                'mappings': [],
                'skip_lines': 1,
                'poste_strategy': 1,
            })

    def getPosteData(self, rows):
        return {
                'meteor': rows[RowsId.NOM_USUEL.value],
                'ALTI': rows[RowsId.ALTI.value],
                'LAT': rows[RowsId.LAT.value],
                'LON': rows[RowsId.LON.value],
                'CODE': rows[RowsId.NUM_POSTE.value].strip()
        }

    def hackHeader(self, header):
        return header

    def getStopDate(self, rows):
        tmp_dt = rows[RowsId.AAAAMMJJHH.value]
        return str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[4:6] + '-' + tmp_dt[6:8] + 'T' + tmp_dt[8:10] + ':00:00')
