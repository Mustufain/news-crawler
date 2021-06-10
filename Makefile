PROJECT_NAME=news-crawler
DOCKER_REPO=$(PROJECT_NAME)
DOCKER_TAG?=latest

.virtualenv:
	virtualenv -p python3 .virtualenv
	. .virtualenv/bin/activate; \
	pip install -r requirements.txt

clean:
	rm -rf *.egg-info
	rm -rf .virtualenv/

test: .virtualenv
	(. .virtualenv/bin/activate; \
	pycodestyle --max-line-length=79 news_crawler test; \
	pylint --fail-under=9.0 --rcfile=pylintrc news_crawler ; \
	pylint --fail-under=9.0 --rcfile=pylintrc-test test ; \
	nosetests test --with-coverage --cover-tests --cover-min-percentage=80 --cover-package=news_crawler)

build-container:
	docker build -t $(DOCKER_REPO) .

build: test clean build-container

run-local: .virtualenv
	. .virtualenv/bin/activate; \
	. ./run.sh

.PHONY: test clean build-container publish build run-local
