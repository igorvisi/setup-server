# Protmail

Promtail is an agent which ships the contents of local logs to a private Loki instance or Grafana Cloud. It is usually deployed to every machine that has applications needed to be monitored.

## Jobs
* Discovers targets
* Attaches labels to log streams
* Pushes them to the loki instance

Currently, Promtail can tail logs from two sources: local log files and the systemd journal (on AMD64 machines only).


## Our configuration

Protmail must run in every server to send logs in one instance which make possible to centralize logs. Protmail doesn't remove logs from server, It just read and send to a Loki instance.

So the configuration is in loki-promtail.yml, we must add the domaine name of instance to send logs ( /var/log/*log ). For Docker container, we use a Docker logging driver: Loki driver, to good format of logs.

Always with Traefik running


## Docker logging driver : Loki

### Download and install the Loki driver

```bash
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```

### Restart docker and list plugins
```bash
sudo systemctl restart docker
sudo docker plugin ls
```

### add Loki logging for all docker running
I'ts possible to add just in a docker-compose file, so the Loki logging will be available for only container in this docker-compose file.
But we prefere to add globaly

```json
{
    "debug" : true,
    "log-driver": "loki",
    "log-opts": {
        "loki-url": "https://dashboard.avenirbiz.com/loki/api/v1/push"
    }
}
```

loki-url is the url of Loki instance