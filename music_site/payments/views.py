from django.shortcuts import render
from django.views.generic import ListView

from payments.models import Premium


class SelectPremiumView(ListView):
    model = Premium
    context_object_name = 'premiums'
    template_name = 'payments/select_premium.html'
