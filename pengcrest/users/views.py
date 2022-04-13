import datetime

from decimal import Decimal

from django.db.models import Sum

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template, render_to_string
from django.utils.safestring import mark_safe

from django.views.generic import DetailView, RedirectView, UpdateView, CreateView


from .forms import KYCForm, UserUpdateForm
from pengcrest.utils.logger import LOGGER

from .models import Addresses, Deposit, TransactionHistory, KYCVerify, Wallet, Withdraw
from pengcrest.mode.models import Currency

from pengcrest.utils.emails import plain_email

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        btcusd = Currency.objects.filter(name="btc")[0]
        ethusd = Currency.objects.filter(name="eth")[0]
        ltcusd = Currency.objects.filter(name="ltc")[0]
        dashusd = Currency.objects.filter(name="dash")[0]


        context["btc_bal"] = self.request.user.wallet.btc / btcusd.amount
        context["eth_bal"] = self.request.user.wallet.eth / ethusd.amount
        context["ltc_bal"] = self.request.user.wallet.ltc / ltcusd.amount
        context["dash_bal"] = self.request.user.wallet.dash / dashusd.amount
        context["total_asset"] = self.request.user.wallet.total_asset # Deposit.objects.filter(user=self.request.user, status=Deposit.SUCCESS).aggregate(Sum('amount'))

        context["transactions"] = self.request.user.transaction.all().exclude(transaction_type="ROI")
        context["roi"] = self.request.user.transaction.filter(transaction_type="ROI")[:50]
        context["quick"] = User.objects.filter(username=self.request.user.username).prefetch_related("quickfund").all()
        return context

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    form_class = UserUpdateForm
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        btcusd = Currency.objects.filter(name="btc")[0]
        ethusd = Currency.objects.filter(name="eth")[0]
        ltcusd = Currency.objects.filter(name="ltc")[0]
        dashusd = Currency.objects.filter(name="dash")[0]


        context["btc_bal"] = self.request.user.wallet.btc / btcusd.amount
        context["eth_bal"] = self.request.user.wallet.eth / ethusd.amount
        context["ltc_bal"] = self.request.user.wallet.ltc / ltcusd.amount
        context["dash_bal"] = self.request.user.wallet.dash / dashusd.amount
        context["total_asset"] = Deposit.objects.filter(user=self.request.user, status=Deposit.SUCCESS).annotate(Sum('amount'))
        # context["transactions"] = self.request.user.transaction.all().exclude(transaction_type="ROI")[:50]
        # context["roi"] = self.request.user.transaction.filter(transaction_type="ROI")[:50]
        return context

user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

user_redirect_view = UserRedirectView.as_view()


def get_referrals(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "users/refs.html", context={"object":user})

def get_transactions(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "users/trans.html", context={"transactions":user.transaction.all().exclude(transaction_type="ROI")})

def user_dashboard(request, username):
    user = get_object_or_404(User, username=username)
    btc_bal = user.wallet.btc
    eth_bal = user.wallet.eth
    ltc_bal = user.wallet.ltc
    dash_bal = user.wallet.dash

    btcusd = Currency.objects.filter(name="btc")[0]
    ethusd = Currency.objects.filter(name="eth")[0]
    ltcusd = Currency.objects.filter(name="ltc")[0]
    dashusd = Currency.objects.filter(name="dash")[0]

    context = {
        "object":user,
        "btc_bal":btc_bal / btcusd.amount,
        "eth_bal":eth_bal / ethusd.amount,
        "ltc_bal":ltc_bal / ltcusd.amount,
        "dash_bal":dash_bal / dashusd.amount,
        "transactions":user.transaction.all()[:50]
    }
    return render(request, "users/dashboard.html", context)


