from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import CheckoutView, OrderViewSet, checkout_success

routers = routers.DefaultRouter()
routers.register(r"orders", OrderViewSet)

urlpatterns = [
    path("orders/", include(routers.urls), name="orders"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkout_success/", checkout_success, name="checkout_success"),
]
