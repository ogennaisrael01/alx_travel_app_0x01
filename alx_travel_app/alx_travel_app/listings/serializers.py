from rest_framework import serializers
from .models import Bookings

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ["bookings_type", "booking_date", "total_price"]

class BookingsOut(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ["id", "user_id", "status", "booking_type", "booking_date", "total_price", "is_booked", "created_at"]