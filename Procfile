release: chmod u+x release.sh && ./dokku_commands.sh
web: gunicorn config.wsgi:application --worker-class gevent
worker: python task.py
