
import os
import django

# Tell Django where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from alx_travel_app.listings.models import Products, Reviews, Bookings
from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

def run():
    product = Products.objects.filter(name="Horton-Vasquez").first()
    reviews = product.reviews.all()
    if not reviews:
        return None
    print(reviews)

    print(connection.queries)


if __name__ == "__main__":
    run()