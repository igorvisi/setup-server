# Ansible

Voir en français dans le fichier README_fr.md .

Ansible is a free software platform for computer configuration and management. It combines multi-node software deployment, ad-hoc task execution, and configuration management. It manages individual nodes through SSH and does not require any additional software to be installed on them. Modules communicate via standard output in JSON notation and can be written in any programming language. The system uses YAML to express reusable system descriptions, called playbooks.

## Structure

On this project we have:
### **playbook.yml**
This playbook has the following role:
- Install the essential software for a server
- Install docker, docker-compose and its dependencies.
- Create a **dk** user with his home in /opt/dk and assign it to a **docker** group to manipulate docker with unprivileged rights.
- Create a docker service that will run the docker-compose files contained on each folder in /opt/dk/

### **templates**
This folder contains the jinja templates that will be go to different directories in server .
- docker-dk.service.j2 to create a dk service
- rkhunter.conf.local.j2 configuration of rkhunter.
- rkhunter.service.j2 creation of a systemd service
- rkhunter.timer.j2 creation of a repetitive task
- sudoers.j2 to give the dk user the rights to stop, start or restart the created dk service

### **hosts**
This file contains the different IP adresses and users of hosts that must be configured.

More documentation, see the Ansible website.

## How to run

Edit hosts file and run playbook:

```bash
ansible-playbook -i hosts playbook
```