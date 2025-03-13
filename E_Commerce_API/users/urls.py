from django.urls import include, path
from rest_framework import routers

from .views import (
    AddressViewSet,
    StoreAddressViewSet,
    StoreRetriveAuthView,
    StoreViewSet,
    UserRegisterView,
    UserRetrieveUpdateDestroyView,
)

router = routers.DefaultRouter()
router.register(r"stores", StoreViewSet)
router.register(r"user/addresses", AddressViewSet, basename="address")
router.register(r"store/addresses", StoreAddressViewSet, basename="store-address")

urlpatterns = [
    path("", include(router.urls)),
    path("user/register/", UserRegisterView.as_view(), name="user-register"),
    path("user/", UserRetrieveUpdateDestroyView.as_view(), name="user-retrieve-update-destroy"),
]
