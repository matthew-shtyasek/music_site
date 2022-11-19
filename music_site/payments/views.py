from django.utils import timezone
import braintree

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from payments.models import Premium, Receipt


class SelectPremiumView(ListView):
    model = Premium
    context_object_name = 'premiums'
    template_name = 'payments/select_premium.html'


class PaymentsView(LoginRequiredMixin, View):
    template_name = 'payments/payments.html'

    def get_context_data(self, **kwargs):
        try:
            braintree_client_token = braintree.ClientToken.generate({'cutomer_id': self.request.user.id})
        except:
            braintree_client_token = braintree.ClientToken.generate({})

        try:
            premium = Premium.objects.get(pk=kwargs['premium_pk'])
        except:
            raise Http404('Данный премиум не найден!')

        context = {'braintree_client_token': braintree_client_token,
                   'premium': premium}
        context.update(kwargs)
        return context

    def get(self, request, **kwargs):
        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        braintree.Configuration.configure(environment=braintree_env,
                                          merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                          public_key=settings.BRAINTREE_PUBLIC_KEY,
                                          private_key=settings.BRAINTREE_PRIVATE_KEY)

        return render(request,
                      self.template_name,
                      self.get_context_data(premium_pk=kwargs['premium_pk']))

    def post(self, request, **kwargs):
        if 'done' in request.POST:
            if request.POST['done']:
                messages.add_message(request, messages.SUCCESS, 'Оплата прошла успешно!')
                premium = Premium.objects.get(pk=kwargs['premium_pk'])
                receipt = Receipt(premium=premium,
                                  price=premium.price,
                                  discount=premium.discount,
                                  owner=request.user,
                                  premium_end_date=timezone.timedelta(days=30 * premium.months) + timezone.now())
                receipt.save()
            else:
                messages.add_message(request, messages.ERROR, 'При оплате возникли ошибки, попробуйте ещё раз!')
        else:
            payment_method_nonce = request.POST['payment_method_nonce']
            customer = braintree.Customer.create({'first_name': None,
                                                  'last_name': request.user.username,
                                                  'email': request.user.email})
            context = self.get_context_data(premium_pk=kwargs['premium_pk'])
            result = braintree.Transaction.sale({
                'amount': Premium.objects.get(premium_pk=kwargs['premium_pk']).get_result_price(),
                'payment_method_nonce': payment_method_nonce,
                'merchant_account_id': settings.BRAINTREE_MERCHANT_ACCOUNT_ID,
                'options': {
                    'submit_for_settlement': True,
                },
            })
        return JsonResponse(dict())
