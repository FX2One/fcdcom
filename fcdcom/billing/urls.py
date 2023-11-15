from django.urls import path
from .views import billing

app_name = "billing"

urlpatterns = [
    path("", view=billing, name="home"),
]
