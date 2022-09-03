SHELL = /bin/bash
package = shagen/locked-dict

.DEFAULT_GOAL := all
isort = isort locked_dict test
black = black -S -l 120 --target-version py310 locked_dict test

.PHONY: install
install:
	pip install -U pip wheel
	pip install -r test/requirements.txt
	pip install -U .

.PHONY: install-all
install-all: install
	pip install -r test/requirements-dev.txt

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: init
init:
	pip install -r test/requirements.txt
	pip install -r test/requirements-dev.txt

.PHONY: lint
lint:
	python setup.py check -ms
	flake8 locked_dict/ test/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: mypy
mypy:
	@echo Skipping mypy locked_dict

.PHONY: test
test: clean
	pytest --asyncio-mode=strict --cov=locked_dict --cov-report term-missing:skip-covered --cov-branch --log-format="%(levelname)s %(message)s"

.PHONY: testcov
testcov: test
	@echo "building coverage html"
	@coverage html

.PHONY: all
all: lint mypy testcov

.PHONY: clean
clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -rf .cache htmlcov *.egg-info build dist/*
	@rm -f .coverage .coverage.* *.log
	python setup.py clean
	@rm -fr site/*

.PHONY: name
name:
	@printf "Revision.is(): sha1:%s\n" "$$(git rev-parse HEAD)"
	@printf "Name.derive(): '%s'\n" "$$(git-release-name "$$(git rev-parse HEAD)")"
