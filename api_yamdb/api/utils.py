import uuid

from django.conf import settings
from django.core.mail import send_mail


def send_confirm_code(user_email):
    """Send confirmation_code"""
    confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, user_email)
    send_mail(
        subject='Код авторизации',
        message=f'Ваш код для авторизации на сайте: {confirmation_code}',
        from_email={settings.EMAIL_HOST_USER},
        recipient_list=[user_email],
        fail_silently=False,
    )
