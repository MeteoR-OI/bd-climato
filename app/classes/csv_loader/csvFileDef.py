from abc import ABC, abstractmethod
from app.tools.dateTools import str_to_datetime
from app.classes.repository.mesureMeteor import MesureMeteor
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.repository.obsMeteor import QA
import re
from datetime import timedelta, datetime


class CsvFileSpec(ABC):
    def __init__(self, __spec) -> None:
        self.__spec = __spec

    @abstractmethod
    def getPosteData(self, rows):
        pass

    @abstractmethod
    def hackHeader(self, header):
        pass

    @abstractmethod
    def getStopDate(self, rows):
        pass

    def isItForMe(self, file_path, file_name) -> bool:
        self.__file_path = file_path
        self.__file_name = file_name
        self.__header = []
        for a_pattern in self.__spec['pattern']:
            match = re.match(a_pattern, file_name)
            if match:
                return True
        return True

    def nextBlockLines(self):
        obs_data = []
        min_data = []
        max_data = []
        total_line = 0

        cur_poste = None
        obs_data_in_db = {}
        last_meteor = 'not a meteor !@££$'
        with open(self.__file_path + '/' + self.__file_name, newline='') as file:
            line_count = 0
            row = file.readline()
            while row:
                my_fields = row.split(';')
                if line_count < self.__spec['skip_lines']:
                    self.__header.append(row)
                    if line_count == self.__spec['skip_lines'] - 1:
                        self.decodeHeader(my_fields)
                    total_line += 1
                    line_count += 1
                    row = file.readline()
                    continue

                self.__poste_info = self.getPosteData(my_fields)
                j_stop_dat_utc = self.getStopDate(my_fields)
                str_stop_dat_utc = str(j_stop_dat_utc)

                b_check_obs_data_in_db = False
                if obs_data_in_db is None:
                    if obs_data_in_db.get(str_stop_dat_utc) is not None:
                        b_check_obs_data_in_db = True

                # is it time to flush our buffers ?
                if cur_poste is None or line_count > 500:
                    print('yielding data: ' + str(len(obs_data)) + ' obs, ' + 'line_cout: ' + str(line_count) + '/' + str(total_line))
                    yield {'obs_data': obs_data, 'min_data': min_data, 'max_data': max_data}
                    obs_data = []
                    min_data = []
                    max_data = []
                    line_count = 0

                if (total_line % 1000) == 0:
                    print('total line processed: ' + str(total_line))

                # get new poste if needed
                if self.__poste_info['meteor'] != last_meteor:
                    cur_poste = PosteMeteor(self.__poste_info['meteor'])
                    if cur_poste.data.id is None:
                        # Create on the flight a new poste
                        cur_poste.data.type = "???"
                        cur_poste.data.altitude = float(self.__poste_info["ALTI"]) if self.__poste_info["ALTI"] != '' else None
                        cur_poste.data.lat = float(self.__poste_info["LAT"]) if self.__poste_info["LAT"] != '' else None
                        cur_poste.data.long = float(self.__poste_info["LON"]) if self.__poste_info["LON"] != '' else None
                        cur_poste.data.other_code = self.__poste_info["CODE"] if self.__poste_info["CODE"] != '' else None
                        cur_poste.data.owner = "Meteo France"
                        cur_poste.data.data_source = 1
                        cur_poste.data.delta_timezone = 4       # assume all meteo france data are in UTC+4
                        cur_poste.data.save()
                    last_meteor = self.__poste
                    date_already_loaded = str_to_datetime(cur_poste.data.last_obs_date)

                if j_stop_dat_utc > date_already_loaded:
                    #  process row
                    self.processRow(my_fields, cur_poste, obs_data, min_data, max_data, b_check_obs_data_in_db, obs_data_in_db)
                    line_count += 1

                # get next line
                total_line += 1
                row = file.readline()

            if len(obs_data) > 0:
                yield {'obs_data': obs_data, 'min_data': min_data, 'max_data': max_data}

    def processRow(self, my_fields, cur_poste, obs_data, min_data, max_data, b_check_obs_data_in_db, obs_data_in_db):
        poste_id = cur_poste.data.id
        for a_mesure in self.__mesures:
            cur_val, cur_q_val, obs_date_utc = self.get_valeurs(a_mesure, my_fields)
            if cur_val is None:
                continue

            # Check if mesure already loaded in obs
            if b_check_obs_data_in_db:
                str_obs_date_utc = str(obs_date_utc)
                if obs_data_in_db.get(str_obs_date_utc) is not None:
                    for a_mid in obs_data_in_db[str_obs_date_utc]['mids']:
                        if a_mid == a_mesure['id']:
                            continue

            obs_date_local = obs_date_utc + timedelta(hours=cur_poste.data.delta_timezone)
            data_args = (poste_id, obs_date_utc, obs_date_local, a_mesure['id'], 60, cur_val, cur_q_val)
            # 'obs_data': [(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value)],
            obs_data.append(data_args)

            if a_mesure['min'] is True:
                cur_min, cur_min_qa, cur_min_time_local, is_it_obs_data = self.get_valeur_min(cur_poste, a_mesure, my_fields, cur_val, obs_date_local)
                # 'min_data': [(poste_id, date_local, mesure_id, min, min_time, qa_min, is_it_obs_data)],
                min_data.append((poste_id, obs_date_local, a_mesure['id'], cur_min, cur_min_time_local, cur_min_qa, is_it_obs_data))
            else:
                min_data.append((poste_id, obs_date_local, a_mesure['id'], None, None, None, False))

            if a_mesure['max'] is True:
                cur_max, cur_max_qa, cur_max_time_local, cur_max_dir, is_it_obs_data = self.get_valeur_max(cur_poste, a_mesure, my_fields, cur_val, obs_date_local)
                # 'max_data': [poste_id, date_local, mesure_id, max, qa_max, max_time, max_dir, is_it_obs_data)],
                max_data.append((poste_id, obs_date_local, a_mesure['id'], cur_max, cur_max_time_local, cur_max_qa, cur_max_dir, is_it_obs_data))
            else:
                max_data.append((poste_id, obs_date_local, a_mesure['id'], None, None, None, None, False))

    def decodeHeader(self, field_headers):
        # Change header if needed
        self.__header = self.hackHeader(self.__header)

        # Decode data
        if self.__spec['poste_strategy'] == 1:
            self.__poste = None
        elif self.__spec['poste_strategy'] == 2:
            self.__poste = self.__header[0]['Poste']
            Exception('to be written')

        # prepare field mapping array
        self.__mesures = []
        self.__all_mesures = MesureMeteor.getDefinitions()
        for a_mapping in self.__spec['mappings']:
            idx_mesure = 0
            while idx_mesure < len(self.__all_mesures):
                a_mesure = self.__all_mesures[idx_mesure]
                if a_mapping['mesure'] == a_mesure['name']:
                    a_mesure['csv_field'] = a_mapping['csv_field']      # Header name
                    a_mesure['csv_row_idx'] = a_mapping['csv_idx']      # idx in row array
                    a_mesure['csv_qa_idx'] = a_mapping.get('qa_idx')    # idx in row array for quality data
                    a_mesure['csv_minmax'] = a_mapping['minmax']        # {min_idx: idx inself.__mesure, minTime, max: idx, maxTime, maxDir}

                    self.__mesures.append(a_mesure)
                idx_mesure += 1

    #  returns cur_val, cur_q_val, obs_date_utc
    def get_valeurs(self, a_mesure, fields_array):
        if fields_array[a_mesure['csv_row_idx']] is None or fields_array[a_mesure['csv_row_idx']] == '':
            return None, None, None

        cu_val = float(fields_array[a_mesure['csv_row_idx']])
        cur_q_val = fields_array[a_mesure['csv_qa_idx']] if a_mesure['csv_qa_idx'] is not None else QA.UNSET.value
        if cur_q_val == '':
            cur_q_val = QA.UNSET.value
        obs_date_utc = self.getStopDate(fields_array)

        return cu_val, cur_q_val, obs_date_utc

    # returns cur_min, cur_min_qa, cur_min_time_local, is_it_obs_data
    def get_valeur_min(self, cur_poste, a_mesure, fields_array, cur_val, obs_date_local):
        if a_mesure['min'] is not True:
            return None, None, None, False

        cur_min = float(cur_val)
        cur_min_qa = QA.UNSET.value
        cur_min_time = obs_date_local
        cur_min_field = a_mesure['csv_minmax'].get("min")
        cur_min_field_qa = a_mesure['csv_minmax'].get("qmin")
        cur_min_time_field = a_mesure['csv_minmax'].get("minTime")
        is_it_obs_data = True

        if cur_min_field is not None and cur_min_field != '':
            tmp_min = fields_array[cur_min_field]
            if tmp_min != '' and tmp_min is not None:
                cur_min = float(tmp_min)
                is_it_obs_data = False
            if cur_min_field_qa is not None and cur_min_field_qa != '':
                cur_min_qa = self.transcodeQAMeteoFrance(fields_array[cur_min_field_qa])

        if cur_min_time_field is not None and cur_min_time_field != '':
            tmp_min_time = fields_array[cur_min_time_field]
            if tmp_min_time != '' and tmp_min_time is not None:
                cur_min_time = self.adjustTime(cur_poste, obs_date_local, tmp_min_time)
                is_it_obs_data = False

        return cur_min, cur_min_qa, cur_min_time, is_it_obs_data

    # returns cur_max, cur_max_qa, cur_max_time_local, cur_max_dir, is_it_obs_data
    def get_valeur_max(self, cur_poste, a_mesure, fields_array, cur_val, obs_date_local):
        if a_mesure['max'] is not True:
            return None, None, None, None, False

        cur_max = float(cur_val)
        cur_max_qa = QA.UNSET.value
        cur_max_dir = None
        cur_max_time = obs_date_local
        cur_max_field = a_mesure['csv_minmax'].get("max")
        cur_max_field_qa = a_mesure['csv_minmax'].get("qmax")
        cur_max_time_field = a_mesure['csv_minmax'].get("maxTime")
        cur_max_dir_field = a_mesure['csv_minmax'].get("maxDir")
        is_it_obs_data = True

        if cur_max_field is not None and cur_max_field != '':
            tmp_max = fields_array[cur_max_field]
            if tmp_max != '' and tmp_max is not None:
                cur_max = float(tmp_max)
                is_it_obs_data = False
            if cur_max_field_qa is not None and cur_max_field_qa != '':
                cur_max_qa = self.transcodeQAMeteoFrance(fields_array[cur_max_field_qa])

        if cur_max_time_field is not None and cur_max_time_field != '':
            tmp_max_time = fields_array[cur_max_time_field]
            if tmp_max_time != '' and tmp_max_time is not None:
                cur_max_time = self.adjustTime(cur_poste, obs_date_local, tmp_max_time)
                is_it_obs_data = False

        cur_max_dir = fields_array[cur_max_dir_field] if cur_max_dir is not None else None

        return cur_max, cur_max_qa, cur_max_time, cur_max_qa, is_it_obs_data

    def adjustTime(self, cur_poste, obs_date_local: datetime, time_str):
        if time_str is None or time_str == '':
            return obs_date_local + timedelta(hours=cur_poste.data.delta_timezone)
        obs_date_local = obs_date_local - timedelta(hours=1)
        while len(time_str) < 4:
            time_str = '0' + time_str
        tmp_dt = str(obs_date_local)
        return str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[5:7] + '-' + tmp_dt[8:10] + 'T' + tmp_dt[11:13] + ':' + time_str[0:2] + ':' + time_str[2:4])

    def transcodeQAMeteoFrance(self, qa_meteoFR):
        if qa_meteoFR is None or qa_meteoFR == 0:
            return QA.UNSET.value
        if qa_meteoFR == 2:
            return QA.UNVALIDATED.value
        return QA.VALIDATED.value
