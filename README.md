# Architecture with Docker before Kubernetes
This repo contains all tools docker-compose files used by Avenir Business. Each docker-compose is only one application stack. But for some purpose, two or three docker-compose file can be merged in production.

Example:
* Dashboard ( Grafana + Loki + Prometheus + Alert manager ). (
[github.com/avenirbiz/docker_dashboard/](https://github.com/avenirbiz/docker_dashboard/) ).

* Odoo ( Odoo + Postgres + Adminer + futurice/volume-backup)
[github.com/avenirbiz/docker_odoo](https://github.com/avenirbiz/docker_odoo)

## Description of directory

Each projet can contain:
* **sample.env** contains example of variables must be in .env file. As is not good to put credentials in Github* Alertmanager to send alert based on metrics trigger.
, variables in .env must come from password manager.
* **.env** contains variables and creditentials which must be set per projet like domaine name, database password,...
* **docker-compose.yml** contains configuration of running containers and traefik label for dynamic configuration
* **/etc/** contains configuration which must be insert inside running containers like odoo.conf ...
* **generate.py** Script to generate file like odoo.conf because in some case, configuration must be generated from ( .env or psono ) like odoo.conf,... like in Odoo, if database container run with database password from .env, the odoo.conf must have the same database password.

## Custom way to setup dev env
Nota: For develop, you are not obliged to put projet in /opt/dk/ and create a dk user. You can put projet in your home like /home/ivisi/Work/. But you must configure the same process of installation and adapt installation with your directory /home/ivisi/Work/. But it often a good idea to have the dev env which is getting closer to the prod env

## Configure the Docker environnement
Running Docker in production requires many security. The first and more important is to run only trusted image. Docker registry doesn't verify if a image contains malicious code or not.
1. Update server

```bash
sudo apt update && sudo apt upgrade
```

2. Install unattended-upgrades for automatically install security update
we can configure alert with alertmanager in github.com/avenirbiz/docker_dashboard.

```bash
sudo apt install unattended-upgrades
# Uncomment security update only
sudo vim /etc/apt/apt.conf.d/50unattended-upgrades
# "${distro_id}:${disto_codename}-security";
```
3. Install tools for audit & malware scanner
```bash
sudo apt install lynis rkhunter chkrootkit
sudo lynis audit system
sudo rkhunter --check
sudo chkrootkit

# To make cron with this tools
sudo dkpg-reconfigure rkhunter
sudo dkpg-reconfigure chkrootkit
# Result of log can be see in our dashboard
```

1. Install docker in Linux. [Installation](https://docs.docker.com/engine/install/ubuntu/)
2. Create user docker. It's not recommended to run docker with a root user. If a process in Container run as root, so the process can access in the host as root. Before running a image in a production, we must verify in the Dockerfile, they use an none root user. You can use tool like hadolint to check Dockerfile

```bash
sudo useradd -r -m -d /opt/dk dk
sudo usermod -aG docker dk # Add the user in docker group
```

Inside /opt/dk, we will put all projet. Every projet in will be a git projet from Github.


3. To make every projet inside /opt/dk running as a Systemd service, we must create a file /etc/systemd/system/dk@.service

```bash
[Unit]
Description=%i service with Docker-compose inside /opt/dk/i%
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=/opt/dk/%i
ExectStart=/usr/docker-compose up -d
ExecStop=/usr/docker-compose stop
User=dk
Group=docker

[Install]
WantedBy=multi-user.target
```

```bash
# Reload systemd daemon
sudo systemctl daemon-reload
```

After that, every directory inside /opt/dk/, become a service and can be run by systemctl start dk@directory_name.service .

## Run container app
There is two way to run. One for developing and the other for production or testing

For developing, you need to add domaine manualy in /etc/hosts and create local certificat and configure traefik with dev config. See bellow.

For testing or developing, certificat are auto generated with LetsEncrypt in the domaine point correctly to the server. It's our traefik default configuration.

#### [FOR DEVELOP MODE ONLY] Add your user in dk & docker groups
```bash
sudo usermod -aG dk $USER # Will add your user in dk and docker groups
sudo usermod -aG docker $USER
```
#### [FOR DEVELOP MODE ONLY] Create local SSL certificat for developing test with mkcert [download binary](https://github.com/FiloSottile/mkcert/releases)

```bash
sudo apt install libnss3-tools
# Exec the mkcert binary
mkcert -install

# Add your local domaine name from /etc/hosts
# '*.localhost' means all domaine with .localhost will use this certificat
mkcert -key-file key.pem -cert-file cert.pem '*.localhost' '*.test' localhost 127.0.0.1
```
#### Run traefik container. Traefik is entry point for all container application. It must be run before all other container. It listens the port 80 and 443, so this ports must be free.

```bash
# clone this repo from github and copy traefik directory to /opt/dk/
sudo git clone https://github.com/avenirbiz/traefik /opt/dk/traefik
```

#### [FOR DEVELOP MODE] copy the generated key to /opt/dk/traefik/etc

```bash
# copy key.pem cert.pem in /opt/dk/traefiK/etc/
sudo cp key.pem cert.pem /opt/dk/traefik/etc/
```
#### [FOR DEVELOP MODE ONLY] in traefik docker-compose /opt/dk/traefik/etc/docker-compose, comment prod conf and uncomment dev conf
```yaml
      #- "./etc/traefik.yml:/traefik.yml:ro"
      - "./etc/traefik-dev.yml:/traefik.yml:ro" # Only for dev test

```

#### Start traefik container
```bash
sudo systemctl start dk@traefik.service
```
### Configure a backup directory
Many docker-compose are configured to puts backups in /mnt/backups/. In developing, you can create the repo. In production, It can be a mounted NFS from storage backups.
#### Run docker apps

Example, we want to run absoins__lerocher.

```bash
# Get the repo contains psono docker-compose
sudo -u dk git clone https://github.com/avenirbiz/absoins__lerocher /opt/dk/absoins__lerocher
# With odoo Docker, in this case, the name path of module become absoins__lerocher. This can create confusion with the path using when the module is developed, example for Odoo web.

# See in absoins__lerocher/README.md how to configure absoins__lerocher with traefik.

# After you can start absoins__lerocher
# You must be sure that traefik service run before
sudo systemclt start absoins__lerocher

# You can open in browser the domaine name you have configure in your .env file

```

#### To see logs of running container
```bash
sudo docker ps -a # to see all containers
sudo docker logs -f container_name
```
NB:
The name of container is not the name of systemd service. It's possible to stop or restart a service with docker commands. The systemd service run a docker-compose file in /opt/dk/**



## Plan with Docker before Kubernetes
![Plan for Docker](plan-docker.png)

Each server runs [github.com/avenirbiz/docker_traefik](github.com/avenirbiz/docker_traefik), [github.com/avenirbiz/docker_dashboard](github.com/avenirbiz/docker_dashboard) ( Grafana, Prometheus, Loki, Promtail, Alertmanager, Cadvisor and nodeexporter )
### Server absolutions01
* Drone.io for CD/CI. Containers rerun with updated images every times we make a push in github.
* Docker-registry, tool for saving image. Is a private repository for customs docker images.
* makabo test
* abeducat demo
* absoins demo
* abhotel demo
* abfaith demo.
* backup container attached to all container volume need to be backups. We mount absolutions01 backup storage NFS in /mnt/backups. Then every backups will go there.

### Server abprod01
* cmbantu
* cmhappiness
* cmlerocher
* venushotelrdc
* eceuk.org
* backup container attached to all container volume need to be backups. We mount absolutions01 backup storage NFS in /mnt/backups. Then every backups will go there.

### Server abcust01
* avenirbank
* avenirbiz
* makabo ( Not ready )
* zando ( Not ready )
* donate.avenirbiz
* backup container attached to all container volume need to be backups. We mount absolutions01 backup storage NFS in /mnt/backups. Then every backups will go there.

## Next step: with Kubernetes
With Kubernetes, orchestration becomes simple and node can be add only when charge increases. But before we must study how it works and how it can resolve ours problems with docker architecture.

Problems with Docker:
* We manage and scales nodes and containers manually.
* Nodes are not connected each others. A instance of container can be run only in one node.
* Logs & metrics can be provide easy by Kubernetes