"""
WSGI config for Clim_MeteoR project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from app.classes.workers.svcAggreg import SvcAggreg
from app.classes.workers.svcAutoLoad import SvcAutoLoad
# from app.classes.workers.svcLoadObs import SvcLoadObs
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Clim_MeteoR.settings")

application = get_wsgi_application()

SvcAutoLoad.GetInstance().Start()
SvcAggreg.GetInstance().Start()
# SvcLoadObs.GetInstance().Start()

# httpd = make_server('', 8080, application)
# httpd.serve_forever()

app = make_wsgi_app()
httpd = make_server('', 8000, app)
# httpd.serve_forever()
