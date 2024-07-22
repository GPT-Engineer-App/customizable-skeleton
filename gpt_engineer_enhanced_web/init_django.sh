#!/bin/sh

python manage.py migrate
python manage.py setup_initial_data
python manage.py collectstatic --noinput
