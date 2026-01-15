from rest_framework.decorators import api_view
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Bookings
from .serializers import (
    BookingsOutSerializer, 
    BookingSerializer, 
    RegisterSerializer, 
    LoginSerializer,
    ProductCreateSerializer,
    ProductOutSerializer,
    PaymentSerializer, 
)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from .models import Products, Payments
from rest_framework.pagination import CursorPagination
import secrets
from .helpers import get_booking_by_id
from .payments import payment_init

class CustomPagination(CursorPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50
    ordering = ["-created_at"]


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


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["bookings__user"]
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
            serializer.save()
            return Response(serializer.validated_data) 
        

    def destroy(self, request, *args, **kwargs):
        product_obj = self.get_object()
        if self.check_object_permission(request, product_obj):
            self.perform_destroy(product_obj)  
        return Response(status=status.HTTP_204_NO_CONTENT)

    queryset = (
        Products.objects.select_related(
            "user"
        ).prefetch_related(
            "bookings", "reviews"
        )
    )
    def get_queryset(self):
        return self.queryset.all().order_by("-created_at")
    
    def get_serializer_class(self):
        if self.action in ("create", "update", "patch", "destroy"):
            return ProductCreateSerializer
        return ProductOutSerializer
    
class PaymentView(APIView):
    http_method_names = ["post"]

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_pk=None):
        booking_dict = get_booking_by_id(booking_pk)

        if booking_dict.get("status") == "success":
            booking = booking_dict.get("booking")

        print(booking.user, request.user)
        serializer = self.serializer_class(data=request.data, context={"request": request, "booking": booking})
        serializer.is_valid(raise_exception=True)
        pmt_ref = secrets.token_urlsafe(30)
        email = request.user.email
        first_name = request.user.first_name if request.user.first_name else email[:5]
        last_name = request.user.last_name if request.user.last_name else email[5:]
        phone = request.user.phone_number if request.user.phone_number else None
        amount = 0
        pmt_choices = ["FULL_PAYMENT", "PAY_PERNIGHT"]
        pmt_size = serializer.validated_data.get("pmt_size")
        if pmt_size == pmt_choices[0]:
            amount = float(booking.product.price)
        elif pmt_size == pmt_choices[1]:
            amount = float(booking.product.price_per_night)
        else:
            amount = None
            raise NotFound("amount not  provided")
        try:
            initiate_payment = payment_init(
                email=email, 
                amount=amount,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                pmt_ref=pmt_ref
            )
        except Exception:
            raise

        return Response(initiate_payment, status=status.HTTP_200_OK)



        