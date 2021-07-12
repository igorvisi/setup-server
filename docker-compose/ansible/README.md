# Ansible

Ansible est une plate-forme logicielle libre pour la configuration et la gestion des ordinateurs. Elle combine le déploiement de logiciels (en) multi-nœuds, l'exécution des tâches ad-hoc, et la gestion de configuration. Elle gère les différents nœuds à travers SSH et ne nécessite l'installation d'aucun logiciel supplémentaire sur ceux-ci. Les modules communiquent via la sortie standard en notation JSON et peuvent être écrits dans n'importe quel langage de programmation. Le système utilise YAML pour exprimer des descriptions réutilisables de systèmes, appelées playbook.

## Playbook

Nous avons deux playbook sur ce projet.
* **cloud.playbook.yml**
Ce playbook a pour rôle:
- Installer les logiciels essentiels pour un serveur
- Installer docker, docker-compose et ses dépendances.
- Créer un utilisateur **dk** et l'assigner dans un groupe **docker** pour manipuler docker avec des droits non privilégés.
- Créer un service docker