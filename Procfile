release: python manage.py migrate
web: gunicorn config.wsgi:application --worker-class gevent
worker: python manage.py daily_roi
