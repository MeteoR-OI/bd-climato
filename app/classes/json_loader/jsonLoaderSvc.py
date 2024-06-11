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
from app.tools.myTools import getDirNameInSettings
from app.tools.dbTools import refreshMV
from django.conf import settings
import json
import os
import shutil

class JsonLoader(JsonLoaderABC):
    def __init__(self):
        super().__init__()

        # boolean to stop processing files
        self.stopRequested = False

        # get directories settings
        self.json_dir = getDirNameInSettings("JSON_AUTOLOAD")
        self.archive_dir = getDirNameInSettings("ARCHIVE_DIR")
        self.failed_dir = getDirNameInSettings("FAILED_DIR")
        self.waiting_dir = getDirNameInSettings("JSON_WAITING")

    # ----------------
    # public methods
    # ----------------
    def addNewWorkItem(self, work_item):
        work_item['info'] = "chargement de json "
        return
    
    def getNextWorkItem(self):
        file_names = []

        # get json first json file
        root_file, a_filename = self.search_json_file(self.json_dir)
        if a_filename is None:
            return None

        # load the first json file
        texte = ""

        with open(os.path.join(root_file, a_filename), "r") as f:
            lignes = f.readlines()
            for aligne in lignes:
                texte += str(aligne)
        my_json = JsonPlus().loads(texte)
        if 'dict' in str(type(my_json)):
            my_json = [my_json]

        meteor = 'inconnu'
        try:
            if len(root_file.split('/')) > 3:
                if str(a_filename).split(".")[1] == root_file.split('/')[-1]:
                    meteor = root_file.split('/')[-1]
            else:
                # old style...
                meteor = str(a_filename).split(".")[1]
        except Exception:
            pass
        
        if meteor == 'inconnu':
            t.logError('jsonloader', "meteor name not found", {"filename": a_filename, "root": root_file})
            raise Exception("meteor name not found")

        return {
            'f': a_filename,
            'r': root_file,
            'json': my_json,
            'meteor': meteor,
            'info': "chargement du json " + os.path.join(root_file, a_filename)
        }

    def succeedWorkItem(self, work_item):
        # Don't move JSON files if we are in a "dump then json mode"
        cur_poste = PosteMeteor(work_item['meteor'])
        if not os.path.exists(self.archive_dir + "/" + work_item['meteor'] + "/"):
            os.makedirs(self.archive_dir + "/" + work_item['meteor'] + "/")

        # Reactivate wainting json files
        if work_item.get('MOVE_TO_WAIT_LIST') is not None and work_item['MOVE_TO_WAIT_LIST'] is True:
            files = os.listdir(self.waiting_dir + '/' + work_item['meteor'])

            # Iterate over the files and copy the JSON files to the /destination directory
            for file in files:
                if file.endswith('.json'):
                    source = os.path.join(self.waiting_dir + '/' + work_item['meteor'], file)
                    destination = os.path.join(self.json_dir, work_item['meteor'], file)
                    shutil.copy(source, destination)
            return

        # Move the json file to the waiting directory
        if (cur_poste.data.load_type & Load_Type.LOAD_FROM_DUMP_THEN_JSON) == Load_Type.LOAD_FROM_DUMP_THEN_JSON:
            os.rename(os.path.join(work_item['r'], work_item['f']), self.waiting_dir + "/" + work_item['meteor'] + "/" + work_item['f'])
            return

        # delete the file
        if hasattr(settings, 'NO_DELETE_JSON') is True and settings.NO_DELETE_JSON is True:
            os.rename(os.path.join(work_item['r'], work_item['f']), os.path.join(self.archive_dir, work_item['meteor'], work_item['f']))
        else:
            os.remove(os.path.join(work_item['r'], work_item['f']))

        # refresh our materialized view
        refreshMV()

    def failWorkItem(self, work_item, exc):
        meteor = work_item['meteor']

        if not os.path.exists(self.failed_dir + "/" + meteor + "/"):
            os.makedirs(self.failed_dir + "/" + meteor + "/")

        dest_file = os.path.join(self.failed_dir, meteor, work_item['f'])

        os.rename(os.path.join(work_item['r'], work_item['f']), dest_file)
        t.logError('jsonloader', "file moved to fail directory", {"filename": work_item['f'], "dest": dest_file})

    def processWorkItem(self, work_item: json):
        self.processJson(work_item)

    def search_json_file(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    return root, file 
            for dir in dirs:
                print ('searching in ' + root + '/' + dir + ', directory: ' + directory)
                self.search_json_file(root + '/' + dir)
        return None, None
