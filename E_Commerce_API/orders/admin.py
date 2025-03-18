from django.contrib import admin

from .models import Order, OrderItem, Payment


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ("order_id", "created_at", "updated_at")
    list_display = ("user__username", "order_id", "status", "total_amount", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username",)
    ordering = ("-created_at",)


class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ("order_item_id", "created_at", "updated_at")
    list_display = ("product__name", "order_item_quantity", "unit_price", "order_item_id", "order", "created_at")
    list_filter = ("order__status",)
    search_fields = ("product__name", "order__user__username", "product__store__name")
    ordering = ("-created_at",)


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ("payment_id", "created_at", "updated_at")
    list_display = ("payment_id", "order", "status", "amount", "created_at")
    list_filter = ("status",)
    search_fields = ("order__user__username",)
    ordering = ("-created_at",)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
