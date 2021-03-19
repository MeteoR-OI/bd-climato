from django.core.management.base import BaseCommand
from app.tools.jsonPlus import JsonPlus
from app.classes.metier.calculus import Calculus
import os
import glob


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, nargs='?', default='*', help='filename with extension (should be in data/json_not_in_git')

    def handle(self, *args, **options):
        if options['filename']:
            self.stdout.write('loadJson started: ' + str(options['filename']))
        else:
            self.stdout.write('loadJson started: all files !!!')

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for a_file in glob.glob(base_dir + '/../../data/json_not_in_git/*.json'):
            if options['filename'] == '*' or a_file.endswith(options['filename']):
                self.processJson(a_file)

        # self.stdout.write('loadJson ended')

    def processJson(self, file_name: str):
        try:
            calc = Calculus()
            texte = ''

            with open(file_name, "r") as f:
                lignes = f.readlines()
                for aligne in lignes:
                    texte += str(aligne)

                my_json = JsonPlus().loads(texte)
                calc.run(my_json, True)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
