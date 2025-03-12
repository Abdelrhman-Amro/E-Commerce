# from rest_framework import serializers

# from .models import CustomUser, Seller


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = [
#             "email",
#             "username",
#             "password",
#             "first_name",
#             "last_name",
#             "role",
#         ]
#         # write_only_fields = [
#         #     "password",
#         # ] DEPRECATED
#         extra_kwargs = {
#             "email": {"required": True},
#             "username": {"required": True},
#             "password": {"required": True, "write_only": True},
#         }

#     def create(self, validated_data):
#         """
#         Create and return a new user
#         Hashing password before saving the user
#         """
#         password = validated_data.pop("password", None)  # Get and Remove password
#         instance = self.Meta.model(**validated_data)  # Create user instance
#         if password:
#             instance.set_password(password)  # Update instacne with Hashed password
#         instance.save()  # save user instance
#         return instance

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing user
#         Hashing password before saving user
#         """
#         password = validated_data.pop("password", None)  # Get and Remove password
#         if password:
#             instance.set_password(password)  # Update instacne with Hashed password
#         return super().update(instance, validated_data)


# class SellerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Seller
#         fields = [
#             "seller_id",
#             "store_name",
#             "contact_email",
#             "description",
#             "contact_phone",
#             "address",
#             "created_at",
#         ]
#         read_only_fields = ["created_at", "seller_id"]
#         extra_kwargs = {
#             "store_name": {"required": True},
#             "contact_email": {"required": True},
#         }