class KYCVerify(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = KYCVerify
    form_class = KYCForm
    template_name = 'users/kyc.html'
    success_message = _("KYC Verification Successful")

    def get_success_url(self):
        self.request.user.get_absolute_url()
        return super().get_success_url()

    def form_valid(self, form):
        form.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        btcusd = Currency.objects.filter(name="btc")[0]
        ethusd = Currency.objects.filter(name="eth")[0]
        ltcusd = Currency.objects.filter(name="ltc")[0]
        dashusd = Currency.objects.filter(name="dash")[0]


        context["btc_bal"] = self.request.user.wallet.btc / btcusd.amount
        context["eth_bal"] = self.request.user.wallet.eth / ethusd.amount
        context["ltc_bal"] = self.request.user.wallet.ltc / ltcusd.amount
        context["dash_bal"] = self.request.user.wallet.dash / dashusd.amount
        return context

kycverify = KYCVerify.as_view()


def withdraw_bonus(request, username):
    user = get_object_or_404(User, username=username)
    if user.bonus > 100:
        body = f"""
        Hello Webmaster,
        <br>
        <br>
        There is a request to withdraw referral bonus for
        <br>
        User: {user.username.title()} - {user.email}
        <br>
        Amount: {user.bonus}
        <br>
        <br>
        """
        body2 = f"""
        Hello {user.username.title()},
        <br>
        <br>
        You have successfully withdraw your referral bonus
        <br>
        Date: {datetime.date.today()}
        <br>
        Amount: {user.bonus}
        <br>
        <br>
        """

        User.objects.filter(username=user.username).update(bonus=0)

        messages.success(request, f"Bonus Withdrawal Initiated to account {user.wallet_address}. Pending 1 of 3. ")
        admin_message = get_template('mail/admin_mail.html').render(context={"subject": "Referral Bonus Withdrawal Initiated", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "Referral Bonus Withdrawal Initiated", "body": mark_safe(body2)})
        plain_email(to_email=user.email, subject="Referral Bonus Withdrawal Initiated", body=user_message)
        plain_email(to_email="admin@pengcrest.com", subject="Referral Bonus Withdrawal Initiated", body=admin_message)
    return redirect(reverse("users:detail", kwargs={"username":user.username}))

def withdraw_roi(request, username):
    user = get_object_or_404(User, username=username)
    if user.can_withdraw_roi and user.roi > 0:
        body = f"""
        Hello Webmaster,
        <br>
        <br>
        There is a request to withdraw ROI for
        <br>
        User: {user.username.title()} - {user.email}
        <br>
        Amount: {user.roi}
        <br>
        <br>
        """

        body2 = f"""
        Hello {user.username.title()},
        <br>
        <br>
        You have successfully withdraw your ROI bonus
        <br>
        Date: {datetime.date.today()}
        <br>
        Amount: {user.roi}
        <br>
        <br>
        """

        User.objects.filter(username=user.username).update(roi=0, can_withdraw_roi=False)

        messages.success(request, f"ROI Withdrawal Initiated to account {user.wallet_address}. Pending 1 of 3. ")
        admin_message = get_template('mail/admin_mail.html').render(context={"subject": "ROI Withdrawal Initiated", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "ROI Withdrawal Initiated", "body": mark_safe(body2)})
        plain_email(to_email=user.email, subject="ROI Withdrawal Initiated", body=user_message)
        plain_email(to_email="admin@pengcrest.com", subject="ROI Withdrawal Initiated", body=admin_message)
    return redirect(reverse("users:detail", kwargs={"username":user.username}))
    # return HttpResponseRedirect(reverse('users:detail', kwargs={"username":user.username}))



def deposit(request, username):
    user = get_object_or_404(User, username=username)
    amount = request.POST.get('amount')
    currency = request.POST.get('currency')


    if float(amount) != None:
        LOGGER.info(f"Deposit Amount: {amount}")
        fmt_amount = float(amount)
        Wallet.objects.filter(user=user).update(invested_date = datetime.datetime.now())
        Deposit.objects.create(
            user=user,
            currency= currency,
            status= "PENDING",
            amount= Decimal(fmt_amount),
        )

        body = f"""
            Hello Webmaster,
            <br>
            <br>
            There is a deposit request awaiting your approval
            <br>
            User: {user.username.title()} - {user.email}
            <br>
            Currency: {currency}
            <br>
            Amount: {amount}
            <br>
            <br>
        """
        body2 = f"""
            Hello {user.email},
            <br>
            <br>
            You have successfully deposited into your wallet.
            <br>
            Date: {datetime.date.today()}
            <br>
            Currency: {currency}
            <br>
            Amount: {amount}
            <br>
            <br>
        """
        LOGGER.info("deposit successful")

        messages.success(request, f"Deposited {amount} into your {currency} wallet. Processing your payment verification 1 of 3")
        admin_message = get_template('mail/admin_mail.html').render(context={"subject": "New Deposit Request", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "New Deposit Request", "body": mark_safe(body2)})
        plain_email(to_email=user.email, subject="New Deposit Initiated", body=user_message)
        plain_email(to_email="admin@pengcrest.com", subject="New Deposit Initiated", body=admin_message)



        transactions = user.transaction.all()

        wallet = Addresses.objects.filter(currency=currency)

        context = {
            "object": user,
            "transactions": transactions,
            "wallet": wallet.wallet if wallet.exists() else "uhdi8uhdj8U9usj(**(^(%j78hdye,k"
        }

        return render(request, 'users/deposit.html', context)
    messages.error(request, "Input an amount")
    return redirect(user.get_absolute_url)

def topup(request, username):
    user = get_object_or_404(User, username=username)
    amount = request.POST.get('amount')
    currency = request.POST.get('currency')

    if amount != "":
        LOGGER.info(f"Topup Amount: {amount}")
        User.objects.filter(username=user.username).update(has_toped = True)
        Deposit.objects.create(
            user=user,
            currency= currency,
            status= "PENDING",
            amount= amount,
        )

        body = f"""
            Hello Webmaster,
            <br>
            <br>
            There is a top up request awaiting your approval
            <br>
            User: {user.username.title()} - {user.email}
            <br>
            Currency: {currency}
            <br>
            Amount: {amount}
            <br>
            <br>
        """
        body2 = f"""
            Hello Webmaster,
            <br>
            <br>
            You have successfully deposited into your wallet.
            <br>
            Date: {datetime.date.today()}
            <br>
            Currency: {currency}
            <br>
            Amount: {amount}
            <br>
            <br>
        """

        messages.success(request, f"Topped {amount} into your {currency} wallet. Processing your payment verification 1 of 3")
        admin_message = get_template('mail/admin_mail.html').render(context={"subject": "New Top-Up Request", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "New Top-Up Request", "body": mark_safe(body2)})
        plain_email(to_email=user.email, subject="New Top-Up Initiated", body=user_message)
        plain_email(to_email="admin@pengcrest.com", subject="New Top-Up Initiated", body=admin_message)

        wallet = Addresses.objects.filter(currency=currency)
        transactions = user.transaction.all()


        context = {
            "object": user,
            "transactions": transactions,
            "wallet": wallet.wallet if wallet.exists() else "uhdi8uhdj8U9usj(**(^(%j78hdye,k"
        }

        return render(request, 'users/deposit.html', context)
    messages.error(request, "Input and amount")
    return redirect(reverse("users:detail", kwargs={"username":user.username}))

def withdraw(request, username):
    user = get_object_or_404(User, username=username)
    amount = request.POST.get('amount')
    currency = request.POST.get('currency')
    wallet = request.POST.get('wallet')

    if user.can_withdraw and amount != "":
        LOGGER.info(f"Withdrawn Amount: {amount}")
        Withdraw.objects.create(
            user=user,
            currency= currency,
            status= "PENDING",
            amount= amount,
            wallet = wallet
        )

        User.objects.filter(user=user).update(has_toped=False, has_invested=False)

        # transactions = user.transaction.all()

        body = f"""
            Hello Webmaster,
            <br>
            <br>
            There is a deposit request awaiting your approval
            <br>
            User: {user.username.title()} - {user.email}
            <br>
            Currency: {currency}
            <br>
            Amount: {amount}
            <br>
            <br>
        """
        body2 = f"""
            Hello Webmaster,
            <br>
            <br>
            You have successfully withdrawn from your wallet.
            <br>
            Date: {datetime.date.today()}
            <br>
            Currency: {currency}
            <br>
            Amount: {amount}
            <br>
            <br>
        """

        messages.success(request, f"Pending withdraw: {amount} {currency} from wallet. Processing your transaction: verification 1 of 3")
        admin_message = get_template('mail/admin_mail.html').render(context={"subject": "New Withdrawal Request", "body": mark_safe(body)})
        user_message = get_template('mail/simple_mail.html').render(context={"subject": "New Withdrawal Request", "body": mark_safe(body2)})
        plain_email(to_email=user.email, subject="New Withdrawal Initiated", body=user_message)
        plain_email(to_email="admin@pengcrest.com", subject="New Withdrawal Initiated", body=admin_message)
    else:

        # context = {
        #     "object": user,
        #     "transactions": transactions
        # }

        # return render(request, 'users/withdraw.html', context)
        messages.error(request, "Input and amount")
    return redirect(reverse("users:detail", kwargs={"username":user.username}))























def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("This username already exists")
    else:
        return HttpResponse("")

def check_email(request):
    email = request.POST.get('email')
    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse("This email already exists")
    else:
        return HttpResponse("")


