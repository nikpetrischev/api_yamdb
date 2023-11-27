# Django Library
from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER

MIN_SCORE_VALUE = 1
MAX_SCORE_VALUE = 10
MAX_SLUG_LENGTH = 50


def send_confirmation_code(SUBJECT, MESSAGE, RECIPIENT_LIST):
    send_mail(
        subject=SUBJECT,
        message=MESSAGE,
        from_email=EMAIL_HOST_USER,
        recipient_list=RECIPIENT_LIST,
        fail_silently=False,
        auth_user=EMAIL_HOST_USER,
        auth_password=EMAIL_HOST_PASSWORD
    )
