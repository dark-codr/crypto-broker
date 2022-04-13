from string import digits
from xmlrpc.client import Boolean
from django.db.models import CharField, DecimalField, BooleanField

from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel
from tinymce import HTMLField

# Create your models here.
class Mode(TimeStampedModel):
    DARK = "dark"
    LIGHT = "light"
    THEME = (
        (DARK, DARK),
        (LIGHT, LIGHT)
    )
    ip = CharField(max_length=500, blank=False, unique=True)
    theme = CharField(max_length=10, blank=False, choices=THEME, default=LIGHT)

    def __str__(self):
        return str(self.ip)

    class Meta:
        managed = True
        verbose_name = "Dark or Light Theme"
        verbose_name_plural = "Dark or Light Themes"
        ordering = ["-created"]

    # def save(self, *args, **kwargs):
    #     if self.__class__.objects.count():
    #         self.pk = self.__class__.objects.first().pk
    #     super().save(*args, **kwargs)

class Currency(TimeStampedModel):
    name = CharField(max_length=10, blank=False, unique=True)
    amount = DecimalField(decimal_places=7, max_digits=20, default=0.00, blank=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = True
        verbose_name = "Crypto Currency"
        verbose_name_plural = "Crypto Currencies"
        ordering = ["-created"]

class FAQ(TimeStampedModel):
    question = CharField(max_length=700)
    answer = HTMLField('Answer')

    def __str__(self):
        return str(self.question)

    class Meta:
        managed = True
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["-created"]

class Privacy(TimeStampedModel):
    doc = HTMLField('Privacy')

    def __str__(self):
        return str(self.doc[:50])

    class Meta:
        managed = True
        verbose_name = "Privacy Statement"
        verbose_name_plural = "Privacy Statements"
        ordering = ["-created"]

class Return(TimeStampedModel):
    doc = HTMLField('Return')

    def __str__(self):
        return str(self.doc[:50])

    class Meta:
        managed = True
        verbose_name = "Return Policy"
        verbose_name_plural = "Return Policies"
        ordering = ["-created"]

class Agreement(TimeStampedModel):
    doc = HTMLField('Agreement')

    def __str__(self):
        return str(self.doc[:50])

    class Meta:
        managed = True
        verbose_name = "Customer Agreement"
        verbose_name_plural = "Customer Agreements"
        ordering = ["-created"]


class TradeOpen(TimeStampedModel):
    open = BooleanField(default=True)

    def __str__(self):
        return "Daily ROI Opened" if self.open else "Daily ROI Closed"

    class Meta:
        managed = True
        verbose_name = "Trade Week Open/Close"
        verbose_name_plural = "Trade Week Open/Close"
