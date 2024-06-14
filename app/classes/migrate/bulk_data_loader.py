# from abc import ABC, abstractmethod
from app.classes.repository.mesureMeteor import MesureMeteor
from app.models import Aggreg_Type, Code_QA as QA
from app.tools.dateTools import FromTimestampToLocalDateTime, FromTimestampToUTCDateTime
from app.tools.dbTools import getPGConnexion
from datetime import datetime
from operator import itemgetter

class BulkDataLoader():
    def __init__(self):
        self.measures = MesureMeteor.getDefinitions()
        self.insert_cde = None
        self.col_mapping = None

    def getObsDateTime(self, row2, cur_poste):
        date_obs_utc = FromTimestampToUTCDateTime(row2[self.col_mapping['date_obs']])
        date_obs_local = FromTimestampToLocalDateTime(row2[self.col_mapping['date_obs']], cur_poste.data.delta_timezone)
        return date_obs_utc, date_obs_local

    def getConvertKey(self):
        return 'w_dump'

    def loadColMapping(self, my_cur):
        if self.col_mapping is None:
            # load field_name/row_id mapping for weewx select
            col_mapping = {'date_obs': 0, 'usUnits': 1, 'interval': 2}

            idx = 3
            while idx < len(my_cur.column_names):
                col_mapping[my_cur.column_names[idx]] = idx
                idx += 1
            self.col_mapping = col_mapping


    def isMesureQualified(self, a_measure):
        if a_measure['json_input'] == 'rain_utc':
            return False
        return False if a_measure['archive_col'] is None else True

    def getValues(self, cur_row, a_mesure):
        cur_val = cur_row[self.col_mapping[a_mesure['archive_col']]]
        if cur_val is None or cur_val == '' or (cur_val == 0 and a_mesure['zero'] is False):
            return None, None
        if a_mesure['convert'] is not None and a_mesure['convert'].get(self.getConvertKey()) is not None:
            cur_val = eval(a_mesure['convert'][self.getConvertKey()])(cur_val)
        cur_qa_val = QA.UNSET.value
        return cur_val, cur_qa_val

    def getMinMaxValues(self, cur_row, a_mesure, cur_val, date_obs_local):
        max_dir = None if a_mesure['diridx'] is None else cur_row[self.col_mapping[self.measures[a_mesure['diridx']]['archive_col']]]

        return cur_val, date_obs_local, cur_val, date_obs_local, max_dir

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

    def bulkLoad(self, cur_poste, data_iterator, min_max=[]):
        pg_conn = None
        pg_cur = None
        tmp_dt = datetime.now()

        try:
            pg_conn = getPGConnexion()
            pg_cur = pg_conn.cursor()

            min_max = self.loadObs(pg_cur, cur_poste, data_iterator, min_max)
            # print('loadObs done in : ' + str(datetime.now() - tmp_dt))
            tmp_dt = datetime.now()

            if min_max is not None:
                del_cde = self.LoadMaxMin(pg_cur, cur_poste, min_max)
                # print('LoadMaxMin done in : ' + str(datetime.now() - tmp_dt))
                min_max = None
                for a_del_sql in del_cde:
                    tmp_dt = datetime.now()
                    pg_cur.execute(a_del_sql)
                    # print('exec delete(s) done in : ' + str(datetime.now() - tmp_dt))
    
            tmp_dt = datetime.now()
            pg_conn.commit()
            # print('commit done in : ' + str(datetime.now() - tmp_dt))
    
        except Exception as e:
            if pg_conn is not None:
                pg_conn.rollback()
            raise e

        finally:
            if pg_conn is not None:
                pg_conn.close()

    def loadSqlInsert(self):
        if self.insert_cde is None:
            self.insert_cde = {
                "sql": "insert into obs(poste_id, date_utc, date_local, duration",
                "mog": "(%s, %s, %s, %s"
            }
            for a_mesure in self.measures:
                if self.isMesureQualified(a_mesure) is False:
                    continue
                self.insert_cde['sql'] += ", " + a_mesure['json_input']
                self.insert_cde['mog'] += ", %s"

            self.insert_cde['sql'] += ", qa_all) values "
            self.insert_cde['mog'] += ", %s)"

    def loadObs(self, pg_cur, cur_poste, data_iterator, min_max):
        self.loadSqlInsert()
        self.loadColMapping(data_iterator)

        data_args = []
        idx = 0
        obs_count = 0
        idx_initial = len(min_max)
        cur_row = data_iterator.fetchone()


        while cur_row is not None:
            try:
                if cur_row[self.col_mapping['usUnits']] != 16:
                    raise Exception('bad usUnits: ' + str(cur_row[self.col_mapping['usUnits']]) +\
                                    ', dateTime(UTC): ' + str(cur_row[self.col_mapping['date_utc']]))

                date_obs_utc, date_obs_local = self.getObsDateTime(cur_row, cur_poste)
                qa_all = QA.UNSET.value
                qa_j = {}

                values_arg = [cur_poste.data.id, str(date_obs_utc), str(date_obs_local), cur_row[self.col_mapping['interval']]]

                if (cur_poste.data.last_obs_date_local is None or date_obs_local > cur_poste.data.last_obs_date_local):
                    for a_mesure in self.measures:
                        if self.isMesureQualified(a_mesure) is False:
                            continue

                        cur_val, cur_qa_val = self.getValues(cur_row, a_mesure)

                        if cur_val is None:
                            values_arg.append(None)
                        else:
                            values_arg.append(cur_val)
                            if cur_qa_val != QA.UNSET.value:
                                qa_j[a_mesure['archive_col']] = cur_qa_val
                                if cur_qa_val > qa_all:
                                    qa_all = cur_qa_val

                            cur_min, date_min, cur_max, date_max, max_dir = self.getMinMaxValues(cur_row, a_mesure, cur_val, date_obs_local)

                            if cur_qa_val != QA.UNVALIDATED.value:
                                if a_mesure['is_wind'] is True:
                                    min_max.append({'min': cur_min, 'max': cur_max, 'date_min': date_min,
                                                    'date_max': date_max, 'max_dir': max_dir, 'mid': a_mesure['id'], 'obs_id': obs_count})
                                else:
                                    min_max.append({'min': cur_min, 'max': cur_max, 'date_min': date_min,
                                                    'date_max': date_max, 'mid': a_mesure['id'], 'obs_id': obs_count})

                    obs_count += 1
                    values_arg.append(qa_all)
                    data_args.append(tuple(values_arg))

            finally:
                cur_row = data_iterator.fetchone()

        if len(data_args) == 0:
            return None
        
        # print('data_args: ' + str(len(data_args)))

        # cursor.mogrify() to insert multiple values
        args = ','.join(pg_cur.mogrify(self.insert_cde['mog'], i).decode('utf-8') for i in data_args)
        pg_cur.execute(self.insert_cde['sql'] + args + ' returning id')
        new_ids = pg_cur.fetchall()

        idx = idx_initial
        tmp_l = str(len(new_ids))
        print('idx_initial: ' + str(idx_initial) + ', len(new_ids): ' + tmp_l + ', len(min_max): ' + str(len(min_max)))
        while idx < len(new_ids):
            my_minmax = min_max[idx]
            print ('idx: ' + str(idx) + ', len(new_ids): ' + tmp_l + ', id in my_minmax: ' + str(my_minmax['obs_id']))
            print('    old obs_id: ' + str(my_minmax['obs_id']) + ' => ' + str(new_ids[my_minmax['obs_id']][0]))
            my_minmax['obs_id'] = new_ids[my_minmax['obs_id']][0]
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
            if a_mesure['agreg_type'] == Aggreg_Type.SUM:
                mesure_sum_id.append(a_mesure['id'])

        for a_record in new_records:
            cur_mesure = mesures_hash[a_record['mid']]
            if cur_mesure['agreg_type'] == 0:
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

        # keep only 3 min/max per day
        min_arg_sorted = sorted(min_args, key=itemgetter(2, 3, 1, 4))
        min_args = []
        max_arg_sorted = sorted(max_args, key=itemgetter(2, 3, 1, 4))
        max_args = []

        tmp_date = None
        tmp_poste_id = -1
        tmp_mesure_id = -1
        idx = 0
        idx_per_mesure = 0
        while idx < len(min_arg_sorted):
            if tmp_poste_id != min_arg_sorted[idx][2] or tmp_mesure_id != min_arg_sorted[idx][3] or tmp_date != min_arg_sorted[idx][1]:
                tmp_poste_id = min_arg_sorted[idx][2]
                tmp_date = min_arg_sorted[idx][1]
                tmp_mesure_id = min_arg_sorted[idx][3]
                idx_per_mesure = 0

            if idx_per_mesure < 3:
                min_args.append(min_arg_sorted[idx])
                idx_per_mesure += 1
            idx += 1

        tmp_date = None
        tmp_poste_id = -1
        tmp_mesure_id = -1
        idx = len(max_arg_sorted) - 1
        idx_per_mesure = 0
        while idx >= 0:
            if tmp_poste_id != max_arg_sorted[idx][2] or tmp_mesure_id != max_arg_sorted[idx][3] or tmp_date != max_arg_sorted[idx][1]:
                tmp_poste_id = max_arg_sorted[idx][2]
                tmp_date = max_arg_sorted[idx][1]
                tmp_mesure_id = max_arg_sorted[idx][3]
                idx_per_mesure = 0

            if idx_per_mesure < 3:
                max_args.append(max_arg_sorted[idx])
                idx_per_mesure += 1
            idx -= 1

        min_arg_sorted = []
        max_arg_sorted = []

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
