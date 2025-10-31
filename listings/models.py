from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class BookingType(models.TextChoices):
    HOTEL = "HOTEL", "Hotel"
    FLIGHT = "FLIGHT", "Flight"
    PACKAGE = "PACKAGE", "Package"


class Status(models.TextChoices):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
 
class Bookings(models.Model):
    id = models.UUIDField(primary_key=True, null=False, max_length=40)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", default="rueooow-22-2929")
    bookings_type = models.CharField(max_length=10, choices=BookingType.choices, editable=False, default=BookingType.HOTEL)
    booking_date = models.DateField()
    status = models.CharField(max_length=200,choices=Status.choices, default=Status.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Booking by {self.user_id.username} --- {self.booking_type} ------ On {self.created_at}"


