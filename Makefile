GLRBIN ?= gitlab-runner
GLRFLAGS ?= --docker-volumes /var/run/docker.sock \
	--docker-volumes /tmp/gl-cache \
	--docker-cache-dir /tmp/gl-cache \
	--cache-dir /tmp/gl-cache \
	--docker-privileged=true \
	--env DOCKER_DRIVER=zfs \
	--env CI_REGISTRY=$(CI_REGISTRY)

.PHONY: all help

all: help

package:
	python setup.py sdist
install:
	pip install dist/python-mailcow-9999.999.99.dev9.tar.gz
list:
	pip show python-mailcow

glr-build: glr-check
	${GLRBIN} exec docker build ${GLRFLAGS}
glr-pylint: glr-check
	${GLRBIN} exec docker test:pylint ${GLRFLAGS}
glr-check:
ifeq ($(CI_REGISTRY),)
	$(error CI_REGISTRY env variable is not set)
endif

help:
	@echo -e "Available targets:\n"
	@awk -F ':' '$$0~/^\S+:$$/ || $$2 ~ /glr-check/ {print $$1}' Makefile
