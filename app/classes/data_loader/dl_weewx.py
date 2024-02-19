from app.classes.data_loader.bulk_data_loader import BulkDataLoader
from app.tools.myTools import FromTimestampToDateTime
from app.classes.repository.obsMeteor import QA


class DlWeewx(BulkDataLoader):
    def __init__(self):
        super().__init__()
        self.col_mapping = None

    def getObsDateTime(self, row2, col_mapping, cur_poste):
        date_obs_utc = FromTimestampToDateTime(row2[col_mapping['date_obs']])
        date_obs_local = FromTimestampToDateTime(row2[col_mapping['date_obs']], cur_poste.data.delta_timezone)
        return date_obs_utc, date_obs_local

    def getConvertKey(self):
        return 'weewx'

    def getColMapping(self, my_cur):
        if self.col_mapping is None:
            # load field_name/row_id mapping for weewx select
            col_mapping = {'date_obs': 0, 'usUnits': 1, 'interval': 2}

            idx = 3
            while idx < len(my_cur.column_names):
                col_mapping[my_cur.column_names[idx]] = idx
                idx += 1
            self.col_mapping = col_mapping

        return self.col_mapping

    def isMesureQualified(self, a_measure):
        return False if a_measure['archive_col'] is None else True

    def getValues(self, cur_row, col_mapping, a_mesure):
        cur_val = cur_row[col_mapping[a_mesure['archive_col']]]
        if cur_val is None or cur_val == '' or (cur_val == 0 and a_mesure['zero'] is False):
            return None, None, None
        if a_mesure['convert'] is not None and a_mesure['convert'].get(self.getConvertKey()) is not None:
            cur_val = eval(a_mesure['convert'][self.getConvertKey()])(cur_val)
        cur_qa_val = QA.UNSET.value
        interval = 60 if (cur_row[col_mapping['interval']] is None or cur_row[col_mapping['interval']] == 0) else cur_row[col_mapping['interval']]
        return cur_val, cur_qa_val, interval

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
