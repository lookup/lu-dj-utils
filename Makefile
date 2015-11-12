
SHELL = /usr/bin/env bash

default: clean
.PHONY: default clean

clean:
	find . -iname '*.pyc' -delete
	find . -iname '*.pyo' -delete
	rm -rf __pycache__/
	rm -rf */__pycache__/
	rm -rf .tox
	rm -rf build
	rm -rf dist
	rm -rf Django-*
	rm -rf *.egg-info
