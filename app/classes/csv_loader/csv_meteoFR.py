from app.classes.csv_loader.csvFileDef import CsvFileSpec
from app.tools.dateTools import str_to_datetime
from app.classes.csv_loader.file_format.all_formats import all_formats


class CSV_MeteoFR(CsvFileSpec):

    def __init__(self):
        self.all_formats = all_formats()
        patterns = []
        idx = 0
        while idx < len(all_formats):
            for a_pattern in all_formats[idx].pattern:
                self.patterns.append({'p': a_pattern, 'idx': idx})
                idx += 1

        super().__init__(patterns, self.all_formats)

    def getPosteData(self, idx, rows):
        return {
                'meteor': rows[self.all_formats[idx].RowsId.NOM_USUEL.value],
                'ALTI': rows[self.all_formats[idx].RowsId.ALTI.value],
                'LAT': rows[self.all_formats[idx].RowsId.LAT.value],
                'LON': rows[self.all_formats[idx].RowsId.LON.value],
                'CODE': rows[self.all_formats[idx].RowsId.NUM_POSTE.value].strip()
        }

    def hackHeader(self, idx, header):
        return header

    def getStopDate(self, idx, rows):
        tmp_dt = rows[self.all_formats[idx].RowsId.AAAAMMJJHH.value]
        return str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[4:6] + '-' + tmp_dt[6:8] + 'T' + tmp_dt[8:10] + ':00:00')
