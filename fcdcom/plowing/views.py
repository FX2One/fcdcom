from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from fcdcom.plowing.models import PlowingRequest, PlowingService


# Create your views here.
def plowing_home(request: HttpRequest) -> HttpResponse:
    avail_services = PlowingService.objects.exclude(provider=request.user)
    avail_requests = PlowingRequest.objects.filter(service__provider=request.user, status="pending")
    return render(
        request,
        "plowing/plowing_home.html",
        context={"avail_services": avail_services, "avail_requests": avail_requests},
    )


def plowing_service(request: HttpRequest, service_id: str) -> HttpResponse:
    service: PlowingService = get_object_or_404(PlowingService, pk=service_id)
    PlowingRequest.objects.create(service=service, requestor=request.user)

    messages.add_message(request, messages.SUCCESS, message="Sent successfully")
    return redirect("plowing:home")


def manage_request(request: HttpRequest, request_id: str) -> HttpResponse:
    p_request: PlowingRequest = get_object_or_404(PlowingRequest, pk=request_id)
    action = request.GET.get("action")
    if action == "accept":
        if p_request.charge_customer():
            messages.add_message(request, messages.SUCCESS, message="Payment successful. Request accepted.")
        else:
            messages.add_message(request, messages.ERROR, message="Payment failed. Try again.")
    elif action == "reject":
        p_request.status = "rejected"
        p_request.save()
    return redirect("plowing:home")
