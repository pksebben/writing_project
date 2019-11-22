#!/bin/bash

# this script is meant to get us up and running, set venv, and export the app to flask app.  Flask run is left to the user.

export CDPATH=$HOME

cd Documents/code/Creative/writing_project

source .venv/dev/bin/activate

export FLASK_APP=src/app.py
