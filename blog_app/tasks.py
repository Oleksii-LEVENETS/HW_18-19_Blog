from blog_core import settings

from celery import shared_task

from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse


@shared_task
def send_mail_temp(subject, message, user_email=None):
    email_to = [settings.EMAIL_HOST_USER, user_email]
    if user_email is None:
        email_to = [settings.EMAIL_HOST_USER]
    try:
        send_mail(
            subject=f"{subject}",
            message=f"{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_to,
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
