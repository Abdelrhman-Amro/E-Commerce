from rest_framework import serializers

from .models import Address, CustomUser, Store


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Perform Create/Update/Delete/Retrieve operations
    """

    class Meta:
        model = CustomUser
        fields = [
            "user_id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "role",
            "date_joined",
        ]
        read_only_fields = ["role", "user_id", "date_joined"]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "password": {"required": True, "write_only": True},
        }

    def create(self, validated_data):
        """
        Create and return a new user
        Hashing password before saving the user
        """
        password = validated_data.pop("password", None)  # Get and Remove password
        instance = self.Meta.model(**validated_data)  # Create user instance
        if password:
            instance.set_password(password)  # Update instacne with Hashed password
        instance.save()  # save user instance
        return instance

    def update(self, instance, validated_data):
        """
        Update and return an existing user
        Hashing password before saving user
        """
        password = validated_data.pop("password", None)  # Get and Remove password
        if password:
            instance.set_password(password)  # Update instacne with Hashed password
        return super().update(instance, validated_data)


# create/update/delete/list/retrieve
class StoreSerializer(serializers.ModelSerializer):
    """
    Perform Create/Update/Delete/Retrieve/List operations
    """

    seller_name = serializers.SlugRelatedField(slug_field="username", read_only=True)
    seller_email = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Store
        fields = [
            "store_id",
            "user_id",
            "store_name",
            "seller_name",
            "seller_email",
            "description",
            "created_at",
        ]
        read_only_fields = ["created_at", "store_id", "user_id"]
        extra_kwargs = {
            "store_name": {"required": True},
            "user_id": {"required": True},
        }


class AddressSerializer(serializers.ModelSerializer):
    """
    Perform Create/Update/Delete/Retrieve/List operations
    """

    class Meta:
        model = Address
        fields = [
            "address_id",
            "user",
            "store",
            "street_address",
            "country",
            "city",
            "special_mark",
            "state",
            "postal_code",
            "created_at",
        ]
        read_only_fields = ["address_id", "created_at", "user", "store"]
        extra_kwargs = {
            "street_address": {"required": True},
            "country": {"required": True},
            "city": {"required": True},
        }
