release: python manage.py migrate; python manage.py crontab add
web: gunicorn config.wsgi:application
