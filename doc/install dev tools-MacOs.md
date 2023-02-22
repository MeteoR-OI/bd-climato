![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Projet BD Climato**

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.	Introduction](#2introduction)
- [3.	Installation des outils de dévelopement](#3installation-des-outils-de-dévelopement)
  - [a. **Terminal**](#a-terminal)
  - [b. **git**](#b-git)
  - [c. **Python update**](#c-python-update)
- [4. Activation d'un environnement local, et initialisation des modules](#4-activation-dun-environnement-local-et-initialisation-des-modules)
- [5. VSCode et extensions](#5-vscode-et-extensions)
  - [a.	**VS-Code**](#avs-code)
  - [b.	**Extensions Markdown All in One**](#bextensions-markdown-all-in-one)
  - [b.	**Extensions Python**](#bextensions-python)
- [5.	Postgres v 13.1](#5postgres-v-131)
  - [a.	**Postgres - Mac OS**](#apostgres---mac-os)
  - [b. Création de la base de données locale vide](#b-création-de-la-base-de-données-locale-vide)
- [6. Activer le setting local](#6-activer-le-setting-local)
- [7.	**Lancer VS Code sur le projet**](#7lancer-vs-code-sur-le-projet)
- [8, Code coverage](#8-code-coverage)
- [9. Ajout d'un bouton pour declencher le code cov](#9-ajout-dun-bouton-pour-declencher-le-code-cov)

<!-- /code_chunk_output -->

**Doc v 0.53**

# 1.	Historique mises à jour
- V 0.5 : 10/01/2021. Version initiale, partielle couvrant l’installation sur **Mac OS**.
- v 0.51: 16/01/2021. Images well displayed on github.com 
- v 0.52: 17/01/2021. Ajout de la copie du settings.py lors de l'installation, et init git
- v 0.53: 19/01/2021. Ajout info login postgres, et variable d'environnement

# 2.	Introduction
Installation d’un environnement de developpement pour le projet **BD Climato**
Cette documentation est écrite pour un mac sous MacOs Big Sur (v11.1)

# 3.	Installation des outils de dévelopement
Il est recommandé de faire les installations dans l'ordre de ce tutorial

## a. **Terminal**
Il est recommandé d'utiliser le terminal avancé iTerm2. A télécharger à partir de : [iTerm2](https://iterm2.com)


## b. **git**
Le mieux est d'utiliser la version de git de **Xcode Command Line Tools**

Lancer la commande:
``` shell
git --version
```
Si git n'est pas installé, il vous demandera de le faire
(Sinon aussi possible d'installer l'outil graphique de github [Install]( https://desktop.github.com))

Ensuite il faut cloner le projet (= recuperer les sources), pour cela allez dans le repertoire parent ou vous voulez copier le projet. Puis taper la commande:

```shell
git clone https://github.com/MeteoR-OI/bd-climato.git
git checkout developpement    # Activer la branche developpement
```

Si c'est la premiere fois que git est utilisé, il faut définir le nom et l'email:
```git
    git config --global user.name "Votre Nom"
    git config --global user.email "email@server.com"
    git config --global --list  # pour voir les donnees saisies
```

## c. **Python update**
brew install python3  (Version doit etre >= 3.9.1)

lancer la commande pip3 --list, pour vérifier s'il est nécessaire de faire une mise à jour du programme pip3. Si cela est le cas, exécuter la commande indiquée.

# 4. Activation d'un environnement local, et initialisation des modules
Cela n'est a faire qu'une fois.
Un environnement local permet de charger les modules que dans le cadre de ce projet.
Dans le repertoire du projet, taper les commandes (terminal de MacOs):
``` shell
    python3 -m venv .venv
    source .venv/bin/activate   # le prompt va indiquer l'environnement
    pip3 list     # si necessaire faire la mise a jour de pip3
                  # comme indiqué
    pip3 install -r requirements.txt  # install les modules
    pip3 list     # doit retourner les modules installés
    exit          # Fermer cette session
```
L'environnement va etre automatiquement activé par VS Code lost de l'ouverture d'un fichier python, ou de l'activation du terminal de VS Code.

# 5. VSCode et extensions
## a.	**VS-Code**
Installation suivre la doc : [Visual Studio Code Install - Mac](https://code.visualstudio.com/docs/setup/mac)

Suivre la procédure indiqué dans le chapitre **Launching from the command line**, qui permet de lancer vs code, à partir du répertoire contenant les sources, avec la commande

```
   code .
```

Avant que l'extension Python soit installée, ou pour faire des tests ou tuto, il est préférable d'être dans un répertoire différent que celui du projet BD Climato.

vIntroduction pour les nouveaux utilisateurs :
-  [visual studio tutorial](https://code.visualstudio.com/docs/getstarted/introvideos).
-  Nombreux **tutos** à partir de google… 

## b.	**Extensions Markdown All in One**

**=> Très utile pour visualiser ce fichier à partir de VS Code**

Permet sur un fichier markdown (.md) d'afficher un preview de la doc, via le raccourci command-k v
Aussi maintient automatiquement le TOC de chaque fichier .md

Pour installer: racourci Shift-Command-P, puis **Extensions:Install Extensions**, chercher l'extension **Markdown All in One**, et l'installer.


## b.	**Extensions Python**
Python, l'extension principale de Python
![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/pythonextenstion.png)

Il est recommandé de lire les deux documents suivants, et pour les novices en Django de faire le tutorial de la doc **Django-VS Code**


[**Lien vers doc: Extension python/VS Code**](https://code.visualstudio.com/docs/python/python-tutorial#_prerequisites). Explique bien la notion d'environnement, et comment VS Code l'active automatiquement


[**Lien vers doc: Utilisation Django-VS Code**](https://code.visualstudio.com/docs/python/tutorial-django)


# 5.	Postgres v 13.1
## a.	**Postgres - Mac OS**
Install Postgres en suivant la procédure : [Install Postgres](https://postgresapp.com)

Un nouvel icone est ajouté, permettant de gérer la version, le paramétrage du serveur (démarrage automatique, utilisation de plusieurs versions, mise à jour, ports utilisés…)

![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/postgresAppAdmin.png)

Sur MacOs BigSur, mettre à jour le fichier .zshrc (Sur des versions antérieures, vérifier le shell utilisé, et au besoin passer sous zsh). Ajouter les lignes suivantes (commande: **sudo code .zshrc**) :
```shell
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin
```
Relancer le terminal, et tester que Postgres fonctionne :
```shell
   psql -U postgres
   -> doit afficher la version du serveur
   \q    (pour sortir)
```

Le login vers postgres est gere de la façon suivante:
- User: Variable d'environnement PGUSER, ou 'bd_clim'
- Password: Variable d'environnement PGPASS, ou mot de passe dans settings.py
- Host name: 'localhost'

Pour initialiser les variables d'environnement, mettre un export dans le fichier
~/.zshrc (big Sur, ou shell zsc), ~/.bashrc (version plus ancienne, shell bash)
exemple:
    export PGUSER=postgres
    export PGPASS=votre_mot_de_passe

## b. Création de la base de données locale vide
Tapez les commandes suivantes dans un terminal:
```shell
psql -U postgres    # Vous allez etre dans le prompt de psql

CREATE DATABASE climatest;
\q                  # retour sur le prompt du terminal
exit
```

# 6. Activer le setting local
Dans le repertoire **Clim_MeteoR** lancer la commande:
```shell
cp settings.local.py settings.py
```
Le fichier settings.py n'est pas inclus dans le depot Git.
Il est donc possible de le personnaliser pour chaque machine.

# 7.	**Lancer VS Code sur le projet**
Aller dans le repertoire du projet, et lancer VS Code.
```
code .
```

Activer l'environnement python si cela est demandé.
![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/selectPython.png)

S
Activer la version de python installée, v3.9.1 au moment d'ecrire ce tutorial)
(voir coment faire dans la doc de l'extension)
![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/pyver.png)

Pour initialiser la base de données (a faire qu'une fois): dans le terminal de VS Code, tapez la commande:
```shell
  python3 manage.py migrate
````

Le programme peut etre lancé, ou debug
python3 manage.py runserver

# 8. Debug code Django
Pour ajouter Django comme commande du debugger, il faut ajouter les lignes suivantes dans le fichier .vscode/lanunch.json:

```JSON
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: 
    // https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver"
            ],
            "env": {
                "DJANGO_SETTINGS_MODULE": "Clim_MeteoR.settings",
            },
            "django": true
        }
    ]
}
```
# 8, Code coverage
Mes tests me chargent pas dans le test explorer de python.
J'ai installe **l'extension Python Test Explorer** for Visual Studio Code

Pour avoir la visualisation du code coverage dans vs code, il faut installer l'extension:
  **coverage-gutters**. J'ai prefere la version 2.60, downloadé par 89K personnes

On doit pouvoir faire une tache vs code pour automatiser tout cela.
pour le moment je passe en mode commande pour mettre a jour le code coverage:

``` shell
  coverage run -m pytest tests
  coverage xml
```

pour generer les pages html dans le repertoire htmlcov (non envoye sur git):
``` shell
  coverage html
  open htmlcov/index.html
````

# 9. Ajout d'un bouton pour declencher le code cov
Installer l extension **VsCode Action Buttons**
Un bouton Jaune **CodeCov** permettant de lancer la commande de code coverage va apparaitre dans la barre de status (en bas)
