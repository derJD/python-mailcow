.PHONY: all help

all: help

package:
	pyproject-build --sdist --wheel
install:
	pip install .
list:
	pip show python-mailcow
lint:
	pylint --exit-zero -f parseable src/

help:
	@echo -e "Available targets:\n"
	@awk -F ':' '$$0~/^\S+:$$/ || $$2 ~ /glr-check/ {print $$1}' Makefile
