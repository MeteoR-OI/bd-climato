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
from app.classes.repository.posteMeteor import PosteMeteor
from app.classes.repository.incidentMeteor import IncidentMeteor
from app.classes.data_loader.json_data_loader import JsonDataLoader
from app.tools.jsonValidator import checkJson
from app.tools.dateTools import str_to_datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import app.tools.myTools as t
from app.tools.jsonPlus import JsonPlus
from django.conf import settings
import json
import os


class JsonLoader(JsonDataLoader):

    def __init__(self):
        super().__init__()

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

    # ----------------
    # public methods
    # ----------------
    def addNewWorkItem(self, work_item):
        work_item['info'] = "chargement du json " + work_item['f']
        return

    def getNextWorkItem(self):
        file_names = []

        # get json file names
        filenames = os.listdir(self.base_dir)
        for filename in filenames:
            if str(filename).endswith('.json'):
                file_names.append(filename)

        # stop processing
        if len(file_names) == 0:
            return None

        file_names = sorted(file_names)
        a_filename = file_names[0]
        # load our json file
        texte = ""

        with open(self.base_dir + '/' + a_filename, "r") as f:
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
        if (cur_poste.data.load_type & PosteMeteor.Load_Type.LOAD_FROM_DUMP_THEN_JSON) == PosteMeteor.Load_Type.LOAD_FROM_DUMP_THEN_JSON:
            return

        # move the file to archive
        str_annee = 'inconnu'
        str_mois = 'inconnu'
        meteor = 'inconnu'
        try:
            str_annee = str(work_item['f']).split(".")[2].split("-")[0]
            str_mois = str(work_item['f']).split(".")[2].split("-")[1]
            meteor = str(work_item['f']).split(".")[1]
        except Exception:
            pass

        tmp_prefix = ""
        if work_item.get('is_loaded') is not None and work_item['is_loaded'] is not False:
            tmp_prefix = "/skipped/"

        filename_prefix = self.archive_dir + "/" + meteor + tmp_prefix + "/" + str_annee + "/" + str_mois + "/"
        if not os.path.exists(filename_prefix):
            os.makedirs(filename_prefix)

        os.rename(self.base_dir + "/" + work_item['f'], filename_prefix + work_item['f'])

        # refresh our materialized view
        pgconn = self.getPGConnexion()
        pgconn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        pg_cur = pgconn.cursor()

        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_hour')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('obs_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_min_month')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_day')))
        pg_cur.execute(sql.SQL("CALL refresh_continuous_aggregate('{}', null, null);").format(sql.Identifier('x_max_month')))

        pg_cur.close()
        pgconn.commit()
        pgconn.close()

    def failWorkItem(self, work_item, exc):
        # Don't move JSON files if we are in a "dump then json mode"
        cur_poste = PosteMeteor(work_item['meteor'])
        if (cur_poste.data.load_type & PosteMeteor.Load_Type.LOAD_FROM_DUMP_THEN_JSON) == PosteMeteor.Load_Type.LOAD_FROM_DUMP_THEN_JSON:
            return

        meteor = 'inconnu'
        try:
            meteor = str(work_item['f']).split(".")[1]
        except Exception:
            pass

        str_annee = 'inconnu'
        str_mois = 'inconnu'
        meteor = 'inconnu'
        try:
            str_annee = str(work_item['f']).split(".")[2].split("-")[0]
            str_mois = str(work_item['f']).split(".")[2].split("-")[1]
            meteor = str(work_item['f']).split(".")[1]
        except Exception:
            pass

        tmp_prefix = "/failed"
        filename_prefix = self.archive_dir + "/" + meteor + tmp_prefix + "/" + str_annee + "/" + str_mois + "/"
        if not os.path.exists(filename_prefix):
            os.makedirs(filename_prefix)
        os.rename(self.base_dir + "/" + work_item['f'], filename_prefix + work_item['f'])

        j_info = {"filename": work_item['f'], "dest": self.archive_dir + "/" + meteor + "/failed/" + work_item['f']}
        t.logError('jsonloader', "file moved to fail directory", j_info)
        IncidentMeteor.new('_getJsonFileNameAndData', 'error', 'file ' + work_item['f'] + ' moved to failed directory', j_info)

    def processWorkItem(self, work_item: json):
        work_item['is_loaded'] = False
        filename = work_item['f']
        jsons_to_load = work_item['json']
        idx_global = 0
        cur_meteor = "inconnu"

        check_result = checkJson(jsons_to_load, filename)
        if check_result is not None:
            raise Exception("Invalid Json file: " + filename + ": " + check_result)

        while idx_global < jsons_to_load.__len__():
            try:
                json_to_load = jsons_to_load[idx_global]
                meteor = str(json_to_load.get("meteor"))

                if meteor != cur_meteor:
                    work_item['meteor'] = cur_poste = PosteMeteor(meteor)
                    if cur_poste.data is None or cur_poste.data.load_type is None:
                        raise Exception("code meteor inconnu: " + meteor + ', idx_global: ' + str(idx_global) + ' dans le fichier: ' + filename)

                    if (cur_poste.data.load_type & PosteMeteor.Load_Type.LOAD_FROM_JSON.value) == 0:
                        t.logInfo('jsonload', meteor + ' inactif json_load is False), skipping file ' + filename)
                        return

                    cur_meteor = meteor

                idx_data = 0
                while idx_data < json_to_load['data'].__len__():
                    try:
                        a_work_item = json_to_load['data'][idx_data]

                        # get data from our json item
                        j_stop_dat = a_work_item["stop_dat"]
                        stop_date = str_to_datetime(j_stop_dat)
                        j_duration = a_work_item["duration"]

                        if (cur_poste.data.load_type & PosteMeteor.Load_Type.LOAD_FROM_DUMP_THEN_JSON.value) == PosteMeteor.Load_Type.LOAD_FROM_DUMP_THEN_JSON.value:
                            if j_stop_dat <= cur_poste.data.last_obs_date:
                                cur_poste.data.load_type = PosteMeteor.Load_Type.LOAD_FROM_JSON.value
                                cur_poste.data.save()
                                t.notifyAdmin('jsonload', meteor + ' switching to Load_From_Json mode data from ' + filename + ', stop_date: ' + stop_date)
                            else:
                                t.logInfo('jsonload', meteor + ' waiting for an older json file, skipping file ' + filename + ', stop_date: ' + stop_date)
                                return

                        if j_stop_dat <= cur_poste.data.last_obs_date:
                            t.logInfo('jsonload', meteor + ' skipping data already loaded rom ' + filename + ', stop_date: ' + stop_date + ', last_obs_date: ' + str(cur_poste.data.last_obs_date))
                            return

                        self.load_obs_data_j(cur_poste, a_work_item['valeurs'], j_stop_dat, j_duration)

                    finally:
                        idx_data += 1

            finally:
                idx_global += 1

        work_item['is_loaded'] = True

    def getPGConnexion(self):
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Funiculi",
            database="climato"
        )
