.SUFFIXES: .js .css .html .svg .jpeg .png .htm
SHELL:=/bin/bash

ROOT_DIR:=$(shell dirname "$(realpath $(lastword $(MAKEFILE_LIST)))")
APP_DIR:=${ROOT_DIR}/web_minify
TESTS_DIR:=${ROOT_DIR}/tests
CODE_QUALITY_DIR:=${APP_DIR}/code_quality
FK_VERSION:=$(shell cat "$(ROOT_DIR)/VERSION")

CI_COMMIT_REF_NAME?=$(shell git rev-parse --abbrev-ref HEAD)
FK_GIT_ACTUAL_BRANCH:=$(CI_COMMIT_REF_NAME)
FK_GIT_HASH?=$(shell git rev-parse HEAD)
FK_GIT_HASH_SHORT?=$(shell git rev-parse --short HEAD)

FK_BUILD_DATE=?=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

VENV_NAME:=venv

GITLAB_CACHE_DIR:=$(shell pwd)/gitlab_cache

.PHONY: all code-quality test tests setup up req



define twine_config
[distutils]
index-servers=pypi
[pypi]
username=__token__
password=${TWINE_TOKEN}
endef
export twine_config


all: help

info:
	@echo "ROOT_DIR=$(ROOT_DIR)"
	@echo "FK_VERSION=$(FK_VERSION)"
	@echo "APP_DIR=$(APP_DIR)"
	@echo "TESTS_DIR=$(TESTS_DIR)"
	@echo "FK_GIT_ACTUAL_BRANCH=$(FK_GIT_ACTUAL_BRANCH)"
	@echo "CI_COMMIT_REF_NAME=$(CI_COMMIT_REF_NAME)"
	@echo "CI_COMMIT_TAG=$(CI_COMMIT_TAG)"
	@echo "CI_PROJECT_DIR=$(CI_PROJECT_DIR)"
	@echo "GITLAB_CACHE_DIR=$(GITLAB_CACHE_DIR)"
	@echo "VENV_NAME=$(VENV_NAME)"

env:
	@echo "ENV START"
	env | sort
	#| grep -v "CI_"
	@echo ""
	@echo "ENV END"

ver:
	@echo "### PACK:"
	cat VERSION
	@echo "### OS:"
	@echo "$(shell cat  /etc/os-release)"
	@echo "### PYTHON & PIP:"
	@. venv/bin/activate;\
	python --version || python3 --version || echo "NO PYTHON";\
	pip --version || pip3 --version || echo "NO PIP"
	@echo ""

req-base:
	pip install --upgrade pip
	pip uninstall octomy-clockwork -y
	pip install --upgrade pip-tools wheel twine

req-clockwork:
	cd "$(ROOT_DIR)/requirements"; \
	cat requirements.in | sort -u > temporary_requirements.in; \
	pip-compile --output-file=requirements.txt temporary_requirements.in; \
	cat requirements.in test_requirements.in | sort -u > temporary_requirements.in; \
	pip-compile --output-file=test_requirements.txt temporary_requirements.in; \
	[ ! -e temporary_requirements.in ] || rm temporary_requirements.in; \
	pip install -r requirements.txt; \
	pip install -r test_requirements.txt

req: req-base req-clockwork
	

test:
	cd "${TESTS_DIR}" && make all || echo "OOOPS"

uninstall:
	pip uninstall -y octomy-clockwork;

# Build and re-install package locally
setup: uninstall
	pip install -e $(ROOT_DIR);

# Install prequisites and prepare for development on apk based environment
apk-prep:
	@echo "PREP APK START"
	apk --no-cache --update add make py-pip python3-dev postgresql-dev libffi-dev openssl-dev build-base libc-dev ca-certificates curl tar which git 
	#pass gnupg2 
	pip3 install --upgrade pip
	pip3 install virtualenv setuptools wheel flake8 mypy pylint pytest pytest-cov pytest-mock pytest-mypy pytest-timeout pytest-flakes pytest-asyncio pip-tools black mock
	command -v docker-compose || pip3 install docker-compose || echo "Could not pip3 install docker-compose"
	virtualenv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate
	mkdir -p "$(GITLAB_CACHE_DIR)"
	@echo "PREP APK END"


pack:
	@echo "Packaging"
	python setup.py build --parallel 99
	python setup.py sdist bdist_wheel
	ls -halt dist/

push:
	@echo "Pushing"
	echo "$$twine_config" > 'twine.conf'
	twine upload --config-file twine.conf dist/*.tar.gz --skip-existing --verbose
	rm 'twine.conf'

push-local:
	@echo "Pushing using username and pass"
	twine upload dist/*.tar.gz --skip-existing --verbose

code-quality:
	cd code_quality; \
	make all

help:
	@echo ""
	@echo " Convenience makefile for FK tools"
	@echo " ---------------------------------"
	@echo ""
	@echo "  Preparation:"
	@echo ""
	@echo "    make apk-prep            - Prepare environment for development in apk based linux (alpine comaptible)"
	@echo "    make pack                - Package the build into a PyPi package"
	@echo "    make push                - Push the package to PyPi"
	@echo ""
	@echo "  Information output:"
	@echo ""
	@echo "    make ver                 - Lists current tool versions"
	@echo "    make info                - Lists internal variables"
	@echo "    make env                 - Lists environment variables"
	@echo "    make req                 - Rebuild pinned versions in *requirements.txt from *requirements.in"
	@echo "    make test                - Run tests. NOTE: For more options see tests/Makefile"
	@echo ""
	@echo "  Code quality:"
	@echo ""
	@echo "    make code-quality        - Run all code quality checks. NOTE: For more options see code_quality/Makefile"
	
