# Usage:
#   make up                        build and start all 10 askers (ports 5010-5019)
#   make up TASK="zebrocy triton"  start only some tasks (names = folders / compose services)
#   make down                      stop everything
#   make ps                        list running containers
#   make logs [TASK=...]           follow logs
#   make test [HOST=1.2.3.4]       play every task with its answer key over TCP and check the flag
#   make gen                       regenerate askers + walkthroughs after editing tools/questions.py
COMPOSE := docker compose -f docker-compose.yml
TASK ?=
HOST ?= 127.0.0.1

.PHONY: up down ps logs test gen
up:
	$(COMPOSE) up -d --build $(TASK)
down:
	$(COMPOSE) down
ps:
	$(COMPOSE) ps
logs:
	$(COMPOSE) logs -f $(TASK)
test:
	python3 tools/smoke_test.py $(HOST)
gen:
	python3 tools/gen.py
