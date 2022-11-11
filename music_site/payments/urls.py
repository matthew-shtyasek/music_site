from django.urls import path

from payments.views import SelectPremiumView, PaymentsView

app_name = 'payments'

urlpatterns = [
    path('select_premium/', SelectPremiumView.as_view(), name='select_premium'),
    path('pay/<int:premium_pk>/', PaymentsView.as_view(), name='pay'),
]
