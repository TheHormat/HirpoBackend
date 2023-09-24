from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.views import PasswordResetView
from account.models import *
from django.urls import path

# Register your models here.

User = get_user_model()
# admin.site.register(Activationcode)
