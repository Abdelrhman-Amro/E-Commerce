from cart.models import Cart
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import CustomUser, Store


@receiver(post_save, sender=Store)
def update_user_role_to_seller(sender, instance, created, **kwargs):
    """
    After create store, update user role to seller
    """

    if created:
        user = instance.user
        if user.role != "seller":
            user.role = "seller"
            user.save()


@receiver(post_delete, sender=Store)
def update_user_role_to_buyer(sender, instance, **kwargs):
    """
    After delete store, update user role to buyer
    """

    user = instance.user
    if user.role == "seller":
        user.role = "buyer"
        user.save()


@receiver(post_save, sender=CustomUser)
def create_cart_opject_user(sender, instance, created, **kwargs):
    """
    After create user, create cart object
    """

    if created:
        Cart.objects.create(user=instance)
