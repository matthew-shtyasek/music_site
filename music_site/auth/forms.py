from django import forms as dj_forms
from django.contrib.auth import forms
from django.forms import fields

from auth.models import CustomUser


class LoginForm(forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control'
            item.help_text = ''


class RegisterForm(forms.UserCreationForm):
    username = dj_forms.CharField(max_length=64,
                                  label='Логин')
    email = dj_forms.EmailField(max_length=150,
                                label='Электронная почта')

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control'
            item.help_text = ''


class SetPasswordForm(forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control'
            item.help_text = ''
