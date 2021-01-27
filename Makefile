

.PHONY: all help

all: help

package:
	python setup.py sdist
install:
	pip install dist/python-mailcow-9999.999.99.dev9.tar.gz
list:
	pip show python-mailcow

gitlab-runner:
ifeq ($(CI_REGISTRY),)
	$(error CI_REGISTRY env variable is not set)
endif
	gitlab-runner exec docker build \
		--docker-volumes /var/run/docker.sock \
		--docker-volumes /tmp/gl-cache \
		--docker-cache-dir /tmp/gl-cache \
		--cache-dir /tmp/gl-cache \
		--docker-privileged=true \
		--env DOCKER_DRIVER=zfs \
		--env CI_REGISTRY=$(CI_REGISTRY)

help:
	@echo -e "Available targets:\n"
	@awk -F ':' '$$0~/^\S+:$$/ {print $$1}' Makefile
