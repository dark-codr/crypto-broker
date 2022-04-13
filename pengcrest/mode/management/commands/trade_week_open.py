from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from pengcrest.utils.logger import LOGGER
from pengcrest.mode.models import TradeOpen

class Command(BaseCommand):
    """Open a trade week for general operations on the website

    Args:
        BaseCommand (_type_): _description_
    """
    help = _("Open Trade Week so Daily ROI Can Run")

    def handle(self, *args, **kwargs):
        """Checks to see if the tradeweek is open and if it is not it open it.
        Works with the server crontab excluding saturdays and sundays
        """
        if TradeOpen.objects.filter(id=1, open=False).exists():
            TradeOpen.objects.filter(id=1).update(open=True)
            #.exclude(created__week_day__in=[1, 7]) exclude sunday and saturday
            LOGGER.info(" Trade Open?: True")
        else:
            LOGGER.info("Trade weekend")

        self.stdout.write("Trade Week Open")
