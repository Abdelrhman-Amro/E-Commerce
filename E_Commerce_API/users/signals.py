# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver

# from .models import CustomUser, Seller


# @receiver(post_save, sender=Seller)
# def update_user_role_to_seller(sender, instance, created, **kwargs):
#     """
#     After create seller, update user role to seller
#     """
#     if created:
#         user = instance.user_id
#         if user.role != "seller":
#             user.role = "seller"
#             user.save()


# @receiver(post_delete, sender=Seller)
# def update_user_role_to_buyer(sender, instance, **kwargs):
#     """
#     After delete seller, update user role to buyer
#     """
#     user = instance.user_id
#     if user.role == "seller":
#         user.role = "buyer"
#         user.save()
