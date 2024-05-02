from app.classes.csv_loader.csvFileSpec import CsvFileSpec
from app.tools.dateTools import str_to_datetime
from app.classes.csv_loader.file_format.all_OVPF_formats import all_formats
from app.models import Code_QA
import app.tools.myTools as t
import os
from django.conf import settings
import re


class CsvOpvf(CsvFileSpec):

    def __init__(self):
        self.all_formats = all_formats
        patterns = []
        idx = 0
        while idx < len(all_formats):
            for a_pattern in all_formats[idx].pattern:
                patterns.append({'p': a_pattern, 'idx': idx})
                idx += 1

        # get directories settings
        if hasattr(settings, "PLUVIO_FILES") is True:
            self.base_dir = settings.PLUVIO_FILES
        else:
            self.base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/../../data/ovpf")

        super().__init__(patterns, self.all_formats)

    def findNextWorkItem(self):
        files_spec = []

        # get json file names
        filenames = os.listdir(self.base_dir)
        for filename in filenames:
            if str(filename).endswith('.csv'):
                files_spec.append({"d": self.base_dir, "f": filename})

        for filename in filenames:
            if str(filename).endswith('.txt.data'):
                files_spec.append({"d": self.base_dir, "f": filename})

        # self.addOvpfFiles(files_spec)

        # stop processing
        if len(files_spec) == 0:
            return None

        files_spec = sorted(files_spec, key=lambda k: k['f'])

        idx_file_spec = 0
        while idx_file_spec < len(files_spec):
            a_file_spec = files_spec[idx_file_spec]

            # find our file specification
            idx_provider = 0

            while idx_provider < len(self.__all_providers):
                id_format = self.__all_providers[idx_provider].isItForMe(a_file_spec['d'], a_file_spec['f'])

                if id_format >= 0:
                    return {
                        'f': a_file_spec['f'],
                        'path': a_file_spec['d'],

                        'id_format': id_format,
                        'info': 'loading file: ' + a_file_spec['f'],
                        'move_file': False
                    }
                idx_provider += 1

        t.logError('csvLoader', "No file spec found for " + a_file_spec['d'] + "/" + a_file_spec['f'])
        idx_file_spec += 1
        return None
        
    def getPosteData(self, idx, rows, file_name):
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

    def getStopDate(self, idx, rows):
        tmp_dt = rows[self.all_formats[idx].RowId.DATE.value]
        return str_to_datetime(
            tmp_dt[0:4] + '-' +
            tmp_dt[4:6] + '-' +
            tmp_dt[6:8] + 'T' +
            tmp_dt[8:10] + ':00:00')

    def getQualityCode(self, code_txt, id_format):
        return Code_QA.UNSET.value
