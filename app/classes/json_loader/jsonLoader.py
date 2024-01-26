# JsonLoader process
#   addNewWorkItem(self, work_item)
#       not supported in jsonLoader
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
from app.tools.jsonValidator import checkJson
from app.tools.dateTools import str_to_datetime
import datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import app.tools.myTools as t
from app.tools.jsonPlus import JsonPlus
from django.db import transaction
from django.conf import settings
import json
import os


class JsonLoader:
    def __init__(self):
        # save mesures definition
        self.mesures = MesureMeteor.getDefinitions()

        # boolean to stop processing files
        self.stopRequested = False

        # get directories settings
        if hasattr(settings, "JSON_AUTOLOAD") is True:
            self.base_dir = settings.JSON_AUTOLOAD
        else:
            self.base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/json_auto_load")

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
            if str(filename).endswith('.json'):
                file_names.append(filename)

        # stop processing
        if len(file_names) == 0:
            return None

        file_names = sorted(file_names)
        a_filename = file_names[0]
        # load our json file
        texte = ""

        with open(self.base_dir + '/' + a_filename, "r") as f:
            lignes = f.readlines()
            for aligne in lignes:
                texte += str(aligne)
        my_json = JsonPlus().loads(texte)
        if 'dict' in str(type(my_json)):
            my_json = [my_json]

        meteor = 'inconnu'
        try:
            meteor = str(a_filename).split(".")[1]
        except Exception:
            pass

        return {
            'f': a_filename,
            'json': my_json,
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

        # refresh our materialized view
        pgconn = self.getPGConnexion()
        pgconn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        pg_cur = pgconn.cursor()

        start_tm = datetime.datetime.now()
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_hour')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_month')))

        my_span.add_event('jsonloader', work_item['f'] + ': refresh_continuous_aggregate: ' + str(datetime.datetime.now() - start_tm) + ' ms')

        pg_cur.close()
        pgconn.commit()
        pgconn.close()

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
        t.logError('jsonloader', "file moved to fail directory", None, j_info)
        IncidentMeteor.new('_getJsonFileNameAndData', 'error', 'file ' + work_item['f'] + ' moved to failed directory', j_info)

    @transaction.atomic
    def processWorkItem(self, work_item: json, my_span):
        work_item['is_loaded'] = False
        filename = work_item['f']
        jsons_to_load = work_item['json']
        idx_global = 0
        meteor = str(jsons_to_load[0].get("meteor"))
        if meteor == 'None':
            raise Exception('invalid format, unreadable meteor key ' + filename)
        pid = PosteMeteor.getPosteIdByMeteor(jsons_to_load[0]["meteor"])
        b_load = PosteMeteor(pid).data.load_raw_data
        if b_load is False:
            my_span.add_event('jsonload', meteor + ' inactif json_load is False), skipping file ' + filename)
            return
        my_span.set_attribute('file', filename)
        my_span.set_attribute('meteor', meteor)
        check_result = checkJson(jsons_to_load, pid, filename)
        if check_result is not None:
            my_span.set_event('check_json', check_result)
            raise Exception("Invalid Json file: " + filename + ": " + check_result)

        while idx_global < jsons_to_load.__len__():
            try:
                json_to_load = jsons_to_load[idx_global]
                meteor = str(json_to_load.get("meteor"))
                cur_poste = PosteMeteor.getPosteByMeteor(json_to_load["meteor"])
                pid = cur_poste.data.id
                if pid is None:
                    raise Exception("code meteor inconnu: " + meteor + ', idx_global: ' + str(idx_global))
                poste_tz = cur_poste.data.delta_timezone

                idx_data = 0
                while idx_data < json_to_load['data'].__len__():
                    try:
                        a_work_item = json_to_load['data'][idx_data]

                        # get data from our json item
                        j_stop_dat = a_work_item["stop_dat"]
                        stop_date = str_to_datetime(j_stop_dat)
                        j_duration = a_work_item["duration"]

                        # Load the obs we need in cache
                        all_obs = ObsMeteor.load_obs(pid, stop_date)

                        # load attributes in our sub_spam
                        my_span.set_attribute("stop_dat", str(j_stop_dat))

                        # NCNC -> futur: check if stop_dat in range ]time-duration, time]

                        # check if json already loaded on the main obs in cache
                        if all_obs[0]['obs'].data.duration != 0:
                            if a_work_item.__contains__("force_replace") is not True:
                                t.logInfo(
                                        'already loaded', my_span,
                                        {'meteor': meteor, 'file': filename, 'idx': idx_data, 'stop_dat': str(j_stop_dat)})
                                continue
                            else:
                                # delete our obs, and linked extremes and obs
                                all_obs[0]['obs'].data.delete()

                                # reload a new set of obs (first will be new now)
                                all_obs = ObsMeteor.load_all_needed_obs(pid, self.decas, j_stop_dat, poste_tz)

                        all_obs[0]['obs'].data.duration = j_duration
                        # all_obs[0]['obs'].data.save()

                        keys_found = self.load_obs_data_j(pid, all_obs, a_work_item['valeurs'], j_stop_dat)
                        if keys_found is not None:
                            # t.logInfo("keys loaded from json: " + str(keys_found), my_span)
                            pass
                        else:
                            t.logError("jsonloder", "no keys loaded !!!", my_span)

                        # save obs, store dependencies in histoObs
                        histo_obs_new = []
                        histo_x_new = []
                        idx_obs_all = 0
                        while idx_obs_all < len(all_obs):
                            an_obs = all_obs[idx_obs_all]
                            an_obs['obs'].data.save()
