from django.contrib.auth import views as auth_views
from django.urls import path

from auth.views import CustomLoginView

app_name = 'auth'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
]
