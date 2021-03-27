![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Doc migration**

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1. Historique mises à jour](#1-historique-mises-à-jour)
- [2. Initialisation](#2-initialisation)
- [3. Format Json test calculus](#3-format-json-test-calculus)

<!-- /code_chunk_output -->

** Doc v 0.5 **


# 1. Historique mises à jour
- V0.5 : 09/02/2021. Version initiale

# 2. Initialisation
- utiliser Clim_MeteoR/settings.app.py -> settings.py
  Ajuster au besoin les parametres (nom/pass pour postgres)
- creer une base climatest
- lancer les commandes:


```python
python3 manage.py migrate
python3 manage.py makemigrations app
python3 manage.py migrate app
python3 manage.py createsuperuser   # creation de votre compte d'admin
psql -U <user> -P <pass> -d climatest < ./data/appInit.sql
```

- start Django
- Test the following URLs:
  - http://127.0.0.1:8000/admin
    Log in, Look at the data in the db, do not edit them at this stage
  - http://localhost:8000/app/calc/test1.json => lance le calcul sur le fichier data/json_not_in_git/test1.json
  [] est affiché dans le navigateur à la fin du calcul, mais les tables ont ete mises a jour dans la bd

# 3. Format Json test calculus
[lien](calculus_test_suite.md)
