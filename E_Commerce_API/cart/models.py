from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Cart(models.Model):
    # Default fields
    cart_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="carts",
    )

    def total_amount(self):
        """
        Calculate total amount of cart items
        """
        return sum([item.product.price * item.cart_item_quantity for item in self.items.all()])

    def __str__(self):
        return f"Cart {self.cart_id} for {self.user.username}"

    class Meta:
        db_table = "cart"
        verbose_name = "cart"
        verbose_name_plural = "carts"


class CartItem(models.Model):
    # Default fields
    cart_item_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="cart_items")

    # Required fields
    cart_item_quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.cart_item_quantity} x {self.product.name} in Cart {self.cart.cart_id}"

    def item_total_price(self):
        """
        Calculate total price of cart item
        """
        return self.product.price * self.cart_item_quantity

    def clean(self):
        """
        Ensure quantity does not exceed available stock and cart is active.
        """
        if self.cart_item_quantity > self.product.stock_quantity:
            raise ValidationError(f"Quantity ({self.cart_item_quantity}) exceeds available stock quantity ({self.product.stock_quantity})")

    def save(self, *args, **kwargs):
        """
        Enure clening before saving
        """
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "cart_item"
        verbose_name = "cart item"
        verbose_name_plural = "cart items"
        unique_together = [("cart", "product")]
        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["product"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(cart_item_quantity__gte=1), name="cart_item_quantity_gte_1"),
        ]
