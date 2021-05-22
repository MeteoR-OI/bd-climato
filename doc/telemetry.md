
![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png) .............. **Telemetry**

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.    Architecture](#2----architecture)
- [3.  Installation en local sur mac](#3--installation-en-local-sur-mac)
- [4.    Visualisation de la Telemetry](#4----visualisation-de-la-telemetry)

**Doc v 0.5**

# 1.	Historique mises à jour
- V 0.5 : 18/01/2021. Version initiale

# 2.    Architecture

- Jaeger : gere les span remontés par django
  http:localhost:16686
  Jaeger ne fait que de stocker les span sur le disque.
  UI tres basic, c'est surtout un backend. Le UI est la surtout pour afficher un span, quand on le connait
  La recherche de span se fait a partir du log (et plus tard a partir de sample de performance), via le champ traceID
  (voir la definition dans grafana/datasource/loki)

- Loki : integre des logs dans Grafana. Stocke les data dans le filesystem
  restructure les donnees a partir de log texte/json, et integre ces donnees dans Grafana.
  Si la ligne de log contient le traceID, il est possible de lier le log avec jaeger

- Prometheus: Gere les metrics
  Pour le moment les metrics de l'application django passent par le log
  Integre les metrics de docker (pas sur mac), jaeger, loki et grafana)
  Langage d'interrogation PromQL
  UI tres basic, c'est surtout un backend

- Grafana : Gere l'affichage de toutes les composantes
  Grafana utilise une base MySQL pour stocker les def des panel (a voir si possible de connecter sur pg...)
  Langage d'interrogation PromQL(prometheus), ou LogQL (loki)

# 3.  Installation en local sur mac
  Installer Docker
  Installer le plus in Docker (de Microsoft) dans VS Code

  Il y a 2 situations:
  - faire tourner toutes les composantes (telemetry, django, et postgres) dans des containers:
    commande: docker-compose -f dc-telemetry-full.yaml up
    (dans ce cas postgres tourne sur le port 5435)
    (dans ce cas django utilise le setting: settings_telemetry_full.py  ** ne pas modifier ** )
  - faire tourner la telemetry dans les containers, et django/postgres en local
    commande: docker-compose -f dc-telemetry-only.yaml up
    (dans ce cas django utilise le port 5434 pour se connecter a postgres)
    (dans ce cas il faut que django utilise le setting: settings_telemetry_only.py  ** ne pas modifier **. faire un export !!! )

  -> la 1ere fois docker-compose telecharge les images en local, et cree des containers (instance d'une image).
  -> les fois suivantes demarre juste les containers
  A partir de VS code, on peut voir les logs, attache un shell au container,..

  Pour arreter: la meme commande avec down a la fin, ou CTRL-C sur la fenetre de la commande

  remise a zero de la telemetry:
     sh ./scripts/clean_localStorage.sh
     dans vs code, dans l'icone Docker, click sur l'icone 'Prune' (a gauche de la roue crantee) dans containers, networks et volumes
     en relancant les containers, la telemetry repartira de zero

  Note: lors de la 1ere utilisation, ou apres une reinitisation, le service promtail n'active pas le scan du log, car le fichier n'existe pas.
    Il est necessaire de langer l'appli django (si pas dans un container), et apres de redemarer le container grrafana/promtail
    Au bout de qq instants les logs de django seront remontes dans Loki

# 4.    Visualisation de la Telemetry
- Tout se passera dans grafana, mais il faut creer les panel....
  localhost:3000

  Il y a de dashboard de base que j'ai trouve, mais pas adapté...

  Dans explore, choisir Loki, puis selectionner le log avec job: django-log
  Visualiser le log

  Et apres il faut apprendre LogQL...
