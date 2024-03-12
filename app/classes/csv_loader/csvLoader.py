# CsvLoader process
#   addNewWorkItem(self, work_item)
#       not supported in CsvLoader
#   work_item = class.getNextWorkItem()
#       return None -> no more work for now
#       return a work_item data, which should include enought info for other calls
#   processItem(work_item):
#       Process the work item
#   succeedWorkItem(work_item):
#       Mark the work_item as processed
#   failWorkItem(work_item, exc):
#       mark the work_item as failed
from app.classes.repository.mesureMeteor import MesureMeteor
import app.tools.myTools as t
from django.conf import settings
import json
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.classes.csv_loader.csv_meteoFR import CSV_MeteoFR


class CsvLoader:
    def __init__(self):
        # save mesures definition
        self.__all_mesures = MesureMeteor.getDefinitions()

        # boolean to stop processing files
        self.stopRequested = False

        # get directories settings
        if hasattr(settings, "CSV_AUTOLOAD") is True:
            self.base_dir = settings.CSV_AUTOLOAD
        else:
            self.base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/csv_auto_load")

        if hasattr(settings, "ARCHIVE_DIR") is True:
            self.archive_dir = settings.ARCHIVE_DIR
        else:
            self.archive_dir = self.base_dir

        self.__all_providers = [
            CSV_MeteoFR()
        ]

    # ----------------
    # public methods
    # ----------------
    def addNewWorkItem(self, work_item):
        work_item['info'] = "chargement du fichier: " + work_item['f']
        return

    def getNextWorkItem(self):
        file_names = []

        # get json file names
        filenames = os.listdir(self.base_dir)
        for filename in filenames:
            if str(filename).endswith('.csv'):
                file_names.append(filename)

        # stop processing
        if len(file_names) == 0:
            return None

        file_names = sorted(file_names)
        a_filename = file_names[0]

        # find our file specification
        idx_provider = 0

        while idx_provider < len(self.__all_providers):
            id_spec = self.__all_providers[idx_provider].isItForMe(
                self.base_dir,
                a_filename,
            )
            if id_spec >= 0:
                return {
                    'f': a_filename,
                    'path': self.base_dir,
                    'idx_provider': idx_provider,
                    'id_spec': id_spec,
                    'info': 'loading file: ' + a_filename
                }
            idx_provider += 1

        Exception("No file spec found for " + a_filename)

    def succeedWorkItem(self, work_item):
        # move the file to archive
        target_dir = self.archive_dir + "/meteoFR/"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        os.rename(self.base_dir + "/" + work_item['f'], target_dir + work_item['f'])

        # refresh our materialized view
        pgconn = self.getPGConnexion()
        pgconn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        pg_cur = pgconn.cursor()

        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_hour')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_month')))

        pg_cur.close()
        pgconn.commit()
        pgconn.close()

    def failWorkItem(self, work_item, exc):
        # move the file to failed archive
        target_dir = self.archive_dir + "/failed/meteoFR/"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        os.rename(self.base_dir + "/" + work_item['f'], target_dir + work_item['f'])

        t.logError('CsvLoader', "file moved to failed directory", {"filename": work_item['f'], "dest": target_dir})

    # Load data per block
    def processWorkItem(self, work_item: json):
        cur_provider = self.__all_providers[work_item['idx_provider']]
        pg_conn = self.getPGConnexion()

        for data_to_flush in cur_provider.nextBlockLines(work_item['id_spec']):
            # data_to_flush = {
            #     'obs_data': [(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value)],
            #     'min_data': [(poste_id, date_utc, date_local, mesure_id, min, min_time, is_it_obs_data)],
            #     'max_data': [(poste_id, date_utc, date_local, mesure_id, max, max_time, max_dir, is_it_obs_data)],
            # }

            if data_to_flush is None:
                break

            self.flush_data(pg_conn, data_to_flush)
            pg_conn.commit()

        # self.flush_data(pg_conn, data_to_flush)
        # pg_conn.commit()
        pg_conn.close()

    def flush_data(self, pg_conn, data_to_flush):
        if len(data_to_flush['obs_data']) == 0:
            return

        sql_obs_insert = "insert into obs(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value) values "
        pg_cur = pg_conn.cursor()

        # cursor.mogrify() to insert multiple values
        args = ','.join(pg_cur.mogrify("( %s, %s, %s, %s, %s, %s, %s )", i).decode('utf-8')
                        for i in data_to_flush['obs_data'])

        pg_cur.execute(sql_obs_insert + args + ' returning id')

        # get new obd.id => and inject them in min/max
        new_ids = pg_cur.fetchall()

        data_to_flush['obs_data'] = []
        min_data_shrinked = []
        max_data_shrinked = []

        idx = 0
        while idx < len(new_ids):
            # load min/max_data_shrinked, add obs_id
            cur_min_data = data_to_flush['min_data'][idx]
            cur_max_data = data_to_flush['max_data'][idx]

            if cur_min_data[4] is not None:
                # min_data_shrink = [(poste_id, date_local, mesure_id, min, min_time, qa_min, obs_id)]
                min_data_shrinked.append(
                    (cur_min_data[0],
                     cur_min_data[1],
                     cur_min_data[2],
                     cur_min_data[3],
                     cur_min_data[4],
                     cur_min_data[5],
                     (new_ids[idx][0]) if cur_min_data[5] is False else None))

            if cur_max_data[4] is not None:
                # max_data_shrink = [(poste_id, date_local, mesure_id, max, max_time, qa_max, max_dir, obs_id)]
                max_data_shrinked.append(
                    (cur_max_data[0],
                     cur_max_data[1],
                     cur_max_data[2],
                     cur_max_data[3],
                     cur_max_data[4],
                     cur_max_data[5],
                     cur_max_data[6],
                     (new_ids[idx][0] if cur_max_data[6] is False else None)))
            idx += 1
        data_to_flush = []

        # insert min/max
        if len(min_data_shrinked) > 0:
            sql_min_insert = "insert into x_min(poste_id, date_local, mesure_id, min, min_time, qa_min, obs_id) values "
            args_min = ','.join(pg_cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8')
                                for i in min_data_shrinked)
            pg_cur.execute(sql_min_insert + args_min)

        if len(max_data_shrinked) > 0:
            sql_max_insert = "insert into x_max(poste_id, date_local, mesure_id, max, max_time, qa_max, max_dir, obs_id) values "
            args_max = ','.join(pg_cur.mogrify("( %s, %s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8')
                                for i in max_data_shrinked)
            pg_cur.execute(sql_max_insert + args_max)

    def getPGConnexion(self):
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Funiculi",
            database="climato"
        )
