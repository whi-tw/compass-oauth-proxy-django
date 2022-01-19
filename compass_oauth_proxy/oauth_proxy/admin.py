from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CompassUser

admin.site.register(CompassUser, UserAdmin)
