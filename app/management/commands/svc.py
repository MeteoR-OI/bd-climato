from django.core.management.base import BaseCommand
from app.tools.climConstant import SvcRequestType
import requests
from app.tools.jsonPlus import JsonPlus


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('serviceName', type=str, nargs='?', default='*', help='service name')
        parser.add_argument('--list', action='store_true', help='list all available services')
        parser.add_argument('--run', action='store_true', help='activate the service')
        parser.add_argument('--start', action='store_true', help='start the service')
        parser.add_argument('--stop', action='store_true', help='stop the service')
        parser.add_argument('--status', action='store_true', help='get the status of the service')
        parser.add_argument('--trace', action='store_true', help='display trace')
        parser.add_argument('--notrace', action='store_true', help='stop the tracing of the service')

    def handle(self, *args, **options):
        command = SvcRequestType.Nope

        if options['serviceName']:
            svc_name = options['serviceName']
        else:
            self.list_services()

        if options['start']:
            command |= SvcRequestType.Start

        if options['stop']:
            command |= SvcRequestType.Stop

        if options['status']:
            command |= SvcRequestType.Status

        if options['list']:
            command |= SvcRequestType.List

        if options['run']:
            command |= SvcRequestType.Run

        trace_flag = None
        if options['trace']:
            trace_flag = True

        if options['notrace']:
            trace_flag = False

        try:
            url = "http://localhost:8000/app/svc"
            data = {"svc": svc_name, "cde": command, "trace_flag": trace_flag}
            headers = {'content-type': 'application/json'}

            r = requests.post(url, data=JsonPlus().dumps(data), headers=headers)
            rj = r.json()
            if rj.__contains__('status'):
                if rj['status'] == 'ok':
                    if rj.__contains__('result'):
                        for a_result in rj['result']:
                            self.stdout.write(a_result)
                    else:
                        self.stdout.write('ok')
                else:
                    if rj.__contains__('errMsg'):
                        self.stderr('Error(s):')
                        for an_err_msg in rj['errMsg']:
                            self.stderr.write(an_err_msg)
                    else:
                        self.stderr.write('Error encountered')
            else:
                self.stderr.write('Error: protocol error')

        except Exception as inst:
            self.stderr.write('Error (bug): ' + inst)

    def display_help(self):
        self.stdout.write('python manage svc --list   -> List all available services')
        self.stdout.write('python manage svc [serviceName] [command]')
        self.stdout.write('   where [command] can be:')
        self.stdout.write('   --start     start the service')
        self.stdout.write('   --stop      stop the service')
        self.stdout.write('   --status    get the status of the service')
        self.stdout.write('   --trace     ask to trace the service')
        self.stdout.write('   --notrace   stop the trace of the service')

    def callService(self, service_name: str, command: int, trace_flag: bool):
        try:
            url = "http://localhost:8000"
            data = {"svc": service_name, "cde": command, "trace_flag": trace_flag}
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=JsonPlus().dumps(data), headers=headers)
            rj = r.json()
            for a_result in rj['result']:
                self.stdout.write(a_result)

        except Exception as inst:
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
