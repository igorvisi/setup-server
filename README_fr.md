# Serveurs

*See in english in README.md file.*

Ce repo contient la documentation pour les configurations de déploiement sur les différents serveurs.

Pour l'instant, nous avons une configuration qui tourne autour de docker et docker-compose. Voir le dossier docker-compose pour voir la configuration.

Il est prévu de passer à Kubernetes ou/et Nomad après avoir compris et tester en local.

## docker-compose
Ce dossier contient les configurations actuelles des serveurs qui tournent sous Docker et Docker-compose.

## kubernetes
Ce dossier contiendra les configurations tests concernant kubernetes

## nomad
 Ce dossier contiendra les configurations tests concernant nomad.

## Feuille de route

- [**docker-compose**] Mettre en place un système de backup:
Les conteneurs avec Odoo peuvent utiliser le module auto_backup par contre les autres applications vont utiliser les backups de système docker.

- [**docker-compose**] Mettre en place un système de monitoring ainsi que des logs vers Grafana.com ( Prometheus & Loki )

- [**nomad/kubernetes**] Passer à Kubernetes ou/et Nomad. Nomad pour les installations locales et Kubernetes managé pour le cloud.