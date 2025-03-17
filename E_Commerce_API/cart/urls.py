from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import CartItemViewSet, RetrieveCart

router = routers.DefaultRouter()
router.register(r"cart-items", CartItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("cart/", RetrieveCart.as_view(), name="cart"),
]
