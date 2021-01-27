# Docker Registry


## What it is
The Registry is a stateless, highly scalable server side application that stores and lets you distribute Docker images. The Registry is open-source, under the permissive Apache license.

## Why use it
You should use the Registry if you want to:

* tightly control where your images are being stored
* fully own your images distribution pipeline
* integrate image storage and distribution tightly into your in-house development workflow


## Requirements
The Registry is compatible with Docker engine version 1.6.0 or higher.

## Basic commands
Start your registry

```bash
docker run -d -p 5000:5000 --name registry registry:2
```
Pull (or build) some image from the hub

```bash
docker pull ubuntu
```
Tag the image so that it points to your registry

```bash
docker image tag ubuntu localhost:5000/myfirstimage
```

Push it

```bash
docker push localhost:5000/myfirstimage
```

Pull it back

```bash
docker pull localhost:5000/myfirstimage
```

## Our configuration

Docker registry in our docker-compose use authentification from the file in config/password. 
How to generate the password file which have hash password ?
* install apache2-utils 
* htpasswd -B password.file userName  
It creates a password.file with the userName and the password.

### Configure the .env to add domaine name and the network docker for Traefik

This configuration must run with the traefik container. See Traefik container