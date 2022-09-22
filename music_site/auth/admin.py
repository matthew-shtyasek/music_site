from django.contrib import admin
from django.contrib.admin import ModelAdmin

from auth.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    fields = ('username',
              'email',
              'password',
              'is_active',
              'is_staff',
              'is_superuser',
              'last_login',
              'date_joined')
    list_display = ('username',
                    'email',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'date_joined')
    list_filter = ('is_active',
                   'is_staff',
                   'is_superuser',
                   'last_login',
                   'date_joined')
    search_fields = ('username',
                     'email')
    list_editable = ('is_active',
                     'is_staff',
                     'is_superuser')
