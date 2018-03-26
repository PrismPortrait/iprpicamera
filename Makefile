# vim: set noet sw=4 ts=4 fileencoding=utf-8:

# External utilities
PYTHON=python
PIP=pip
PYTEST=unittest
COVERAGE=coverage
PYFLAGS=
DEST_DIR=/

SUBDIRS:=


# Default target
all:
	@echo "make test - Run tests"
	@echo "make clean - Get rid of all generated files"

test:
	$(COVERAGE) run --rcfile coverage.cfg -m $(PYTEST) discover -s tests -v
	$(COVERAGE) report --rcfile coverage.cfg

clean:
	$(PYTHON) $(PYFLAGS) setup.py clean
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir clean; \
	done
	find $(CURDIR) -name "*.pyc" -delete

.PHONY: all test clean $(SUBDIRS)
