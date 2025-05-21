# Путь к docker-compose файлам
BASE_COMPOSE=docker-compose.yaml
AIRFLOW_COMPOSE=airflow_2/docker-compose.yaml

# Объединённая команда
DC=docker-compose -f $(BASE_COMPOSE) -f $(AIRFLOW_COMPOSE)

up:
	$(DC) up -d

down:
	$(DC) down

stop:
	$(DC) stop

start:
	$(DC) start

restart:
	$(DC) restart

logs:
	$(DC) logs -f

ps:
	$(DC) ps

prune:
	$(DC) down --volumes --remove-orphans

rebuild:
	$(DC) down --volumes --remove-orphans
	$(DC) build --no-cache
	$(DC) up -d

init:
	$(DC) up airflow-init

.PHONY: up down stop start restart logs ps prune rebuild init
