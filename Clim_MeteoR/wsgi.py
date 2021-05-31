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

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Clim_MeteoR.settings")

application = get_wsgi_application()

SvcAutoLoad.GetInstance().Start()
SvcAggreg.GetInstance().Start()
# SvcLoadObs.GetInstance().Start()
