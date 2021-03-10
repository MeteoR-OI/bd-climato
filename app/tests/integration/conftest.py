import pytest
from django.db import connections
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management import call_command


def run_sql(sql):
    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    from django.conf import settings

    settings.DATABASES['default']['NAME'] = 'clima_test'

    run_sql('DROP DATABASE IF EXISTS clima_test')
    run_sql('CREATE DATABASE clima_test TEMPLATE climatest')

    with django_db_blocker.unblock():
        call_command('loaddata', 'app/tests/integration/fixtures/climato_data.json')

    yield

    for connection in connections.all():
        connection.close()

    run_sql('DROP DATABASE clima_test')
