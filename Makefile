PROJECT_NAME=news-crawler
DOCKER_REPO=$(PROJECT_NAME)
DOCKER_TAG?=latest
DOCKER_URL=633157335118.dkr.ecr.us-east-1.amazonaws.com

.virtualenv:
	virtualenv -p python3 .virtualenv
	. .virtualenv/bin/activate; \
	pip install -r requirements.txt

clean:
	find . -name __pycache__ -exec rm -rf {} +
	rm -rf *.egg-info
	rm -rf .virtualenv/

test: .virtualenv
	(. .virtualenv/bin/activate; \
	pycodestyle --max-line-length=79 news_crawler test; \
	pylint --fail-under=9.0 --rcfile=pylintrc news_crawler ; \
	pylint --fail-under=9.0 --rcfile=pylintrc-test test ; \
	nosetests test --with-coverage --cover-tests --cover-min-percentage=90 --cover-package=news_crawler)

build-container: docker build -t $(DOCKER_REPO) .

publish: build
	@docker tag $(DOCKER_REPO) $(DOCKER_URL)/$(DOCKER_REPO):$(DOCKER_TAG)
	@docker push $(DOCKER_URL)/$(DOCKER_REPO):$(DOCKER_TAG)

build: test clean build-container

run-local: .virtualenv
	. .virtualenv/bin/activate; \
	   . ./run.sh

.PHONY: test clean build-container publish build run-local
