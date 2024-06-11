from django.core.management.base import BaseCommand, CommandError
import json
import requests
import os

class Command(BaseCommand):
    help = "Control service processes"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('action',                  default='status', type=str, help='list, start, stop, run, status, add_param')
        parser.add_argument('service_name', nargs='?', default='--help', type=str, help='service name')
        parser.add_argument('option',       nargs='?', default={},       type=str, help='parameter used only with run, add_param')
        parser.add_argument('option2',      nargs='?', default=None,     type=str, help='supplemental parameter used only with run, add_param')

    def handle(self, *args, **options):
        try:
            name = options['service_name']
            action = options['action']
            param = options['option']
            option2 = options['option2']

            # print(name, action, param)
            self.callService(name, action, param, option2)

        except Exception as ex:
            raise CommandError('Error ' + str(ex))

    def callService(self, service_name: str, action: str, params: json, option2: json):
        if os.getenv("CC_PYTHON_MODULE") is None:
            url = "http://localhost:8000/app/svc"
        else:
            url = "http://localhost:8080/app/svc"
        data = {"svc": service_name, "action": action, "params": params, "params2": option2}
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        # if r.status_code
        rj = r.json()
        if rj['status'] == 'ok':
            self.stdout.write('ok')
            for a_result in rj['result']:
                self.stdout.write('   ' + a_result)
        else:
            self.stderr.write('** ERROR **')
            for a_result in rj['result']:
                self.stderr.write('   ' + a_result)

