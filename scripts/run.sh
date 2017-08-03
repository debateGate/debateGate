#!/bin/bash

cd ~/debategate
source ~/debategate/flask/bin/activate
export OAUTHLIB_INSECURE_TRANSPORT=1
gunicorn --bind 0.0.0.0:8000 wsgi:app
