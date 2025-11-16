from django.urls import path, include
from .views import booking_view, register

urlpatterns = [
    path("bookings/", booking_view, name="bookings"),
    path("register/", register, name="register"),
    path("auth/", include("rest_framework.urls"))
]