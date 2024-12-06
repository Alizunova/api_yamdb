from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Регистрируем модель в админке:
admin.site.register(User, UserAdmin)

# Register your models here.
