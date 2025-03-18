import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Category(models.Model):
    # Default fields
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Required fields
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"


class Product(models.Model):
    # Default fields
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    store_id = models.ForeignKey("users.Store", on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    # Required fields
    name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.00)])
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])

    # Optional fields
    quick_overview = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product"
        verbose_name = "product"
        verbose_name_plural = "products"
        constraints = [
            models.CheckConstraint(check=models.Q(price__gt=0), name="price_gt_0"),
            models.CheckConstraint(check=Q(stock_quantity__gte=0) & Q(stock_quantity__lte=9999), name="stock_quantity_gte_0"),
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["store_id"]),
            models.Index(fields=["category_id"]),
        ]


class Review(models.Model):
    # Default fields
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_reviews")
    reviewer = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="user_reviews")

    # Required fields
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Optional fields
    comment_title = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} ({self.rating} stars)"

    class Meta:
        db_table = "review"
        verbose_name = "review"
        verbose_name_plural = "reviews"

        ordering = ("-created_at",)
        unique_together = [("product", "reviewer")]  # Ensure a user can only review a product once
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name="rating_range_1_to_5"),
        ]

        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product", "rating"]),
            models.Index(fields=["is_verified_purchase"]),
            models.Index(fields=["reviewer"]),
        ]
