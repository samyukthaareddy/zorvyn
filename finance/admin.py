from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Transaction


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "role", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("owner", "type", "amount", "category", "date")
    list_filter = ("type", "category", "date")
    search_fields = ("category", "notes")
