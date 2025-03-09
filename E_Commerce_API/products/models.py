import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100, unique=True, null=False)
    category_image_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # Default fields
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    seller_id = models.ForeignKey("users.Seller", on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Required fields
    name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)

    # Optional fields
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gt=0), name="price_gt_0"),
            models.CheckConstraint(
                check=Q(stock_quantity__gte=0) & Q(stock_quantity__lte=9999),
                name="stock_quantity_gte_0",
            ),
        ]


class Review(models.Model):
    # Default fields
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="reviews"
    )

    # Required fields
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # Optional fields
    comment = models.TextField(null=True, blank=True)

    # is_verified_purchase = models.BooleanField(
    #     default=False, help_text="Indicates if reviewer purchased the product"
    # )

    def __str__(self):
        return f"{self.product.name} ({self.rating} stars)"

    class Meta:
        # Ensure one review per user per product
        constraints = [
            models.UniqueConstraint(
                fields=["product", "reviewer"], name="unique_product_reviewer"
            )
        ]
        # Default ordering for queries
        ordering = ["-created_at"]

        # Improve query performance
        #     indexes = [
        #         models.Index(fields=["product", "rating"]),
        #         models.Index(fields=["reviewer"]),
        #     ]

        # # Optional: Custom validation
        # def clean(self):
        #     """Additional validation if needed"""
        #     super().clean()
        #     if self.rating < 1 or self.rating > 5:
        #         raise ValidationError("Rating must be between 1 and 5")
