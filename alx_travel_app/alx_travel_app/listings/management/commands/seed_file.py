from django.core.management.base import BaseCommand
from ...models import CustomUser, Products, Bookings
from faker import Faker
from django.db.models import Q
import random
import string
import json
import uuid
import re


class Command(BaseCommand):
    help = "Populate database with data"

    def generate_random_pass(self):
        chars = string.ascii_lowercase + "1234567890"
        return "".join(random.choice(chars) for _ in range(12))

    def handle(self, *args, **options):
        faker = Faker()
        # Clear all data in db 
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
        users = CustomUser.objects.filter(Q(role='ADMIN') | Q(role="HOST"))
        data = []
        for i in range(PRODUCT_SIZE):
            self.stdout.write(f"seeding {i+1} product data....")
            price = faker.random_int(min=100_000, max=1_000_000)
            products  = Products(
                product_id=uuid.uuid4(),
                user=random.choice(users),
                name=faker.company(),
                description=faker.text()[:30],
                location=faker.address(),
                price_per_night=price / 10,
                price=price
            )

            data.append(products)
            if len(data) == BATCHES:
                self.stdout.write(F"SEEDING {BATCHES} DATA .....")
                Products.objects.bulk_create(data)
                data.clear()
        
        if len(data) > 0:
            self.stdout.write(f"SEEDING REMAINS {len(data)} DATA....")
            Products.objects.bulk_create(data)
        data.clear()
        self.stdout.write("Seeded product data")

        BOOKING_TYPE = ['HOTEL', 'FLIGHT', 'PACKAGE']
        STATUS = ['PENDING', "CONFIRMED", "CANCELLED"]
        BOOKING_SIZE = 2_000
        CREATE_BATCH = 200
        BOOKING_DATA = []
        products = Products.objects.all()
        users = CustomUser.objects.all()
        for i in range(BOOKING_SIZE):
            self.stdout.write(f"Seeding {i+1} booking data....")
            bookings = Bookings(
                booking_id=uuid.uuid4(),
                product=random.choice(products),
                user=random.choice(users),
                bookings_type=random.choice(BOOKING_TYPE),
                start_date=faker.date_between(start_date="now", end_date="+30d"),
                end_date=faker.date_between(start_date="now", end_date="+30d"),
                status=random.choice(STATUS),
                is_booked=faker.boolean(chance_of_getting_true=50)


            )
            BOOKING_DATA.append(bookings)
            if len(BOOKING_DATA) == CREATE_BATCH:
                self.stdout.write(f"SEDING {len(BOOKING_DATA)} BOOKING DATA ....")
                Bookings.objects.bulk_create(BOOKING_DATA)
                BOOKING_DATA.clear()
        if len(BOOKING_DATA) > 0:
            self.stdout.write(F"SEEDING {len(BOOKING_DATA)} BOOKING DATA....")
            Bookings.bulk_create(BOOKING_DATA)
            BOOKING_DATA.clear()

        self.stdout.write('SUCCESSFULLY POPULATED THE DB WITH SAMPLE DATA.')




            

        

    
