from django.core.management.base import BaseCommand
from orders.models import Order, OrderItem
from products.models import Product
from users.models import CustomUser


class Command(BaseCommand):
    help = "Seed the database with initial order data"

    def handle(self, *args, **kwargs):
        # Get user and products
        user = CustomUser.objects.filter(role="buyer").first()
        product1 = Product.objects.first()
        product2 = Product.objects.last()

        # Create order
        order = Order.objects.create(
            user_id=user,
            total_amount=product1.price + product2.price,
            order_status="pending",
        )

        # Create order items
        OrderItem.objects.create(
            order_id=order,
            product_id=product1,
            order_item_quantity=1,
            order_item_total_price=product1.price,
        )
        OrderItem.objects.create(
            order_id=order,
            product_id=product2,
            order_item_quantity=1,
            order_item_total_price=product2.price,
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database"))
