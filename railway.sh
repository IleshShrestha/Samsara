#!/bin/bash
gunicorn home.wsgi --log-file
python manage.py && gunicorn home.wsg