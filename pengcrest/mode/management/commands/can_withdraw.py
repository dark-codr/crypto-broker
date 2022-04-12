import json
from datetime import timezone
from decimal import Decimal
import datetime

from decimal import Decimal
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
    help = _("Get daily roi")

    def handle(self):
        for u in users:
            three_months = u.wallet.invested_date + datetime.timedelta(weeks=12)
            if u.wallet.invested_date and datetime.date.today() > three_months:
                u.can_withdraw = True
                u.save()

        self.stdout.write("Can Withdraw Set Successfully.")
