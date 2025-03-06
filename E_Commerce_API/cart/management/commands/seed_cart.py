from cart.models import Cart, CartItem
from django.core.management.base import BaseCommand
from products.models import Product
from users.models import CustomUser


class Command(BaseCommand):
    help = "Seed the database with initial cart data"

    def handle(self, *args, **kwargs):
        # Get user and product
        user = CustomUser.objects.filter(role="buyer").first()
        product = Product.objects.first()

        # Create cart
        cart = Cart.objects.create(user_id=user)

        # Create cart item
        CartItem.objects.create(cart_id=cart, product_id=product, cart_item_quantity=2)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database"))
