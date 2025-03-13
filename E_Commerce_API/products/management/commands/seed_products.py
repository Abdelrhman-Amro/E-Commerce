from django.core.management.base import BaseCommand
from products.models import Category, Product, Review
from users.models import CustomUser, Seller


class Command(BaseCommand):
    """
    create 5 categoreis

    create 9 products 3 for each store
    create 3 products 1 for each store without category

    create 10 reviewes 2 by each customer
    create 6 reviewes 2 by each seller
    """

    help = "Seed the database with initial product data"

    def handle(self, *args, **kwargs):

        catgories = []
        for i in range(8):
            catgories.append(
                {
                    "name": f"Category-{i}",
                }
            )
        Category.objects.bulk_create(Category(**category) for category in catgories)

        sellers_objs = Seller.objects.all()
        categories_objs = Category.objects.all()
        print(sellers_objs.count())
        products = []
        for i in range(100):
            # seller1[20], seller2[20], seller3[20], seller4[20], seller5[20]
            products.append(
                {
                    "name": f"Product-{i}",
                    "price": 100.00,
                    "stock_quantity": 100,
                    "seller_id": sellers_objs[((i // 20) % 5)],  # ((start / group) % range)
                    "category_id": categories_objs[i % 8],
                }
            )

        Product.objects.bulk_create(Product(**product) for product in products)

        reviews = []
        buyers_objs = CustomUser.objects.filter(role="buyer")
        products = Product.objects.all()
        for i in range(100):
            reviews.append(
                {
                    "rating": 5,
                    "comment": "Good",
                    "product": products[i],
                    "reviewer": buyers_objs[i % 10],
                }
            )
        for i in range(99):
            reviews.append(
                {
                    "rating": 2,
                    "comment": "Bad",
                    "product": products[i + 1],
                    "reviewer": buyers_objs[i % 10],
                }
            )
        Review.objects.bulk_create(Review(**review) for review in reviews)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database"))
