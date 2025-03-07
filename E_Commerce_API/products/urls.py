from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    ProductListView,
    ProductRetrieveView,
    SellerProductViewSet,
)

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"seller/products", SellerProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("products/", ProductListView.as_view()),
    path("products/<uuid:pk>/", ProductRetrieveView.as_view()),
]
