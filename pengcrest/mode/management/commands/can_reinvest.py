from datetime import timedelta
import datetime

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from pengcrest.utils.logger import LOGGER
from pengcrest.users.models import User

# User = get_user_model()


class Command(BaseCommand):
    help = _("Make a user able to reinvest his capital or withdraw")

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for u in users:
            three_months = u.wallet.invested_date + timedelta(weeks=12)
            if u.wallet.invested_date and datetime.date.today() > three_months:
                User.objects.filter(username=u.username).update(has_invested = False)
                LOGGER.info(f"{u.username.title()} can now reinvest")
            else:
                LOGGER.info(f"{u.username.title()} plan is still running")

        self.stdout.write("Can Reinvest Set Successfully.")
