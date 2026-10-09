# Usage:
#   make up SERIES=mreya      start one series' askers
#   make up                   start every series
#   make down [SERIES=cloud]  stop
#   make ps                   list running challenge containers
#   make build-containers     build the three Docker-series images
COMPOSE_SERIES := mreya cloud
SERIES ?= $(COMPOSE_SERIES)

.PHONY: up down ps build-containers
up:
	@for s in $(SERIES); do docker compose -f $$s/docker-compose.yml up -d --build; done
down:
	@for s in $(SERIES); do docker compose -f $$s/docker-compose.yml down; done
ps:
	@for s in $(COMPOSE_SERIES); do docker compose -f $$s/docker-compose.yml ps; done
build-containers:
	@for d in containers/0*/; do (cd $$d && ./build.sh); done
