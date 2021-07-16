# Traefik

## What is it ?
Traefik is an open-source Edge Router that makes publishing your services a fun and easy experience. It receives requests on behalf of your system and finds out which components are responsible for handling them.

## Official documentation
To see in [Traefik](https://doc.traefik.io/traefik/)

## Our configuration

The configuration file of Traefik is in traefik.yml file.
Traefik has two types of configuration ( Static and dynamic)

In static conf, we make traefik conf to get https from Let's encrypt automaticaly, we configure entrypoint, listing port and provider ( Docker in our case).

In dynamic conf, configuration comes dynamicaly from running docker container. So a container can define its domaine name, his route,... with labels in docker-compose and traefik will automaticaly send request to this domaine with Let's encrypt with auto renew.

Traefik works many provider like File, Docker, Kubernetes,... It will be use with Kubernetes in the future

Authentication can be set with Traefik with middleware, so before to access a site which doesn't have authentication SSL or login mode. Traefik as reverse proxy will provide SSL with LetsEncrypt and Login mode with his module basicAuth

For basicAuth, It possible to protect route with password. For that purpose, you can generate password file inside etc/ in the /opt/dk/traefik. It contains a list of user:password encrypt.


How to generate the password file which have hash password ?
* install apache2-utils ( sudo apt install apache2-utils)
* htpasswd -B password.file userName
It creates a password.file with the userName and the password prompted.

It's possible to get many password file depending on the portals to be protected, set and change the file according to the users that need to be logged in. May be later, we can see how to connect with a password manager like psono.

So you can configure every route in Docker labels with password auth which point to our password file generated. You can see sample in github.com/avenirbiz/docker_registry

## Env
there is two env:
* traefik-dev.yml for development with local certificate
* traefik.yml for production with Letsencrypt certificate
You can change in docker-compose.yml to switch.

## To run
```bash
sudo su dk && cd ~
# clone this repo from github and copy traefik directory to /opt/dk/
cp -r docker/samples/traefik /opt/dk/
cd traefik
```
Configure .env

```bash
# Configure password
cd /opt/dk/traefik/etc/passwd
htpasswd -cB user.password root
```

Nota:
* make sure the DEFAULT_NETWORK in .env is created. So all containers which will use this network to be discovered by traefik.
* Our configuration make Traefik listen on 80 and 443. This ports must be free.

```bash
docker network create TheNetworkName
```

```bash
# Run service
exit # Come back to your $USER to use sudo
sudo systemctl start dk@traefik
```

## How its works.
Traefik gets conf from provider. Docker in our case.
So every running container can set configuration with labels.
[https://doc.traefik.io/traefik/](https://doc.traefik.io/traefik/)

Sample: for domaineName & www.domaineName must be defined in docker labels like that:


```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=${DEFAULT_NETWORK}"
      - "traefik.http.routers.${PROJECT_NAME}_drone.entrypoints=websecure"
      - "traefik.http.routers.${PROJECT_NAME}_drone.rule=Host(`${DOMAINE_NAME}`)"
      - "traefik.http.routers.${ODOO_CONTAINER}.rule=Host(`${DOMAINE_NAME}`) || Host(`www.${DOMAINE_NAME}`)"
      - "traefik.http.middlewares.${ODOO_CONTAINER}-redirectregex.redirectregex.regex=^https://www.${DOMAINE_NAME}/(.*)"
      - "traefik.http.middlewares.${ODOO_CONTAINER}-redirectregex.redirectregex.replacement=https://${DOMAINE_NAME}/$${1}"
      - "traefik.http.routers.${ODOO_CONTAINER}.middlewares=${ODOO_CONTAINER}-redirectregex"
```

sample: for domaineName only

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=${DEFAULT_NETWORK}"
      - "traefik.http.routers.${PROJECT_NAME}_drone.entrypoints=websecure"
      - "traefik.http.routers.${PROJECT_NAME}_drone.rule=Host(`${DOMAINE_NAME}`)"
```
Nota: Domaine can be setup directly in labels but in our case, we suppose that every projet has .env that docker-compose will use to get variables.

Good Youtube tutorials:
* Traefik: A Scalable and Highly Available Edge Router by Damien Duportalt
 [https://www.youtube.com/watch?v=AqiGcLsVMeI](https://www.youtube.com/watch?v=AqiGcLsVMeI)
* Traefik Crash Course - Architecture, L7 & L4 Proxying, Weighted Round Robin, Enabling TLS 1.2/1.3
 [https://www.youtube.com/watch?v=C6IL8tjwC5E](https://www.youtube.com/watch?v=C6IL8tjwC5E)