from django.urls import path, include
from .views import register, ProductVIewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"products", ProductVIewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register, name="register"),
    path("auth/", include("rest_framework.urls"))
]
