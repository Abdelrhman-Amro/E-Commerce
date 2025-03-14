from django.contrib import admin

from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    readonly_fields = ("cart_id", "created_at", "updated_at")


class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ("cart_item_id", "created_at", "updated_at")
    list_display = ("cart", "product", "cart_item_quantity", "created_at", "updated_at")
    ordering = ("updated_at", "created_at")
    search_fields = ("cart", "product")


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
