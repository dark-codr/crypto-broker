import datetime

from decimal import Decimal
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe

from django.dispatch import receiver

from allauth.account.signals import user_signed_up

from pengcrest.utils.logger import LOGGER
from pengcrest.utils.emails import plain_email
from pengcrest.utils.unique_generators import unique_id_generator

from .models import Wallet, QuickFund, TransactionHistory, Withdraw, Deposit

User = get_user_model()


@receiver(pre_save, sender=User)
def generate_unique_id(instance, *args, **kwargs):
    if not instance.unique_id:
        instance.unique_id = unique_id_generator(instance)
        LOGGER.info(f"Created New ID: {instance.unique_id}")

@receiver(post_save, sender=User)
def user_post_save_signal(created, instance, *args, **kwargs):
    if created:
        Wallet.objects.get_or_create(user=instance)
        if not instance.unique_id:
            instance.unique_id = unique_id_generator(instance)
            LOGGER.info(f"Created New ID: {instance.unique_id}")
        LOGGER.info("Sent Registration Email to admin")


@receiver(post_save, sender=Withdraw)
def withdraw_approve_signal(instance, *args, **kwargs):
    if instance.status == Withdraw.FAILED:
        TransactionHistory.objects.create(
            user=instance.user,
            currency= instance.currency,
            transaction_type= TransactionHistory.WITHDRAW,
            status= TransactionHistory.FAILED,
            amount= instance.amount,
        )

    if instance.status == Withdraw.SUCCESS:
        TransactionHistory.objects.create(
            user=instance.user,
            currency= instance.currency,
            transaction_type= TransactionHistory.WITHDRAW,
            status= TransactionHistory.SUCCESS,
            amount= instance.amount,
        )
        if instance.currency == "BTC":
            amount = instance.user.wallet.btc - instance.amount
            Wallet.objects.filter(user=instance.user).update(btc = amount)
        elif instance.currency == "ETH":
            amount = instance.user.wallet.eth - instance.amount
            Wallet.objects.filter(user=instance.user).update(eth = amount)
        elif instance.currency == "LTC":
            amount = instance.user.wallet.ltc - instance.amount
            Wallet.objects.filter(user=instance.user).update(ltc = amount)
        elif instance.currency == "DASH":
            amount = instance.user.wallet.dash - instance.amount
            Wallet.objects.filter(user=instance.user).update(dash = amount)

        body = f"""
        Hello Webmaster,
        <br>
        <br>
        You have confirmed a withdrawal request
        <br>
        User: {instance.user.username.title()} - {instance.user.email}
        <br>
        Amount: {instance.amount}
        <br>
        <br>
        """
        body2 = f"""
        Hello {instance.user.username.title()},
        <br>
        <br>
        You withdrawal request has been confirmed
        <br>
        Date: {datetime.date.today()}
        <br>
        Amount: {instance.amount}
        <br>
        <br>
        """

        admin_message = get_template('mail/admin_mail.html').render(context={"subject": "Withdrawal Confirmed", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "Withdrawal Confirmed", "body": mark_safe(body2)})
        plain_email(to_email=instance.user.email, subject="Withdrawal Confirmed", body=user_message)
        plain_email(to_email="admin@pengcrest.com", subject="Withdrawal Confirmed", body=admin_message)

