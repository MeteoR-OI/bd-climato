from django.core.management.base import BaseCommand
from app.tools.jsonPlus import JsonPlus
import os
import glob


class Command(BaseCommand):
    def handle(self, *args, **options):
        # self.stdout.write('loadJson started')

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for a_file in glob.glob(base_dir + '/../../data/json_not_in_git/*.json'):
            self.processJson(a_file)

        # self.stdout.write('loadJson ended')

    def processJson(self, file_name: str):
        texte = ''

        with open(file_name, "r") as f:
            lignes = f.readlines()
            for aligne in lignes:
                texte += str(aligne)

            my_json = JsonPlus().loads(texte)

            self.stdout.write('need to process file: ' + file_name)
            self.stdout.write(JsonPlus().dumps(my_json))
