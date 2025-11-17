
import os
import django

# Tell Django where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from alx_travel_app.listings.models import Products, Reviews
from django.db import connection

def run():
    product = Products.objects.get(name="Taylor-Elliott")
    reviews = product.reviews.all()
    total = 0
    total_len = len(reviews)
    for review in reviews:
        total += review.ratings
    print(f"avg = {total / total_len}" )

    print(connection.queries)


if __name__ == "__main__":
    run()