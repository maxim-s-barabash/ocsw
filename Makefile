checkfiles = ocsw/ tests/ setup.py
black_opts = -l 79 -t py36 --quiet
isort_opts = -w 79 -m 3 --tc
bandit_opts = -s B322,B102 -x tests --silent
mypy_opts = --ignore-missing-imports
py_warn = PYTHONDEVMODE=1

help:
	@echo "ocsw development makefile"
	@echo ""
	@echo "usage: make <target>"
	@echo "Targets:"
	@echo "    deps     Ensure dev/test dependencies are installed"
	@echo "    check    Checks that build is sane"
	@echo "    lint     Reports all linter violations"
	@echo "    test     Runs all tests"
	@echo "    style    Auto-formats the code"
	@echo "    pyclean  Remove all *.pyc file"


deps:
	@pip3 install -U -r requirements.txt -r requirements-dev.txt

style:
	@isort $(isort_opts) $(checkfiles)
	@black $(black_opts) $(checkfiles)

check:
#	@mypy $(mypy_opts) $(checkfiles)
	@flake8 $(checkfiles)
	@bandit $(bandit_opts) -r $(checkfiles)
	@radon cc -a -s -nc $(checkfiles)
	@black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)

test:
	$(py_warn) py.test

lint:
	pylint --rcfile=setup.cfg  $(checkfiles)

pyclean:
	@find . -type d -name __pycache__ -exec rm -r {} \+
