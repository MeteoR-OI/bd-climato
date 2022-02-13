![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Projet BD Climato**

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.    Poste](#2----poste)
- [3. Type instrument (table type_instrument)](#3-type-instrument-table-type_instrument)
- [4. Exclusion (table exclusion)](#4-exclusion-table-exclusion)
- [5. Observation (table obs)](#5-observation-table-obs)
- [6. aggTodo (table agg_todo)](#6-aggtodo-table-agg_todo)
- [7. Extreme todo (extreme_todo)](#7-extreme-todo-extreme_todo)
- [8. Aggregation horaire (table: agg_hour)](#8-aggregation-horaire-table-agg_hour)
- [9. Aggrégation de niveau supérieur (tables: agg_day, agg_month, agg_year, agg_all)](#9-aggrégation-de-niveau-supérieur-tables-agg_day-agg_month-agg_year-agg_all)
- [10. Historique Aggrégation (table: agg_histo)](#10-historique-aggrégation-table-agg_histo)
- [11. Incident (table: incident)](#11-incident-table-incident)
- [12. Creation de la base de données](#12-creation-de-la-base-de-données)

<!-- /code_chunk_output -->

**Doc v 1.0**

# 1.	Historique mises à jour
- V0.5 : 21/01/2022. Version initiale

# 2.    Poste

Un enregistrement par station météo du réseau meteoR

```
id: clé du poste
meteor: code de la station dans le réseau meteoR
fuseau: nombre d'heure entre TU et heure locale (4 par défaut)
lock_calculus: indicateur de blocage logique de la station, car un calcul est en-cours

-- Données non utilisées actuellement:
meteofr: code de la station chez météo Francelock_calculus
title:
owner:
email:
phone:
address:
zip:
city:
country:
latitude:
longitude:
start_dat: date de debut de mise en ligne dans le reseau meteoR
stop_dat: date de deconnexion du reseau meteoR
comment:
```

# 3. Type instrument (table type_instrument)

```
Un enregistrement par type d'instrument:
    1	Temp
    2	Humidite
    3	Pression
    4	Rain
    5	Wind
    6	Solar
    7	Interieur
    9	Divers
    
id: clé (ne peut pas être changé)
name: nom du type
model_value: Json specifiant les clés possibles pour les exclusions (futur developpement)
    Tableay de key/value
        key: = nom de la clé de la mesure (ex out_temp)
        value: type (float, int, string)
```

# 4. Exclusion (table exclusion)

```
id: no chronologique
poste: id de la station
type_instrument: cle du type instrument
start_dat: date debut de l'exclusion (inclue dans l'exclusion)
stop_dat: date fin de l'exclusion (inclue)
value: pour chaque "key"
    valeur du type defini dans model_value -> force une valeur
    "null": ne pas tenir compte des observations
```

# 5. Observation (table obs)

```
id: no chronologique
poste: id de la station
agg_start_dat: date/heure de l'aggregation horaire principal ou seront aggregées les données (si pas de decalage). Calculé lors de l'intégration des fichiers json dans la bd
stop_dat: date/heure de fin de l'observation
duration: durée de la donnée elementaire
filename: nom du fichier json d'ou ces données ont ete chargées

qa_modifications: futur
qa_incidents: futur
qa_check_done: boolean si le check qualité a ete fait sur cette donnée
j: json. Les clés utilisées sont decrite dans le document doc/bd_schema/specification_json.doc
j_agg: données d'aggrégation pré-calculé par weeWX
```

# 6. aggTodo (table agg_todo)

```
Table contenant les delta de données provenant d'une observation, en attente d'intégration dans les aggrégations. Est supprimé quand l'intégration a ete faite.

id: no chronologique
priority:
status: 0: wait pour integration, 9: error-non intégré, 999 intégré non supprimé (mode debug)
j_dv: delta des valeurs a intégrer dans les aggrégations
j_agg: aggrégation pré-calculé par weeWX
j_error: error information, quand le status est = 9
```

# 7. Extreme todo (extreme_todo)

```
Liste des extreme a recalculer, suite a certaines mise a jour

id: no chronologique
poste: id de la station
level: niveau de l'agregation de depart (H, D, M, Y, A).
   l'extreme sera recalculé à ce niveau, et aux niveaux supérieur si nécessaire
start_dat: date/heure de l'aggrégation

...A specifier...
invalid_type
status:
j_recompute:
```

# 8. Aggregation horaire (table: agg_hour)

```
Aggrégations horaire pré-calculées
-> La structure est la même dans les niveaux supérieurs

id: no chronologique
poste: id de la station
start_dat: date/heure du debut de l'aggrégation (heure ronde pour aggrégation horaire)
duration_sum: somme des duration des observations aggrégées
duration_max: somme totale des durations pour que l'aggrégation soit complétement chargée

qa_modifications: futur
qa_incidents: futur
qa_check_done: boolean si le check qualité a ete fait sur cette donnée

j: json contenant les données aggrégées. Spécifié dans le document: doc/bd_schema/specification_json.doc
```

# 9. Aggrégation de niveau supérieur (tables: agg_day, agg_month, agg_year, agg_all)

```
Même structure que celle de l'aggrêgation horaire
```

# 10. Historique Aggrégation (table: agg_histo)

```
Table gardant trace de quelles observations ont mis à jour quelles aggrégations horaires et journalières

id: no chronologique
obs_id: id de l'observation
agg_id: id de l'aggrégation (agg_hour ou agg_day)
agg_level: 'H' ou 'D'
delta_duration: delta de duration pour l'aggrégation
j: delta de valeurs mis à jour
```

# 11. Incident (table: incident)

```
Table des incidents

id: no chronologique
dat: date/heure de l'incident
source:
level:
reason:
j: json data
active: defaut True, mis à False quand l'incident a ete corrigé
```

# 12. Creation de la base de données
Dans psql, supprimer la base si elle existe.
Executer le script suivant:

```
psql -U postgres
   -> create database climatest;
   \q
python manage.py migrate
python manage.py createsuperuser
   -> mettre un mot de passe (outil d'admin)
psql -d climatest < data/appInit.sql
```
