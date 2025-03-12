# from rest_framework import serializers

# from .models import Category, Product, Review


# class CategorySerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Category model.
#     Handles CRUD operations for product categories.
#     """

#     class Meta:
#         model = Category
#         fields = ["category_id", "name", "category_image_url"]
#         read_only_fields = ["category_id"]


# class ProductSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Product model.
#     Handles CRUD operations for products with validation.
#     """

#     # Get category name for display rather than just ID
#     category_name = serializers.StringRelatedField(source="category_id", read_only=True)

#     class Meta:
#         model = Product
#         fields = [
#             "product_id",
#             "name",
#             "description",
#             "price",
#             "stock_quantity",
#             "image_url",
#             "seller_id",
#             "category_id",
#             "category_name",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["product_id", "created_at", "updated_at"]

#     def validate_price(self, value):
#         """
#         Validate that the price is greater than zero.
#         """
#         if value <= 0:
#             raise serializers.ValidationError("Price must be greater than zero.")
#         return value

#     def validate_stock_quantity(self, value):
#         """
#         Validate that stock quantity is between 0 and 9999.
#         """
#         if value < 0 or value > 9999:
#             raise serializers.ValidationError(
#                 "Stock quantity must be between 0 and 9999."
#             )
#         return value


# class ReviewSerializer(serializers.ModelSerializer):
#     """
#     Serializer for Review model providing full detail representation
#     Handles CRUD operations for reviews with validations
#     """

#     reviewer_username = serializers.CharField(
#         source="reviewer.username", read_only=True
#     )

#     class Meta:
#         model = Review
#         fields = [
#             "review_id",
#             "product",
#             "reviewer",
#             "reviewer_username",
#             "rating",
#             "comment",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = [
#             "review_id",
#             "reviewer",
#             "created_at",
#             "updated_at",
#             "reviewer_username",
#         ]

#     def validate_rating(self, value):
#         """
#         Validate that rating is between 1 and 5
#         """
#         if value < 1 or value > 5:
#             raise serializers.ValidationError("Rating must be between 1 and 5")
#         return value

#     # def validate(self, data):
#     #     """
#     #     Check if user has already reviewed this product
#     #     """
#     #     if self.context["request"].method == "POST":
#     #         reviewer = data.get("reviewer")
#     #         product = data.get("product")

#     #     # # Seller can't review his product
#     #     # if hasattr(product, "seller_id") and product.seller_id == reviewer:
#     #     #     raise serializers.ValidationError("You cannot review your own product")

#     #     # Can't review same product twice
#     #     if Review.objects.filter(reviewer=reviewer, product=product).exists():
#     #         raise serializers.ValidationError("You have already reviewed this product")
#     #     return data


# class ReviewListSerializer(serializers.ModelSerializer):
#     """
#     Serializer optimized for listing reviews
#     Reduces payload size for better performance
#     """

#     reviewer_username = serializers.CharField(
#         source="reviewer.username", read_only=True
#     )
#     product_name = serializers.CharField(source="product.name", read_only=True)

#     class Meta:
#         model = Review
#         fields = [
#             "review_id",
#             "product_name",
#             "reviewer_username",
#             "rating",
#             "comment",
#             "created_at",
#         ]
