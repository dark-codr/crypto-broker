import uuid
import datetime

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    FileField,
    ForeignKey,
    ManyToManyField,
    ImageField,
    IntegerField,
    OneToOneField,
    PositiveSmallIntegerField,
    UUIDField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pengcrest.mode.models import Currency

from stdimage import StdImageField
from model_utils.models import TimeStampedModel
from countries_plus.models import Country
from django.utils.timezone import now

def three_months():
    return datetime.datetime.now() + datetime.timedelta(days=90)

def two_weeks():
    return datetime.datetime.now() + datetime.timedelta(days=14)

def one_week():
    return datetime.datetime.now() + datetime.timedelta(days=7)

class User(AbstractUser):
    """
    Default custom user model for pengcrest.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    bonus = DecimalField(decimal_places=2, max_digits=20, default=0.00, blank=False)
    roi = DecimalField(decimal_places=2, max_digits=20, default=0.00, blank=False)

    unique_id = CharField(max_length=50, editable=True, blank=True, unique=True)

    # can_withdraw = BooleanField(default=False)
    # can_topup = BooleanField(default=False)
    # withdraw_roi = BooleanField(default=False)
    newsletter = BooleanField(default=False)
    first_investment = BooleanField(default=True)

    phone = CharField(unique=False, max_length=17, blank=True, help_text=_("eg: 018276475673"))
    wallet_address = CharField(max_length=250, blank=True)
    eth_address = CharField(max_length=250, blank=True)
    ltc_address = CharField(max_length=250, blank=True)
    dash_address = CharField(max_length=250, blank=True)

    recommended_by = ForeignKey("self", on_delete=CASCADE, blank=True, null=True, related_name='ref_by')

    has_invested = BooleanField(default=False)
    has_toped = BooleanField(default=False)
    can_withdraw = BooleanField(default=False)
    can_topup = BooleanField(default=False)
    can_withdraw_roi = BooleanField(default=False)

    # def has_invested(self):
    #     if self.wallet.invested_date:
    #         return True
    #     else:
    #         return False

    # def can_withdraw(self):
    #     if self.wallet.invested_date:
    #         td = self.wallet.invested_date + datetime.timedelta(days=90)
    #         if datetime.date.today() > td:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False


    # def can_withdraw_roi(self):
    #     if self.wallet.invested_date:
    #         td = self.wallet.invested_date + datetime.timedelta(days=15)
    #         if datetime.date.today() > td and self.bonus > Decimal(20.00) :
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False

    # def daily_roi(self):
    #     td = self.wallet.invested_date + datetime.timedelta(days=90)
    #     roi = self.wallet.total_asset * 0.02
    #     if now < td:
    #         self.roi += roi
    #         self.save()
    #         return True
    #     return False



    def get_recommended_profiles(self):
        qs = User.objects.all()
        # empty recommended lists
        my_recs = []
        for profile in qs:
            if profile.recommended_by == self:
                my_recs.append(profile)
        return my_recs

    def get_recommended_count(self):
        qs = User.objects.all()
        # empty recommended lists
        my_recs = []
        for profile in qs:
            if profile.recommended_by == self:
                my_recs.append(profile)
        return len(my_recs) or 0


    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class Wallet(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name=_("wallet"))
    btc = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)
    eth = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)
    ltc = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)
    dash = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)

    invested_date = DateField(blank=True, null=True)

    @property
    def total_asset(self):
        # currency = Currency.objects.all()

        # if currency[0].name == "BTC":
        btc = self.btc #* currency[0].amount
        # if currency[1].name == "ETH":
        eth = self.eth #* currency[1].amount
        # if currency[2].name == "LTC":
        ltc = self.ltc #* currency[2].amount
        # if currency[3].name == "DASH":
        dash = self.dash #* currency[3].amount

        total = float(btc + eth + ltc + dash)
        return Decimal(total)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        managed = True
        verbose_name = "User Wallet"
        verbose_name_plural = "User Wallets"
        ordering = ["-created"]

class QuickFund(TimeStampedModel):
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DASH = "DASH"
    CURRENCY = (
        (BTC, BTC),
        (ETH, ETH),
        (LTC, LTC),
        (DASH, DASH)
    )
    user = ForeignKey(User, on_delete=CASCADE, related_name=_("quickfund"))
    currency = CharField(max_length=6, blank=False, choices=CURRENCY, default=BTC)
    amount = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        managed = True
        verbose_name = "Quick Fund"
        verbose_name_plural = "Quick Funds"
        ordering = ["-created"]

class TransactionHistory(TimeStampedModel):
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DASH = "DASH"
    # ROI = "ROI"
    # AFFILIATE = "AFFILIATE"
    CURRENCY = (
        (BTC, BTC),
        (ETH, ETH),
        (LTC, LTC),
        (DASH, DASH),
        # (ROI, ROI),
        # (AFFILIATE, "AFFILIATE")
    )

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    AFFILIATE = "AFFILIATE"
    ROI = "ROI"
    TTYPE = (
        (AFFILIATE, AFFILIATE),
        (DEPOSIT, DEPOSIT),
        (WITHDRAW, WITHDRAW),
        (ROI, ROI),
    )

    PENDING = "PENDING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"
    STATUS = (
        (PENDING, PENDING),
        (FAILED, FAILED),
        (SUCCESS, SUCCESS),
    )

    user = ForeignKey(User, on_delete=CASCADE, related_name=_("transaction"))
    currency = CharField(max_length=16, blank=False, choices=CURRENCY, default=BTC)
    transaction_type = CharField(max_length=15, blank=False, choices=TTYPE, default=DEPOSIT)
    status = CharField(max_length=15, blank=False, choices=STATUS, default=PENDING)
    amount = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)

    def __str__(self):
        return str(self.user.username)


    class Meta:
        managed = True
        verbose_name = "Transaction History"
        verbose_name_plural = "Transaction Histories"
        ordering = ["-created"]


class KYCVerify(TimeStampedModel):
    # PASSPORT = "PASSPORT"
    # ID_CARD = "ID_CARD"
    # DRIVERS_LICENSE = "DRIVERS_LICENSE"
    # ID_TYPE = (
    #     (PASSPORT, "PASSPORT"),
    #     (ID_CARD, "ID CARD"),
    #     (DRIVERS_LICENSE, "DRIVERS LICENSE"),
    # )
    user = OneToOneField(User, on_delete=CASCADE, related_name=_("kyc"))
    # id_type = CharField(
    #     choices=ID_TYPE, default=PASSPORT, max_length=15, null=True, blank=True
    # )
    pass_front = StdImageField(upload_to="passport/front", blank=True)
    pass_back = StdImageField(upload_to="passport/back", blank=True)
    # selfie = StdImageField(upload_to="passport/selfie", blank=True)
    # birth_cert = StdImageField(upload_to="passport/bcert", blank=True)

    approved = BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        managed = True
        verbose_name = "KYC Verification"
        verbose_name_plural = "KYC Verifications"
        ordering = ["-created"]


class Addresses(TimeStampedModel):
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DASH = "DASH"
    # ROI = "ROI"
    # AFFILIATE = "AFFILIATE"
    CURRENCY = (
        (BTC, BTC),
        (ETH, ETH),
        (LTC, LTC),
        (DASH, DASH),
        # (ROI, ROI),
        # (AFFILIATE, "AFFILIATE")
    )
    currency = CharField(max_length=16, blank=False, choices=CURRENCY, default=BTC)
    wallet = CharField(max_length=250, blank=True)
    active = BooleanField(default=True)

    class Meta:
        managed = True
        verbose_name = "Wallet Address"
        verbose_name_plural = "Wallet Addresses"
        ordering = ["-modified"]


class Deposit(TimeStampedModel):
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DASH = "DASH"
    # ROI = "ROI"
    # AFFILIATE = "AFFILIATE"
    CURRENCY = (
        (BTC, BTC),
        (ETH, ETH),
        (LTC, LTC),
        (DASH, DASH),
        # (ROI, ROI),
        # (AFFILIATE, "AFFILIATE")
    )

    PENDING = "PENDING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"
    STATUS = (
        (PENDING, PENDING),
        (FAILED, FAILED),
        (SUCCESS, SUCCESS),
    )
    user = ForeignKey(User, on_delete=CASCADE, related_name=_("depsit"))
    currency = CharField(max_length=16, blank=False, choices=CURRENCY, default=LTC)
    status = CharField(max_length=15, blank=False, choices=STATUS, default=PENDING)
    amount = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)

    def __str__(self):
        return str(self.user.username)


    class Meta:
        managed = True
        verbose_name = "Deposit History"
        verbose_name_plural = "Deposit Histories"
        ordering = ["-created"]

class Withdraw(TimeStampedModel):
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DASH = "DASH"
    # ROI = "ROI"
    # AFFILIATE = "AFFILIATE"
    CURRENCY = (
        (BTC, BTC),
        (ETH, ETH),
        (LTC, LTC),
        (DASH, DASH),
        # (ROI, ROI),
        # (AFFILIATE, "AFFILIATE")
    )

    PENDING = "PENDING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"
    STATUS = (
        (PENDING, PENDING),
        (FAILED, FAILED),
        (SUCCESS, SUCCESS),
    )
    user = ForeignKey(User, on_delete=CASCADE, related_name=_("withraw"))
    currency = CharField(max_length=16, blank=False, choices=CURRENCY, default=BTC)
    status = CharField(max_length=15, blank=False, choices=STATUS, default=PENDING)
    wallet = CharField(max_length=250, blank=True)
    amount = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)

    def __str__(self):
        return str(self.user.username)


    class Meta:
        managed = True
        verbose_name = "Withdraw History"
        verbose_name_plural = "Withdraw Histories"
        ordering = ["-created"]



