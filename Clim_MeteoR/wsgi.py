"""
WSGI config for Clim_MeteoR project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import django
django.setup()
import os
from django.conf import settings

if os.getenv("CC_PYTHON_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Clim_MeteoR.settings")

# from app.classes.workers.svcLoadCsv import SvcCsvLoader
# from app.classes.workers.svcLoadJson import SvcJsonLoader
from app.classes.workers.svcMigrate import SvcMigrate
from django.core.wsgi import get_wsgi_application

# svc_csv_loader = SvcCsvLoader()
# svc_csv_loader.Start()
# svc_csv_loader.RunMe()

# svc_json_loader = SvcJsonLoader()
# svc_json_loader.Start()
# svc_json_loader.RunMe()

svc_migrate = SvcMigrate()
svc_migrate.Start()
svc_migrate.RunMe()

# from prometheus_client import make_wsgi_app
# from wsgiref.simple_server import make_server


application = get_wsgi_application()

# SvcAutoLoad.GetInstance().Start()
# SvcAggregate.GetInstance().Start()

# httpd = make_server('', 8080, application)
# httpd.serve_forever()

# app = make_wsgi_app()
# httpd = make_server('', 8000, app)
# httpd.serve_forever()
