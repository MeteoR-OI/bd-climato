from app.classes.csv_loader.csvFileSpec import CsvFileSpec
from app.tools.dateTools import str_to_datetime
from app.classes.csv_loader.file_format.all_OVPF_formats import all_formats
from app.classes.repository.posteMeteor import PosteMeteor
from app.models import Code_QA
import app.tools.myTools as t
import os
from django.conf import settings
import re
from datetime import datetime
import subprocess

class CsvOpvf(CsvFileSpec):

    def __init__(self):
        if hasattr(settings, "OVPF_FILES") is True:
            self.base_dir = settings.OVPF_FILES
        else:
            self.base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/ovpf")

        self.all_formats = all_formats
        # be sure to have those 2 self variable in ABC class
        super().__init__(self.all_formats)

    def findNextWorkItem(self):
        ovpf_stations = PosteMeteor.getOvpfStations()

        for a_station in ovpf_stations:
            cur_year =  datetime.now().year
            while cur_year >= 2007:
                if os.path.exists(self.base_dir + '/' + str(cur_year) + '/' + a_station['meteor'] + '.csv'):
                    break
                cur_year -= 1
            line = subprocess.check_output(['tail', '-1', self.base_dir + '/' + str(cur_year) + '/' + a_station['meteor'] + '.csv'])
            line = str(line)[2:len(line)+1]
            last_csv_date = datetime.strptime(line[0:10] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            if last_csv_date > a_station['last_obs_date_local']:
                year_to_process = a_station['last_obs_date_local'].year
                return {
                    'f': str(year_to_process) + '/' + a_station['meteor'] + '.csv',
                    'path': self.base_dir,
                    'meteor': a_station['meteor'].upper(),
                    'id_format': 0,
                    'info': 'loading file: ' + str(a_station['last_obs_date_local'].year) + '/' + a_station['meteor'] + '.csv',
                    'move_file': self.all_formats[0].move_file,
                    'year_processed': year_to_process,
                    'fix_obs_last_date': self.all_formats[0].fix_obs_last_date
                }

        return None
        
    def getPosteData(self, idx, rows, work_item):
        csv_format = self.all_formats[idx]
        if csv_format.poste_strategy == 1:
            return {
                    'meteor': work_item['meteor'],
                    'ALTI': 0,
                    'LAT': 0,
                    'LON': 0,
                    'code':  None
            }
        if csv_format.poste_strategy == 2:
            return self.__poste_info

    def hackHeader(self, idx, header, row):
        return

    def getStopDate(self, idx, rows, tz_hours=0):
        tmp_dt = rows[self.all_formats[idx].RowId.DATE.value] + ' 00:00:00'
        dt_utc = datetime.strptime(tmp_dt, '%Y-%m-%d %H:%M:%S')
        tmp_dt = rows[self.all_formats[idx].RowId.DATE.value] + ' 04:00:00'
        dt_local = datetime.strptime(tmp_dt, '%Y-%m-%d %H:%M:%S')
        return dt_utc, dt_local

    def getQualityCode(self, code_txt, id_format):
        return Code_QA.UNSET.value
