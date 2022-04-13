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



class Command(BaseCommand):
    help = _("Can Withdraw ROI")

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for u in users:
            three_months = u.wallet.invested_date + datetime.timedelta(weeks=12)
            first_week = u.wallet.invested_date + datetime.timedelta(weeks=2)
            second_week = u.wallet.invested_date + datetime.timedelta(weeks=4)
            if u.wallet.invested_date and u.has_invested and not u.can_withdraw and datetime.date.today() > first_week < three_months:
                u.can_withdraw_roi = True
                u.save()
                LOGGER.success(f"{u.username.title()} can withdraw first 2week ROI")
            elif u.wallet.invested_date and u.has_invested and not u.can_withdraw and datetime.date.today() > second_week < three_months:
                u.can_withdraw_roi = True
                u.save()
                LOGGER.success(f"{u.username.title()} can withdraw secont 2week ROI")
            else:
                LOGGER.error(f"{u.username.title()} investment is barely 2 weeks old")

        self.stdout.write("Can Withdraw ROI Set Successfully.")
