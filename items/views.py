import stripe
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View

from django.shortcuts import get_list_or_404

from . import models


class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelView(TemplateView):
    template_name = 'cancel.html'


class ItemsView(ListView):
    model = models.Item
    template_name = 'index.html'
    context_object_name = 'items'


class DetailItem(DetailView):
    model = models.Item
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        item_id = self.kwargs['pk']
        item = models.Item.objects.get(pk=item_id)
        context = super(DetailItem, self).get_context_data(**kwargs)
        context.update({
            'item': item,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


# class ProductLandingPageView(TemplateView):
#     template_name = 'landing.html'

#     def get_context_data(self, **kwargs):
#         item = models.Item.objects.get(id=1)
#         context = super(ProductLandingPageView, self).get_context_data(**kwargs)
#         context.update({
#             'item': item,
#             'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
#         })
#         return context


@csrf_exempt
def create_checkout_session(request, item_id):
    if request.method == 'GET':
        item = get_list_or_404(models.Item, pk=item_id)

        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': str(item[0].name),
                            },
                            'unit_amount': int(item[0].price),
                        },
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})





# class CreateCheckoutSessionView(View):
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             item_id = self.kwargs['pk']
#             item = models.Item.objects.get(id=item_id)
#             print(item)
#             stripe.api_key = settings.STRIPE_SECRET_KEY
#             YOUR_DOMAIN = "http://127.0.0.1:8000/"
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[
#                     {
#                         'price_data': {
#                             'currency': 'usd',
#                             'unit_amount': item.price,
#                             'item_data': {
#                                 'name': item.name,
#                             },
#                         },
#                         'quantity': 1,
#                     },
#                 ],
#                 mode='payment',
#                 success_url=YOUR_DOMAIN + '/success/',
#                 cancel_url=YOUR_DOMAIN + '/cancel/',
#             )

#             return JsonResponse({
#                 'id': checkout_session['id']
#             })