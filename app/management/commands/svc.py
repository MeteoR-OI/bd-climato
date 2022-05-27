from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('service_name', default='--help', type=str)
        parser.add_argument('action', default='status', type=str)
        parser.add_argument('option', nargs='?', default={}, type=str)

        # Named (optional) arguments
        parser.add_argument(
            '--param',
            action='store_true',
            help='Parameter to pass to the service',
        )

    def handle(self, *args, **options):
        try:
            name = options['service_name']
            action = options['action']
            param = options['option']

            print("svc: " + str(name) + ", action: " + str(action) + ", param: " + str(param))
        except Exception as ex:
            raise CommandError('Error ' + str(ex))
