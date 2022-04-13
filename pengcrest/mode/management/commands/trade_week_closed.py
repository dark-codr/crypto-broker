from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from pengcrest.utils.logger import LOGGER
from pengcrest.mode.models import TradeOpen

class Command(BaseCommand):
    """Close a trade week for general operations on the website

    Args:
        BaseCommand (_type_): _description_
    """
    help = _("Close Trade Week so Daily ROI Can not Run")

    def handle(self, *args, **kwargs):
        """Checks to see if the trade week is open and if it is, this will close it.
        Works with the server crontab excluding saturdays and sundays
        """
        if TradeOpen.objects.filter(id=1, open=True).exists():
            TradeOpen.objects.filter(id=1).update(open=False)
            #.exclude(created__week_day__in=[1, 7]) exclude sunday and saturday
            LOGGER.info(" Trade Open?: Closed")
        else:
            LOGGER.info("Trade week")

        self.stdout.write("Trade Week Closed")
