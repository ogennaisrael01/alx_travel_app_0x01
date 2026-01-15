from rest_framework import serializers
from .models import Bookings, Products, Reviews
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
        fields = [
            "booking_id", 
            "user", 
            "status",
            "bookings_type", 
            "start_date",
            "end_date", 
            "total_price", 
            "is_booked", 
            "created_at"
            ]

    def get_total_price(self, obj):
        """ get total price for each booking by multiplying the booking days to the price of the product"""
        duration_of_days = obj.start_date - obj.end_date
        number_of_days = duration_of_days.days
        price_per_night = float(obj.product.price_per_night)
        total_price = number_of_days * price_per_night 
        return total_price

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    product = serializers.ReadOnlyField(source="product.name")
    class Meta:
        model = Reviews   
        fields = [
            "review_id", 
            "user", 
            "product", 
            "ratings", 
            "message", 
            "created_at"
            ]
        read_only_fields = ["review_id", "user", "product", "created_at"] 

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            "product_id",
            "name", 
            "location", 
            "price_per_night", 
            "description", 
            "price"
            ]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("provide your property name")
        value.title()
        return value
    
class ProductOutSerializer(serializers.ModelSerializer):
    bookings = BookingsOutSerializer(read_only=True, many=True)
    user = serializers.ReadOnlyField(source="user.email")
    avg_ratings = serializers.SerializerMethodField()
    reviews = ReviewSerializer(read_only=True, many=True)
    class Meta:
        model = Products
        fields = [
            "product_id", 
            "user", 
            "name", 
            "location", 
            "description", 
            "price", 
            "price_per_night", 
            'created_at', 
            "bookings",
            "reviews",
            "avg_ratings"
            ]
    
    def get_avg_ratings(self, obj):
        reviews = obj.reviews.all()
        avg_ratings = 0
        total_sum = 0
        if not reviews:
            return avg_ratings
        for review in reviews:
            total_sum += review.ratings
        avg_ratings = total_sum / len(reviews)
        return avg_ratings


class PaymentSerializer(serializers.Serializer):
    pmt_choices = ["FULL_PAYMENT", "PAY_PERNIGHT"]
    pmt_size = serializers.ChoiceField(choices=pmt_choices, write_only=True, required=True)
  
    def validate(self, attrs):
        request = self.context.get("request")
        booking = self.context.get("booking")
        if getattr(booking, "user", None) != getattr(request, "user", None):
            raise serializers.ValidationError("You dont have access to perform this action")
        # if getattr(booking, "status") != Bookings.Status.CONFIRMED:
        #     raise serializers.ValidationError("You can only pay for confirmed bookings")
        return attrs
    
        
