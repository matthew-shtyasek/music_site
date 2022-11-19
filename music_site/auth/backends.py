from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from auth.models import CustomUser


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(raw_password=password):
                return user
        except CustomUser.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            pass
