SHELL = /bin/bash
package = shagen/locked-dict

.DEFAULT_GOAL := all
isort = isort locked_dict tests
black = black -S -l 120 --target-version py310 locked_dict tests

.PHONY: install
install:
	pip install -U pip wheel
	pip install -r tests/requirements.txt
	pip install -U .

.PHONY: install-all
install-all: install
	pip install -r tests/requirements-dev.txt

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: init
init:
	pip install -r tests/requirements.txt
	pip install -r tests/requirements-dev.txt

.PHONY: lint
lint:
	python setup.py check -ms
	flake8 locked_dict/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: mypy
mypy:
	mypy locked_dict

.PHONY: test
test: clean
	pytest --asyncio-mode=strict --cov=locked_Dict --cov-report term-missing:skip-covered --cov-branch --log-format="%(levelname)s %(message)s"

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
	@rm -rf .cache
	@rm -rf htmlcov
	@rm -rf *.egg-info
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -rf build
	@rm -f *.log
	python setup.py clean
	@git status
