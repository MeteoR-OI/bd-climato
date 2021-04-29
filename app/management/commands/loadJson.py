from django.core.management.base import BaseCommand
from django.core.management import call_command
from app.classes.calcul.calcAggreg import CalcAggreg
from app.tools.jsonPlus import JsonPlus
from app.classes.calcul.calcObservation import CalcObs
import os
import glob


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, nargs='?', default='*', help='filename with extension (should be in data/json_not_in_git')
        parser.add_argument('--delete', action='store_true', help='delete all aggregations before loading json')
        parser.add_argument('--nodel', action='store_true', help='do not delete all aggregations before loading json')
        parser.add_argument('--validation', action='store_true', help='use validation data instead of aggregations')
        parser.add_argument('--noaggreg', action='store_true', help='do not start aggregation computation')
        parser.add_argument('--trace', action='store_true', help='Trace temporary calculus')
        parser.add_argument('--tmp', action='store_true', help='compute in the temp tables')

    def handle(self, *args, **options):
        if options['filename']:
            self.stdout.write('loadJson started: ' + str(options['filename']))
        else:
            self.stdout.write('loadJson started: all files !!!')

        if options['delete']:
            delete_flag = True
        else:
            delete_flag = False

        if options['trace']:
            trace_flag = True
        else:
            trace_flag = False

        if options['tmp']:
            is_tmp = True
            # set the delete_flag if not given
        else:
            is_tmp = False

        if options['nodel']:
            delete_flag = False

        no_aggreg = False
        if options['noaggreg']:
            no_aggreg = True

        validation_flag = False
        if options['validation']:
            validation_flag = True

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        b_file_found = False
        for a_file in glob.glob(base_dir + '/../../data/json_not_in_git/*.json'):
            if options['filename'] == '*' or a_file.endswith(options['filename']):
                b_file_found = True
                self.processJson(a_file, delete_flag, trace_flag, is_tmp, validation_flag)

        if b_file_found is False:
            self.stderr.write('no file found, exiting')
            return

        # compute aggregations if needed
        if no_aggreg is False:
            if is_tmp is True:
                CalcAggreg().ComputeAggreg(is_tmp)
            else:
                call_command('svc', 'aggreg', '--run')

    def processJson(self, file_name: str, delete_flag: bool, trace_flag: bool, is_tmp, use_validation: bool = False):
        try:
            calc = CalcObs()
            texte = ''

            with open(file_name, "r") as f:
                lignes = f.readlines()
                for aligne in lignes:
                    texte += str(aligne)

                my_json = JsonPlus().loads(texte)

                ret = calc.loadJson(my_json, trace_flag, False, is_tmp, use_validation)
                if trace_flag is True:
                    self.stdout.write(JsonPlus().dumps(ret))

        except Exception as inst:
            print('in ' + file_name + ':')
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
