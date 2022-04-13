import datetime

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from pengcrest.utils.logger import LOGGER
from pengcrest.users.models import User
# User = get_user_model()
users = User.objects.all()


class Command(BaseCommand):
    help = _("Withdraw investment capital")

    def handle(self, *args, **kwargs):
        for u in users:
            if u.wallet.invested_date:
                three_months = u.wallet.invested_date + datetime.timedelta(weeks=12)
                if u.wallet.invested_date and datetime.date.today() > three_months:
                    User.objects.filter(username=u.username).update(can_withdraw = True)
                    LOGGER.success(f"{u.username.title()} investment plan has ended")
                else:
                    LOGGER.error(f"{u.username.title()} investment plan is still running")

        self.stdout.write("Can Withdraw Set Successfully.")
