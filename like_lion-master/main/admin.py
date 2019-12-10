from django.contrib import admin
from .models import *
from main.models import Customer, Service, Clothe, Request
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.



admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Clothe)
admin.site.register(Request)
