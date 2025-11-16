from django.urls import path, include
from .views import booking_view, register
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'bookings', BookingViewSets, basename="booking")

urlpatterns = [
    path("bookings/", booking_view, name="bookings"),
    path("register/", register, name="register"),
    path("auth/", include("rest_framework.urls"))
]
