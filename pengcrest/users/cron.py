import datetime

from decimal import Decimal
from django.db.models import Sum

from django.conf import settings
from django.contrib.auth import get_user_model

from pengcrest.utils.logger import LOGGER

from .models import Deposit, TransactionHistory, User, Wallet

# def three_months():
#     return datetime.datetime.now() + datetime.timedelta(days=90)

# def two_weeks():
#     return datetime.datetime.now() + datetime.timedelta(days=14)

# def one_week():
#     return datetime.datetime.now() + datetime.timedelta(days=7)

users = User.objects.all()

def daily_roi():
    for u in users:
        if u.wallet.invested_date:
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


def can_topup():
    for u in users:
        if u.wallet.invested_date:
            # td = u.wallet.invested_date + datetime.timedelta(days=30)
            # if datetime.date.today() > td:
            u.has_toped = False
            u.save()

def can_reinvest():
    for u in users:
        if u.wallet.invested_date:
            # td = u.wallet.invested_date + datetime.timedelta(days=30)
            # if datetime.date.today() > td:
            u.has_invested = False
            u.save()


def can_withdraw():
    for u in users:
        if u.wallet.invested_date:
            # td = u.wallet.invested_date + datetime.timedelta(days=90)
            # if datetime.date.today() > td:
            u.can_withdraw = True
            u.save()


def can_withdraw_roi():
    for u in users:
        if u.wallet.invested_date:
            # td = u.wallet.invested_date + datetime.timedelta(days=15)
            # if datetime.date.today() > td:
            u.can_withdraw_roi = True
            u.save()
