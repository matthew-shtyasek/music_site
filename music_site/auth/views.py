from django.contrib.auth.views import LoginView
from django.shortcuts import render

from auth.forms import LoginForm


class CustomLoginView(LoginView):
    extra_context = {'alerts': set(),
                     'current_page': 'login'}
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        var = super().get(request, *args, **kwargs)
        return var

    def form_valid(self, form):
        self.extra_context['alerts'] = set()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.extra_context['alerts'].add(('Ошибка входа: ', 'Логин или пароль неверны!'))
        return super().form_invalid(form)
