from rest_framework import serializers
from .models import Listing, Booking
# Create your serializers here 

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["listing_id", "host", "name"]

class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ["booking_id", "listing", "total_price", "status"]

