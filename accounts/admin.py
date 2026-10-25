from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("İletişim", {"fields": ("email",)}),
    )
    list_display = ("username", "email", "is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")
