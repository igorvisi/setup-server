# Servers

*Voir en français dans le fichier README.md .*

This repo contains the documentation for the deployment configurations on the different servers.

For now, we have a configuration that revolves around docker and docker-compose. See the docker-compose folder to see the configuration.

The plan is to move to Kubernetes or/and Nomad after we understand and test in local.

## docker-compose
This folder contains the current configurations of the servers running Docker and Docker-compose.

## kubernetes
This folder will contain the test configurations for kubernetes

## nomad
 This folder will contain the test configurations for nomad.

## Roadmap

- Set up a backup system:
Containers with Odoo can use the auto_backup module however other applications will use docker system backups.

- Set up a monitoring system and logs to Grafana.com ( Prometheus & Loki )

- Nomad/kubernetes**] Switch to Kubernetes or/and Nomad. Nomad for local installations and managed Kubernetes for the cloud.