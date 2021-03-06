import threading
import schedule
import os
import time
from subprocess import check_call

# def run_continuously(interval=1):
#     """Continuously run, while executing pending jobs at each
#     elapsed time interval.
#     @return cease_continuous_run: threading. Event which can
#     be set to cease continuous run. Please note that it is
#     *intended behavior that run_continuously() does not run
#     missed jobs*. For example, if you've registered a job that
#     should run every minute and you set a continuous run
#     interval of one hour then your job won't be run 60 times
#     at each interval but only once.
#     """
#     cease_continuous_run = threading.Event()

#     class ScheduleThread(threading.Thread):
#         @classmethod
#         def run(cls):
#             while not cease_continuous_run.is_set():
#                 schedule.run_pending()
#                 time.sleep(interval)

#     continuous_thread = ScheduleThread()
#     continuous_thread.start()
#     return cease_continuous_run


def run_commands():
    dokku_commands = check_call(r"""
    python manage.py rates
    python manage.py daily_roi
    python manage.py can_topup
    python manage.py can_withdraw_roi
    python manage.py can_reinvest
    python manage.py can_withdraw""", shell=True)
    print("scripts ran with status code: %d" % dokku_commands)

schedule.every(1).day.at("01:15").do(run_commands) # run commands every day at 3:30 am
# schedule.every(1).seconds.do(run_commands) # run commands every day at 3:30 am

# # Start the background thread
# stop_run_continuously = run_continuously()

# time.sleep(10)

# # Stop the background thread
# stop_run_continuously.set()


while True:
    schedule.run_pending()
    time.sleep(10)
