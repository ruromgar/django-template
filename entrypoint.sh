#!/bin/bash

# Run Django migrations
echo "Migrating database..."
python manage.py migrate

# Load graph data
echo "Loading graph db data..."
python manage.py load_agraph

# Create users (if needed)
echo "Creating users..."
python manage.py create_users

# Updating users (if needed)
echo "Updating users..."
python manage.py update_users

# Create cards (if needed)
echo "Creating cards..."
python manage.py create_cards

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000
#exec gunicorn core.wsgi:application
