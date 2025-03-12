# from django.urls import include, path
# from rest_framework import routers

# from .views import (  # SellerRegisterView,; SellerRetrieveUpdateDestroyView,
#     SellerViewSet,
#     UserRegisterView,
#     UserRetrieveUpdateDestroyView,
# )

# router = routers.DefaultRouter()
# router.register(r"sellers", SellerViewSet)

# urlpatterns = [
#     path("", include(router.urls)),
#     path("user/register/", UserRegisterView.as_view(), name="user-register"),
#     path(
#         "user/",
#         UserRetrieveUpdateDestroyView.as_view(),
#         name="user-retrieve-update-destroy",
#     ),
# ]
