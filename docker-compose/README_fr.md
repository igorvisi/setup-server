# Docker
Docker est un logiciel libre permettant de lancer des applications dans des conteneurs logiciels.

Selon la firme de recherche sur l'industrie 451 Research, « Docker est un outil qui peut empaqueter une application et ses dépendances dans un conteneur isolé, qui pourra être exécuté sur n'importe quel serveur ».


# Comment notre système fonctionne actuellement ?

Les logiciels à installé se trouvent sur le script ansible cloud.playbook.yml se trouvant dans ansible. Le script créera aussi un utilisateur dk qui n'aura pas les privilèges sudo mais appartenant au groupe docker qui lui donne le possibilité de manipuler docker.

Tous les projets se trouvent sur /opt/dk/ qui appartient à l'utilisateur dk.

Chaque projet contiendra un ensemble de fichiers. Le dossier docker/samples contient les exemples de projets.

