SHELL=/bin/bash

PROJECT_NAME=product
SETTINGS=test_app.settings
BIND_TO=127.0.0.1
RUNSERVER_PORT=8000
flake8=flake8 --max-complexity=7 --exclude '*migrations*'

PYTHONPATH=$(CURDIR)

MANAGE= PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(SETTINGS) django-admin.py

syncdb:
	@echo Syncing...
	$(MANAGE) syncdb --noinput
	$(MANAGE) migrate --noinput
	$(MANAGE) loaddata $(PROJECT_NAME)/fixtures/*
	@echo Done

test:
	$(flake8) product
	$(flake8) test_app
	$(MANAGE) test

run:
	@echo Starting $(PROJECT_NAME)...
	$(MANAGE) runserver $(BIND_TO):$(RUNSERVER_PORT)