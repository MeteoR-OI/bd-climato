@import "meteoi.re-logo_mini.png"
**Projet BD Climato**

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.	Introduction](#2introduction)
- [3.	Installation des outils de dévelopement](#3installation-des-outils-de-dévelopement)
  - [a. **Terminal**](#a-terminal)
  - [b. **git**](#b-git)
  - [c. **Python update**](#c-python-update)
- [4.	VSCode et extensions](#4vscode-et-extensions)
  - [a.	**VS-Code**](#avs-code)
  - [b.	**Extensions Markdown Preview Enhanced**](#bextensions-markdown-preview-enhanced)
  - [b.	**Extensions Python**](#bextensions-python)
- [5.	Postgres v 13.1](#5postgres-v-131)
  - [a.	**Postgres - Mac OS**](#apostgres-mac-os)
  - [b. Création d'une base de test](#b-création-dune-base-de-test)
- [6.	**Lancer VS Code sur le projet**](#6lancer-vs-code-sur-le-projet)

<!-- /code_chunk_output -->

** Doc v 0.5 **

# 1.	Historique mises à jour
- V0.5 : 10/01/2021. Version initiale, partielle couvrant l’installation sur **Mac OS**.


# 2.	Introduction
Installation d’un environnement de developpement pour le projet **BD Climato**
Cette documentation est écrite pour un mac sous MacOs Big Sur (v11.1)

# 3.	Installation des outils de dévelopement
Il est recommandé de faire les installations dans l'ordre de ce tutorial

## a. **Terminal**
Il est recommandé d'utiliser le terminal avancé iTerm2. A télécharger à partir de : [iTerm2](https://iterm2.com)


## b. **git**
?? Faut il installer outil de dev Mac pour avoir git, ou est ce inclus avec VS Code ??

Pour cloner ce projet, allez dans le repertoire parent ou vous voulez cloner le projet. Puis taper la commande:
```shell
git clone https://github.com/MeteoR-OI/bd-climato.git
```


## c. **Python update**
brew install python3

lancer la commande pip3 --list, pour vérifier s'il est nécessaire de faire une mise à jour du programme pip3. Si cela est le cas, exécuter la commande indiquée.

# 4.	VSCode et extensions
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

## b.	**Extensions Markdown Preview Enhanced**

**=> Très utile pour visualiser ce fichier à partir de VS Code**

Permet sur un fichier markdown (.md) d'afficher un preview de la doc, via le raccourci command-k v

Pour installer: racourci Shift-Command-P, puis **Extensions:Install Extensions**, chercher l'extension **Markdown Preview Enhanced**, et l'installer.


## b.	**Extensions Python**
Python, l'extension principale de Python
@import "pythonextenstion.png"

Il est recommandé de lire les deux documents suivants, et pour les novices en Django de faire le tutorial de la doc **Django-VS Code**


[**Lien vers doc: Extension python/VS Code**](https://code.visualstudio.com/docs/python/python-tutorial#_prerequisites). Explique bien la notion d'environnement, et comment VS Code l'active automatiquement


[**Lien vers doc: Utilisation Django-VS Code**](https://code.visualstudio.com/docs/python/tutorial-django)


# 5.	Postgres v 13.1
## a.	**Postgres - Mac OS**
Install Postgres en suivant la procédure : [Install Postgres](https://postgresapp.com)

Un nouvel icone est ajouté, permettant de gérer la version, le paramétrage du serveur (démarrage automatique, utilisation de plusieurs versions, mise à jour, ports utilisés…)

@import "./postgresAppAdmin.png"

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

## b. Création d'une base de test
?? Comment creer, et charger une base de donnees de test ??


# 6.	**Lancer VS Code sur le projet**
Aller dans le repertoire du projet, et lancer VS Code.
```
code .
```
Activer l'environnement python si cela est demandé.
@import "selectPython.png"


Activer la version de python installée, v3.9.1 au moment d'ecrire ce tutorial)
(voir coment faire dans la doc de l'extension)
@import "pyver.png"


?? Faire un test sur le projet pour verifier que tout est ok ??
