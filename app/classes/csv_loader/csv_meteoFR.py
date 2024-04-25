from app.classes.csv_loader.csvFileSpec import CsvFileSpec
from app.tools.dateTools import str_to_datetime
from app.classes.csv_loader.file_format.all_formats import all_formats
from app.models import Code_QA


class CSV_MeteoFR(CsvFileSpec):

    def __init__(self):
        self.all_formats = all_formats
        patterns = []
        idx = 0
        while idx < len(all_formats):
            for a_pattern in all_formats[idx].pattern:
                patterns.append({'p': a_pattern, 'idx': idx})
                idx += 1

        super().__init__(patterns, self.all_formats)

    def getPosteData(self, idx, rows, file_name):
        csv_format = self.all_formats[idx]
        if csv_format.poste_strategy == 1:
            return {
                    'meteor': None,
                    'ALTI': 0,
                    'LAT': 0,
                    'LON': 0,
                    'code':  rows[csv_format.RowId.POSTE.value].strip()
            }
        if csv_format.poste_strategy == 2:
            return self.__poste_info

    def hackHeader(self, idx, header, row):
        return

    def getStopDate(self, idx, rows):
        tmp_dt = rows[self.all_formats[idx].RowId.DATE.value]
        return str_to_datetime(
            tmp_dt[0:4] + '-' +
            tmp_dt[4:6] + '-' +
            tmp_dt[6:8] + 'T' +
            tmp_dt[8:10] + ':00:00')

    def getQualityCode(self, code_txt, id_spec):
        if code_txt is None:
            return Code_QA.UNSET.value

        for a_mapping in self.all_formats[id_spec].qa_mapping:
            if code_txt[0] == a_mapping[0]:
                return a_mapping[1]

        return Code_QA.UNSET.value
