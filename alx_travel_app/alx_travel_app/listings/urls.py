from django.urls import path
from .views import booking_view

urlpatterns = [
    path("bookings/", booking_view, name="bookings")
]