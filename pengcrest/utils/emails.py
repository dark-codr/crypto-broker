from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.mail import EmailMessage

# sender = settings.EMAIL_HOST_USER
# admins = settings.ADMINS

def plain_email(to_email, subject, body):
    message = EmailMessage(subject=subject, body=body, from_email="noreply@pengcrest.com", to=[to_email], bcc=["webmaster@pengcrest.com"], fail_silently=False)
    message.content_subtype = "html"
    message.send()

def support_email(to_email, subject, body, from_email):
    message = EmailMessage(subject=subject, body=body, from_email=from_email, to=[to_email], bcc=["webmaster@pengcrest.com"], reply_to=[from_email], fail_silently=False,)
    message.content_subtype = "html"
    message.send()


# def pdf_attachment_email(to_email, subject, body, filepath, filename):
#     from_email = sender
#     subject = subject
#     body = body
#     message = EmailMessage(subject, body, from_email, ["programmingtext@gmail.com", to_email])
#     file_data = open(filepath, "rb")
#     message.attach(filename, file_data.read(), "application/pdf")
#     message.content_subtype = "html"
#     file_data.close()
#     message.send()


# def image_attachment_email(to_email, subject, body, filepath, filename):
#     from_email = sender
#     subject = subject
#     body = body
#     message = EmailMessage(subject, body, from_email, ["programmingtext@gmail.com", to_email])
#     file_data = open(filepath, "rb")
#     message.attach(filename, file_data.read(), "image/jpeg")
#     message.content_subtype = "html"
#     file_data.close()
#     message.send()
