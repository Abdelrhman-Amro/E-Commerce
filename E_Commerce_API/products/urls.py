# from django.conf.urls import include
# from django.urls import path
# from rest_framework import routers

# from .views import (
#     CategoryViewSet,
#     ProductListView,
#     ProductRetrieveView,
#     ReviewViewSet,
#     SellerProductViewSet,
# )

# router = routers.DefaultRouter()
# router.register(r"categories", CategoryViewSet)
# router.register(r"seller/products", SellerProductViewSet)
# router.register(r"reviews", ReviewViewSet)

# urlpatterns = [
#     path("", include(router.urls)),
#     path("products/", ProductListView.as_view()),
#     path("products/<uuid:pk>/", ProductRetrieveView.as_view()),
# ]
