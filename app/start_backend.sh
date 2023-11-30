#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)

PIPENV_DONT_LOAD_ENV=1 pipenv run python -m manage migrate
PIPENV_DONT_LOAD_ENV=1 pipenv run python -m manage runserver 0.0.0.0:8000
