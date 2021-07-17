# Docker
Docker is open source software for running applications in software containers.

According to industry research firm 451 Research, "Docker is a tool that can package an application and its dependencies into an isolated container, which can be run on any server."


# How does our system currently work?

The software to be installed is on the ansible script cloud.playbook.yml found in ansible. The script will also create a user dk who will not have sudo privileges but will belong to the docker group which gives him the ability to manipulate docker.

All projects are located on /opt/dk/ which belongs to the user dk.

Each project will contain a set of files. The folder docker/samples contains the sample projects.