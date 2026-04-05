release: python manage.py migrate --noinput
web: gunicorn config.wsgi --timeout 120 --workers 2
