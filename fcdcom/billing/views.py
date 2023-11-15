from django.shortcuts import render

from django.http import HttpResponse, HttpRequest


# Create your views here.
def billing(request: HttpRequest) -> HttpResponse:
    return render(request,'billing/billing_home.html')
