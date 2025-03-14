from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    ProductListView,
    ProductRetrieveView,
    ReviewViewSet,
    StoreProductViewSet,
)

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)

store_products_router = routers.DefaultRouter()
store_products_router.register(r"products", StoreProductViewSet)

reviews_router = routers.DefaultRouter()
reviews_router.register(r"reviews", ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("products/", ProductListView.as_view()),
    path("products/<uuid:pk>/", ProductRetrieveView.as_view()),
    path("store/", include(store_products_router.urls)),
    path("products/<uuid:product_pk>/", include(reviews_router.urls)),
]
