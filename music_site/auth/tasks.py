from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail


@shared_task
def send_confirm_message(user: User):
    subject = f'Подтверждение регистрации на Musify'
    message = f'Для подтверждения регистрации на сайте Musify перейдите по следующей ссылке:\n' \
              f'{"confirm"}\n' \
              f'Если вы не регистрировались на сайте Musify под логином {user.username}, проигнорируйте данное сообщение.'
    return send_mail(subject, message, from_email='musify@admin.ru', recipient_list=[user.email])
