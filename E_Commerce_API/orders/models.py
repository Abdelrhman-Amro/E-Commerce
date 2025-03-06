from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

User = get_user_model()


class Order(models.Model):
    # Order status choices
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    # Default fields
    order_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # M:1

    # Required fields
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    order_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_amount__gt=0), name="total_amount_gt_0"
            ),
        ]

    def __str__(self):
        return str(self.order_id)


class OrderItem(models.Model):
    # Default fields
    order_item_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Relationships
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)  # M:1
    product_id = models.ForeignKey("products.Product", on_delete=models.CASCADE)  # M:1

    # Required fields
    order_item_quantity = models.IntegerField()
    order_item_total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(order_item_quantity__gt=0),
                name="order_item_quantity_gt_0",
            ),
            models.CheckConstraint(
                check=models.Q(order_item_total_price__gt=0),
                name="order_item_total_price_gte_0",
            ),
        ]

    def __str__(self):
        return str(self.order_item_id)
