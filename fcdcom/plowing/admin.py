from django.contrib import admin

# Register your models here.
from fcdcom.plowing.models import PlowingRequest, PlowingService

admin.site.register(PlowingService)
admin.site.register(PlowingRequest)
