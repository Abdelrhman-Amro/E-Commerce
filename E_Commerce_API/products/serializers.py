from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Handles CRUD operations for product categories.
    """

    class Meta:
        model = Category
        fields = ["category_id", "name"]
        read_only_fields = ["category_id"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Handles CRUD operations for products with validation.
    """

    # Get category name for display rather than just ID
    category_name = serializers.StringRelatedField(source="category_id", read_only=True)

    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "description",
            "price",
            "stock_quantity",
            "image_url",
            "seller_id",
            "category_id",
            "category_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["product_id", "created_at", "updated_at"]

    def validate_price(self, value):
        """
        Validate that the price is greater than zero.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock_quantity(self, value):
        """
        Validate that stock quantity is between 0 and 9999.
        """
        if value < 0 or value > 9999:
            raise serializers.ValidationError(
                "Stock quantity must be between 0 and 9999."
            )
        return value


class ProductListSerializer(ProductSerializer):
    """
    Simplified serializer for listing products,
    with fewer fields for better performance.
    """

    class Meta(ProductSerializer.Meta):
        fields = ["product_id", "name", "price", "image_url", "category_name"]


class ProductDetailSerializer(ProductSerializer):
    """
    Detailed serializer for retrieving a single product.
    Includes additional information about the seller.
    """

    seller = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        # Include all fields from the parent plus the seller info
        pass

    def get_seller(self, obj):
        """
        Get the seller's store name and contact details.
        """
        return {
            "store_name": obj.seller_id.store_name,
            "contact_email": obj.seller_id.contact_email,
        }
