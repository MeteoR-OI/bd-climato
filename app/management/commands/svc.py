from django.core.management.base import BaseCommand
from app.tools.climConstant import SvcRequestType
import app.tools.myTools as t
import sys
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
        parser.add_argument('--tmp', action='store_true', help='use tmp tables')
        parser.add_argument('--validation', action='store_true', help='use json data only from the validation key')

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

        if options['trace']:
            command |= SvcRequestType.TraceOn

        if options['notrace']:
            command |= SvcRequestType.TraceOff

        if options['tmp']:
            is_tmp = True
        else:
            is_tmp = False

        if options['validation']:
            use_validation = True
        else:
            use_validation = False

        try:
            url = "http://localhost:8000/app/svc"
            data = {"svc": svc_name, "cde": command, "params": {"is_tmp": is_tmp, "validation": use_validation}}
            headers = {'content-type': 'application/json'}

            r = requests.post(url, data=JsonPlus().dumps(data), headers=headers)
            rj = r.json()
            if rj.__contains__('status'):
                if rj['status'] == 'ok':
                    for a_result in rj['result']:
                        print(a_result)
                else:
                    print('ok')
            else:
                if r.__contains__('errMsg'):
                    print('Error(s):')
                    for an_err_msg in r.errMsg:
                        print(an_err_msg)
                else:
                    print('Error encountered')

        except Exception as e:
            if e.__dict__.__len__() == 0 or 'done' not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                funcname = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "n": funcname,
                    "f": filename,
                    "l": line_number,
                }
                e.done = True
            errMsg = t.LogCritical(e, None, {}, True)
            print(errMsg)
            exit(0)
