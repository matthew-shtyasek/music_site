from django.contrib.auth import views, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from auth import forms, form_error_parser
from auth.forms import SetPasswordForm
from auth.models import CustomUser
from auth.tasks import send_token_message
from auth.token import user_tokenizer


class LoginView(views.LoginView):
    extra_context = {'current_page': 'login'}
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        var = super().get(request, *args, **kwargs)
        return var

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Логин или пароль введены неверно!')
        messages.add_message(self.request, messages.INFO, f'<a href="#" class="forgot-password">Забыли пароль?</a>')
        return super().form_invalid(form)


class RegisterView(View):
    context = {
        'current_page': 'signin',
        'submit_name': 'Регистрация',
    }

    def get(self, request, *args, **kwargs):
        self.context['form'] = forms.RegisterForm()
        return render(request, template_name='registration/register.html', context=self.context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                validate_email(request.POST.get('email'))
                user = CustomUser.objects.get(email=request.POST.get('email'))
            except ValidationError:
                try:
                    user = CustomUser.objects.get(username=request.POST.get('email'))
                except CustomUser.DoesNotExist:
                    user = None
                    messages.add_message(request, messages.ERROR, 'Пользователя с таким логином не существует!')

            if user:
                if user.is_active:
                    send_token_message.delay(user.id, request.build_absolute_uri(reverse("auth:set_password")))
                    messages.add_message(request, messages.INFO, 'Сообщение со ссылкой для смены пароля было отправлено на вашу почту')
                else:
                    messages.add_message(request, messages.ERROR, 'Ваш пользователь заблокирован, вы не можете восстановить пароль!')

            return render(request, template_name='messages.html', context={'messages': messages.get_messages(request)})
        else:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = CustomUser(username=cd['username'], email=cd['email'])
                user.save()
                send_token_message.delay(user.id, request.build_absolute_uri(reverse("auth:set_password")))
                messages.add_message(request, messages.INFO, 'Сообщение со ссылкой для смены пароля было отправлено на вашу почту')
            else:
                form_error_parser.parse(request, form)
            self.context['form'] = form

        return render(request, template_name='registration/register.html', context=self.context)


class SetPasswordView(View):
    def get(self, request):
        user = CustomUser.objects.get(id=request.GET['id'])

        if user and user_tokenizer.check_token(user, request.GET['token']):
            return render(request, template_name='registration/set_password.html', context={'form': SetPasswordForm(user)})
        messages.add_message(request, messages.ERROR, 'Использована некорректная ссылка для активации аккаунта')
        return redirect(reverse('auth:signin'))

    def post(self, request):
        user = CustomUser.objects.get(id=request.GET['id'])
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user.set_password(cd['new_password1'])
            user.is_active = True
            user.save()
            return redirect(reverse('musics:main'))
        form_error_parser.parse(request, form)
        return render(request, template_name='registration/set_password.html', context={'form': form})


# class ChangePasswordView


def logout_view(request):
    logout(request)
    return redirect('musics:main')
