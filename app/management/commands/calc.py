from django.core.management.base import BaseCommand
from app.tools.climConstant import SvcRequestType
from app.tools.jsonPlus import JsonPlus
import app.tools.myTools as t
import requests
import json


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--trace', action='store_true', help='Trace temporary calculus')
        parser.add_argument('--tmp', action='store_true', help='compute in the temp tables')

    def handle(self, *args, **options):

        if options['trace']:
            trace_flag = True
        else:
            trace_flag = False

        if options['tmp']:
            is_tmp = True
        else:
            is_tmp = False

        params = {
            "is_tmp": is_tmp,
        }
        self.callService('aggreg', SvcRequestType.Run, trace_flag, params)

    def callService(self, service_name: str, command: int, trace_flag: bool, params: json):
        try:
            url = "http://localhost:8000/app/svc"
            data = {"svc": service_name, "cde": command, "trace_flag": trace_flag, "params": params}
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=JsonPlus().dumps(data), headers=headers)
            # if r.status_code
            rj = r.json()
            for a_result in rj['result']:
                self.stdout.write(a_result)

        except Exception as inst:
            t.LogException(inst)
