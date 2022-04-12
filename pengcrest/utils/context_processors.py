import json
import datetime

from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.gis.geoip2 import GeoIP2
# from django.contrib.gis.db.models.functions import GeometryDistance
# from django.contrib.gis.geos import Point
from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject

from pengcrest.utils.logger import LOGGER
from pengcrest.mode.models import Mode, FAQ, Currency, Privacy, Return, Agreement

User = get_user_model()

dt = datetime.datetime.now()

def context_settings(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        if settings.PRODUCTION:
            ip = request.META.get('REMOTE_ADDR')
        else:
            ip = '8.8.8.8'

    #  Get current location on google map
    # g = GeoIP2()
    # location = g.city(ip)
    # location_country = location["country_name"]
    # location_country_code = location["country_code"]
    # location_latitude = location["latitude"]
    # location_longitude = location["longitude"]
    # location_city = location["city"]

    # current_loc = Point(location_longitude, location_latitude, srid=4326)

    if not Mode.objects.filter(ip=ip).exists():
        Mode.objects.create(ip=ip, theme="light")
    dark_mode = Mode.objects.filter(ip=ip, theme=Mode.DARK).exists()

    if dt.hour >= 4 and dt.hour < 12:
        greeting = "Good Morning"
        sleep = False
    elif dt.hour >= 12 and dt.hour < 17:
        greeting = "Good Afternoon"
        sleep = False
    elif dt.hour >= 17 and dt.hour < 22:
        greeting = "Good Evening"
        sleep = False
    elif dt.hour >= 22 and dt.hour < 4:
        greeting = "Good Night"
        sleep = True
    else:
        greeting = "Welcome"
        sleep = False

    faqs = FAQ.objects.all()

    btcprice = Currency.objects.get_or_create(name="btc")
    ethprice = Currency.objects.get_or_create(name="eth")
    ltcprice = Currency.objects.get_or_create(name="ltc")
    dashprice = Currency.objects.get_or_create(name="dash")

    privacy = Privacy.objects.all().first() if Privacy.objects.all().exists() else None
    returns = Return.objects.all().first() if Return.objects.all().exists() else None
    agreement = Agreement.objects.all().first() if Agreement.objects.all().exists() else None

    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "DEBUG": settings.DEBUG,

        'user_ip': ip,
        # 'location_country': location_country,
        # 'location_country_code': location_country_code,
        # 'location_latitude': location_latitude,
        # 'location_longitude': location_longitude,
        # 'location_city': location_city,

        "privacy": privacy,
        "returns": returns,
        "agreement": agreement,

        # Time greeting
        'greeting': greeting,
        'sleep_time': sleep,

        # themedate_joined
        'dark': dark_mode,
        'faqs': faqs,
        'btcprice': btcprice if btcprice.exists() else 0.00,
        'ethprice': ethprice if ethprice.exists() else 0.00,
        'ltcprice': ltcprice if ltcprice.exists() else 0.00,
        'dashprice': dashprice if dashprice.exists() else 0.00,

        'site': SimpleLazyObject(lambda: get_current_site(request)) if not settings.DEBUG else "localhost:8000",
    }

