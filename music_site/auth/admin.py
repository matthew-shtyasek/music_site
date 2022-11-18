from django.contrib import admin
from django.contrib.admin import ModelAdmin

from auth.models import CustomUser
from payments.models import Receipt


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    fields = ('pk',
              'username',
              'email',
              'password',
              'is_active',
              'is_staff',
              'is_superuser',
              'groups',
              'user_permissions',
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
                   'groups',
                   'last_login',
                   'date_joined')
    search_fields = ('username',
                     'email')
    list_editable = ('is_active',
                     'is_staff',
                     'is_superuser')
    readonly_fields = ('pk',)
