#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U postgres; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "PostgreSQL is up - executing command"

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser if it does not exist..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@healthcare.com').exists():
    User.objects.create_superuser(email='admin@healthcare.com', username='admin', password='admin123', name='Admin User')
"

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
