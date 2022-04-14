#!/bin/bash

# Running dokku tasks everyday

python manage.py rates && python manage.py daily_roi && python manage.py can_topup && python manage.py can_withdraw_roi && python manage.py can_reinvest && python manage.py can_withdraw

# Processes has ended
