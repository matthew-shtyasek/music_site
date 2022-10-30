from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password='', **extra_fields):
        if not email:
            raise ValueError('The e-mail must be set')
        if 'username' not in extra_fields or not extra_fields['username']:
            raise ValueError('The username must be set')
        if not extra_fields.get('is_superuser'):
            extra_fields['is_active'] = False

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,
                              db_index=True,
                              verbose_name='Электронная почта')
    username = models.CharField(max_length=64,
                                unique=True,
                                db_index=True,
                                verbose_name='Логин')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Персонал')
    is_active = models.BooleanField(default=False,
                                    verbose_name='Активирован')
    date_joined = models.DateTimeField(default=timezone.now,
                                       verbose_name='Дата регистрации')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_absolute_uri(self):
        return reverse('profiles:profile', args=[self.pk])

    class Meta:
        ordering = ('username', 'date_joined')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
