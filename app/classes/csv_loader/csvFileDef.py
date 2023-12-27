from app.tools.dateTools import str_to_datetime
from app.classes.repository.mesureMeteor import MesureMeteor
from app.classes.repository.posteMeteor import PosteMeteor
import re
import csv
import datetime


class CsvFileSpec:
    def __init__(self) -> None:
        pass

    def isItForMe(self, file_path, file_name) -> bool:
        self.__file_path = file_path
        self.__file_name = file_name
        self.__header = []
        for a_pattern in self.__spec['pattern']:
            match = re.match(a_pattern, file_name)
            if match:
                return True
        return False

    def getMesures(self):
        return self.__mesures
    
    def getPoste(self):
        return self.__poste

    def nextLine(self) -> (PosteMeteor, datetime.datetime, dict):
        cur_poste = None
        last_meteor = 'not a meteor !@££$'
        with open(self.__file_path + '/' + self.__file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            line_count = 0
            for row in reader:
                if line_count < self.__spec['skip_lines']:
                    if line_count == self.__spec['skip_lines'] - 1:
                        self.decodeHeader(row.split(';'))
                    self.__header.append(row)
                    line_count += 1
                    continue

                self.__poste_info = self._getPoste(self.__data[self.__current_line - 1])

                if self.__poste_info['meteor'] != last_meteor:
                    cur_poste = PosteMeteor(self.__poste_info['meteor'])
                    if cur_poste.data.id is None:
                        # Create on the flight a new poste
                        cur_poste = PosteMeteor(self.__poste_info['meteor'])
                        cur_poste.data.data_source = 1
                        cur_poste.data.type = "inconnu"
                        cur_poste.data.altitude = float(cur_poste["ALTI"])
                        cur_poste.data.lat = float(cur_poste["LAT"])
                        cur_poste.data.long = float(cur_poste["LON"])
                        cur_poste.data.other_code = cur_poste["CODE"]
                        cur_poste.data.owner = "Meteo France"
                        cur_poste.data.delta_timezone = 4
                        cur_poste.data.save()
                    last_meteor = self.__poste

                tmp_dt = row["AAAAMMJJHH"]
                j_stop_dat_utc = str_to_datetime(tmp_dt[0:4] + '-' + tmp_dt[4:6] + '-' + tmp_dt[6:8] + 'T' + tmp_dt[8:10] + ':00:00')
    
                my_fields = row.split(';')
                idx_field = 0
                row_dict = {}
                while idx_field < len(my_fields):
                    a_field = my_fields[idx_field]
                    for a_mesure in self.__mesures:
                        if a_field == a_mesure['csv_field']:
                            tmp_idx = idx_field
                            my_mesure = a_mesure
                            if a_mesure['ommidx_csv'] is not None:
                                tmp_idx = a_mesure['ommidx_csv']
                                my_mesure = self.__mesures[tmp_idx]
                            row_dict[my_mesure['name']] = {'idx': tmp_idx, 'mid': my_mesure['id'], 'val': float(a_field)}
                    idx_field += 1

                yield cur_poste, j_stop_dat_utc, row_dict
                line_count += 1

    def decodeHeader(self, field_headers):
        # Decode data
        if self.__spec['poste_strategies'] == 1:
            self.__poste = None
        elif self.__spec['poste_strategies'] == 2:
            self.__poste = self.__header[0]['Poste']
            Exception('to be written')

        # prepare field mapping array
        self.__mesures = []
        idx_field = 0
        self.__all_mesures = MesureMeteor.getDefinitions()
        while idx_field < len(field_headers):
            a_field = field_headers[idx_field]
            for a_mapping in self.__spec['mappings']:
                if a_field == a_mapping['csv_field']:
                    for a_mesure in self.__all_mesures:
                        if a_mapping['mesure'] == a_mesure['name']:
                            a_mesure['csv_field'] = a_field
                            a_mesure['csv_idx'] = idx_field
                            a_mesure['csv_minmax'] = a_mapping['minmax']
                            self.__mesures.append(a_mesure)
            idx_field += 1

        for a_mesure in self.__mesures:
            if a_mesure['ommidx'] is not None:
                idx_omm = 0
                while idx_omm < len(self.__mesures):
                    a_mesure['ommidx_csv'] = idx_omm if self.__mesures[idx_omm]['id'] == a_mesure['ommidx'] else None
                    idx_omm += 1
