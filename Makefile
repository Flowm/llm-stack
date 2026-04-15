include .env

.PHONY: up down backup restore update

up:
	docker compose --profile custom-ui --profile gpu up --remove-orphans --build -d

down:
	docker compose --profile custom-ui --profile gpu down

logs:
	docker compose logs -f

backup:
	docker compose exec -T database pg_dump -Fc -U $(DATABASE_USER) $(DATABASE_NAME) > ~/backup/$(DATABASE_NAME)-$$(date +%F-%H-%M-%S).bck

restore:
ifndef FILE
	$(error Usage: make restore FILE=~/backup/db.bck)
endif
	docker compose up -d --wait database
	docker compose cp $(FILE) database:/tmp/restore.bck
	docker compose exec -T database pg_restore -Fc -U $(DATABASE_USER) -d $(DATABASE_NAME) /tmp/restore.bck
	docker compose exec -T database rm /tmp/restore.bck
	@echo "Restore complete."

update:
	docker run --rm -it -u $$(id -u):$$(id -g) -v $$(pwd):/cwd -w /cwd ghcr.io/updatecli/updatecli:latest apply
