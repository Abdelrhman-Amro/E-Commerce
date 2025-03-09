from django.core.management.base import BaseCommand
from users.models import CustomUser, Seller


class Command(BaseCommand):
    help = "Seed the database with initial user data"

    def handle(self, *args, **kwargs):
        data = []
        for i in range(10):
            data.append(
                {
                    "email": f"buyer{i}@example.com",
                    "username": f"buyer{i}",
                    "password": "testgg44",
                    "role": "buyer",
                }
            )
        CustomUser.objects.bulk_create(CustomUser(**user) for user in data)

        # fix password
        for user in CustomUser.objects.all():
            user.set_password(user.password)
            user.save()

        data = []
        CustomUsers = CustomUser.objects.all()

        for i in range(5):
            data.append(
                {
                    "store_name": f"store{i}",
                    "contact_email": f"store{i}@example.com",
                    "user_id": CustomUsers[i],
                }
            )
        Seller.objects.bulk_create(Seller(**user) for user in data)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database"))
