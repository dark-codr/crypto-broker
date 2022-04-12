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
    help = _("Get daily roi")

    def handle(self):
        for u in users:
            three_months = u.wallet.invested_date + datetime.timedelta(weeks=12)
            if u.wallet.invested_date and u.wallet.invested_date <= three_months :
                # td = u.wallet.invested_date + datetime.timedelta(days=90)
                asset = u.wallet.total_asset #Deposit.objects.filter(user=u, status=Deposit.SUCCESS).aggregate(Sum('amount'))
                LOGGER.info(asset)
                roi =  asset  * Decimal(0.02)
                TransactionHistory.objects.create(
                    user=u,
                    currency="BTC",
                    transaction_type= TransactionHistory.ROI,
                    status= TransactionHistory.SUCCESS,
                    amount= roi,
                )
                # if datetime.datetime.now() < td:
                u.roi += roi
                u.save()

        self.stdout.write("Daily ROI Retrieved Successfully.")
