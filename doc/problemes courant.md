![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Projet BD Climato**

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.	Environnement virtuel](#2environnement-virtuel)
- [2.1 suppression des modules installés en global](#21-suppression-des-modules-installés-en-global)
- [2.2 Reactivation de l'environnement](#22-reactivation-de-lenvironnement)
- [3. Postgres ne demarre pas](#3-postgres-ne-demarre-pas)
- [4. Info sur manage.py et migration](#4-info-sur-managepy-et-migration)
- [5. Regeneration de la base de données](#5-regeneration-de-la-base-de-données)


**Doc v 0.5**

# 1.	Historique mises à jour
- V0.5 : 15/01/2021. Version initiale


# 2.	Environnement virtuel

# 2.1 suppression des modules installés en global
 pip3 uninstall -r requirements.txt

# 2.2 Reactivation de l'environnement
- desinstaller les modules installés en global
- en mode commande (hors VS Code), dans le repertoire du projet, taper:
```shell
  python3 -m venv .venv
  code .
```
- Si l'environnement n'est pas activé, essayer:
  - ouvrir manage.py (l'environnement doit s'activer automatiquement)
  - Sinon taper la commande dans un terminal de VS Code:
      source .venv/bin/activate
- dans un terminal de VS Code taper:
  ``` shell
  pip3 list                              # affiche les modules installés
                                         # globaux et locaux
  python3 -m pip install --upgrade pip   # update pip3 si demandé
  pip3 install -r requirements.txt       # Recharge les modules dans l'env.
  ```
- La commande 'pip3 list' dans un terminal d'OSX ne doit retourner que les modules globaux

# 3. Postgres ne demarre pas
Cela peut etre du au fichier postmaster.pid non supprimé sur postgres13

Click sur l'elephant dans la barre du haut, puis Preferences/Server settings
Click sur boutton **Show** du **Data Directory**
Effacer le fichier postmaster.pid s'il existe
Click sur *start**

Si ce n'est pas cela, regarder les dernieres lignes du log...

# 4. Info sur manage.py et migration
https://docs.djangoproject.com/fr/3.1/ref/django-admin/

# 5. Regeneration de la base de données
lancer les commandes suivantes:
``` code
psql
    drop database climatest;
    create database climatest;
    \q
python3 manage.py migrate
python3 manage.py createsuperuser
psql -d climatest < data/appInit.sql
python3 manage.py runserver

=> Aller dans http://localhost/admin. Toutes les tables (sauf agg_xxx) ont qq donnees.
```

Si psql refuse de se connecter, mettre les noms utilisateurs et mot de passe comme suit:
export PGUSER=toto     (nom utilisateur)
export PGPASS=titi     (mot de passe)
(Pas d'espace de chaque cote du signe =)