@receiver(post_save, sender=Deposit)
def deposit_approve_signal(instance, *args, **kwargs):
    User.objects.filter(username=instance.user.username, can_withdraw=True).update(can_withdraw=False)
    if instance.status == Withdraw.FAILED:
        TransactionHistory.objects.create(
            user=instance.user,
            currency= instance.currency,
            transaction_type= TransactionHistory.DEPOSIT,
            status= TransactionHistory.FAILED,
            amount= instance.amount,
        )

    if instance.user.first_investment:
        two_percent = instance.amount * Decimal(0.02)
        referrer = User.objects.filter(username=instance.user.recommended_by).exists()
        LOGGER.info(referrer)
        if referrer:
            user = User.objects.get(username=instance.user.recommended_by)
            if user.bonus < 1.00:
                profit = Decimal(0.00) + two_percent
            else:
                profit = user.bonus + two_percent
            User.objects.filter(username=instance.user.recommended_by).update(bonus=profit)
            TransactionHistory.objects.create(
                user=user,
                currency="BTC",
                transaction_type= TransactionHistory.AFFILIATE,
                status= TransactionHistory.SUCCESS,
                amount= two_percent,
            )

    User.objects.filter(username=instance.user.username).update(has_invested = True, can_withdraw=False, first_investment=False)


    if instance.status == Deposit.SUCCESS:
        TransactionHistory.objects.create(
            user=instance.user,
            currency= instance.currency,
            transaction_type= TransactionHistory.DEPOSIT,
            status= TransactionHistory.SUCCESS,
            amount= instance.amount,
        )

        if instance.currency == "BTC":
            amount = instance.user.wallet.btc + instance.amount
            Wallet.objects.filter(user=instance.user).update(btc = amount)
        elif instance.currency == "ETH":
            amount = instance.user.wallet.eth + instance.amount
            Wallet.objects.filter(user=instance.user).update(eth = amount)
        elif instance.currency == "LTC":
            amount = instance.user.wallet.ltc + instance.amount
            Wallet.objects.filter(user=instance.user).update(ltc = amount)
        elif instance.currency == "DASH":
            amount = instance.user.wallet.dash + instance.amount
            Wallet.objects.filter(user=instance.user).update(dash = amount)

        body = f"""
        Hello Webmaster,
        <br>
        <br>
        You have confirmed a Deposit request
        <br>
        User: {instance.user.username.title()} - {instance.user.email}
        <br>
        Amount: {instance.amount}
        <br>
        <br>
        """
        body2 = f"""
        Hello {instance.user.username.title()},
        <br>
        <br>
        You Deposit request has been confirmed
        <br>
        Date: {datetime.date.today()}
        <br>
        Amount: {instance.amount}
        <br>
        <br>
        """

        admin_message = get_template('mail/admin_mail.html').render(context={"subject": "Deposit Confirmed", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "Deposit Confirmed", "body": mark_safe(body2)})
        plain_email(to_email=instance.user.email, subject="Deposit Confirmed", body=user_message)
        plain_email(to_email="admin@pengcrest.com", subject="Deposit Confirmed", body=admin_message)


@receiver(user_signed_up)
def referral_signals(request, user, **kwargs):
    LOGGER.info("Creating Referral")
    referrer_id = request.session.get("ref_profile")

    admin_body = f"""
    Hello Webmaster,
    <br>
    <br>
    {user.username.title()} Has just successfully signed up.
    <br>
    <br>
    """

    admin_message = get_template('mail/admin_mail.html').render(context={"subject": "New Referral", "body": mark_safe(admin_body)})
    plain_email(to_email="admin@pengcrest.com", subject="New Referral", body=admin_message)

    LOGGER.info("Sent new registration email to admin")

    if referrer_id is not None:
        recommended_by_user = User.objects.get(id=referrer_id)
        recommender_email = recommended_by_user.email
        new_user = user
        new_user.recommended_by = recommended_by_user
        new_user.save()

        body = f"""
        Hello {recommended_by_user.username.title()},
        <br>
        <br>
        Your referral code: {recommended_by_user.unique_id} was used to refer
        <br>
        <br>
        <strong>NEW USER: {new_user.username.title()}</strong>
        <br>
        <br>
        Be informed that upon their initial investment capital, you will earn <strong>2%</strong> from that investment, which shall be added to your referral bonus.
        <br>
        <br>
        """

        body2 = f"""
        Hello {new_user.username.title()},
        <br>
        <br>
        Your have successfully signed up with the referral code: {recommended_by_user.unique_id}
        <br>
        <br>
        Be informed that upon your initial investment capital, your referrer will earn <strong>2%</strong> from your investment.
        <br>
        <br>
        """

        referrer_message = get_template('mail/simple_mail.html').render(context={"subject": "New Referral", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "Successfully Referrer Registration", "body": mark_safe(body2)})
        plain_email(to_email=user.email, subject="Successfully Referrer Registration", body=user_message)
        plain_email(to_email=recommender_email, subject="New Referral", body=referrer_message)
        LOGGER.info(f"Sent new referrer registration email to {recommended_by_user.username.title()}")


