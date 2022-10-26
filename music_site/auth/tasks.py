from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from auth.models import CustomUser
from auth.token import user_tokenizer


@shared_task
def send_token_message(user_id, absolute_uri):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = False
    user.save()

    subject = 'Подтверждение смены пароля'
    token = user_tokenizer.make_token(user)
    context = {'absolute_uri': absolute_uri,
               'user': user,
               'token': token}
    html_message = render_to_string('mail_messages/change_password.html', context=context)
    text_message = strip_tags(html_message)
    email_status = send_mail(subject=subject,
                             message=text_message,
                             from_email=settings.EMAIL_HOST,
                             recipient_list=[user.email],
                             html_message=html_message)
    return email_status
