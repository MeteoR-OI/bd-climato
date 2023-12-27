# CsvLoader process
#   addNewWorkItem(self, work_item)
#       not supported in CsvLoader
#   work_item = class.getNextWorkItem()
#       return None -> no more work for now
#       return a work_item data, which should include enought info for other calls
#   processItem(work_item, my_span):
#       Process the work item
#   succeedWorkItem(work_item, my_span):
#       Mark the work_item as processed
#   failWorkItem(work_item, exc, my_span):
#       mark the work_item as failed
from app.classes.repository.mesureMeteor import MesureMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.xMaxMeteor import xMaxMeteor
from app.classes.repository.xMinMeteor import xMinMeteor
from datetime import timedelta
import app.tools.myTools as t
from app.tools.dateTools import str_to_datetime
from django.db import transaction
from django.conf import settings
import json
import csv
import os

import csvH_974


class CsvLoader:
    __file_spec = [
        csvH_974.CsvH_974()
    ]

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

    # ----------------
    # public methods
    # ----------------
    def addNewWorkItem(self, work_item):
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
        idx_file_spec = 0

        while idx_file_spec < len(self.__file_spec):
            if self.__file_spec[idx_file_spec].isItForMe(self.base_dir, a_filename) is True:
                return {
                    'f': a_filename,
                    'path': self.base_dir,
                    'spec': idx_file_spec,
                    'spanID': 'load of ' + a_filename,
                    'info': a_filename
                }
            idx_file_spec += 1

        Exception("No file spec found for " + a_filename)

    def succeedWorkItem(self, work_item, my_span):
        # move the file to archive
        target_dir = self.archive_dir + "/meteoFR/"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        os.rename(self.base_dir + "/" + work_item['f'], target_dir + work_item['f'])

    def failWorkItem(self, work_item, exc, my_span):
        # move the file to failed archive
        t.logException(exc, my_span)
        target_dir = self.archive_dir + "/meteoFR/failed/"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        os.rename(self.base_dir + "/" + work_item['f'], target_dir + work_item['f'])

        j_info = {"filename": work_item['f'], "dest": target_dir}
        t.logError('CsvLoader', "file moved to failed directory", None, j_info)
        IncidentMeteor.new('_getJsonFileNameAndData', 'error', 'file ' + work_item['f'] + ' moved to failed directory', j_info)

    # Commit ttx every 1000 insert
    def processWorkItem(self, work_item: json, my_span):
        cur_spec = self.__file_spec[work_item['spec']]
        cur_spec.loadCsv(work_item['path'], work_item['f'])

        my_span.set_attribute('file', work_item['f'])
        work_item['is_loaded'] = False

        b_continue = True
        while b_continue:
            b_continue = self.processWorkItemTtx(work_item, cur_spec, my_span)

    @transaction.atomic
    def processWorkItemTtx(self, work_item: json, cur_spec, my_span):
        ttx_count = 0

        while True:
            try:
                cur_poste, j_stop_dat_utc, fields_dict = cur_spec.nextLine()

                if self.load_a_row_indb(cur_poste, fields_dict, j_stop_dat_utc) is True:
                    ttx_count += 1

            finally:
                if ttx_count >= 1000:
                    return True

        work_item['is_loaded'] = True
        return False

    def load_a_row_indb(self, cur_poste, fields_dict, stop_dat_utc):
        b_one_insert = False
        for a_value in fields_dict:
            # t[my_mesure['name']] = {'idx': tmp_idx, 'mid': my_mesure['id'], 'val': float(a_field)}

            # -> check if data already loaded for this poste+date+mid
            if ObsMeteor.countObsForAMesure(cur_poste.data.id, stop_dat_utc, a_value['mid']) > 0:
                # data already loaded
                continue

            my_mesure = self.__my_mesures[a_value['idx']]

            cur_val, cur_q_val, date_obs = self.get_valeurs(my_mesure, my_mesure['val'], stop_dat_utc)
            if cur_val is None:
                continue
            stop_dat_local = stop_dat_utc + timedelta(hours=cur_poste.data.delta_timezone)

            new_obs = ObsMeteor(-1)
            new_obs.data.poste_id = cur_poste.data.id
            new_obs.data.mesure_id = my_mesure['id']
            new_obs.data.duration = 60
            new_obs.data.value = cur_val
            new_obs.data.qa_value = cur_q_val
            new_obs.data.date_utc = stop_dat_utc
            new_obs.data.date_local = stop_dat_local
            b_one_insert = True
            new_obs.save()

            cur_min, cur_min_time, cur_min_obs_id = self.get_valeur_min(my_mesure, my_mesure['val'], cur_val, stop_dat_local, new_obs.data.id)
            cur_max, cur_max_time, cur_max_dir, cur_max_obs_id = self.get_valeur_max(my_mesure, my_mesure['val'], cur_val, stop_dat_local, new_obs.data.id)

            if cur_min is not None:
                new_min = xMinMeteor(-1)
                new_min.data.poste_id = cur_poste.data.id
                new_min.data.mesure_id = my_mesure['id']
                new_min.data.date_local = cur_min_time + timedelta(hours=cur_poste.data.delta_timezone)
                new_min.data.date_utc = cur_min_time
                new_min.data.min = cur_min
                new_min.data.min_time = cur_min_time
                new_min.data.obs_id = cur_min_obs_id
                new_min.data.save()

            if cur_max is not None:
                new_max = xMaxMeteor(-1)
                new_max.data.poste_id = cur_poste.data.id
                new_max.data.mesure_id = my_mesure['id']
                new_max.data.date_local = cur_max_time + timedelta(hours=cur_poste.data.delta_timezone)
                new_max.data.date_utc = cur_max_time
                new_max.data.max = cur_max
                new_max.data.max_time = cur_max_time
                new_max.data.max_dir = cur_max_dir
                new_max.data.obs_id = cur_max_obs_id
                new_max.data.save()

        return b_one_insert

    def get_valeurs(self, a_mesure, cur_csv, stop_dat, a_mesure_ori=None):
        # for omm values, get the underlying data
        if a_mesure['ommidx_csv'] is not None:
            return self.get_valeurs(self.mesures[a_mesure['ommidx_csv']], cur_csv, stop_dat, a_mesure)

        cur_val = cur_csv.get(' ' + a_mesure['csv_field']) if cur_csv.get(a_mesure['csv_field']) is None else cur_csv.get(a_mesure['csv_field'])
        if cur_val is None or cur_val == '':
            return None, None, None
        cur_qa = cur_csv.get(' Q' + a_mesure['csv_field']) if cur_csv.get(' Q' + a_mesure['csv_field']) is None else cur_csv.get(' Q' + a_mesure['csv_field'])

        obs_date = stop_dat + timedelta(hours=a_mesure['valdk'] if a_mesure_ori is None else a_mesure_ori['valdk'])

        return cur_val, cur_qa, obs_date

    def get_valeur_min(self, a_mesure, cur_csv, cur_val, stop_dat, obs_id):
        # for omm values, get the underlying data
        if a_mesure['min'] is not True:
            return None, None, None

        cur_min = cur_val
        cur_min_time = stop_dat
        cur_min_field = a_mesure['csv_minmax'].get("min")
        cur_min_time_field = a_mesure['csv_minmax'].get("minTime")
        cur_min_obs_id = obs_id

        if cur_min_field is not None and cur_min_field != '':
            tmp_min = cur_csv[cur_min_field]
            if tmp_min != '' and tmp_min is not None:
                cur_min = float(tmp_min)
                cur_min_obs_id = None

        if cur_min_time_field is not None and cur_min_time_field != '':
            tmp_min_time = cur_csv[cur_min_time_field]
            if tmp_min_time != '' and tmp_min_time is not None:
                while len(tmp_min_time) < 4:
                    tmp_min_time = '0' + tmp_min_time
                tmp_dt = cur_csv["AAAAMMJJHH"]
                cur_min_time = str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[4:6] + '-' + tmp_dt[6:8] + 'T' + tmp_dt[8:10] + ':' + tmp_min_time[0:2] + ':' + tmp_min_time[2:4])
                cur_min_time = cur_min_time + timedelta(hours=a_mesure['mindk'])

        return cur_min, cur_min_time, cur_min_obs_id

    def get_valeur_max(self, a_mesure, cur_csv, cur_val, stop_dat, obs_id):
        # for omm values, get the underlying data
        if a_mesure['max'] is not True:
            return None, None, None, None

        cur_max = cur_val
        cur_max_time = stop_dat
        cur_max_dir = None
        cur_max_field = a_mesure['csv_minmax'].get("max")
        cur_max_time_field = a_mesure['csv_minmax'].get("maxTime")
        cur_max_dir_field = a_mesure['csv_minmax'].get("maxDir")
        cur_max_obs_id = obs_id

        if cur_max_field is not None:
            tmp_max = cur_csv[cur_max_field]
            if tmp_max != '' and tmp_max is not None:
                cur_max_obs_id = None
                cur_max = float(tmp_max)

        if cur_max_time_field is not None:
            tmp_max_time = cur_csv[cur_max_time_field]
            if tmp_max_time != '' and tmp_max_time is not None:
                while len(tmp_max_time) < 4:
                    tmp_max_time = '0' + tmp_max_time
                tmp_dt = cur_csv["AAAAMMJJHH"]
                cur_max_time = str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[4:6] + '-' + tmp_dt[6:8] + 'T' + tmp_dt[8:10] + ':' + tmp_max_time[0:2] + ':' + tmp_max_time[2:4])
                cur_max_time = cur_max_time + timedelta(hours=a_mesure['maxdk'])

        if cur_max_dir_field is not None:
            tmp_dir = cur_csv[cur_max_dir_field]
            if tmp_dir != '' and tmp_dir is not None:
                cur_max_dir = float(tmp_dir)

        return cur_max, cur_max_time, cur_max_dir, cur_max_obs_id
