from django.urls import path

from .views import manage_request, plowing_home, plowing_service

app_name = "plowing"

urlpatterns = [
    path("", view=plowing_home, name="home"),
    path("<str:service_id>/", view=plowing_service, name="service"),
    path("manage/<str:request_id>/", view=manage_request, name="request"),
]
