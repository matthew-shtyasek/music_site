from django.contrib.auth import views as auth_views
from django.urls import path
from auth.views import LoginView, RegisterView, SetPasswordView

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-in/', RegisterView.as_view(), name='signin'),
    path('set-pass/', SetPasswordView.as_view(), name='set_password'),
]
