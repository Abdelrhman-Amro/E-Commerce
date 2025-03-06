import uuid

from django.db import models
from django.db.models import Q


class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, null=False)

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
