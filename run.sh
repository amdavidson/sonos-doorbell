#!/bin/bash

FLASK_APP=sonos-doorbell /usr/local/bin/pipenv run python -m flask run --host=0.0.0.0
