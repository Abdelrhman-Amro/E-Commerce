from django.core.management.base import BaseCommand
from users.models import CustomUser, Seller


class Command(BaseCommand):
    help = "Seed the database with initial user data"

    def handle(self, *args, **kwargs):
        # Create users
        user1 = CustomUser.objects.create_user(
            email="buyer1@example.com",
            username="buyer1",
            password="password123",
            role="buyer",
        )
        user2 = CustomUser.objects.create_user(
            email="seller1@example.com",
            username="seller1",
            password="password123",
            role="seller",
        )

        # Create seller
        Seller.objects.create(
            user_id=user2,
            store_name="Seller One Store",
            contact_email="contact@seller1store.com",
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database"))
