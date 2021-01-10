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
  - [d. **Django**](#d-django)
- [4.	VSCode](#4vscode)
  - [a.	**VS-Code**](#avs-code)
  - [b.	**Extensions Markdown Preview Enhanced**](#bextensions-markdown-preview-enhanced)
  - [b.	**Extensions Python**](#bextensions-python)
  - [c.	**Autre extension,,,**](#cautre-extension)
- [5.	Postgres v 13.1](#5postgres-v-131)
  - [a.	**Postgres - Mac OS**](#apostgres-mac-os)

<!-- /code_chunk_output -->

** Doc v 0.5 **

# 1.	Historique mises à jour
- V0.5 : 10/01/2021. Version initiale, partielle couvrant l’installation sur **Mac OS**.


# 2.	Introduction
Installation d’un environnement de developpement pour le projet **BD Climato**
Cette documentation est écrite pour un mac sous MacOs Big Sur (v11.1)

# 3.	Installation des outils de dévelopement


## a. **Terminal**
Il est recommandé d'utiliser le terminal avancé iTerm2. A télécharger à partir de : [iTerm2](https://iterm2.com)


## b. **git**
?? Faut il installer outil de dev Mac pour avoir git, ou est ce inclus avec VS Code ??

Pour cloner ce projet, allez dans le repertoire parent ou vous voulez cloner le projet. Puis taper la commande:
```shell
git clone https://github.com/MeteoR-OI/bd-climato.git
```


## c. **Python update**
[Download](https://www.python.org/downloads/)
ou brew upgrade ???


## d. **Django**
??


# 4.	VSCode
## a.	**VS-Code**
Installation suivre la doc : [Visual Studio Code Install - Mac](https://code.visualstudio.com/docs/setup/mac)

Suivre la procédure indiqué dans le chapitre **Launching from the command line**, qui permet de lancer vs code, à partir du répertoire contenant les sources, avec la commande

```
   code .
```


Introduction pour les nouveaux utilisateurs :
-  [visual studio tutorial](https://code.visualstudio.com/docs/getstarted/introvideos)
-  Nombreux **tutos** à partir de google… 

## b.	**Extensions Markdown Preview Enhanced**

**Trés utile pour visualiser ce fichier a partir de VS Code**

Permet sur un fichier markdown (.md) d'afficher un preview de la doc, via le raccourci command-k v

Pour installer: racourci Shift-Command-P, puis **Extensions:Install Extensions**, chercher l'extension **Markdown Preview Enhanced**, et l'installer.


## b.	**Extensions Python**
Python, l'extension principale de Python

Il est recommandé de lire les deux documents suivants, et pour les novices en Django de faire le tutorial de la doc **Django-VS Code**


[**Lien vers doc: Extension python/VS Code**](https://code.visualstudio.com/docs/python/python-tutorial#_prerequisites)


[**Lien vers doc: Utilisation Django-VS Code**](https://code.visualstudio.com/docs/python/tutorial-django)


## c.	**Autre extension,,,**
A completer


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
