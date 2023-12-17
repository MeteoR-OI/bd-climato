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
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.repository.obsMeteor import ObsMeteor
from app.classes.repository.extremeMeteor import ExtremeMeteor
from app.tools.jsonValidator import checkJson
import psycopg2
from datetime import timedelta
import app.tools.myTools as t
from app.tools.jsonPlus import JsonPlus
from app.tools.dateTools import str_to_date
from django.db import transaction
from django.conf import settings
import json
import csv
import os


class CsvLoader:
    def __init__(self):
        # save mesures definition
        self.mesures = []
        for a_mesure in MesureMeteor.getDefinitions():
            if a_mesure['csv_field'] is not None:
                self.mesures.append(a_mesure)

        self.decas = MesureMeteor.getAllDecas()

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
        # load our json file
        my_csv = []

        with open(self.base_dir + '/' + a_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                print(str(row))
                my_csv.append(row)
                
        meteor = 'inconnu'

        return {
            'f': a_filename,
            'csv': my_csv,
            'spanID': 'load of ' + a_filename,
            'meteor': meteor,
            'info': a_filename
        }

    def succeedWorkItem(self, work_item, my_span):
        # move the file to archive
        str_annee = 'inconnu'
        str_mois = 'inconnu'
        meteor = 'inconnu'
        try:
            str_annee = str(work_item['f']).split(".")[2].split("-")[0]
            str_mois = str(work_item['f']).split(".")[2].split("-")[1]
            meteor = str(work_item['f']).split(".")[1]
        except Exception:
            pass

        tmp_prefix = ""
        if work_item.get('is_loaded') is not None and work_item['is_loaded'] is not False:
            tmp_prefix = "/skipped/"

        filename_prefix = self.archive_dir + "/" + meteor + tmp_prefix + "/" + str_annee + "/" + str_mois + "/"
        if not os.path.exists(filename_prefix):
            os.makedirs(filename_prefix)

        os.rename(self.base_dir + "/" + work_item['f'], filename_prefix + work_item['f'])

    def failWorkItem(self, work_item, exc, my_span):
        meteor = 'inconnu'
        try:
            meteor = str(work_item['f']).split(".")[1]
        except Exception:
            pass

        t.logException(exc, my_span)

        str_annee = 'inconnu'
        str_mois = 'inconnu'
        meteor = 'inconnu'
        try:
            str_annee = str(work_item['f']).split(".")[2].split("-")[0]
            str_mois = str(work_item['f']).split(".")[2].split("-")[1]
            meteor = str(work_item['f']).split(".")[1]
        except Exception:
            pass

        tmp_prefix = "/failed"
        filename_prefix = self.archive_dir + "/" + meteor + tmp_prefix + "/" + str_annee + "/" + str_mois + "/"
        if not os.path.exists(filename_prefix):
            os.makedirs(filename_prefix)
        os.rename(self.base_dir + "/" + work_item['f'], filename_prefix + work_item['f'])

        j_info = {"filename": work_item['f'], "dest": self.archive_dir + "/" + meteor + "/failed/" + work_item['f']}
        t.logError('CsvLoader', "file moved to fail directory", None, j_info)
        IncidentMeteor.new('_getJsonFileNameAndData', 'error', 'file ' + work_item['f'] + ' moved to failed directory', j_info)

    @transaction.atomic
    def processWorkItem(self, work_item: json, my_span):
        work_item['is_loaded'] = False
        filename = work_item['f']
        csvs_to_load = work_item['csv']
        idx_global = 1  # skip first line
        last_meteor = "??? Not Set ???"
        my_span.set_attribute('file', filename)
        cur_poste = None

        while idx_global < csvs_to_load.__len__():
            try:
                cur_csv = csvs_to_load[idx_global]
                meteor = cur_csv["NOM_USUEL"]
                if meteor != last_meteor:
                    cur_poste = PosteMeteor.getPosteIdByMeteor(meteor)
                    if cur_poste is None:
                        # Create on the flight a new poste
                        cur_poste = PosteMeteor(meteor)
                        cur_poste.data.data_source = 1
                        cur_poste.data.type = "inconnu"
                        cur_poste.data.altitude = cur_csv["ALTI"]
                        cur_poste.data.lat = cur_csv["LAT"]
                        cur_poste.data.long = cur_csv["LON"]
                        cur_poste.data.other_code = cur_csv["NUM_POSTE"]
                        cur_poste.data.owner = "Meteo France"
                        cur_poste.data.delta_timezone = 4
                        cur_poste.data.save()
                        cur_poste = PosteMeteor.getPosteIdByMeteor(meteor)
                    last_meteor = meteor
                    my_span.event('load CSV for', last_meteor)
                    my_span.set_attribute('meteor', meteor)

                tmp_dt = cur_csv["AAAAMMJJHHMM"]
                j_stop_dat = str_to_date(tmp_dt[0:4] + '-' + tmp_dt[4:6] + '-' + tmp_dt[6:8] + 'T' + tmp_dt[8:10] + ':' + tmp_dt[10:12] + ':00')

                # -> check if data already loaded for this poste+date
                if ObsMeteor.count_obs_poste_date(cur_poste.data.id, j_stop_dat) > 0:
                    # data already loaded
                    continue

                self.load_obs_data_j(cur_poste, cur_csv, j_stop_dat)

            finally:
                idx_global += 1

        work_item['is_loaded'] = True

    def load_obs_data_j(self, cur_poste, cur_csv, stop_dat):
        for a_mesure in self.mesures:
            NICO
            cur_vals = self.get_valeurs(a_mesure, cur_csv, stop_dat)
            cur_obs_idx = self.get_cur_obs_idx(all_obs, a_mesure)
            cur_obs = all_obs[cur_obs_idx]

            # if current value is None, try with the second input key
            if cur_vals[0] is None:
                if a_mesure.get("col2") is not None and a_mesure['col2'] is not None:
                    cur_vals = self.get_valeurs(a_mesure, valeurs, stop_dat, False, True)

            # store the value in the observation data
            if cur_vals[0] is not None:
                cur_obs['obs'].data.__setattr__(a_mesure['col'], cur_vals[0])
                if a_mesure['iswind'] is True and cur_vals[1] is not None:
                    cur_obs['obs'].data.__setattr__(a_mesure['col'] + '_dir', cur_vals[1])
                keys_found.append(a_mesure['col'])

            # store min/max
            self.insert_extremes(
                pid,
                histo_x_list[cur_obs_idx],
                a_mesure,
                [
                    {'col': 'min', 'v': cur_vals[2], 't': cur_vals[3], 'd': None},
                    {'col': 'max', 'v': cur_vals[4], 't': cur_vals[5], 'd': cur_vals[6]}
                ]
            )
        return None if keys_found.__len__ == 0 else keys_found

    def get_valeurs(self, a_mesure, valeurs, stop_dat, force_abs=False, use_second_input_key=False):
        #  [0]   [1]       [2]     [3]      [4]      [5]       [6]
        # val, dir|None, valmin, min_time, valmax, max_time, max_dir

        # for omm values, get the underlying data
        if a_mesure['ommidx'] is not None:
            return self.get_valeurs(self.mesures[a_mesure['ommidx']], valeurs, stop_dat, True, use_second_input_key)

        # if a_mesure['col'] == 'rain':
        #     print('rain')

        suffix_key1 = '_avg'
        suffix_key2 = '_s'

        mesure_key = a_mesure['col']
        if use_second_input_key is True and a_mesure.get('col2') is not None and a_mesure['col2'] is not None:
            mesure_key = a_mesure['col2']

        # load keys used to look for our value in order of importance
        if force_abs is True or a_mesure['isavg'] is False:
            j_keys = [mesure_key + suffix_key2, mesure_key, mesure_key + suffix_key1]
        else:
            j_keys = [mesure_key + suffix_key1, mesure_key, mesure_key + suffix_key2]

        my_val = None
        my_val_dir = None
        my_val_min = my_val_min_time = None
        my_val_max = my_val_max_time = my_val_max_dir = None

        # get our value
        for a_key in j_keys:
            if valeurs.get(a_key) is not None:
                my_val = valeurs[a_key]
                if a_mesure['iswind'] is True and valeurs.get(a_key + '_dir') is not None:
                    my_val_dir = valeurs[a_key + '_dir']
                break

        # get our min
        if valeurs.get(mesure_key + '_min') is not None:
            my_val_min = valeurs[mesure_key + '_min']
            my_val_min_time = valeurs[mesure_key + '_min_time']
        else:
            if my_val is not None:
                my_val_min = my_val
                my_val_min_time = stop_dat

        # get our max
        if valeurs.get(mesure_key + '_max') is not None:
            my_val_max = valeurs[mesure_key + '_max']
            my_val_max_time = valeurs[mesure_key + '_max_time']
            if a_mesure['iswind'] is True and valeurs.get(mesure_key + '_max_dir') is not None:
                my_val_max_dir = valeurs[mesure_key + '_max_dir']
        else:
            if my_val is not None:
                my_val_max = my_val
                my_val_max_time = stop_dat
                my_val_max_dir = my_val_dir

        return [my_val, my_val_dir, my_val_min, my_val_min_time, my_val_max, my_val_max_time, my_val_max_dir]


    def insert_extremes(self, pid, x_histo_array, a_mesure, x_data):
        x_row = None
        b_insert_histo = False
        for a_data in x_data:
            if a_mesure[a_data['col']] is True and (a_data['v'] is not None and a_data['t'] is not None):
                x_date_key = a_data['t'] + timedelta(hours=a_mesure[a_data['col'] + 'dk'])
                x_date_key = x_date_key.date()
                if x_row is None or x_row.data.date != x_date_key:
                    if x_row is not None:
                        x_row.data.save()
                        if b_insert_histo is True:
                            x_histo_array.append(x_row.data.id)
                            b_insert_histo = False
                    x_row = ExtremeMeteor.get_extreme(pid, a_mesure['id'], x_date_key)
                if (a_data['col'] == 'min' and
                        (hasattr(x_row.data, a_data['col']) is False or
                         x_row.data.__getattribute__(a_data['col']) is None or
                         a_data['v'] < x_row.data.__getattribute__(a_data['col']))) or \
                   (a_data['col'] == 'max' and
                        (hasattr(x_row.data, a_data['col']) is False or
                         x_row.data.__getattribute__(a_data['col']) is None or
                         a_data['v'] > x_row.data.__getattribute__(a_data['col']))):
                    # set the new value for the extreme
                    b_insert_histo = True
                    x_row.data.__setattr__(a_data['col'], a_data['v'])
                    x_row.data.__setattr__(a_data['col'] + '_time', a_data['t'])
                    if a_data['d'] is not None:
                        x_row.data.__setattr__(a_data['col'] + '_dir', a_data['d'])

        if x_row is not None:
            x_row.data.save()
            if b_insert_histo is True:
                x_histo_array.append(x_row.data.id)
                b_insert_histo = False

    def getPGConnexion(self):
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Funiculi",
            database="climato"
        )
