from django.core.management.base import BaseCommand
from products.models import Category, Product
from users.models import Seller


class Command(BaseCommand):
    help = "Seed the database with initial product data"

    def handle(self, *args, **kwargs):
        # Create categories
        category1 = Category.objects.create(name="Electronics")
        category2 = Category.objects.create(name="Books")

        # Get seller
        seller = Seller.objects.first()

        # Create products
        Product.objects.create(
            name="Smartphone",
            price=699.99,
            stock_quantity=50,
            category_id=category1,
            seller_id=seller,
        )
        Product.objects.create(
            name="Laptop",
            price=999.99,
            stock_quantity=30,
            category_id=category1,
            seller_id=seller,
        )
        Product.objects.create(
            name="Fiction Book",
            price=19.99,
            stock_quantity=100,
            category_id=category2,
            seller_id=seller,
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database"))
