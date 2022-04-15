release: chmod u+x dokku_commands.sh && ./dokku_commands.sh
web: gunicorn config.wsgi:application --worker-class gevent
