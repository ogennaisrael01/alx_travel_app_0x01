from rest_framework import serializers
from .models import Bookings
from django.contrib.auth.password_validation import validate_password
import email_validator
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=50,
     write_only=True,
     required=True,
     error_messages={
        "blank": "password cannot be empty",
        "required": "please provide your password"
     })
    email = serializers.EmailField(max_length=200)
    
    def validate_email(self, value:str):
        email =value.lower()
        try:
            valid_email = email_validator.validate_email(email, check_deliverability=True)
        except email_validator.EmailNotValidError as e:
            raise serializers.ValidationError("Email not valid")
        if User.objects.filter(email=valid_email, is_active=True).exists():
            raise serializers.ValidationError("user with this email already exists")
        return valid_email.normalized

    def validate(self, attrs):
        if attrs["password"] and attrs["password"] not in attrs["username"]:
            validate_password(attrs["password"])

            return attrs
        raise serializers.ValidationError("Error occured while validating password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=50)
    
    def validate_password(self, value: str):
        ...


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ["bookings_type", "booking_date", "total_price"]

class BookingsOut(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ["id", "user_id", "status", "booking_type", "booking_date", "total_price", "is_booked", "created_at"]