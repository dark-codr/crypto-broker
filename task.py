import threading
import schedule
import os
import time
from django.core.management import call_command


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def run_commands():
    dokku_commands = os.system("dokku run -rm pengcrest python manage.py rates && dokku run -rm pengcrest python manage.py daily_roi && dokku run -rm pengcrest python manage.py can_topup && dokku run -rm pengcrest python manage.py can_withdraw_roi && dokku run -rm pengcrest python manage.py can_reinvest && dokku run -rm pengcrest python manage.py can_withdraw")
    print("scripts ran with status code: %d" % dokku_commands)

schedule.every(1).day.at("15:30").do(run_commands) # run commands every day at 3:30 am

# Start the background thread
stop_run_continuously = run_continuously()

time.sleep(64800)

# Stop the background thread
stop_run_continuously.set()


# while True:
#     schedule.run_pending()
#     time.sleep(1)
