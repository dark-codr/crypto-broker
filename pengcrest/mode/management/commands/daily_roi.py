from decimal import Decimal
import datetime


from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from pengcrest.utils.logger import LOGGER
from pengcrest.mode.models import TradeOpen
from pengcrest.users.models import TransactionHistory, User

class Command(BaseCommand):
    """This command updates a users Daily ROI depending
     if the user has invested and his/her
    investment is running within three months before it stops.

    If the trade week is weekend, the ROI wont work.

    Args:
        BaseCommand (_type_): _description_
    """
    help = _("Get daily roi")

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        trade_open = TradeOpen.objects.filter(id=1,open=True).exists()
        for u in users:
            three_months = u.wallet.invested_date + datetime.timedelta(weeks=12)
            if trade_open and u.wallet.invested_date and u.wallet.invested_date <= three_months :
                # td = u.wallet.invested_date + datetime.timedelta(days=90)
                asset = u.wallet.total_asset #Deposit.objects.filter(user=u, status=Deposit.SUCCESS).aggregate(Sum('amount'))
                roi =  Decimal(asset)  * Decimal(0.015)
                TransactionHistory.objects.create(
                    user=u,
                    currency="BTC",
                    transaction_type= TransactionHistory.ROI,
                    status= TransactionHistory.SUCCESS,
                    amount= roi,
                )
                u_roi = u.roi + roi
                User.objects.filter(username=u.username).update(roi=u_roi)

                LOGGER.success(f"{u.username.title()} Asset:{asset} ROI:{Decimal(roi)}")
            else:
                LOGGER.error(f"{u.username.title()} Trade week is closed")

        self.stdout.write("Daily ROI Retrieved Successfully.")
