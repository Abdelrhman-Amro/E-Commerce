from rest_framework import serializers

from .models import CustomUser, Seller


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "role",
        ]
        write_only_fields = ["password"]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "password": {"required": True},
        }


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            "store_name",
            "contact_email",
            "description",
            "contact_phone",
            "address",
            "created_at",
        ]
        read_only_fields = ["created_at"]
        extra_kwargs = {
            "store_name": {"required": True},
            "contact_email": {"required": True},
        }
