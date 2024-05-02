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
from app.classes.repository.posteMeteor import PosteMeteor
import app.tools.myTools as t
from django.conf import settings
import json
from datetime import datetime
import os
from app.classes.csv_loader.csv_meteoFR import CsvMeteoFR
from app.classes.csv_loader.csv_OVPF import CsvOpvf
from app.tools.dbTools import getPGConnexion, refreshMV
from app.models import Load_Type


class CsvLoader:
    def __init__(self):
        # save mesures definition
        self.__all_mesures = MesureMeteor.getDefinitions()

        # boolean to stop processing files
        self.stopRequested = False

        self.__all_providers = [
            CsvMeteoFR(),
            CsvOpvf()
        ]

    # ----------------
    # public methods
    # ----------------
    def addNewWorkItem(self, work_item):
        work_item['info'] = "chargement du fichier: " + work_item['f']
        return

    def getNextWorkItem(self):
        idx_provider = 0
        while idx_provider < len(self.__all_providers):
            work_item = self.__all_providers[idx_provider].findNextWorkItem()
            if work_item is not None:
                work_item['idx_provider'] = idx_provider
                return work_item
            idx_provider += 1
        return None

    def succeedWorkItem(self, work_item):
        # move the file to archive
        if work_item['move_file'] is True:
            target_dir = self.__all_providers[work_item['idx_provider']].getArchivePath(work_item)
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            os.rename(work_item['path'] + "/" + work_item['f'], target_dir + work_item['f'])

        # Change year when full year was processed
        if work_item.get('fix_obs_last_date') is True:
            if work_item['year_processed'] != datetime.now().year:
                cur_poste = PosteMeteor(work_item['meteor'])
                cur_poste.data.last_obs_date_local = datetime(work_item['year_processed'] + 1, 1, 1, 0, 0, 0)
                cur_poste.save()

        # refresh our materialized view
        refreshMV()

    def failWorkItem(self, work_item, exc):
        # move the file to failed archive
        if work_item['move_file'] is True:
            target_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/failed/csv/"
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            os.rename(work_item['path'] + "/" + work_item['f'], target_dir + work_item['f'])
            t.logError('CsvLoader', "file moved to failed directory", {"filename": work_item['f'], "dest": target_dir})

    # Load data per block
    def processWorkItem(self, work_item: json):
        cur_provider = self.__all_providers[work_item['idx_provider']]
        pg_conn = getPGConnexion()

        for data_to_flush in cur_provider.nextBlockLines(work_item, Load_Type.LOAD_CSV_FOR_METEOFR.value):
            # data_to_flush = {
            #     'obs_data': [(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value)],
            #     'min_data': [(poste_id, date_utc, date_local, mesure_id, min, min_time, is_it_obs_data)],
            #     'max_data': [(poste_id, date_utc, date_local, mesure_id, max, max_time, max_dir, is_it_obs_data)],
            # }

            if data_to_flush is None:
                break

            self.flush_data(pg_conn, data_to_flush)
            pg_conn.commit()

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
                     (new_ids[idx][0]) if cur_min_data[6] == True else None))

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
                     (new_ids[idx][0] if cur_max_data[7] == True else None)))
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
