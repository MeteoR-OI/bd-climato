![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png)
**Intro GIT**

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.	Introduction](#2introduction)
- [3. Techniques avancées](#3-techniques-avancées)

**Doc v 0.5**

# 1.	Historique mises à jour
- V 0.5 : 18/01/2021. Version initiale

# 2.	Introduction
Git est un gestionnaire de source.
Il est integré à VS Code ![menu GIT](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/gitMenu.png)

Une intro en anglais: [lien](https://www.youtube.com/watch?v=F2DBSH2VoHQ)

Tout d'abord il faut cloner ( = copier dans un sous-repertoire) le dépot ( = code source du projet).
La commande est:
```git
    git clone https://github.com/MeteoR-OI/bd-climato.git
    git checkout developpement    # Activer la branche developpement
```

(Attention pour installer correctement le projet, il faut suivre la doc d'installation du projet dans MacOs)

A partir de ce moment toutes les modifications faites en locale sont gardees dans le workspace local, et l'icone a gauche de git ![logo git](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/gitIcone.png)
va indiquer le nombre de fichiers modifiés.
L'icone en haut permet de visualiser les modifications dans un code source
![icone Visu Change](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/gitVisuChange.png)


Pour recevoir les modifications faites par un autre membre de l'equipe:
```git
    git pull    # en mode commande, ou
    VS Code: click sur fleche vers le bas dans le menu **Commits** de l'interface de GIT
```

Avec des modifications actives, il est impossible de changer de branche, ou de recevoir des commits du serveur
La il y a 2 strategies:

1 - Faire un commit local de vos modifications

2 - Annuler toutes les modifications faites localement :
```git
    git reset --hard    # annule toutes les modifications, action definitive !
```

Pour envoyer les modifications vers le serveur, il faut faire passer les fichiers modifies en mode stage, puis faire un commit local. Enfin il faudra faire un push (fleche vers le haut) pour envoyer le commit vers le serveur github

Voir la video pour plus d'info, mais tout se passe dans la barre de **Commits** ![commitBar](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/gitCommitBar.png)

Sinon en mode commande, dans le terminal de VS Code:
```git
# en mode commande, dans le repertoire du depot
git add -A   # 'stage' toutes les modifications
git status   # visualise les fichiers en mode staging
git commit -m 'message expliquand ce qui est fait'  # creation d'un commit local
git push    # pousse le commit vers le serveur   # sinon les autres ne verront pas les modifications
```

# 3. Techniques avancées
Git workflow, un peu theorique, mais permet de comprendre comment git fonctionne [lien](https://www.youtube.com/watch?v=3a2x1iJFJWc)

Une explication de la resolution de conflit, a voir quand le probleme arrivera... [lien](https://www.youtube.com/watch?v=VQ4GF9X2Ix0)
