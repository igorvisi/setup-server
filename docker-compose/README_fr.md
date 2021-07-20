# Docker

See in english in README.md file.

Docker est un logiciel libre permettant de lancer des applications dans des conteneurs logiciels.

Selon la firme de recherche sur l'industrie 451 Research, « Docker est un outil qui peut empaqueter une application et ses dépendances dans un conteneur isolé, qui pourra être exécuté sur n'importe quel serveur ».

## Docker-compose

Docker Compose est un outil permettant d'exécuter des applications multi-conteneurs sur Docker définies à l'aide du format de fichier Compose. Un fichier Compose est utilisé pour définir la manière dont sont configurés le ou les conteneurs qui composent votre application. Une fois que vous avez un fichier Compose, vous pouvez créer et démarrer votre application avec une seule commande : docker-compose up.

## Comment notre système fonctionne actuellement ?

Nous utilisons Ansible pour setup le serveur, en installant et configurant les logiciels pré-réquis comme docker, docker-compose, rkhunter... Voir la configuration d'Ansible dans le dossier **docker-compose/ansible**.

Tous les projets se placent sur /opt/dk/ qui appartient à l'utilisateur dk ( utilisateur ne possèdant pas les privilèges administrateurs)

Grâce au service créé **dk@.service**, tous les projets dans /opt/dk/ peuvent s'excuter avec docker-compose.

Example:

```bash
# The two commands below are the same
sudo systemctl start dk@zando.service

sudo -u dk docker-compose -f /opt/dk/zando/docker-compose.yml up
# The two commands below are the same too
sudo systemctl start dk@avenirbiz.service

sudo -u dk docker-compose -f /opt/dk/avenirbiz/docker-compose.yml up
```
Le dossier **docker-compose/docker/samples** contient les exemples de comment est structuré les projets déployés.