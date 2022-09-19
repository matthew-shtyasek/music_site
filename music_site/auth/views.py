from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import views
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from auth import forms, form_error_parser
from auth.forms import SetPasswordForm
from auth.token import user_tokenizer

User = get_user_model()


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
        messages.add_message(self.request, messages.INFO, f'<a href="#">Забыли пароль?</a>')
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
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User(username=cd['username'], email=cd['email'])
            user.save()
            subject = 'Подтверждение'
            token = user_tokenizer.make_token(user)
            message = f'Для подтверждения регистрации перейдите по ссылке {request.build_absolute_uri(reverse("auth:set_password"))}' + f'?id={user.id}&token={token}'
            email_status = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST, recipient_list=[user.email])
            if email_status == 1:
                messages.add_message(request, messages.INFO, 'Письмо со ссылкой успешно отправлено на ваш электронный почтовый ящик')
            else:
                messages.add_message(request, messages.ERROR, 'При отправке письма со ссылкой на ваш электронный почтовый ящик произошла ошибка')
        else:
            form_error_parser.parse(request, form)
        self.context['form'] = form
        return render(request, template_name='registration/register.html', context=self.context)


class SetPasswordView(View):
    def get(self, request):
        user = User.objects.get(id=request.GET['id'])

        if user and user_tokenizer.check_token(user, request.GET['token']):
            return render(request, template_name='registration/set_password.html', context={'form': SetPasswordForm(user)})
        messages.add_message(request, messages.ERROR, 'Использована некорректная ссылка для активации аккаунта')
        return redirect(reverse('auth:signin'))

    def post(self, request):
        user = User.objects.get(id=request.GET['id'])
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user.set_password(cd['new_password1'])
            user.is_active = True
            user.save()
            return redirect(reverse('musics:main'))
        form_error_parser.parse(request, form)
        return render(request, template_name='registration/set_password.html', context={'form': form})
