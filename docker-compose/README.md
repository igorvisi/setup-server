# Docker

Voir en français dans le fichier README_fr.md .

Docker is an open source software for running applications in software containers.

According to industry research firm 451 Research, « Docker is a tool that can package an application and its dependencies into an isolated container that can be run on any server ».

## Docker-compose

Docker Compose is a tool for running multi-container applications on Docker defined using the Compose file format. A Compose file is used to define how the container(s) that make up your application are configured. Once you have a Compose file, you can create and start your application with a single command: docker-compose up.

## How does our system currently work?

We use Ansible to setup the server, installing and configuring the pre-requisites like docker, docker-compose, rkhunter... See the Ansible configuration in the **docker-compose/ansible** folder.

All projects are placed on /opt/dk/ which belongs to the user dk (user without administrator privileges)

Thanks to the created service **dk@.service**, all projects in /opt/dk/ can be executed with docker-compose.

Example:

```bash
# The two commands below are the same
sudo systemctl start dk@zando.service

sudo -u dk docker-compose -f /opt/dk/zando/docker-compose.yml up
# The two commands below are the same too
sudo systemctl start dk@avenirbiz.service

sudo -u dk docker-compose -f /opt/dk/avenirbiz/docker-compose.yml up
```
The folder **docker-compose/docker/samples** contains the examples of how the deployed projects are structured.