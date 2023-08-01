#!/bin/bash
echo "Wait ..."
sleep 5

echo "Start migrate"
python manage.py migrate --no-input

echo "Start collectstatic"
python manage.py collectstatic --no-input

echo "Create superuser"
DJANGO_SUPERUSER_PASSWORD=$A_PASSWORD python manage.py createsuperuser --username $A_NAME --email $A_EMAIL --noinput

gunicorn pet_todo_list.wsgi:application --bind 0.0.0.0:8017