from django.core.management.base import BaseCommand
from ...models import CustomUser, Products, Bookings
from faker import Faker
from django.db import Q
import random
import string
import json
import uuid

class Command(BaseCommand):
    help = "Populate database with data"

    def generate_random_pass(self):
        chars = string.ascii_lowercase + "1234567890"
        return "".join(random.choice(chars) for _ in range(12))

    def handle(self, *args, **options):
        # Clear all data in db 
        faker = Faker()
        CustomUser.objects.all().delete()
        Products.objects.all().delete()
        Bookings.objects.all().delete()

        role_choices = ["HOST", 'ADMIN', 'GUEST']
        USER_SIZE = 100
        for i in range(USER_SIZE):   
            password = self.generate_random_pass()
            email = faker.email()
            name = faker.name()
            first_name = name.split(" ")[0]
            last_name  = name.split(" ")[1]
            if CustomUser.objects.filter(email=email).exists():
                self.stdout(f"{email} already exists" )
                pass
            self.stdout.write(f"seeding {email} data ....." )
            user = CustomUser.objects.create_user(
                user_id=uuid.uuid4(),
                email=email, 
                first_name=first_name,
                last_name=last_name,
                role = random.choice(role_choices),
                password=password
            )
            data = {
                "email": email,
                'password': password
            }
            with open("users_data.json", "a") as f:
                json.dump(data, f, indent=4)
        self.stdout.write("seeded users data")

        PRODUCT_SIZE = 1_000
        BATCHES = 100
        users = CustomUser.objects.filter(Q(role='ADMIN'), Q(role="HOST"))
        data = []
        for i in range(PRODUCT_SIZE):
            products  = Products(
                product_id=uuid.uuid4(),
                user=random.choice(users),
                name=faker.
            )

        

    
