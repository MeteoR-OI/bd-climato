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
        csv_format = self.all_formats[idx]
        if csv_format.poste_strategy == 1:
            return {
                    'meteor': rows[csv_format.RowsId.NOM_USUEL.value],
                    'ALTI': rows[csv_format.RowsId.ALTI.value],
                    'LAT': rows[csv_format.RowsId.LAT.value],
                    'LON': rows[csv_format.RowsId.LON.value],
                    'CODE': rows[csv_format.RowsId.NUM_POSTE.value].strip()
            }
        if csv_format.poste_strategy == 2:
            return self.__poste_info

    def hackHeader(self, idx, header, row):
        return

    def getStopDate(self, idx, rows):
        tmp_dt = rows[self.all_formats[idx].RowsId.AAAAMMJJHH.value]
        return str_to_datetime(
            tmp_dt[0:4] + '-' +
            tmp_dt[4:6] + '-' +
            tmp_dt[6:8] + 'T' +
            tmp_dt[8:10] + ':00:00')
