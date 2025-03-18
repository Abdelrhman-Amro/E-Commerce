from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from users.models import Store
from users.permissions import IsSeller

from .filters import ProductFilter
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductRetrieveSerializer,
    ReviewSerializer,
    StoreProductSerializer,
)

CustomUser = get_user_model()


#############################################################
#################### Category Endpoints #####################
class CategoryViewSet(viewsets.ModelViewSet):
    """
    -   `Admin`
        -   CREATE/UPDATE/DELETE Categories
    -   `Anyone`
        -   RETRIEVE/LIST Categories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


#############################################################
#################### Product Endpoints ######################
class StoreProductViewSet(viewsets.ModelViewSet):
    """
    -   `Vendor`
        -   CREATE/UPDATE/DELETE/RETRIEVE/LIST own Products
    """

    queryset = Product.objects.all()
    serializer_class = StoreProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "quick_overview"]
    ordering_fields = ["price"]

    def get_queryset(self):
        store_id = Store.objects.get(user=self.request.user)
        return Product.objects.filter(store_id=store_id)

    def perform_create(self, serializer):
        store_id = Store.objects.get(user=self.request.user)
        serializer.save(store_id=store_id)


class ProductListView(ListAPIView):
    """
    -   `Anyone`
        -   LIST Products
    """

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "quick_overview", "store_id__store_name"]
    ordering_fields = ["price"]


class ProductRetrieveView(RetrieveAPIView):
    """
    -   `Anyone`
        -   RETRIEVE Products
    """

    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [AllowAny]


#############################################################
#################### Review Endpoints #######################
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["rating", "is_verified_purchase"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "delete"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        product_id = self.kwargs.get("product_pk")
        return Review.objects.filter(product=product_id)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if self.action in ["update", "partial_update", "delete"]:
            if obj.reviewer != self.request.user:
                self.permission_denied(self.request)

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_pk")
        product = Product.objects.get(product_id=product_id)
        serializer.save(reviewer=self.request.user, product=product)
