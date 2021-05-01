
![logo](https://raw.githubusercontent.com/MeteoR-OI/bd-climato/master/doc/images/meteoi.re-logo_mini.png) .............. **Telemetry**

- [1.	Historique mises à jour](#1historique-mises-à-jour)
- [2.    Architecture](#2----architecture)
- [3.  Installation en local sur mac](#3--installation-en-local-sur-mac)
- [4.    Visualisation de la Telemetry](#4----visualisation-de-la-telemetry)

**Doc v 0.5**

# 1.	Historique mises à jour
- V 0.5 : 18/01/2021. Version initiale

# 2.    Architecture

- Jaeger : gere les span remontes par django dans bd cassandra
  https://medium.com/jaegertracing/a-guide-to-deploying-jaeger-on-kubernetes-in-production-69afb9a7c8e5
  Base de cassandra : demarer un shell a partir du container, lancer sqlsh (syntaxe a la SQL)
  Pour le moment Jaeger ne sait qu'afficher les span. Il y a en dev la generation de statistiques
  a partir des span... cela nous permettrait d'enlever prometheus des composants a avoir sur le serveur

- Loki : integre des logs dans Grafana. ?? ou c'est stocké ??
  restructure les items a partir de log texte/json, et les integre dans Grafana. Si la ligne de log contient
  le span_id, il est possible de lier toutes ces informations ensemble

- Prometheus: Gere les metrics (Voir si on en a besoin, ou si on peut gerer les metrics autrement)
  on va voir si on garde ou pas...

- Grafana : Gere l'affichage et la liaison entre metrics/log/span
  Grafana utilise une base SQL pour stocker les def des panel (a voir si possible de connecter sur pg...)

# 3.  Installation en local sur mac
  Installer Docker
  Installer le plus in Docker (de Microsoft) dans VS Code
  docker compose -f yml/docker-compose.yml up
  -> la 1ere fois telecharge les images en local, et cree des containers (instance d'une image).
  -> les fois suivantes demarre juste les containers
  A partir de VS code, on peut voir les logs, attache un shell au container,..

  Pour activer l'integration de la telemetry dans Climato:
    dans settings.py:
        TELEMETRY = True
    Sans cette variable, la valeur est False

# 4.    Visualisation de la Telemetry
- Tout se passera dans grafana, mais il faut creer les panel....
  localhost:3000
  Il faut installer les sources:
    . jaeger -> http://jaeger-query:16686
    . prometheus -> http://prometheus:9090
    . loki -> http://loki:3100
  Je verrai comment generer les conf, et les panels par defaut....
- Il est possible d'aller directement dans jaeger, mais l'interface est assez pauvre
  localhost:16686 (admin/admin, puis changement de mot de passe a la 1ere connection)
