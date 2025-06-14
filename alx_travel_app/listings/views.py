from django.shortcuts import render
from listings.models import Listing, Booking
from rest_framework import viewsets
from .serializers import ListingSerializer, BookingSerializer
# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingVIewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer