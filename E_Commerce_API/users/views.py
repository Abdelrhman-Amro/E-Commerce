# from django.db import transaction
# from rest_framework import permissions, serializers, status, viewsets
# from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken

# from .models import CustomUser, Seller
# from .permissions import IsMarketOwner, IsSeller
# from .serializers import CustomUserSerializer, SellerSerializer

# # 1.  Anyone: can create a new user ++
# # 2.  Buyer: can create account seller
# # 3.  Buyer users can:
# #     -   Edit/Delete/Retrieve their account ++
# # 4.  Sellers can:
# #     -   Edit/Delete/Retrieve their seller


# class UserRegisterView(CreateAPIView):
#     """
#     Create a new user
#     """

#     serializer_class = CustomUserSerializer
#     permission_classes = [AllowAny]


# class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     """
#     Authenticated users can retrieve, update or delete a user
#     """

#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user


# class LogoutView(CreateAPIView):
#     """
#     Logout a user by blacklisting their refresh token
#     """

#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response(
#                 {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
#             )
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class SellerViewSet(viewsets.ModelViewSet):
#     queryset = Seller.objects.all()
#     serializer_class = SellerSerializer
#     permission_classes = [IsAuthenticated, IsSeller]

#     def get_permissions(self):
#         if self.action in "list":
#             return [AllowAny()]
#         if self.action in ["retrieve", "create"]:
#             return [IsAuthenticated()]

#         # Only allow the owner of the market to update and delete
#         return [IsAuthenticated(), IsSeller(), IsMarketOwner()]

#     def perform_create(self, serializer):
#         """
#         Create a new seller for a user
#         """
#         user = self.request.user
#         # Check if the user is already a seller
#         if user.role == "seller":
#             raise serializers.ValidationError(
#                 "User is already a seller and has a market."
#             )
#         serializer.save(user_id=user)
