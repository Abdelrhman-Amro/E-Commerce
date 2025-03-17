import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Order(models.Model):
    # Status choices
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PREPARING = "preparing", "Preparing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    # Default fields
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="orders")
    shipping_address = models.ForeignKey("users.Address", on_delete=models.PROTECT, related_name="orders")

    # Required fields
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, null=False, blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)

    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"

    def clean(self):

        if self.shipping_address.user != self.user:
            raise ValidationError("Shipping address doesn't belong to the user")

    def save(self, *args, **kwargs):
        """
        Ensure cleaning before saving
        """
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "order"
        verbose_name = "order"
        verbose_name_plural = "orders"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]


class OrderItem(models.Model):
    # Default fields
    order_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name="order_items")

    # Required fields
    order_item_quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(9999)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def clean(self):
        """
        Validate order items
        """
        # Extra check stock availability
        if self.order_item_quantity > self.product.stock_quantity:
            raise ValidationError(f"Quantity ({self.order_item_quantity}) exceeds available stock quatity ({self.product.stock_quantity})")

        # Ensure unit_price matches product price at order time
        if self.unit_price != self.product.price:
            raise ValidationError(f"Unit price ({self.unit_price}) doesn't match product price ({self.product.price})")

    def save(self, *args, **kwargs):
        """
        Ensure cleaning before saving
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_item_quantity} x {self.product.name} in Order {self.order.order_id}"

    class Meta:
        db_table = "order_item"
        verbose_name = "order item"
        verbose_name_plural = "order items"
        unique_together = [("order", "product")]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(order_item_quantity__gte=1), name="order_item_quantity_gte_1"),
            models.CheckConstraint(check=models.Q(unit_price__gt=0), name="unit_price_gt_0"),
        ]


class Payment(models.Model):
    # Status choices
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        REFUNDING = "refunding", "Refunding"
        REFUNDED = "refunded", "Refunded"

    # Default fields
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    order = models.OneToOneField("Order", on_delete=models.CASCADE, related_name="payment")

    # Required fields
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def clean(self):
        """Validate payment"""
        if self.amount != self.order.total_amount:
            raise ValidationError(f"Payment amount ({self.amount}) must match order total ({self.order.total_amount})")

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id}"

    class Meta:
        db_table = "payment"
        verbose_name = "payment"
        verbose_name_plural = "payments"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["status"]),
        ]
