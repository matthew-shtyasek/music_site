from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from auth.models import CustomUser
from auth.token import user_tokenizer


@shared_task
def send_token_message(user_id, absolute_uri):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = False
    user.save()

    subject = 'Подтверждение смены пароля'
    token = user_tokenizer.make_token(user)
    message = f'Для подтверждения смены пароля перейдите по ссылке {absolute_uri}' + f'?id={user.id}&token={token}'
    email_status = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST,
                             recipient_list=[user.email])
    return email_status
