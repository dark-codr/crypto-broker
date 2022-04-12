import json
import requests

from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from django.urls import reverse
from django.template.loader import get_template, render_to_string
from django.utils.safestring import mark_safe

from pengcrest.utils.emails import plain_email, support_email

from pengcrest.utils.logger import LOGGER

from .models import Mode, Currency

User = get_user_model()

# @require_http_methods(['PUT', 'POST'])
# def enable_dark_mode(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         if settings.PRODUCTION:
#             ip = request.META.get('REMOTE_ADDR')
#         else:
#             ip = '8.8.8.8'

#     LOGGER.info(f"IP Address: {ip}")

#     Mode.objects.filter(ip=ip, theme='light').update(theme='dark')

#     # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     return HttpResponse("""
#         <button :class="{'hidden':dark === true, '':dark === false}" x-on:click="dark = true, iziToast.success({'message':'Dark Mode Activated', 'id':'alert-success', 'color':'green', 'title':'DARK MODE', 'timeout': 5000, 'resetOnHover': true, 'balloon': true})" hx-post="/dark_mode/" hx-trigger="click" hx-swap="outerHTML" class="block" type="button">
#             <svg class="w-6 h-6 text-font-darker dark:text-primary" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
#               <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
#             </svg>
#         </button>
#     """)


# @require_http_methods(['PUT', 'POST'])
# def enable_light_mode(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         if settings.PRODUCTION:
#             ip = request.META.get('REMOTE_ADDR')
#         else:
#             ip = '8.8.8.8'

#     LOGGER.info(f"IP Address: {ip}")

#     Mode.objects.filter(ip=ip, theme="dark").update(theme="light")
#     # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     return HttpResponse("""
#         <button :class="{'':dark === true, 'hidden':dark === false}" x-on:click="dark = false, iziToast.error({'message':'Dark Mode Deactivated', 'id':'alert-error', 'color':'red', 'title':'DARK MODE', 'timeout': 5000, 'resetOnHover': true, 'balloon': true,})" hx-put="/light_mode/" hx-trigger="click" hx-swap="outerHTML" class="block" type="button">
#             <svg class="w-6 h-6 text-font-darker dark:text-primary" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
#                 <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
#             </svg>
#         </button>
#     """)



def exhrate(request):
    btcusd = Currency.objects.get(name="btc")
    ethusd = Currency.objects.get(name="eth")
    ltcusd = Currency.objects.get(name="ltc")
    dashusd = Currency.objects.get(name="dash")


    context = {
        "btcusd": 100 / btcusd.amount if btcusd.exists() else 0.00,
        "ethusd": 100 / ethusd.amount if ethusd.exists() else 0.00,
        "ltcusd": 100 / ltcusd.amount if ltcusd.exists() else 0.00,
        "dashusd": 100 / dashusd.amount if dashusd.exists() else 0.00,
    }

    if request.htmx:
        return render(request, "snippets/crypto_price.html", context)
    else:
        return render(request, "pages/home.html", context)


def home(request, *args, **kwargs):
    uid = str(kwargs.get('uid'))
    LOGGER.info(uid)
    try:
        user = User.objects.get(unique_id=uid)
        request.session['ref_profile'] = user.id
        LOGGER.info(f"ID: {user.id} for {user.name.title()}")
    except:
        LOGGER.info("No User ID")


    btcusd = Currency.objects.filter(name="btc")[0]
    ethusd = Currency.objects.filter(name="eth")[0]
    ltcusd = Currency.objects.filter(name="ltc")[0]
    dashusd = Currency.objects.filter(name="dash")[0]

    # context = {
    #     "btcusd": 100 / btcusd,
    #     "ethusd": 100 / ethusd,
    #     "ltcusd": 100 / ltcusd,
    #     "dashusd": 100 / dashusd,
    # }

    context = {
        "btcusd": 100 / btcusd.amount,
        "ethusd": 100 / ethusd.amount,
        "ltcusd": 100 / ltcusd.amount,
        "dashusd": 100 / dashusd.amount,
    }

    if request.htmx:
        return render(request, "snippets/crypto_price.html", context)
    else:
        return render(request, "pages/home.html", context)

# @require_http_methods(['GET', 'POST'])
def contact(request):
    subject = request.POST.get('subject')
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    agree = request.POST.get('newsletter')

    if request.method == 'POST':
        support_message = f"""
        Dear Support,
        <br>
        <br>
        {name.title()} Just sent you a new support email enquiring about
        <br>
        <br>
        Enquiry: {message}
        <br>
        <br>
        Please do well to respond appropriately and on time.
        <br>
        <br>
        """

        if agree and User.objects.filter(email=email).exists():
            User.objects.filter(email=email).update(newsletter=True)


        messages.success(request, "Your message has been sent successfully.")
        message = get_template('mail/simple_mail.html').render(context={"subject": subject.title(), "body": mark_safe(support_message)})
        support_email(to_email="support@pengcrest.com", from_email=email, subject=subject.title(), body=message)

    return render(request, "pages/contact.html")


