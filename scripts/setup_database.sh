#!/bin/bash

export FLASK_APP=app/main.py
flask db init
flask db migrate
flask db upgrade
