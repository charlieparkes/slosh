export COMPOSE_SERVICE_NAME=slosh

-include $(shell curl -sSL -o .build-harness "https://raw.githubusercontent.com/mintel/build-harness/master/templates/Makefile.build-harness"; echo .build-harness)

init: init-build-harness
	@make pipenv
.PHONY: init

.env:
	@read -p "Enter a port for your dev site: " DEV_PORT; \
	echo "# Port for dev site. Must end in a colon (:)." >> .env; \
	echo "DEV_PORT=$$DEV_PORT:" >> .env; \
	echo "Wrote DEV_PORT=$$DEV_PORT: to .env" 1>&2;
	echo "DEBUG=true" >> .env

up: .env compose/up
.PHONY: up

down: .env compose/down
.PHONY: down

restart: compose/rebuild
.PHONY: restart

exec: docker/exec
.PHONY: exec

ps: compose/ps
.PHONY: ps

logs: compose/logs
.PHONY: logs

tail: logs
.PHONY: tail

lint: python/lint
.PHONY: lint

# docker-lint:
#   docker run --rm -i hadolint/hadolint < docker/Dockerfile
# 	# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock --env CI=true wagoodman/dive:latest {id}
# .PHONY: docker-lint

fmt: python/fmt
.PHONY: fmt

test: pytest/test
.PHONY: test

test-post-build: pytest/test-post-build
.PHONY: test-post-build

release_patch: bumpversion/release_patch
.PHONY: release_patch

release_minor: bumpversion/release_minor
.PHONY: release_minor

release_major: bumpversion/release_major
.PHONY: release_major

clean: pipenv/clean python/clean
	@exit 0
.PHONY: clean