# save id to x_min/max

                        my_span.add_event('jsonload', "file: " + filename + " DONE")
                        my_span.add_event('obs', 'new rows: ' + str(len(histo_obs_new)))
                        # my_span.add_event('histo', "new rows: " + str(len(histo_x_new)))
                        my_span.add_event('histo_extreme', "new rows: " + str(len(histo_x_new)))
                        histo_obs_new = []
                        histo_x_new = []

                    finally:
                        idx_data += 1

            finally:
                idx_global += 1

        work_item['is_loaded'] = True

    def load_obs_data_j(self, pid, all_obs, valeurs, stop_dat):
        keys_found = []
        for a_mesure in self.mesures:
            cur_vals = self.get_valeurs(a_mesure, valeurs, stop_dat)
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

    def get_cur_obs_idx(self, all_obs, a_mesure):
        return 0

    def insert_extremes(self, pid, a_mesure, x_data):
        # x_row = None
        # for a_data in x_data:
        #     if a_mesure[a_data['col']] is True and (a_data['v'] is not None and a_data['t'] is not None):
        #         x_date_key = a_data['t'] + timedelta(hours=a_mesure[a_data['col'] + 'dk'])
        #         x_date_key = x_date_key.date()
        #         if x_row is None or x_row.data.date != x_date_key:
        #             if x_row is not None:
        #                 x_row.data.save()
        #             x_row = ExtremeMeteor.get_extreme(pid, a_mesure['id'], x_date_key)
        #         if (a_data['col'] == 'min' and
        #                 (hasattr(x_row.data, a_data['col']) is False or
        #                  x_row.data.__getattribute__(a_data['col']) is None or
        #                  a_data['v'] < x_row.data.__getattribute__(a_data['col']))) or \
        #            (a_data['col'] == 'max' and
        #                 (hasattr(x_row.data, a_data['col']) is False or
        #                  x_row.data.__getattribute__(a_data['col']) is None or
        #                  a_data['v'] > x_row.data.__getattribute__(a_data['col']))):
        #             # set the new value for the extreme
        #             b_insert_histo = True
        #             x_row.data.__setattr__(a_data['col'], a_data['v'])
        #             x_row.data.__setattr__(a_data['col'] + '_time', a_data['t'])
        #             if a_data['d'] is not None:
        #                 x_row.data.__setattr__(a_data['col'] + '_dir', a_data['d'])

        # if x_row is not None:
        #     x_row.data.save()
        #     if b_insert_histo is True:
        #         b_insert_histo = False
        return

    def getPGConnexion(self):
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Funiculi",
            database="climato"
        )
