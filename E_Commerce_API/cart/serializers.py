from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["cart_item_id", "created_at", "updated_at", "cart"]
        extra_kwargs = {
            "cart": {"required": True},
            "product": {"required": True},
        }
