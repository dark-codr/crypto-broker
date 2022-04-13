import json
from datetime import timezone
from decimal import Decimal
import datetime

from django.db.models import Sum

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from pengcrest.utils.logger import LOGGER
from pengcrest.mode.models import Currency
from pengcrest.users.models import Deposit, TransactionHistory, User, Wallet

# User = get_user_model()
users = User.objects.all()


class Command(BaseCommand):
    help = _("One month period has elapsed and the user can now top up")

    def handle(self, *args, **kwargs):
        for u in users:
            one_months = u.wallet.invested_date + datetime.timedelta(weeks=4)
            two_months = u.wallet.invested_date + datetime.timedelta(weeks=8)
            three_months = u.wallet.invested_date + datetime.timedelta(weeks=12)
            if u.wallet.invested_date and datetime.date.today() > (one_months or two_months) < three_months:
                User.objects.filter(username=u.username).update(has_toped = False)
                LOGGER.info(f"{u.username.title()} can now topup their account")
            else:
                LOGGER.info(f"{u.username.title()} plan is still running")


        self.stdout.write("Can Top Up Successfully.")
