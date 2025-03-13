from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from users.models import Address, Store

CustomUser = get_user_model()


class Command(BaseCommand):
    """
    - Create 8 users
        - 3 sellers[1:3]
        - 5 customers[4:8]

    - Create 3 stores 1 for each seller

    - Create 7 addresses
        - 3 addresses 1 for 3 customers[4, 5, 6]
        - 4 addresses 2 for 2 customers[7, 8]

    - Create 3 addresses 1 for each seller And store
    """

    help = "Creates test data with users, stores, and addresses"

    def handle(self, *args, **options):
        # Create 8 users (3 sellers [1-3], 5 customers [4-8])
        for i in range(1, 9):
            role = CustomUser.Role.SELLER if i <= 3 else CustomUser.Role.CUSTOMER
            user = CustomUser.objects.create_user(
                email=f"user{i}@example.com",
                username=f"user{i}",
                password="testgg44",
                role=role,
            )
            self.stdout.write(self.style.SUCCESS(f"Created {role}: {user.username}"))

        # Create 3 stores, one for each seller
        for i in range(1, 4):
            seller = CustomUser.objects.get(username=f"user{i}")
            store = Store.objects.create(user=seller, store_name=f"Store {i}")
            self.stdout.write(self.style.SUCCESS(f"Created store: {store.store_name}"))

        # Create 7 addresses for customers
        # 3 addresses for customers 4,5,6 (1 each)
        for i in range(4, 7):
            customer = CustomUser.objects.get(username=f"user{i}")
            address = Address.objects.create(
                user=customer,
                street_address=f"{i}00 Main St",
                country="USA",
                city=f"City {i}",
                postal_code=f"1000{i}",
            )
            self.stdout.write(self.style.SUCCESS(f"Created address for customer {i}"))

        # 4 addresses: 2 each for customers 7 and 8
        for i in range(7, 9):
            customer = CustomUser.objects.get(username=f"user{i}")
            for j in range(2):
                address = Address.objects.create(
                    user=customer,
                    street_address=f"{i}0{j} Main St",
                    country="USA",
                    city=f"City {i}",
                    postal_code=f"1000{i}{j}",
                )
                self.stdout.write(self.style.SUCCESS(f"Created address {j+1} for customer {i}"))

        # Create 3 addresses, one for each seller and their store
        for i in range(1, 4):
            seller = CustomUser.objects.get(username=f"user{i}")
            store = Store.objects.get(store_name=f"Store {i}")
            address = Address.objects.create(
                user=seller,
                store=store,
                street_address=f"{i}00 Store St",
                country="USA",
                city=f"Store City {i}",
                postal_code=f"2000{i}",
            )
            self.stdout.write(self.style.SUCCESS(f"Created store address for seller {i}"))

        self.stdout.write(self.style.SUCCESS("Successfully created all test data"))
