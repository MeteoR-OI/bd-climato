from abc import ABC, abstractmethod
from app.classes.repository.mesureMeteor import MesureMeteor
from app.models import Aggreg_Type, Code_QA as QA
import psycopg2
from datetime import timedelta
from django.conf import settings
import os
from enum import Enum
from app.tools.dbTools import getPGConnexion


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


class JsonDataLoader(ABC):
    @abstractmethod
    def getConvertKey(self):
        Exception("getConvertKey not implemented")

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

    def loadObsData(self, cur_poste, j_data, stop_dat_local, duration):
        obs_data = []
        min_data = []
        max_data = []
        idx_min_map = []
        idx_max_map = []
        pg_conn = getPGConnexion()
        pg_cur = pg_conn.cursor()
        sql_insert = "insert into obs(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value) values "
        insert_cde_min = "insert into x_min(obs_id, date_local, poste_id, mesure_id, min, min_time, qa_min) values "
        insert_cde_max = "insert into x_max(obs_id, date_local, poste_id, mesure_id, max, max_time, qa_max, max_dir) values "

        try:
            for a_mesure in self.mesures:
                if a_mesure['id'] in (60,61):
                    pass
                cur_vals = self.get_valeurs(a_mesure, j_data, stop_dat_local)
                if cur_vals[0] is None:
                    if a_mesure.get("col2") is not None and a_mesure['col2'] is not None:
                        cur_vals = self.get_valeurs(a_mesure, j_data, stop_dat_local, True)

                if cur_vals[0] is None:
                    continue

                obs_data.append(
                    [   cur_poste.data.id,
                        stop_dat_local - timedelta(hours=cur_poste.data.delta_timezone),
                        stop_dat_local,
                        a_mesure['id'],
                        duration if cur_vals[IDX.IDX_DURATION] is None else cur_vals[IDX.IDX_DURATION],
                        cur_vals[IDX.IDX_VAL.value],
                        cur_vals[IDX.IDX_QVAL.value]
                    ])

                if a_mesure['min'] is not None and a_mesure['min'] is True:
                    min_data.append([
                        None,
                        stop_dat_local.date(),
                        cur_poste.data.id,
                        a_mesure['id'],
                        cur_vals[IDX.IDX_VALMIN.value],
                        cur_vals[IDX.IDX_MIN_TIME.value],
                        cur_vals[IDX.IDX_QVALMIN.value]])
                    idx_min_map.append(len(min_data) - 1)
                else:
                    idx_min_map.append(None)

                if a_mesure['max'] is not None and a_mesure['max'] is True:
                    max_data.append([
                        None,
                        stop_dat_local.date(),
                        cur_poste.data.id,
                        a_mesure['id'],
                        cur_vals[IDX.IDX_VALMAX.value],
                        cur_vals[IDX.IDX_MAX_TIME.value],
                        cur_vals[IDX.IDX_QVALMAX.value],
                        cur_vals[IDX.IDX_MAX_DIR.value]])
                    idx_max_map.append(len(max_data) - 1)
                else:
                    idx_max_map.append(None)

            if len(obs_data) == 0:
                return

            # cursor.mogrify() to insert multiple values
            args = ','.join(pg_cur.mogrify("( %s, %s, %s, %s, %s, %s, %s )", i).decode('utf-8') for i in obs_data)

            pg_cur.execute(sql_insert + args + ' returning id')
            new_ids = pg_cur.fetchall()

            idx = 0
            while idx < len(new_ids):
                if idx_min_map[idx] is not None:
                    min_data[idx_min_map[idx]][0] = new_ids[idx][0]
                if idx_max_map[idx] is not None:
                    max_data[idx_max_map[idx]][0] = new_ids[idx][0]
                idx += 1

            min_args_ok = ','.join(pg_cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in min_data)
            max_args_ok = ','.join(pg_cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in max_data)

            pg_cur.execute(insert_cde_min + min_args_ok)
            pg_cur.execute(insert_cde_max + max_args_ok)

            pg_conn.commit()

        except Exception as e:
            pg_conn.rollback()
            raise e

        finally:
            pg_cur.close()
            pg_conn.close()

    def get_valeurs(self, a_mesure, valeurs, stop_dat, use_second_input_key=False):
        #  [0]  [1]     [2]        [3]      [4]      [5]     [6]      [7]      [8]      [9]     [10]      [11]
        # val, qval, dir|None, adir|None, valmin, qvalmin, min_time, valmax, qvalmax, max_time, max_dir, duration

        suffix_avg = '_avg'
        suffix_sum = '_s'
        my_duration = None

        mesure_keys = a_mesure['col']
        if use_second_input_key is True and a_mesure.get('col2') is not None:
            mesure_keys = a_mesure['col2']

        # load keys index used to look for our value in order of importance
        j_keys = [mesure_keys]
        if a_mesure['agreg_type'] == Aggreg_Type.AVG:
            j_keys = [mesure_keys + suffix_avg, mesure_keys, mesure_keys + suffix_sum]
        elif a_mesure['agreg_type'] == Aggreg_Type.SUM:
            j_keys = [mesure_keys + suffix_sum, mesure_keys, mesure_keys + suffix_avg]

        my_val = my_val_dir = None
        my_qval = my_qval_dir = QA.UNSET.value
        my_val_min = my_val_min_time = None
        my_val_max = my_val_max_time = my_val_max_dir = None
        my_qval_min = my_qval_max = QA.UNSET.value

        # get our value
        for a_key in j_keys:
            if valeurs.get(a_key) is not None:
                my_val = valeurs[a_key]
                my_duration = a_mesure[a_key + '_s']
                if a_mesure['convert'] is not None and a_mesure['convert'].get(self.getConvertKey()) is not None:
                    my_val = eval(a_mesure['convert'][self.getConvertKey()])(my_val)
                if valeurs.get('Q' + a_key) is not None:
                    my_qval = valeurs['Q' + a_key]
                if a_mesure['iswind'] is True and valeurs.get(a_key + '_dir') is not None:
                    my_val_dir = valeurs[a_key + '_dir']
                    if valeurs.get('Q' + a_key + '_dir') is not None:
                        my_qval_dir = valeurs['Q' + a_key + '_dir']
                break

        # get our min
        if valeurs.get(mesure_keys + '_min') is not None:
            my_val_min = valeurs[mesure_keys + '_min']
            my_val_min_time = valeurs[mesure_keys + '_min_time']
            if valeurs.get('Q' + mesure_keys + '_min') is not None:
                my_qval_min = valeurs['Q' + mesure_keys + '_min']
        else:
            if my_val is not None:
                my_val_min = my_val
                my_val_min_time = stop_dat

        # get our max
        if valeurs.get(mesure_keys + '_max') is not None:
            my_val_max = valeurs[mesure_keys + '_max']
            my_val_max_time = valeurs[mesure_keys + '_max_time']
            if valeurs.get('Q' + mesure_keys + '_max') is not None:
                my_qval_max = valeurs['Q' + mesure_keys + '_max']
            if a_mesure['iswind'] is True and valeurs.get(mesure_keys + '_max_dir') is not None:
                my_val_max_dir = valeurs[mesure_keys + '_max_dir']
        else:
            if my_val is not None:
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
            my_duration
        ]
