from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

User = get_user_model()


class Cart(models.Model):
    # Default fields
    cart_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Relationships
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cart_id)


class CartItem(models.Model):
    # Default fields
    cart_item_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Relationships
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)  # M:1
    product_id = models.ForeignKey("products.Product", on_delete=models.CASCADE)  # M:1

    # Required fields
    cart_item_quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(cart_item_quantity__gt=0),
                name="cart_item_quantity_gt_0",
            ),
        ]

    def __str__(self):
        return str(self.cart_item_id)
