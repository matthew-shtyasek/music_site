from django.urls import path

from payments.views import SelectPremiumView

app_name = 'payments'

urlpatterns = [
    path('select_premium/', SelectPremiumView.as_view(), name='select_premium'),
]
