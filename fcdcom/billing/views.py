from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest
from django.conf import settings
import stripe
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def billing(request: HttpRequest) -> HttpResponse:
    return render(request,'billing/billing_home.html')
@login_required
def checkout_session(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        stripe.api_key=settings.STRIPE_SECRET_KEY
        if request.user.stripe_customer_id:
            customer_id = request.user.stripe_customer_id
        else:
            customer = stripe.Customer.create(
                email=request.user.email
            )
            customer_id = customer['id']
            request.user.stripe_customer_id = customer_id
            request.user.save()

        success_url_base = request.build_absolute_uri(reverse('billing:checkout_success'))
        success_url = f'{success_url_base}?session_id={{CHECKOUT_SESSION_ID}}'
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='setup',
            customer=customer_id,
            success_url=success_url,
            cancel_url='http://localhost:4242/cancel',
        )

        return redirect(session.url, code=303)
    return render(request,'billing/checkout_session.html')

@login_required
def checkout_success(request: HttpRequest) -> HttpResponse:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    context = {'session': session}
    print(context)
    return render(request,'billing/checkout_success.html', context)


