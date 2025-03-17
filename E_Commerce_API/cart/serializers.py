from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    item_total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["cart_item_id", "created_at", "updated_at", "cart", "product", "cart_item_quantity", "item_total_price"]
        read_only_fields = ["cart_item_id", "created_at", "updated_at", "cart"]
        extra_kwargs = {
            "cart": {"required": True},
            "product": {"required": True},
        }

    def get_item_total_price(self, obj):
        return obj.item_total_price()


class CartSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["cart_id", "created_at", "updated_at", "user", "total_amount", "items"]
        read_only_fields = ["cart_id", "created_at", "updated_at", "user"]

    def get_total_amount(self, obj):
        return obj.total_amount()
