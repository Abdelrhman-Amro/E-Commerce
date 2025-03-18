from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import (
    CheckoutView,
    OrderItemListView,
    OrderListView,
    OrderUpdateView,
    PaymentListView,
    checkout_success,
)

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<uuid:pk>/items/", OrderItemListView.as_view(), name="order_item_list"),
    path("orders/<uuid:pk>/", OrderUpdateView.as_view(), name="order_update"),
    path("payments/", PaymentListView.as_view(), name="payment_list"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout_success/", checkout_success, name="checkout_success"),
]
