ifeq ($(OS),Windows_NT)
BIN_DIR = Scripts
else
BIN_DIR = bin
endif

APPNAME = hubsyncer
DEPS = mozilla:server-core
VIRTUALENV = virtualenv
NOSE = $(BIN_DIR)/nosetests
NOSETESTS_ARGS = -s
NOSETESTS_ARGS_C = -s --with-xunit --with-coverage --cover-package=hubsyncer --cover-erase
TESTS = hubsyncer/tests
PYTHON = $(BIN_DIR)/python
version = $(shell $(PYTHON) setup.py --version)
tag = $(shell grep tag_build setup.cfg  | cut -d= -f2 | xargs echo )

# *sob* - just running easy_install on Windows prompts for UAC...
ifeq ($(OS),Windows_NT)
EZ = $(PYTHON) $(BIN_DIR)/easy_install-script.py
else
EZ = $(BIN_DIR)/easy_install
endif
COVEROPTS = --cover-html --cover-html-dir=html --with-coverage --cover-package=linkdrop
COVERAGE := coverage
PYLINT = $(BIN_DIR)/pylint
PKGS = hubsyncer

GIT_DESCRIBE := `git describe --long`

ifeq ($(TOPSRCDIR),)
  export TOPSRCDIR = $(shell pwd)
endif

SLINK = ln -sf
ifneq ($(findstring MINGW,$(shell uname -s)),)
  SLINK = cp -r
  export NO_SYMLINK = 1
endif

all: build

clean:

build:
	$(VIRTUALENV) --no-site-packages --distribute .
	$(PYTHON) build.py $(APPNAME) $(DEPS)
	$(EZ) nose
	$(EZ) WebTest
	$(EZ) Funkload
	$(EZ) pylint
	$(EZ) coverage

test:
	$(NOSE) $(NOSETESTS_ARGS) $(TESTS)

coverage:
	$(NOSE) $(NOSETESTS_ARGS_C) $(TESTS)
	$(COVERAGE) xml

.PHONY: clean build test coverage
