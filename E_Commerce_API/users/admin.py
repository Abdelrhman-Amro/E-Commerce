# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# from .models import CustomUser, Seller


# # extends Django’s built-in UserAdmin class, which provides default user management functionality.
# class CustomUserAdmin(UserAdmin):
#     list_display = ("username", "email", "role", "is_active", "is_staff")
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (("Personal Info"), {"fields": ("first_name", "last_name", "email", "role")}),
#         (("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
#         (("Important Dates"), {"fields": ("last_login", "date_joined")}),
#     )


# class SellerAdmin(admin.ModelAdmin):
#     readonly_fields = ("created_at",)
#     list_display = (
#         "store_name",
#         "contact_email",
#         "contact_phone",
#         "address",
#     )
#     search_fields = ["store_name"]
#     fieldsets = (
#         ("Main Info", {"fields": ("store_name", "contact_email")}),
#         ("Optional Info", {"fields": ("description", "contact_phone", "address")}),
#         ("User Info", {"fields": ("user_id",)}),
#         ("Timestamps", {"fields": ("created_at",)}),
#     )


# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Seller, SellerAdmin)
