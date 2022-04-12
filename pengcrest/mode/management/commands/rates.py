import json
from datetime import timezone
from decimal import Decimal

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

User = get_user_model()


class Command(BaseCommand):
    help = _("Collect current bank rates")
    """
    BTC=189
    ETH=195
    LTC=191
    """

    def handle(self):
        url = "https://investing-cryptocurrency-markets.p.rapidapi.com/currencies/get-rate"

        headers = {
            'x-rapidapi-host': "investing-cryptocurrency-markets.p.rapidapi.com",
            'x-rapidapi-key': str(settings.API)
        }

        btc = {"fromCurrency":"189","toCurrency":"12","lang_ID":"1","time_utc_offset":"28800"}
        eth = {"fromCurrency":"195","toCurrency":"12","lang_ID":"1","time_utc_offset":"28800"}
        ltc = {"fromCurrency":"191","toCurrency":"12","lang_ID":"1","time_utc_offset":"28800"}
        dash = {"fromCurrency":"199","toCurrency":"12","lang_ID":"1","time_utc_offset":"28800"}
        btc_res = requests.request("GET", url, params=btc, headers=headers)
        eth_res = requests.request("GET", url, params=eth, headers=headers)
        ltc_res = requests.request("GET", url, params=ltc, headers=headers)
        dash_res = requests.request("GET", url, params=dash, headers=headers)
        if btc_res.status_code != 200:
            return LOGGER.info(f"BTC {btc_res.status_code} - {btc_res.reason}")
        if eth_res.status_code != 200:
            return LOGGER.info(f"ETH {eth_res.status_code} - {eth_res.reason}")
        if ltc_res.status_code != 200:
            return LOGGER.info(f"LTC {ltc_res.status_code} - {ltc_res.reason}")
        if dash_res.status_code != 200:
            return LOGGER.info(f"DASH {dash_res.status_code} - {dash_res.reason}")

        resb = btc_res.json()
        rese = eth_res.json()
        resl = ltc_res.json()
        resd = dash_res.json()

        btcusd = Decimal(resb["data"][0][0]["basic"])
        ethusd = Decimal(rese["data"][0][0]["basic"])
        ltcusd = Decimal(resl["data"][0][0]["basic"])
        dashusd = Decimal(resd["data"][0][0]["basic"])

        try:
            Currency.objects.filter(name="btc").update(amount=btcusd)
            LOGGER.info("BTC Updated")
        except Currency.DoesNotExist:
            Currency.objects.get_or_create(name="btc", amount=btcusd)
            LOGGER.info("BTC Created")

        try:
            Currency.objects.filter(name="eth").update(amount=ethusd)
            LOGGER.info("ETH Updated")
        except Currency.DoesNotExist:
            Currency.objects.get_or_create(name="eth", amount=ethusd)
            LOGGER.info("ETH Created")

        try:
            Currency.objects.filter(name="ltc").update(amount=ltcusd)
            LOGGER.info("LTC Updated")
        except Currency.DoesNotExist:
            Currency.objects.get_or_create(name="ltc", amount=ltcusd)
            LOGGER.info("LTC Created")

        try:
            Currency.objects.filter(name="dash").update(amount=dashusd)
            LOGGER.info("DASH Updated")
        except Currency.DoesNotExist:
            Currency.objects.get_or_create(name="dash", amount=dashusd)
            LOGGER.info("DASH Created")

        self.stdout.write("Exchange Rate Retrieved Successfully.")
