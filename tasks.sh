#!/bin/bash
# Running dokku tasks everyday
# dokku_commands(){
dokku run pengcrest python manage.py rates && dokku run pengcrest python manage.py daily_roi && dokku run pengcrest python manage.py can_topup && dokku run pengcrest python manage.py can_withdraw_roi && dokku run pengcrest python manage.py can_reinvest && dokku run pengcrest python manage.py can_withdraw
# }
# dokku_commands
wait
echo "All Done"
# Processes has ended
