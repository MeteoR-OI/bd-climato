from abc import ABC, abstractmethod
from app.classes.repository.obsMeteor import QA
from app.classes.repository.mesureMeteor import MesureMeteor
import psycopg2
from datetime import datetime
from app.tools.dbTools import getPGConnexion


class BulkDataLoader(ABC):
    def __init__(self):
        self._meteors_to_process = []
        self.measures = self.getMeasuresInitial()

    @abstractmethod
    def getObsDateTime(self, row2, col_mapping, cur_poste):
        Exception("getObsDateTime not implemented")

    @abstractmethod
    def getConvertKey(self):
        Exception("getConvertKey not implemented")

    @abstractmethod
    def getMeasuresInitial(self):
        Exception("getMeasuresInitial not implemented")

    @abstractmethod
    def getColMapping(self, data_iterator):
        Exception("getColMapping not implemented")

    @abstractmethod
    def isMesureQualified(self, a_measure):
        Exception("isMesureQualified not implemented")

    @abstractmethod
    def getValues(self, cur_row, col_mapping, a_mesure):
        Exception("getValues not implemented")

    @abstractmethod
    def getMinMaxValues(self, cur_row, col_mapping, a_mesure, cur_val, date_obs_local):
        Exception("getMinMaxValues not implemented")

    @abstractmethod
    def getNextRow(self, data_iterator):
        Exception("getNextRow not implemented")

    @abstractmethod
    def fixMinMax(self, str_mesure_list, cur_poste, x_max_min_date, x_min_min_date):
        Exception("fixMinMax not implemented")

    def getMeasures(self):
        return self.measures

    def bulkLoad(self, cur_poste, data_iterator, load_missing_data, min_max=[]):
        pg_conn = None
        pg_cur = None

        try:
            pg_conn = self.getPGConnexion()
            pg_cur = pg_conn.cursor()

            min_max = self.loadObs(pg_cur, cur_poste, data_iterator, load_missing_data, min_max)

            if min_max is not None:
                del_cde = self.LoadMaxMin(pg_cur, cur_poste, min_max)
                min_max = None
                for a_del_sql in del_cde:
                    pg_cur.execute(a_del_sql)

            pg_conn.commit()

        except Exception as e:
            if pg_conn is not None:
                pg_conn.rollback()
            raise e

        finally:
            if pg_conn is not None:
                pg_conn.close()
                if pg_cur is not None:
                    pg_cur.close()

    def loadObs(self, pg_cur, cur_poste, data_iterator, load_missing_data, min_max):
        sql_insert = "insert into obs(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value) values "

        minmax_other_len = len(min_max)
        data_args = []
        idx = 0
        cur_row = self.getNextRow(data_iterator)
        col_mapping = self.getColMapping(data_iterator)

        while cur_row is not None:
            try:
                if col_mapping.get('usUnits') is not None and cur_row[col_mapping['usUnits']] != 16:
                    raise Exception('bad usUnits: ' + str(
                        cur_row[col_mapping['usUnits']]) + ', dateTime(UTC): ' + str(cur_row[col_mapping['date_utc']]))

                date_obs_utc, date_obs_local = self.getObsDateTime(
                    cur_row, col_mapping, cur_poste)

                if load_missing_data is False and (cur_poste.data.last_obs_date is None or date_obs_local > cur_poste.data.last_obs_date):
                    for a_mesure in self.measures:
                        if self.isMesureQualified(a_mesure) is False:
                            continue

                        cur_val, cur_qa_val, interval = self.getValues(
                            cur_row, col_mapping, a_mesure)

                        if cur_val is None:
                            continue

                        data_args.append((cur_poste.data.id, date_obs_utc, date_obs_local,
                                         a_mesure['id'], interval, cur_val, cur_qa_val, ))

                        cur_min, date_min, cur_max, date_max, max_dir = self.getMinMaxValues(
                            cur_row, col_mapping, a_mesure, cur_val, date_obs_local)

                        if a_mesure['iswind'] is True:
                            min_max.append({'min': cur_min, 'max': cur_max, 'date_min': date_min,
                                                 'date_max': date_max, 'max_dir': max_dir, 'mid': a_mesure['id'], 'obs_id': -1})
                        else:
                            min_max.append({'min': cur_min, 'max': cur_max, 'date_min': date_min,
                                                 'date_max': date_max, 'mid': a_mesure['id'], 'obs_id': -1})

                if load_missing_data is True and (cur_poste.data.last_obs_date is not None or date_obs_local <= cur_poste.data.last_obs_date):
                    # Future chargement de donnees manquantes
                    pass
            finally:
                cur_row = self.getNextRow(data_iterator)

        if len(data_args) == 0:
            return None

        # cursor.mogrify() to insert multiple values
        args = ','.join(pg_cur.mogrify("( %s, %s, %s, %s, %s, %s, %s )", i).decode(
            'utf-8') for i in data_args)

        pg_cur.execute(sql_insert + args + ' returning id')
        new_ids = pg_cur.fetchall()

        idx = 0
        while idx < len(new_ids):
            min_max[idx + minmax_other_len]['obs_id'] = new_ids[idx][0]
            idx += 1

        return min_max

    def LoadMaxMin(self, pg_cur, cur_poste, new_records):
        # check: nico use: last_in_db for insert-update or insert..
        insert_cde_min = "insert into x_min(obs_id, date_local, poste_id, mesure_id, min, min_time, qa_min) values "
        insert_cde_max = "insert into x_max(obs_id, date_local, poste_id, mesure_id, max, max_time, qa_max, max_dir) values "
        min_args = []
        max_args = []
        mesures_hash = {}
        mesure_sum_id = []
        x_min_min_date = datetime.now().date()
        x_max_min_date = datetime.now().date()

        for a_mesure in self.measures:
            if self.isMesureQualified(a_mesure) is False:
                continue
            mesures_hash[a_mesure['id']] = a_mesure
            if a_mesure['agreg'] == MesureMeteor.Agreg_Type.SUM:
                mesure_sum_id.append(a_mesure['id'])

        for a_record in new_records:
            cur_mesure = mesures_hash[a_record['mid']]
            if cur_mesure['agreg'] == 0:
                continue

            if cur_mesure['min'] is True:
                dt_local_min = a_record['date_min'].date()
                if dt_local_min < x_min_min_date:
                    x_min_min_date = dt_local_min
                if a_record['min'] is not None:
                    min_args.append(
                        (a_record['obs_id'] if a_record['obs_id'] > -1 else None,
                         dt_local_min,
                         cur_poste.data.id,
                         a_record['mid'],
                         a_record['min'],
                         a_record['date_min'],
                         QA.UNSET.value))

            if cur_mesure['max'] is True:
                dt_local_max = a_record['date_min'].date()
                if dt_local_max < x_max_min_date:
                    x_max_min_date = dt_local_max
                if a_record['max'] is not None:
                    max_args.append(
                        (a_record['obs_id'] if a_record['obs_id'] > -1 else None,
                         dt_local_max,
                         cur_poste.data.id,
                         a_record['mid'],
                         a_record['max'],
                         a_record['date_max'],
                         QA.UNSET.value, a_record.get('max_dir')))

        min_args_ok = ','.join(pg_cur.mogrify(
            "(%s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in min_args)
        max_args_ok = ','.join(pg_cur.mogrify(
            "(%s, %s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in max_args)

        pg_cur.execute(insert_cde_min + min_args_ok)
        pg_cur.execute(insert_cde_max + max_args_ok)

        # for sum mesures, remove data from obs, when a record is inserted in x_min/x_max from archive_day_xxx
        str_mesure_list = "(" + ','.join(str(x) for x in mesure_sum_id) + ")"

        # (Load Need to remove min/max k=linked with obs, when mesure is a sum
        return self.fixMinMax(str_mesure_list, cur_poste, x_max_min_date, x_min_min_date)

