from app.classes.txt_loader.csvFileSpec import CsvFileSpec
from app.tools.dateTools import str_to_datetime
from app.classes.csv_loader.file_format.all_csv_formats import all_formats
from app.models import Code_QA
import app.tools.myTools as t
from app.tools.dateTools import str_to_datetime
import os
from django.conf import settings
import re

from datetime import timedelta
class CsvMeteoFR(CsvFileSpec):

    def __init__(self):
        if hasattr(settings, "CSV_AUTOLOAD") is True:
            self.base_dir = settings.CSV_AUTOLOAD
        else:
            self.base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/csv_auto_load")

        # get directories settings
        if hasattr(settings, "ARCHIVE_DIR") is True:
            self.archive_dir = settings.ARCHIVE_DIR
        else:
            self.archive_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/archive")

        self.all_formats = all_formats
        self.patterns = []
        idx = 0
        while idx < len(all_formats):
            for a_pattern in all_formats[idx].pattern:
                self.patterns.append({'p': a_pattern, 'idx': idx})
                idx += 1

        # be sure to have those 2 self variable in ABC class
        super().__init__(self.all_formats)

    def findNextWorkItem(self):
        files_spec = []

        # get json file names
        filenames = os.listdir(self.base_dir)
        for filename in filenames:
            if '{0}'.format(filename).endswith('.txt.data'):
                files_spec.append({"d": self.base_dir, "f": filename})

        # stop processing
        if len(files_spec) == 0:
            return None

        files_spec = sorted(files_spec, key=lambda k: k['f'])

        idx_file_spec = 0
        while idx_file_spec < len(files_spec):
            a_file_spec = files_spec[idx_file_spec]

            # find our file specification
            id_format = self.isItForMe(a_file_spec['d'], a_file_spec['f'])
            if id_format > -1:
                return {
                    'f': a_file_spec['f'],
                    'path': a_file_spec['d'],
                    'id_format': id_format,
                    'info': 'loading file: ' + a_file_spec['f'],
                    'move_file': self.all_formats[id_format].move_file
                }
            idx_file_spec += 1

        return None
        
    # check if a file name match our patterns
    def isItForMe(self, file_path, file_name) -> bool:
        for a_pattern in self.patterns:
            match = re.match(a_pattern['p'], file_name)
            if match:
                # return idx_format
                return a_pattern['idx']
        return -1

    def getPosteData(self, idx, rows, work_item):
        csv_format = self.all_formats[idx]
        if csv_format.poste_strategy == 1:
            return {
                    'meteor': None,
                    'ALTI': 0,
                    'LAT': 0,
                    'LON': 0,
                    'code':  rows[csv_format.RowId.POSTE.value].strip()
            }
        if csv_format.poste_strategy == 2:
            return self.__poste_info

    def hackHeader(self, idx, header, row):
        return

    def getStopDate(self, idx, rows, tz_hours=0):
        tmp_dt = rows[self.all_formats[idx].RowId.DATE.value]
        dt_local = str_to_datetime(
            tmp_dt[0:4] + '-' +
            tmp_dt[4:6] + '-' +
            tmp_dt[6:8] + 'T' +
            tmp_dt[8:10] + ':00:00')
        dt_utc = dt_local - timedelta(hours=tz_hours)
        return dt_utc, dt_local

    def getQualityCode(self, code_txt, id_format):
        if code_txt is None:
            return Code_QA.UNSET.value

        for a_mapping in self.all_formats[id_format].qa_mapping:
            if code_txt[0] == a_mapping[0]:
                return a_mapping[1]

        return Code_QA.UNSET.value
