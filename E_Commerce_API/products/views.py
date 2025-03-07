from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from users.models import Seller
from users.permissions import IsSeller

from .filters import ProductFilter
from .models import Category, Product
from .pagination import ProductPagination
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Allow admin users to perform CRUD operations on categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


class SellerProductViewSet(viewsets.ModelViewSet):
    """
    Allow sellers to perform CRUD operations on their products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        seller_id = Seller.objects.get(user_id=self.request.user)
        return self.queryset.filter(seller_id=seller_id)


class ProductListView(ListAPIView):
    """
    Allow anyone to list all products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    pagination_class = ProductPagination


class ProductRetrieveView(RetrieveAPIView):
    """
    Allow anyone to retrieve a single product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
