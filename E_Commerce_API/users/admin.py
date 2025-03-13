from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Address, Store

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    readonly_fields = ("user_id",)
    list_display = ("username", "email", "role", "date_joined")
    list_filter = ("role",)
    search_fields = ("username", "email")
    ordering = ("username", "date_joined")
    fieldsets = (
        *UserAdmin.fieldsets,
        ("Custom Fields", {"fields": ("user_id", "role")}),
    )


class StoreAdmin(admin.ModelAdmin):
    readonly_fields = ("store_id", "user_id", "created_at", "updated_at")
    list_display = ("store_name", "user_id__username", "created_at")
    search_fields = ("store_name", "description")
    ordering = ("store_name", "created_at")


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ("address_id", "user", "store", "created_at", "updated_at")
    list_display = ("country", "city", "street_address", "user__username", "store__store_name", "created_at")
    list_filter = ("country", "city")
    search_fields = ("country", "city", "street_address")
    ordering = ("country", "city", "street_address", "created_at")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Address, AddressAdmin)
