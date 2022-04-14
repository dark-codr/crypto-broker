release: chmod u+x dokku_commands.sh && chmod u+x tasks.sh && ./dokku_commands.sh
web: gunicorn config.wsgi:application --worker-class gevent
