from django.contrib import admin

from .models import City, State, Subscriber

# Register your models here.
admin.site.register(State)
admin.site.register(City)
admin.site.register(Subscriber)
