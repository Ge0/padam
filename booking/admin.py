from django.contrib import admin

# Register your models here.
from .models import Booking, Car

admin.site.register(Booking)
admin.site.register(Car)
