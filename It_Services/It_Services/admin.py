# myapp/admin.py
from django.contrib import admin
from .models import UserData,Service,Subscription

admin.site.register(UserData)
admin.site.register(Service)
admin.site.register(Subscription)