import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    # role choices
    class Role(models.TextChoices):
        SELLER = "seller", "Seller"
        CUSTOMER = "customer", "Customer"

    # Override fields
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    # Extra fields
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)

    # Authentication fields
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        db_table = "customuser"
        verbose_name = "customuser"
        verbose_name_plural = "customusers"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
        ]


class Store(models.Model):
    # Default fields
    store_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="store")

    # Required fields
    store_name = models.CharField(max_length=100, unique=True)

    # Optional fields
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.store_name

    class Meta:
        db_table = "store"
        verbose_name = "store"
        verbose_name_plural = "stores"
        indexes = [
            models.Index(fields=["store_name"]),
        ]


class Address(models.Model):

    # Default fields
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    # Both can be null as an address might belong to either a user or store
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True)

    # Required fields
    street_address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Optional fields
    special_mark = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street_address}"

    def clean(self):
        """
        Ensure that either user or store is set
        """
        if self.user is None and self.store is None:
            raise ValidationError("Address must set at least to user or store")

    def save(self, *args, **kwargs):
        """
        Ensure cleaning before saving
        """
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "address"
        verbose_name = "address"
        verbose_name_plural = "addresses"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["store"]),
        ]
