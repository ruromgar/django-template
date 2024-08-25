#!/bin/bash

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000
# exec gunicorn core.wsgi:application
