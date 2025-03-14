from rest_framework import serializers

from .models import Category, Product, Review


##############################################################
#################### Category Serializers ####################
class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer for full CRUD operations
    """

    class Meta:
        model = Category
        fields = ["category_id", "name", "created_at"]
        read_only_fields = ["category_id", "name", "created_at"]


#############################################################
#################### Product Serializers ####################
class StoreProductSerializer(serializers.ModelSerializer):
    """
    Displays full product details
    """

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["product_id", "created_at", "updated_at", "store_id"]
        extra_kwargs = {
            "name": {"required": True},
            "price": {"required": True},
            "stock_quantity": {"required": True},
        }


class ProductListSerializer(serializers.ModelSerializer):
    """
    Display only the essential product details
    Reduces payload size for better performance
    """

    category_name = serializers.StringRelatedField(source="category_id", read_only=True)
    store_name = serializers.StringRelatedField(source="store_id", read_only=True)
    store_country = serializers.SerializerMethodField()
    store_city = serializers.SerializerMethodField()

    def get_store_country(self, obj):
        """Get the country from the store's address if it exists"""
        if hasattr(obj.store_id, "addresses") and obj.store_id.addresses:
            return obj.store_id.addresses.country
        return None

    def get_store_city(self, obj):
        """Get the city from the store's address if it exists"""
        if hasattr(obj.store_id, "addresses") and obj.store_id.addresses:
            return obj.store_id.addresses.city
        return None

    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "quick_overview",
            "price",
            "stock_quantity",
            "image_url",
            "store_id",
            "store_name",
            "store_country",
            "store_city",
            "category_id",
            "category_name",
        ]


class ProductRetrieveSerializer(serializers.ModelSerializer):
    """
    Provides full detail representation of a product
    """

    category_name = serializers.StringRelatedField(source="category_id", read_only=True)
    store_name = serializers.StringRelatedField(source="store_id", read_only=True)

    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "quick_overview",
            "price",
            "stock_quantity",
            "image_url",
            "store_id",
            "store_name",
            "category_id",
            "category_name",
            "description",
            "created_at",
            "updated_at",
        ]


#############################################################
#################### Review Serializers #####################
class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model providing full detail representation
    Handles CRUD operations for reviews with validations
    """

    reviewer_username = serializers.CharField(source="reviewer.username", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = [
            "review_id",
            "created_at",
            "updated_at",
            "reviewer",
            "reviewer_username",
            "product",
        ]
        extra_kwargs = {
            "rating": {"required": True},
        }

    def validate_rating(self, value):
        """
        Validate that rating is between 1 and 5
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    # def validate(self, data):
    #     """
    #     Check if user has already reviewed this product
    #     """
    #     if self.context["request"].method == "POST":
    #         reviewer = data.get("reviewer")
    #         product = data.get("product")

    #     # # Seller can't review his product
    #     # if hasattr(product, "seller_id") and product.seller_id == reviewer:
    #     #     raise serializers.ValidationError("You cannot review your own product")

    #     # Can't review same product twice
    #     if Review.objects.filter(reviewer=reviewer, product=product).exists():
    #         raise serializers.ValidationError("You have already reviewed this product")
    #     return data
