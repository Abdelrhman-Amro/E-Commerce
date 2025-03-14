from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, serializers, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Address, CustomUser, Store
from .permissions import IsSeller, IsStoreOwner
from .serializers import AddressSerializer, CustomUserSerializer, StoreSerializer


# **Success
class UserRegisterView(CreateAPIView):
    """
    - Anyone:
        - CREATE new user
    """

    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


# **Success
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    - Authenticated users:
        - CREATE, UPDATE, DELETE own user data
    """

    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# **Success
class LogoutView(CreateAPIView):
    """
    Logout a user by blacklisting own refresh token
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# **Success
class StoreViewSet(viewsets.ModelViewSet):
    """
    - Anyone:
        - LIST stores
        - RETRIEVE store
    - Authenticated:
        - CREATE new store
    - Seller:
        - UPDATE, DELETE own store

    - urls:
        stores/                 LIST, CREATE
        stores/<uuid:pk>/       RETRIEVE, UPDATE, DELETE
    """

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        if self.action in ["retrieve", "create"]:
            return [IsAuthenticated()]

        # Only allow the owner of the store to update and delete
        return [IsAuthenticated(), IsSeller(), IsStoreOwner()]

    def perform_create(self, serializer):
        """
        Create a new seller for a user
        """
        user = self.request.user
        # Check if the user is already a seller
        if user.role == "seller":
            raise serializers.ValidationError("User is already a seller and has a Store.")
        serializer.save(user_id=user)


# **Success
class StoreRetriveAuthView(generics.RetrieveAPIView):
    """
    - Authenticated:
        - RETRIEVE own store
    """

    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.store


class AddressViewSet(viewsets.ModelViewSet):
    """
    -   Customer:
        -   CREATE/UPDATE/DELETE/RETRIEVE/LISTS own address
            -   Notice: that user has access only on his own addresses
    - urls:
        -   `user/addresses/` LIST own user address
        -   `user/addreses/<uuid:pk>` CREATE/UPDATE/DELETE/RETRIEVE own user address
    """

    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only addresses belonging to the current user"""
        user = self.request.user
        return Address.objects.filter(user=user)

    def check_object_permissions(self, request, obj):
        """
        Check if the user is the owner of the address
        """
        if obj.user != self.request.user:
            raise PermissionDenied()

    def perform_create(self, serializer):
        """Set the current user as the owner of the address"""
        serializer.save(user=self.request.user)


class StoreAddressViewSet(viewsets.ModelViewSet):
    """
    -   Anyone:
        -   RETRIEVE/LIST stores addresses
    -   Vendor:
        -   CREATE/UPDATE/DELETE/RETRIEVE own store adress
    """

    # list++ retrieve++
    serializer_class = AddressSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated(), IsSeller()]

        return [IsAuthenticated(), IsSeller(), IsStoreOwner()]

    def get_queryset(self):
        queryset = Address.objects.filter(store__isnull=False)
        return queryset

    def perform_create(self, serializer):
        """
        Set the current store as the owner of the address
        Validate that the store address does not exist
        """
        store = Store.objects.get(user=self.request.user)
        address = Address.objects.get(store=store)

        # Check if the store already has an address
        if address:
            raise serializers.ValidationError("Store already has an address.")
        else:
            serializer.save(store=store, user=self.request.user)
