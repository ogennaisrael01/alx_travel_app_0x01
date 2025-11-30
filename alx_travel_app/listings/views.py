from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import NotFound
from .models import Bookings
from .serializers import (
    BookingsOutSerializer, 
    BookingSerializer, 
    RegisterSerializer, 
    LoginSerializer,
    ProductCreateSerializer,
    ProductOutSerializer
)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from .models import Products
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50


@api_view(["POST"])
def register(request: Request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={
            "success":True,
            "message": "Registration successful",
            "user_id": serializer.data
        })

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProductVIewSet(viewsets.ModelViewSet):
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = []
    search_fields = []
    pagination_class = CustomPagination

    def check_object_permission(self, request: Request, product_obj):
        if product_obj.user != request.user:
            raise PermissionDenied("Permission denied: you can't perform this action")
        return True
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        product_obj = self.get_object()
        if self.check_object_permission(request, product_obj):
            serializer = self.get_serializer(product_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.validated_data) 
        

    def destroy(self, request, *args, **kwargs):
        product_obj = self.get_object()
        if self.check_object_permission(request, product_obj):
            self.perform_destroy(product_obj)  
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = Products.objects.prefetch_related("bookings", "reviews")
        if queryset is None:
            return Response(status=status.HTTP_200_OK, data="Queryset: []")
        
        serializer = ProductOutSerializer(queryset, many=True)
        return Response(serializer.data)