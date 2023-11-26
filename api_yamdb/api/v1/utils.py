from django.core.mail import send_mail

MIN_SCORE_VALUE = 1
MAX_SCORE_VALUE = 10
MAX_SLUG_LENGTH = 50


def send_confirmation_code(SUBJECT, MESSAGE, EMAIL_HOST_USER, RECIPIENT_LIST):
    send_mail(
        subject=SUBJECT,
        message=MESSAGE,
        from_email=EMAIL_HOST_USER,
        recipient_list=RECIPIENT_LIST,
    )
