#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from gestion.management.commands import init
from django.core.management.base import BaseCommand
from gestion.models import POSTE
# from urllib.request import urlopen


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--poste', action='store', dest='poste', default=None,
            type=str
        )
        parser.add_argument(
            '-d', '--data', action='store', dest='data', default=None,
            type=str
        )

    def handle(self, *args, **options):
        if not options['poste']:
            print("Le poste n'est pas défini")
            return

        if not options['data']:
            print("Le fichier de données n'est pas défini")
            return

        file_name = options['data']
        if not(os.path.exists(options['data'])):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_name = os.path.join(base_dir, options['data'])
            if not(os.path.exists(file_name)):
                print(file_name)
                print("Le fichier est introuvable")
                return

        poste = POSTE.objects.get(CODE_POSTE=options['poste'])

        init.initDonnees(file_name, poste.CODE_POSTE)

        init.initH(poste.CODE_POSTE)
        init.initQ(poste.CODE_POSTE)
        init.initMensQ(poste.CODE_POSTE)
        # init = 1 autorise l'automatisation de la récupération
        poste.INIT = 1
        poste.save()
