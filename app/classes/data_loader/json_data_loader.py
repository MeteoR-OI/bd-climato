from abc import ABC, abstractmethod
from app.classes.repository.mesureMeteor import MesureMeteor
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.repository.obsMeteor import ObsMeteor, QA
from app.tools.jsonValidator import checkJson
from app.tools.dateTools import str_to_datetime
import psycopg2
import app.tools.myTools as t
from app.tools.jsonPlus import JsonPlus
from django.conf import settings
import json
import os
from enum import Enum


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


class JsonDataLoader(ABC):
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

    def loadObsData(self, cur_poste, j_data, stop_dat, duration):
        keys_found = []
        for a_mesure in self.mesures:
            cur_vals = self.get_valeurs(a_mesure, j_data, stop_dat)

//Nico
            cur_obs_idx = self.get_cur_obs_idx(all_obs, a_mesure)
            cur_obs = all_obs[cur_obs_idx]

            # if current value is None, try with the second input key
            if cur_vals[0] is None:
                if a_mesure.get("col2") is not None and a_mesure['col2'] is not None:
                    cur_vals = self.get_valeurs(a_mesure, j_data, stop_dat, False, True)

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
        #  [0]  [1]     [2]        [3]      [4]      [5]     [6]      [7]      [8]      [9]     [10]
        # val, qval, dir|None, adir|None, valmin, qvalmin, min_time, valmax, qvalmax, max_time, max_dir

        suffix_key1 = '_avg'
        suffix_key2 = '_s'

        mesure_key = a_mesure['col']
        if use_second_input_key is True and a_mesure.get('col2') is not None:
            mesure_key = a_mesure['col2']

        # load keys used to look for our value in order of importance
        if force_abs is True or a_mesure['isavg'] is False:
            j_keys = [mesure_key + suffix_key2, mesure_key, mesure_key + suffix_key1]
        else:
            j_keys = [mesure_key + suffix_key1, mesure_key, mesure_key + suffix_key2]

        my_val = my_val_dir = None
        my_qval = my_qval_dir = QA.UNSET.value
        my_val_min = my_val_min_time = None
        my_val_max = my_val_max_time = my_val_max_dir = None
        my_qval_min = my_qval_max = QA.UNSET.value

        # get our value
        for a_key in j_keys:
            if valeurs.get(a_key) is not None:
                my_val = valeurs[a_key]
                if valeurs.get('Q' + a_key) is not None:
                    my_qval = valeurs['Q' + a_key]
                if a_mesure['iswind'] is True and valeurs.get(a_key + '_dir') is not None:
                    my_val_dir = valeurs[a_key + '_dir']
                    if valeurs.get('Q' + a_key + '_dir') is not None:
                        my_qval_dir = valeurs['Q' + a_key + '_dir']
                break

        # get our min
        if valeurs.get(mesure_key + '_min') is not None:
            my_val_min = valeurs[mesure_key + '_min']
            my_val_min_time = valeurs[mesure_key + '_min_time']
            if valeurs.get('Q' + mesure_key + '_min') is not None:
                my_qval_min = valeurs['Q' + mesure_key + '_min']
        else:
            if my_val is not None:
                my_val_min = my_val
                my_val_min_time = stop_dat

        # get our max
        if valeurs.get(mesure_key + '_max') is not None:
            my_val_max = valeurs[mesure_key + '_max']
            my_val_max_time = valeurs[mesure_key + '_max_time']
            if valeurs.get('Q' + mesure_key + '_max') is not None:
                my_qval_max = valeurs['Q' + mesure_key + '_max']
            if a_mesure['iswind'] is True and valeurs.get(mesure_key + '_max_dir') is not None:
                my_val_max_dir = valeurs[mesure_key + '_max_dir']
        else:
            if my_val is not None:
                my_val_max = my_val
                my_val_max_time = stop_dat
                my_val_max_dir = my_val_dir
 
        return [my_val, my_qval, my_val_dir, my_qval_dir, my_val_min, my_qval_min, my_val_min_time, my_val_max, my_qval_max, my_val_max_time, my_val_max_dir]

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
