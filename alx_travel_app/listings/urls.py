from django.urls import path, include
from .views import register, ProductViewSet, PaymentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register, name="register"),
    path("auth/", include("rest_framework.urls")),
    path("payment/<uuid:booking_pk>/", PaymentView.as_view(), name="payment")
]
