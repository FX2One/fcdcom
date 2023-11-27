from django.urls import path
from .views import billing, checkout_session, checkout_success

app_name = "billing"

urlpatterns = [
    path("", view=billing, name="home"),
    path("checkout/", view=checkout_session, name="checkout"),
    path("checkout/success", view=checkout_success, name="checkout_success"),
]
