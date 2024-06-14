# -----------------------------------------------------------------------------
# to do in future:
# - allow to load only a few mesures, while other mesures where already loaded
# -----------------------------------------------------------------------------
from abc import ABC, abstractmethod
from app.tools.dateTools import str_to_datetime
from app.models import Code_QA
from app.classes.repository.mesureMeteor import MesureMeteor
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.repository.obsMeteor import ObsMeteor
from datetime import timedelta, datetime
import app.tools.myTools as t
import os
import os


class CsvFileSpec(ABC):
    def __init__(self, all_formats) -> None:
        return

    @abstractmethod
    def getPosteData(self, idx, rows, work_item):
        raise NotImplementedError

    @abstractmethod
    def hackHeader(self, idx, header, row):
        raise NotImplementedError

    @abstractmethod
    def getStopDate(self, idx, rows):
        raise NotImplementedError

    @abstractmethod
    def getQualityCode(self, code_txt, id_format):
        raise NotImplementedError

    @abstractmethod
    def findNextWorkItem(self):
        raise NotImplementedError
    
    def nextBlockLines(self, work_item, load_type_filter=255):
        obs_data = []
        min_data = []
        max_data = []
        total_line = 0
        self.__header = []
        id_format = work_item['id_format']

        cur_poste = None
        last_meteor = 'not a meteor !@££$'
        self.loadMesures(work_item['id_format'])

        file_path = work_item['path'] + '/' + work_item['f']
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            # flake8: noqa
            with open(file_path, newline='') as file:
                line_count = 0
                row = file.readline()
                while row:
                    my_fields = row.split(self.all_formats[id_format].separator)
                    if line_count < self.all_formats[id_format].skip_lines:
                        self.__header.append(row)
                        total_line += 1
                        line_count += 1
                        row = file.readline()
                        if line_count == self.all_formats[id_format].skip_lines:
                            self.decodeHeader(id_format, self.__header, row)
                        continue

                    # is it time to flush our buffers ?
                    if line_count > 500:
                        if len(obs_data) > 0:
                            t.logInfo('yielding data: ' + '{0}'.format(len(obs_data)) + ' obs, ' + 'line_cout: ' + '{0}'.format(line_count) + '/' + '{0}'.format(total_line))
                            yield {'obs_data': obs_data, 'min_data': min_data, 'max_data': max_data}
                            obs_data = []
                            min_data = []
                            max_data = []
                        line_count = 0

                    # get new poste if needed
                    poste_info = self.getPosteData(id_format, my_fields, work_item)
                    if poste_info.get('meteor') is not None:
                        id_station = poste_info['meteor']
                    else:
                        id_station = poste_info['code']

                    if id_station != last_meteor:
                        skip_poste = None
                        cur_poste = PosteMeteor(id_station)
                        if cur_poste is None:
                            cur_poste = PosteMeteor.getPosteByCode(id_station)
                        last_meteor = id_station
                        if cur_poste is None:
                            skip_poste = last_meteor

                    if skip_poste != last_meteor:
                        date_already_loaded = cur_poste.data.last_obs_date_local if cur_poste.data.last_obs_date_local is not None else datetime(1900, 1, 1)

                        obs_date_utc, obs_date_local = self.getStopDate(id_format, my_fields, cur_poste.data.delta_timezone)
                        
                        if obs_date_local > date_already_loaded:
                            #  process row
                            self.processRow(id_format, my_fields, cur_poste, obs_data, min_data, max_data)
                            line_count += 1

                    # get next line
                    total_line += 1
                    row = file.readline()

                if len(obs_data) > 0:
                    yield {'obs_data': obs_data, 'min_data': min_data, 'max_data': max_data}

                t.logInfo('file: ' + work_item['f'] + ', total line processed: ' + '{0}'.format(total_line))

    def processRow(self, id_format, my_fields, cur_poste, obs_data, min_data, max_data):
        poste_id = cur_poste.data.id
        obs_date_utc, obs_date_local = self.getStopDate(id_format, my_fields, cur_poste.data.delta_timezone)
        duration = self.all_formats[id_format].duration

        for a_mesure in self.__mesures:
            cur_val, cur_q_val = self.get_valeurs(id_format, a_mesure, my_fields)
            if cur_val is None:
                continue

            # Check if this measure needs to be loaded.... Future...

            # Check if mesure already loaded in obs
            # if b_check_obs_data_in_db:
            #     str_obs_date_local = '{0}'.format(obs_date_local)
            #     if obs_data_in_db.get(str_obs_date_local) is not None:
            #         for a_mid in obs_data_in_db[str_obs_date_local]['mids']:
            #             if a_mid == a_mesure['id']:
            #                 continue

            data_args = (poste_id, obs_date_utc, obs_date_local, a_mesure['id'], duration, cur_val, cur_q_val)
            # 'obs_data': [(poste_id, date_utc, date_local, mesure_id, duration, value, qa_value)],
            obs_data.append(data_args)

            if a_mesure['min'] is True:
                cur_min, cur_min_qa, cur_min_time_local, is_it_obs_data = self.get_valeur_min(cur_poste, id_format, a_mesure, my_fields, cur_val, cur_q_val, obs_date_local)
                # 'min_data': [(poste_id, date_local, mesure_id, min, min_time, qa_min, is_it_obs_data)],
                min_data.append((poste_id, obs_date_local, a_mesure['id'], cur_min, cur_min_time_local, cur_min_qa, is_it_obs_data))
            else:
                min_data.append((poste_id, obs_date_local, a_mesure['id'], None, None, None, False))

            if a_mesure['max'] is True:
                cur_max, cur_max_qa, cur_max_time_local, cur_max_dir, is_it_obs_data = self.get_valeur_max(cur_poste, id_format, a_mesure, my_fields, cur_val, cur_q_val, obs_date_local)
                # 'max_data': [poste_id, date_local, mesure_id, max, qa_max, max_time, max_dir, is_it_obs_data)],
                max_data.append((poste_id, obs_date_local, a_mesure['id'], cur_max, cur_max_time_local, cur_max_qa, cur_max_dir, is_it_obs_data))
            else:
                max_data.append((poste_id, obs_date_local, a_mesure['id'], None, None, None, None, False))

    def decodeHeader(self, id_format, hdr, row):
        # Change header if needed
        self.__header = self.hackHeader(id_format, hdr, row)

        # Decode data
        csv_format = self.all_formats[id_format]

        if csv_format.poste_strategy == 1:
            pass
        elif csv_format.poste_strategy == 2:
            self.__poste_info = {
                    'meteor': hdr[0].strip(),
                    'ALTI': 0,
                    'LAT': 0,
                    'LON': 0,
                    'CODE': hdr[1].strip()
            }
            Exception('to be written')

    def loadMesures(self, id_format):
        # prepare field mapping array
        self.__mesures = []
        csv_format = self.all_formats[id_format]

        self.__all_mesures = MesureMeteor.getDefinitions()
        for a_mapping in csv_format.mappings:
            idx_mesure = 0
            while idx_mesure < len(self.__all_mesures):
                a_mesure = self.__all_mesures[idx_mesure]
                if a_mapping['mesure'] == a_mesure['name']:
                    a_mesure['csv_field'] = a_mapping['csv_field']      # Header name
                    a_mesure['csv_row_idx'] = a_mapping['csv_idx']      # idx in row array
                    a_mesure['csv_qa_idx'] = a_mapping.get('qa_idx')    # idx in row array for quality data
                    a_mesure['csv_minmax'] = a_mapping['minmax']        # {min_idx: idx inself.__mesure, minTime, max: idx, maxTime, maxDir}
                    a_mesure['convert'] = a_mapping['convert']          # use our convert routines

                    self.__mesures.append(a_mesure)
                    break
    
                idx_mesure += 1

            if idx_mesure == len(self.__all_mesures):
                raise Exception('Mesure not found: ' + a_mapping['mesure'])

    #  returns cur_val, cur_q_val, obs_date_utc
    def get_valeurs(self, id_format, a_mesure, fields_array):
        if fields_array[a_mesure['csv_row_idx']] is None or fields_array[a_mesure['csv_row_idx']] == '':
            return None, None

        # convert with csv loader specific function
        cur_val = float(fields_array[a_mesure['csv_row_idx']].replace(',', '.'))
        if a_mesure['convert'] is not None and a_mesure['convert'].get('mfr_csv') is not None:
            cur_val = eval(a_mesure['convert']['mfr_csv'])(cur_val)

        if a_mesure.get('csv_qa_idx') is not None:
            cur_q_val = self.getQualityCode(fields_array[a_mesure.get('csv_qa_idx')], id_format)
        else:
            cur_q_val = Code_QA.UNSET.value

        return cur_val, cur_q_val

    # returns cur_min, cur_min_qa, cur_min_time_local, is_it_obs_data
    def get_valeur_min(self, cur_poste, id_format, a_mesure, fields_array, cur_val, cur_qval, obs_date_local):
        if a_mesure['min'] is not True:
            return None, None, None, False

        cur_min = float(cur_val)
        cur_min_qa = cur_qval
        cur_min_time = obs_date_local
        cur_min_field = a_mesure['csv_minmax'].get("min")
        cur_min_field_qa = a_mesure['csv_minmax'].get("qmin")
        cur_min_time_field = a_mesure['csv_minmax'].get("minTime")
        is_it_obs_data = True

        if cur_min_field is not None and cur_min_field != '':
            tmp_min = fields_array[cur_min_field]
            if tmp_min != '' and tmp_min is not None:
                cur_min = float(tmp_min.replace(',', '.'))
                if a_mesure['convert'] is not None and a_mesure['convert'].get('mfr_csv') is not None:
                    cur_min = eval(a_mesure['convert']['mfr_csv'])(cur_min)
                is_it_obs_data = False
            if cur_min_field_qa is not None and cur_min_field_qa != '':
                cur_min_qa = self.getQualityCode(fields_array[cur_min_field_qa], id_format)

        if cur_min_time_field is not None and cur_min_time_field != '':
            tmp_min_time = fields_array[cur_min_time_field]
            if tmp_min_time != '' and tmp_min_time is not None:
                cur_min_time = self.adjustTime(cur_poste, obs_date_local, tmp_min_time)
                is_it_obs_data = False

        return cur_min, cur_min_qa, cur_min_time, is_it_obs_data

    # returns cur_max, cur_max_qa, cur_max_time_local, cur_max_dir, is_it_obs_data
    def get_valeur_max(self, cur_poste, id_format, a_mesure, fields_array, cur_val, cur_qval, obs_date_local):
        if a_mesure['max'] is not True:
            return None, None, None, None, False

        cur_max = float(cur_val)
        cur_max_qa = cur_qval
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
                cur_max = float(tmp_max.replace(',', '.'))
                if a_mesure['convert'] is not None and a_mesure['convert'].get('mfr_csv') is not None:
                    cur_max = eval(a_mesure['convert']['mfr_csv'])(cur_max)
                is_it_obs_data = False
            if cur_max_field_qa is not None and cur_max_field_qa != '':
                cur_max_qa = self.getQualityCode(fields_array[cur_max_field_qa], id_format)

        if cur_max_time_field is not None and cur_max_time_field != '':
            tmp_max_time = fields_array[cur_max_time_field]
            if tmp_max_time != '' and tmp_max_time is not None:
                cur_max_time = self.adjustTime(cur_poste, obs_date_local, tmp_max_time)
                is_it_obs_data = False

        cur_max_dir = fields_array[cur_max_dir_field] if cur_max_dir_field is not None and cur_max is not None else None

        return cur_max, cur_max_qa, cur_max_time, cur_max_dir, is_it_obs_data

    def getArchivePath(self, work_item):
        target_dir = self.archive_dir 

        target_sub_dir = self.all_formats[work_item['id_format']].getArchiveSubDir(work_item['f'])
        return target_dir + target_sub_dir

    def adjustTime(self, cur_poste, obs_date_local: datetime, time_str):
        if time_str is None or time_str == '':
            return obs_date_local + timedelta(hours=cur_poste.data.delta_timezone)
        obs_date_local = obs_date_local - timedelta(hours=1)
        while len(time_str) < 4:
            time_str = '0' + time_str
        tmp_dt = '{0}'.format(obs_date_local)
        return str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[5:7] + '-' + tmp_dt[8:10] + 'T' + tmp_dt[11:13] + ':' + time_str[0:2] + ':' + time_str[2:4])

    def transcodeQAMeteoFrance(self, qa_meteoFR):
        if qa_meteoFR is None or qa_meteoFR == 0:
            return ObsMeteor().CodeQA.UNSET.value
        if qa_meteoFR == 2:
            return ObsMeteor.CodeQA.UNVALIDATED.value
        return ObsMeteor.CodeQA.VALIDATED.value
