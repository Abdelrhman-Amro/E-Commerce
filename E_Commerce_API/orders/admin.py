from django.contrib import admin

from .models import Order, OrderItem, Payment


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ("order_id", "created_at", "updated_at")
    list_display = ("user__username", "order_id", "status", "total_amount", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("user__username",)
    ordering = ("-created_at",)


class OrderItemAdmin(admin.ModelAdmin):
    pass


class PaymentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
