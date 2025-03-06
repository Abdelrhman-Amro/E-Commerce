import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # role choices
    class Role(models.TextChoices):
        SELLER = "seller", "Seller"
        BUYER = "buyer", "Buyer"

    # override fields
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)

    # extra fields
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.BUYER,
        null=False,
        blank=False,
    )

    # field used for authentication
    USERNAME_FIELD = "email"

    # required fields for creating a user
    REQUIRED_FIELDS = ["username", "role"]

    def __str__(self):
        return self.username

    class Meta:
        db_table = "customuser"
        verbose_name = "customuser"
        verbose_name_plural = "customusers"


class Seller(models.Model):
    seller_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Required fields
    store_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    contact_email = models.EmailField(
        null=False, blank=False, unique=True, max_length=100
    )

    # Optional fields
    description = models.TextField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    # Relationships
    user_id = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="seller"
    )

    def __str__(self):
        return self.store_name

    class Meta:
        db_table = "seller"
        verbose_name = "seller"
        verbose_name_plural = "sellers"
