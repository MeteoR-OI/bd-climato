![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Projet BD Climato**

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.    Format Fichier JSON de test calculus](#2----format-fichier-json-de-test-calculus)
- [3.    Clé name](#3----clé-name)
- [4.    Clé data](#4----clé-data)
- [5.    Clé results](#5----clé-results)
- [5a.   Selection de la ligne à charger dans la base](#5a---selection-de-la-ligne-à-charger-dans-la-base)
- [5b.   Clès/valeurs à tester](#5b---clèsvaleurs-à-tester)
- [5c.   Count de ligne](#5c---count-de-ligne)

<!-- /code_chunk_output -->

**Doc v 0.52**

# 1.	Historique mises à jour
- V0.5 : 26/03/2021. Version initiale

# 2.    Format Fichier JSON de test calculus
Clés name, data, results

# 3.    Clé name
Correspond a la string passée en paramêtre lors de l'appel de la fonction self.t_engine.run_test dans test_calculus.py

# 4.    Clé data
Clause [data] du fichier json

# 5.    Clé results
Contient un tableau des checks du resultat à faire
Tous les tests sont fait sur le poste_id = 1 par defaut.

Il y a deux parties:
# 5a.   Selection de la ligne à charger dans la base

t => donne le type de table, O, H, D, M, Y, A

selection de la date (*Non nécessaire pour le type 'A', ni en cas de test de 'count'*):

soit clé dat, qui est observation.stop_dat, ou agg_xxxx.start_dat
soit idx: la date est calculee à partir de la stop_dat du data[idx]['current']

# 5b.   Clès/valeurs à tester
nom de la clé qui sera testée en retour du calcul, avec la valeur voulue

# 5c.   Count de ligne
la clé count peut être utilisée, avec comme valeur le nombre désiré.

Next version: Ajouter le mot clé "filter": [k:v, k:v]
