from abc import ABC, abstractmethod
from app.classes.repository.mesureMeteor import MesureMeteor
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.repository.obsMeteor import ObsMeteor
from app.models import Aggreg_Type, Code_QA as QA, Load_Type
from app.tools.dateTools import str_to_datetime
from app.tools.dbTools import getPGConnexion
from app.tools.jsonValidator import checkJson
from datetime import timedelta
from enum import Enum
import app.tools.myTools as t
import json


class IDX(Enum):
    IDX_VAL = 0
    IDX_QVAL = 1
    IDX_DIR = 2
    IDX_QDIR = 3
    IDX_VALMIN = 4
    IDX_QVALMIN = 5
    IDX_MIN_TIME = 6
    IDX_VALMAX = 7
    IDX_QVALMAX = 8
    IDX_MAX_TIME = 9
    IDX_MAX_DIR = 10
    IDX_DURATION = 11
    IDX_OBS_MIN = 12
    IDX_OBS_MAX = 13


class JsonLoaderABC(ABC):
    def __init__(self):
        # save mesures definition
        self.mesures = MesureMeteor.getDefinitions()
        self.insert_cde = None
        
        # boolean to stop processing files
        self.stopRequested = False

    def processJson(self, work_item: json):
        work_item['is_loaded'] = False
        filename = work_item['f']
        jsons_to_load = work_item['json']
        idx_global = 0
        cur_meteor = "inconnu"

        check_result = checkJson(jsons_to_load, filename)
        if check_result is not None:
            raise Exception("Error in Json file: " + filename + ": " + check_result)

        while idx_global < jsons_to_load.__len__():
            try:
                json_to_load = jsons_to_load[idx_global]
                meteor = '{0}'.format(json_to_load.get("meteor"))

                if meteor != cur_meteor:
                    cur_poste = PosteMeteor(meteor)
                    if cur_poste.data is None or cur_poste.data.load_type is None:
                        raise Exception("code meteor inconnu: " + meteor + ', idx_global: ' + '{0}'.format(idx_global) + ' dans le fichier: ' + filename)

                    if (cur_poste.data.load_type & Load_Type.LOAD_FROM_JSON.value) != Load_Type.LOAD_FROM_JSON.value:
                        t.logInfo('jsonload: ' + meteor + ' inactif json_load is False), skipping file ' + filename)
                        return

                    cur_meteor = meteor

                idx_data = 0
                while idx_data < json_to_load['data'].__len__():
                    try:
                        a_work_item = json_to_load['data'][idx_data]

                        # get data from our json item
                        j_stop_dat_local = a_work_item["stop_dat"]
                        stop_date = str_to_datetime(j_stop_dat_local)
                        j_duration = a_work_item["duration"]

                        if (cur_poste.data.load_type & Load_Type.LOAD_FROM_DUMP_THEN_JSON.value) == Load_Type.LOAD_FROM_DUMP_THEN_JSON.value:
                            if cur_poste.data.last_json_date_local > j_stop_dat_local:
                                cur_poste.data.last_json_date_local = j_stop_dat_local
                                cur_poste.data.save()
                            if j_stop_dat_local > cur_poste.data.last_obs_date_local:
                                work_item['WAIT_LIST'] = True
                                # Keep the older JSON date
                                t.logInfo('jsonload: ' + meteor + ' file ' + filename + ' moved to waiting directory, stop_date: ' + '{0}'.format(j_stop_dat_local))
                            return

                        if work_item.get('FORCE_LOAD') is not None and work_item['FORCE_LOAD'] is True:
                            if ObsMeteor.count_obs_poste_local(cur_poste.data.id, stop_date) > 0:
                                raise Exception("jsonload: " + meteor + " skipping data already loaded from " + filename + ", stop_date: " + stop_date)
                            else:
                                # we process our file
                                pass
                        elif cur_poste.data.last_obs_date_local is not None and j_stop_dat_local <= cur_poste.data.last_obs_date_local:
                            t.logInfo('jsonload: ' + meteor + ' skipping data already loaded from ' + filename + ', stop_date: ' + stop_date + ', last_obs_date_local: ' + '{0}'.format(cur_poste.data.last_obs_date_local))
                            return

                        self.loadObsData(cur_poste, a_work_item['valeurs'], j_stop_dat_local, j_duration)

                    finally:
                        idx_data += 1

            finally:
                idx_global += 1

        work_item['is_loaded'] = True

    def loadObsData(self, cur_poste, j_data, stop_dat_local, duration):
        data_args = []
        min_data = []
        max_data = []
        pg_conn = getPGConnexion()
        pg_cur = pg_conn.cursor()
        self.loadSqlInsert()

        try:
            stop_date_utc = stop_dat_local - timedelta(hours=cur_poste.data.delta_timezone)
            values_arg = ['{0}'.format(cur_poste.data.id), '{0}'.format(stop_date_utc), '{0}'.format(stop_dat_local), '{0}'.format(duration)]

            for a_mesure in self.mesures:
                if self.isMesureQualified(a_mesure) is False:
                    continue

                cur_vals = self.get_valeurs(a_mesure, j_data, stop_dat_local, duration)
                if cur_vals[0] is None:
                    if a_mesure.get("json_input_bis") is not None and a_mesure['json_input_bis'] is not None:
                        cur_vals = self.get_valeurs(a_mesure, j_data, stop_dat_local, duration, True)

                if cur_vals[0] is None:
                    values_arg.append(None)
                    continue

                values_arg.append('{0}'.format(cur_vals[0]))

                if a_mesure['min'] is not None and a_mesure['min'] is True:
                    min_data.append([
                        '{0}'.format(cur_vals[IDX.IDX_OBS_MIN.value]) if cur_vals[IDX.IDX_OBS_MIN.value] is not None else None,
                        '{0}'.format(stop_dat_local.date()),
                        '{0}'.format(cur_poste.data.id),
                        '{0}'.format(a_mesure['id']),
                        '{0}'.format(cur_vals[IDX.IDX_VALMIN.value]),
                        '{0}'.format(cur_vals[IDX.IDX_MIN_TIME.value]),
                        '{0}'.format(cur_vals[IDX.IDX_QVALMIN.value])])

                if a_mesure['max'] is not None and a_mesure['max'] is True:
                    max_data.append([
                        '{0}'.format(cur_vals[IDX.IDX_OBS_MAX.value]) if cur_vals[IDX.IDX_OBS_MAX.value] is not None else None,
                        '{0}'.format(stop_dat_local.date()),
                        '{0}'.format(cur_poste.data.id),
                        '{0}'.format(a_mesure['id']),
                        '{0}'.format(cur_vals[IDX.IDX_VALMAX.value]),
                        '{0}'.format(cur_vals[IDX.IDX_MAX_TIME.value]),
                        '{0}'.format(cur_vals[IDX.IDX_QVALMAX.value]),
                        '{0}'.format(cur_vals[IDX.IDX_MAX_DIR.value]) if cur_vals[IDX.IDX_MAX_DIR.value] is not None else None])

            values_arg.append('{0}'.format(QA.UNSET.value))
            data_args.append(tuple(values_arg))

            # cursor.mogrify() to insert multiple values
            args = ','.join(pg_cur.mogrify(self.insert_cde['mog'], i).decode('utf-8') for i in data_args)

            pg_cur.execute(self.insert_cde['sql'] + args + ' returning id')
            new_ids = pg_cur.fetchall()

            idx = 0
            while idx <len(min_data):
                if  min_data[idx][0] is not None:
                    min_data[idx][0] = new_ids[0][0]
                idx += 1

            idx = 0
            while idx <len(max_data):
                if  max_data[idx][0] is not None:
                    max_data[idx][0] = new_ids[0][0]
                idx += 1

            min_args_ok = ','.join(pg_cur.mogrify(self.insert_cde_min_mog, i).decode('utf-8') for i in min_data)
            max_args_ok = ','.join(pg_cur.mogrify(self.insert_cde_max_mog, i).decode('utf-8') for i in max_data)

            pg_cur.execute(self.insert_cde_min + min_args_ok)
            pg_cur.execute(self.insert_cde_max + max_args_ok)

            pg_conn.commit()

        except Exception as e:
            pg_conn.rollback()
            raise e

        finally:
            pg_cur.close()
            pg_conn.close()

    def get_valeurs(self, a_mesure, valeurs, stop_dat, duration, use_second_input_key=False):
        #  [0]  [1]     [2]        [3]      [4]      [5]     [6]      [7]      [8]      [9]     [10]      [11]
        # val, qval, dir|None, adir|None, valmin, qvalmin, min_time, valmax, qvalmax, max_time, max_dir, duration

        suffix_avg = '_avg'
        suffix_sum = '_s'
        my_duration = None

        mesure_primary_key = mesure_key = a_mesure['json_input']

        # switch to json_imput_bis
        if use_second_input_key is True and a_mesure.get('json_input_bis') is not None:
            mesure_key = a_mesure['json_input_bis']
            # hack for measure gust -> wind_max, with max in wind_max_time/wind_max_dir
            if mesure_key.endswith('_max') or mesure_key.endswith('_min'):
                mesure_primary_key = mesure_key[:-4]

        # load keys index used to look for our value in order of importance
        j_keys = [mesure_key]
        if a_mesure['agreg_type'] == Aggreg_Type.AVG:
            j_keys = [mesure_key + suffix_avg, mesure_key, mesure_key + suffix_sum]
        elif a_mesure['agreg_type'] == Aggreg_Type.SUM:
            j_keys = [mesure_key + suffix_sum, mesure_key, mesure_key + suffix_avg]

        my_val = my_val_dir = None
        my_qval = my_qval_dir = QA.UNSET.value
        my_val_min = my_val_min_time = None
        my_val_max = my_val_max_time = my_val_max_dir = None
        my_qval_min = my_qval_max = QA.UNSET.value

        # get our value
        for a_key in j_keys:
            if valeurs.get(a_key) is not None:
                my_val = valeurs[a_key]
                my_duration = duration
                if a_mesure.get(a_key + '_s') is not None:
                    my_duration = a_mesure[a_key + '_s']
                if a_mesure['convert'] is not None and a_mesure['convert'].get('json') is not None:
                    my_val = eval(a_mesure['convert']['json'])(my_val)
                if valeurs.get('Q' + a_key) is not None:
                    my_qval = valeurs['Q' + a_key]
                if a_mesure['is_wind'] is True and valeurs.get(a_key + '_dir') is not None:
                    my_val_dir = valeurs[a_key + '_dir']
                    if valeurs.get('Q' + a_key + '_dir') is not None:
                        my_qval_dir = valeurs['Q' + a_key + '_dir']
                break

        # get our min
        if valeurs.get(mesure_primary_key + '_min') is not None or (a_mesure.get('agreg_type') == Aggreg_Type.MIN and valeurs.get(mesure_primary_key + '_min') is not None):
            my_val_min = valeurs[mesure_primary_key + '_min']
            my_val_min_time = valeurs[mesure_primary_key + '_min_time']
            if valeurs.get('Q' + mesure_primary_key + '_min') is not None:
                my_qval_min = valeurs['Q' + mesure_primary_key + '_min']
        else:
            if my_val is not None:
                my_val_min = my_val
                my_val_min_time = stop_dat

        # get our max
        if valeurs.get(mesure_primary_key + '_max') is not None or (a_mesure.get('agreg_type') == Aggreg_Type.MAX and valeurs.get(mesure_primary_key + '_max') is not None):
            my_val_max = valeurs[mesure_primary_key + '_max']
            my_val_max_time = valeurs[mesure_primary_key + '_max_time']
            if valeurs.get('Q' + mesure_primary_key + '_max') is not None:
                my_qval_max = valeurs['Q' + mesure_primary_key + '_max']
            if a_mesure['is_wind'] is True and valeurs.get(mesure_primary_key + '_max_dir') is not None:
                my_val_max_dir = valeurs[mesure_primary_key + '_max_dir']
        else:
            my_val_max = my_val
            my_val_max_time = stop_dat
            my_val_max_dir = my_val_dir

        return [
            my_val,
            my_qval,
            my_val_dir,
            my_qval_dir,
            my_val_min,
            my_qval_min,
            my_val_min_time,
            my_val_max,
            my_qval_max,
            my_val_max_time,
            my_val_max_dir,
            my_duration,
            -1,
            -1
        ]
  
    def loadSqlInsert(self):
        if self.insert_cde is None:
            # mog has a suppl parameter for qa_all
            self.insert_cde = {
                "sql": "insert into obs(poste_id, date_utc, date_local, duration",
                "mog": "(%s, %s, %s, %s"
            }
            for a_mesure in self.mesures:
                if self.isMesureQualified(a_mesure) is False:
                    continue

                self.insert_cde['sql'] += ", " + a_mesure['json_input']
                self.insert_cde['mog'] += ", %s"

            self.insert_cde['sql'] += ", qa_all) values "
            self.insert_cde['mog'] += ", %s)"
        self.insert_cde_min = "insert into x_min(obs_id, date_local, poste_id, mesure_id, min, min_time, qa_min) values "
        self.insert_cde_min_mog = "(%s, %s, %s, %s, %s, %s, %s)"
        self.insert_cde_max = "insert into x_max(obs_id, date_local, poste_id, mesure_id, max, max_time, qa_max, max_dir) values "
        self.insert_cde_max_mog = "(%s, %s, %s, %s, %s, %s, %s, %s)"

    def isMesureQualified(self, a_measure):
        if a_measure['json_input'] == 'rain_utc':
            return False
        return False if a_measure['archive_col'] is None else True
