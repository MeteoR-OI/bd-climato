

from app.classes.data_loader.bulk_data_loader import BulkDataLoader
from app.tools.myTools import FromTimestampToDateTime
from app.classes.repository.obsMeteor import QA

class DlCsv(BulkDataLoader):
    def __init__(self):
        super().__init__()

    def getObsDateTime(self, row2, col_mapping, cur_poste):
        ..
        return date_obs_utc, date_obs_local

    def getConvertKey(self):
        return 'mfr_csv'

    def getColMapping(self, data_iterator):
        col_mapping = {'date_utc': 0, 'usUnits': 1, 'interval': 2, 'outTemp': 3, 'outHumidity': 4, 'windSpeed': 5, 'windDir': 6, 'rain': 7, 'pressure': 8, 'radiation': 9, 'dewpoint': 10, 'windGust': 11, 'windGustDir': 12, 'windGustTime': 13, 'windGustDirTime': 14, 'windGustTime': 15, 'windGustDirTime': 16}
        return col_mapping

    def isMesureQualified(self, a_measure):
        return True

    def getDataKey(self):
        return 'archive_col'

    def getNextRow(self, data_iterator):
        next_row = data_iterator.fetchone()
        if next_row is None:
            data_iterator.close()
        return next_row

    def fixMinMax(self, str_mesure_list, cur_poste, x_max_min_date, x_min_min_date):
        return ["delete from x_max where obs_id is not null and mesure_id in " + str_mesure_list +
                " and poste_id = " + str(cur_poste.data.id) + " and date_local in " +
                " (select date_local from x_max where obs_id is null and date_local >= '" +
                x_max_min_date.strftime("%Y/%m/%d, %H:%M:%S") + "' and mesure_id in " + str_mesure_list +
                " and poste_id = " + str(cur_poste.data.id) + ")",
                "delete from x_min where obs_id is not null and mesure_id in " + str_mesure_list +
                " and poste_id = " + str(cur_poste.data.id) + " and date_local in " +
                " (select date_local from x_min where obs_id is null and date_local >= '" +
                x_min_min_date.strftime("%Y/%m/%d, %H:%M:%S") + "' and mesure_id in " + str_mesure_list +
                " and poste_id = " + str(cur_poste.data.id) + ")"
                ]

    def transcodeQACode(self, qa_meteoFR):
        if qa_meteoFR is None or qa_meteoFR == 0:
            return QA.UNSET.value
        if qa_meteoFR == 2:
            return QA.UNVALIDATED.value
        return QA.VALIDATED.value
