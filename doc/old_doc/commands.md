![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Intro GIT**

- [1. Historique mises à jour](#1-historique-mises-à-jour)
- [2. Objectif](#2-objectif)
- [3. Chargement des fichiers JSON](#3-chargement-des-fichiers-json)
- [3. Tache de calcul des aggrégations](#3-tache-de-calcul-des-aggrégations)

**Doc v 0.5**

# 1. Historique mises à jour
- V 0.9 : 24/01/2022. Version initiale

# 2. Objectif

Controle le fonctionnement des taches de fond

# 3. Chargement des fichiers JSON

la tache tourne toutes les 30 secondes.
Il est possible de:
```
    Nom de la tache/Synonymes
        svcLoadJson
        svcAutoLoad, autoload, auto, obs, observation, load, loadjson, json
```

Commande: python3 manage.py svc json [options]

Options possibles:
```
  -h, --help            show this help message and exit
  --list                list all available services
  --run                 activate the service
  --start               start the service
  --stop                stop the service
  --status              get the status of the service
  --trace               display trace
  --notrace             stop the tracing of the service
  --tmp                 use tmp tables
  --version             show program's version number and exit
```

# 3. Tache de calcul des aggrégations

la tache tourne toutes les 2 minutes, et est lancée dès qu'un lot de fichiers JSON ont été chargé.

Il est possible de:
```
    Nom de la tache/Synonymes
        svcAggregate
        agg, aggreg, agreg, agregation, aggregation, agregate, aggregate
```

Commande: python3 manage.py svc agg [options]

Options possibles:
```
  -h, --help            show this help message and exit
  --list                list all available services
  --run                 activate the service
  --start               start the service
  --stop                stop the service
  --status              get the status of the service
  --trace               display trace
  --notrace             stop the tracing of the service
  --tmp                 use tmp tables
  --version             show program's version number and exit
```
