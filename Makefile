.DEFAULT_GOAL := all
black = black -S -l 120 --target-version py310 locked_dict test
lint = ruff locked_dict test
pytest = pytest --asyncio-mode=strict --cov=locked_dict --cov-report term-missing:skip-covered --cov-branch --log-format="%(levelname)s %(message)s"
types = mypy locked_dict

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
	$(lint) --fix
	$(black)

.PHONY: init
init:
	pip install -r test/requirements.txt
	pip install -r test/requirements-dev.txt

.PHONY: lint
lint:
	python setup.py check -ms
	$(lint) --diff
	$(black) --check --diff

.PHONY: types
types:
	$(types)

.PHONY: test
test: clean
	$(pytest)

.PHONY: testcov
testcov: test
	@echo "building coverage html"
	@coverage html

.PHONY: all
all: lint types testcov
.PHONY: sbom
sbom:
	@./gen-sbom
	@cog -I. -P -c -r --check --markers="[[fill ]]] [[[end]]]" -p "from gen_sbom import *;from gen_licenses import *" docs/third-party/README.md

.PHONY: version
version:
	@cog -I. -P -c -r --check --markers="[[fill ]]] [[[end]]]" -p "from gen_version import *" locked_dict/__init__.py

.PHONY: secure
secure:
	@bandit --output current-bandit.json --baseline baseline-bandit.json --format json --recursive --quiet --exclude ./test,./build locked_dict
	@diff -Nu {baseline,current}-bandit.json; printf "^ Only the timestamps ^^ ^^ ^^ ^^ ^^ ^^ should differ. OK?\n"

.PHONY: baseline
baseline:
	@bandit --output baseline-bandit.json --format json --recursive --quiet --exclude ./test,./build locked_dict
	@cat baseline-bandit.json; printf "\n^ The new baseline ^^ ^^ ^^ ^^ ^^ ^^. OK?\n"

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
