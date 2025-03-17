from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class RetrieveCart(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Get auth-user Cart with full details
        """
        queryset = self.get_queryset()
        obj = queryset.get(user=self.request.user)
        return obj


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get auth-user CartItems
        """
        cart = Cart.objects.get(user=self.request.user)
        queryset = CartItem.objects.filter(cart=cart)
        return queryset

    def perform_create(self, serializer):
        """
        Add CartItems to auth-user Cart
        """
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)
