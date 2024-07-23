#!/bin/bash

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started"
fi

echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done
echo "Redis started"

# sleep 100
echo "Running migrations"
python manage.py migrate
echo "Successfully migrated database"

echo "Collecting static files"
python manage.py collectstatic --no-input
echo "Successfully collected static files"

django-admin compilemessages
echo "Successfully compiled messages"

echo "Starting server"
gunicorn core.wsgi:application --bind 0.0.0.0:8000