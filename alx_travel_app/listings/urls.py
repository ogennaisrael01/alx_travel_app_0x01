from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings.views import ListingViewSet, BookingVIewSet
# Register your urls here

router = DefaultRouter()
router.register(r'listing', ListingViewSet)
router.register(r'booking', BookingVIewSet)

urlpatterns = [
    path('', include(router.urls))
]