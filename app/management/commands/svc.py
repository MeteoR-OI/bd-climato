from django.core.management.base import BaseCommand
from app.classes.workers.workerRoot import WorkerRoot
from app.classes.workers.svcAggreg import SvcAggreg
from app.classes.workers.svcAutoLoad import SvcAutoLoad


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('serviceName', type=str, nargs='?', default='*', help='service name')
        parser.add_argument('--list', action='store_true', help='list all available services')
        parser.add_argument('--start', action='store_true', help='start the service')
        parser.add_argument('--stop', action='store_true', help='stop the service')
        parser.add_argument('--status', action='store_true', help='get the status of the service')
        parser.add_argument('--trace', action='store_true', help='Trace service')
        parser.add_argument('--notrace', action='store_true', help='Stop the trace of the service')

    def handle(self, *args, **options):
        if options['list']:
            self.list_services()

        if options['serviceName']:
            svc_name = options['serviceName']
        else:
            self.list_services()

        command = 0
        if options['start']:
            if command != 0:
                raise Exception('svc', 'only one command allowed')
            command = 1

        if options['stop']:
            if command != 0:
                raise Exception('svc', 'only one command allowed')
            command = 2

        if options['status']:
            if command != 0:
                raise Exception('svc', 'only one command allowed')
            command = 4

        if command == 0:
            self.display_help()
            return

        trace_flag = None
        if options['trace']:
            trace_flag = True

        if options['notrace']:
            trace_flag = False

        if options['help']:
            self.display_help()
            return
        self.callService(svc_name, command, trace_flag)

    def display_help(self):
        self.stdout.write('python manage svc --list   -> List all available services')
        self.stdout.write('python manage svc [serviceName] [command]')
        self.stdout.write('   where [command] can be:')
        self.stdout.write('   --start     start the service')
        self.stdout.write('   --stop      stop the service')
        self.stdout.write('   --status    get the status of the service')
        self.stdout.write('   --trace     ask to trace the service')
        self.stdout.write('   --notrace   stop the trace of the service')

    def list_services(self):
        svc_list = {}
        all_syn = WorkerRoot.GetSynonym()
        self.stdout.write('all_syn: ' + str(all_syn))
        for a_syn in all_syn:
            if svc_list.get(a_syn['svc']) is None:
                svc_list[a_syn['svc']] = []
            svc_list[a_syn['svc']].append(a_syn['s'])
        self.stdout.write('list of services:')
        for a_svclst in svc_list:
            svc_names = a_svclst[0]
            b_first = False
            for a_syno in a_svclst[1]:
                if b_first is False:
                    b_first = True
                    svc_names += ' synonymes: '
                svc_names += a_syno + ', '
            if b_first:
                svc_names = svc_names[0:-2]
            self.stdout.write(svc_names)

    def callService(self, service_name: str, command: int, trace_flag: bool):
        try:
            self.stdout.write('calling the svc ' + service_name + ', command: ' + str(command) + ', trace: ' + str(trace_flag))

        except Exception as inst:
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
