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
	nosetests test --with-coverage --cover-tests --cover-min-percentage=80 --cover-package=news_crawler)

build: test

.PHONY: test clean
