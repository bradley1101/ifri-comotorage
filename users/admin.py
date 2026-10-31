from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "filiere", "is_staff")
    list_filter = ("role", "filiere", "is_staff")
    fieldsets = UserAdmin.fieldsets + (("Comotorage", {"fields": ("telephone", "role", "filiere", "bio")}),)
