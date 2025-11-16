from rest_framework import serializers
from .models import Bookings, Products
from django.contrib.auth.password_validation import validate_password
import email_validator
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=50,
     write_only=True,
     required=True,
     error_messages={
        "blank": "password cannot be empty",
        "required": "please provide your password"
     })
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=100)
    role = serializers.ChoiceField(choices=["HOST", "ADMIN", "GUEST"])
    
    def validate_email(self, value:str):
        email =value.lower()
        try:
            valid_email = email_validator.validate_email(email, check_deliverability=True)
        except email_validator.EmailNotValidError as e:
            raise serializers.ValidationError("Email not valid")
        if User.objects.filter(email=valid_email, is_active=True).exists():
            raise serializers.ValidationError("user with this email already exists")
        return valid_email.normalized

    def validate_password(self, value):
        if not value:
             raise serializers.ValidationError("Error occured while validating password")
        validate_password(value)
        return value
       

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        return user
        
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=50)
    
    def validate_password(self, value: str):
        ...


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ["bookings_type", "start_date", "end_date"]

    def validate(self, attrs):
        start_date = attrs["start_date"]
        end_date = attrs["end_date"]

        if start_date < timezone.now().date():
            raise serializers.ValidationError("start date can't be less than today")
        if end_date <= start_date:
            raise serializers.ValidationError("end date can't be less than or equal to today")

        return attrs

class BookingsOutSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source="user.email")
    class Meta:
        model = Bookings
        fields = ["id", "user", "status", "booking_type", "start_date","end_date", "total_price", "is_booked", "created_at"]

    def get_total_price(self, obj):
        """ get total price for each booking by multiplying the booking days to the price of the product"""
        total_days = obj.start_date - obj.end_date
        total_price = total_days * obj.products.price_per_night
        return total_price
    

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["name", "location", "price_per_night", "description", "price"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("provide your property name")
        value.title()
        return value
    
class ProductOutSerializer(serializers.ModelSerializer):
    bookings = BookingsOutSerializer()
    user = serializers.ReadOnlyField(source="user.email")
    class Meta:
        model = Products
        fields = ["product_id", "user", "name", "location", "description", "price", "price_per_night", 'created_at', "bookings"]