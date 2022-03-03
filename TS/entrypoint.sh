#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
uwsgi --socket :9001 --workers 4 --master --enable-threads --module techsemester.wsgi