# JsonLoader process
#   addNewWorkItem(self, work_item)
#       not supported in jsonLoader
#   work_item = class.getNextWorkItem()
#       return None -> no more work for now
#       return a work_item data, which should include enought info for other calls
#   processItem(work_item):
#       Process the work item
#   succeedWorkItem(work_item):
#       Mark the work_item as processed
#   failWorkItem(work_item, exc):
#       mark the work_item as failed
from app.models import Load_Type
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.json_loader.json_loader import JsonLoaderABC
import app.tools.myTools as t
from app.tools.jsonPlus import JsonPlus
from django.conf import settings
from app.tools.myTools import getSettingValue
from app.tools.dbTools import refreshMV
import json
import os


class JsonLoader(JsonLoaderABC):
    def __init__(self):
        super().__init__()

        # boolean to stop processing files
        self.stopRequested = False

        # get directories settings
        self.json_dir = getSettingValue("JSON_AUTOLOAD")
        self.archive_dir = getSettingValue("ARCHIVE_DIR")
        self.failed_dir = getSettingValue("FAILED_DIR")

    # ----------------
    # public methods
    # ----------------
    def addNewWorkItem(self, work_item):
        work_item['info'] = "chargement de json "
        return

    def getNextWorkItem(self):
        file_names = []

        # get json file names
        filenames = os.listdir(self.json_dir)
        for filename in filenames:
            if str(filename).endswith('.json'):
                file_names.append(filename)

        # stop processing
        if len(file_names) == 0:
            return None

        file_names = sorted(file_names)
        a_filename = file_names[0]
        # load the first json file
        texte = ""

        with open(self.json_dir + '/' + a_filename, "r") as f:
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
            'meteor': meteor,
            'info': "chargement du json " + filename
        }

    def succeedWorkItem(self, work_item):
        # Don't move JSON files if we are in a "dump then json mode"
        cur_poste = PosteMeteor(work_item['meteor'])
        if (cur_poste.data.load_type & Load_Type.LOAD_FROM_DUMP_THEN_JSON) == Load_Type.LOAD_FROM_DUMP_THEN_JSON:
            return

        # delete the file
        os.remove(self.json_dir + "/" + work_item['f'])

        # refresh our materialized view
        refreshMV()

    def failWorkItem(self, work_item, exc):
        meteor = work_item['meteor']

        if not os.path.exists(self.failed_dir + "/" + meteor + "/"):
            os.makedirs(self.failed_dir + "/" + meteor + "/")
        os.rename(self.json_dir + "/" + work_item['f'], self.failed_dir + "/" + meteor + "/" + work_item['f'])

        j_info = {"filename": work_item['f'], "dest": self.archive_dir + "/" + meteor + "/failed/" + work_item['f']}
        t.logError('jsonloader', "file moved to fail directory", j_info)

    def processWorkItem(self, work_item: json):
        self.processJson(work_item)
