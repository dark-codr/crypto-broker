#!/bin/bash

# Running dokku tasks everyday

dokku run python manage.py rates && dokku run python manage.py daily_roi && dokku run python manage.py can_topup && dokku run python manage.py can_withdraw_roi && dokku run python manage.py can_reinvest && dokku run python manage.py can_withdraw

# Processes has ended
