To be done...


Qq remarques:



# 1.	Historique mises à jour
- V1.0 : 10/01/2021. Version initiale couvrant l’installation sur **Mac OS**.


# 2.	Introduction
Installation d’un environnement de developpement pour le projet **BD Climato**
Cette documentation est écrite pour un mac sous MacOs Big Sur (v11.1)

# 3.	Quelques outils à installer


## a. **Terminal**
Sous **Windows**, avec le sous système Linux, il est recommandé de telecharger à partir du store le nouveau terminal Windows: [**Download Windows Terminal**](https://www.microsoft.com/en-mu/p/windows-terminal-preview/9n0dx20hk701?SilentAuth=1&wa=wsignin1.0&rtc=1&activetab=pivot:overviewtab)


## b. Windows - **Python update**
[Download](https://www.python.org/downloads/)
ou brew upgrade ???

## c. MacOs - **Django**

## d. **git**
Sous MacOs: ?? Faut il installer outil de dev Mac pour avoir git, ou est ce inclus avec VS Code ??

Windows : Idem...

## e. Windows - **Ubuntu subsystem v2**
Sous Windows 2 possibilités:
- Utilisation natif Windows
- Utilisation sous systeme Linux v2

... On documentera quand le besoin existera, mais sous systeme linux est preferable..

# 4.	VSCode
## a.	**VS-Code**
Installation à partir de : [Visual Studio Code Install](https://code.visualstudio.com/docs/setup/setup-overview)

Bien faire la procédure propre à chaque système d'exploitation. Entre autre sur MacOs bien suivre la procédure **Launching from the command line**, qui permet de lancer vs code, à partir du répertoire contenant les sources, avec la commande

```
   code .
```


Introduction pour les nouveaux utilisateurs :
-  [visual studio tutorial](https://code.visualstudio.com/docs/getstarted/introvideos)
-  Nombreux **tutos** à partir de google… 

## b.	**Extensions Markdown Preview Enhanced**
Sur MacOs, sur un fichier markdown (.md), command-k v affiche un preview du fichier markdown

Sous MacOS-VS Code, Shift-Command-P, puis **Extensions:Install Extensions**, chercher l'extension **Markdown Preview Enhanced**, et l'installer.

## b.	**Extensions Python**
ms-python.python, l'extension principale de Python

Il est recommandé de lire les deux documents suivants, et pour les novices en Django de faire le tutorial de la doc **Django-VS Code**


[**Lien vers doc: Extension python/VS Code**](https://code.visualstudio.com/docs/python/python-tutorial#_prerequisites)


[**Lien vers doc: Utilisation Django-VS Code**](https://code.visualstudio.com/docs/python/tutorial-django)

## c.	**Autre extension,,,**

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
