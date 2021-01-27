# Traefik

## What is it ?
Traefik is an open-source Edge Router that makes publishing your services a fun and easy experience. It receives requests on behalf of your system and finds out which components are responsible for handling them.

## Official documentation
To see in [Traefik](https://doc.traefik.io/traefik/)

## Our configuration

The configuration file of Traefik is in traefik.yml file.
Traefik has two types of configuration ( Static and dynamic)

In static conf, we make traefik conf to get https from Let's encrypt automaticaly, we configure entrypoint and listing port.

In dynamic conf, configuration comes dynamicaly from running docker container. So a container can define its domaine name, his route,... with labels in docker-compose and traefik will automaticaly send request to this domaine with Let's encrypt with auto renew.

Traefik works with Docker, Kubernetes,... It will be use with Kubernetes in the future

Authentification can be set with Traefik with middleware, so before to access a site which doesn't have authentification SSL or login mode. Traefik as reverse proxy will provide SSL with LetsEncrypt and Login mode with his module basicAuth

So we use it in metrics tools and docker-registry

For basicAuth, the password file is in conf/password. It contains a list of user:password encrypt. 

How to generate the password file which have hash password ?
* install apache2-utils 
* htpasswd -B password.file userName  
It creates a password.file with the userName and the password prompted.

It's possible to get many password file depending on the portals to be protected, set and change the file according to the users that need to be logged in. May be later, we can see how to connect with a password manager like psono.

In our case, we have:
- password: User for portail
- metric.password: to connect to metrics tools each other