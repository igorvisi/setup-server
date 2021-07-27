# Ansible

See in english in README.md file.

Ansible est une plate-forme logicielle libre pour la configuration et la gestion des ordinateurs. Elle combine le déploiement de logiciels (en) multi-nœuds, l'exécution des tâches ad-hoc, et la gestion de configuration. Elle gère les différents nœuds à travers SSH et ne nécessite l'installation d'aucun logiciel supplémentaire sur ceux-ci. Les modules communiquent via la sortie standard en notation JSON et peuvent être écrits dans n'importe quel langage de programmation. Le système utilise YAML pour exprimer des descriptions réutilisables de systèmes, appelées playbook.

## Structure

Nous avons sur ce projet:
### **playbook.yml**
Ce playbook a pour rôle:
- Installer les logiciels essentiels pour un serveur
- Installer docker, docker-compose et ses dépendances.
- Créer un utilisateur **dk** ainsi que son home dans /opt/dk et l'assigner dans un groupe **docker** pour manipuler docker avec des droits non privilégés.
- Créer un service docker qui va excuter les fichiers docker-compose contenu sur chaque dossier se trouvant dans /opt/dk/

### **templates**
Ce dossier contient les templates jinja qui seront remplacés et envoyer dans les differents dossiers sur le serveur en fonction de la configuration.
- docker-dk.service.j2 pour créer un service dk
- rkhunter.conf.local.j2 configuration de rkhunter.
- rkhunter.service.j2 création d'un service systemd
- rkhunter.timer.j2 création d'une tâche répétitive
- sudoers.j2 pour donner à l'utilisateur dk les droits de stopper,démarrer ou redémarrer le service dk créé

### **hosts**
Ce fichier contient les différentes addresses IP et utilisateurs des hosts qu'il faut configurer.

Plus de documentation, voir le site d' Ansible.

## Comment lancer ?

Éditer le fichier hosts et lancer le playbook:

```bash
ansible-playbook -i hosts playbook -K
# put your password in BECOME password to have sudo privileges
```