from django.db import models
from django.contrib.auth.models import BaseUserManager,  AbstractBaseUser
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please provide your email")
        if not password:
            raise ValueError("please provide your password")
        
        valid_email = self.normalize_email(email)
        user = self.model(email=valid_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields["is_superuser"] != True:
            raise ValueError("An admin user must have is super user set to True")
        if extra_fields["is_staff"] != True:
            raise ValueError("an admin user must have is_staff field set to true")
        user = self.create_user(email=email, password=password, **extra_fields)
        return user
    
class CustomUser(AbstractBaseUser):
    class RoleChoices(models.TextChoices):
        HOST = 'HOST', 'Host'
        ADMIN = 'ADMIN', 'Admin'
        GUEST = 'GUEST', 'Guest'
    
    user_id = models.UUIDField(max_length=20, unique=True, primary_key=True, default=uuid.uuid4())
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number  = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.GUEST)

    objects = CustomUserManager()
    REQUIRED_FIELDS = ['role', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'custom user'
        db_table = 'users'
        indexes = [
            models.Index(fields=['user_id'], name='id_idx'),
            models.Index(fields=["email"], name="email_idx"),
            models.Index(fields=["role"], name="role_idx"),
        ]

    def __str__(self):
        return f"{self.email} ====== {self.role}"

    @property
    def is_admin(self) -> bool:
        return self.is_superuser

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Products(models.Model):
    product_id = models.UUIDField(max_length=20, primary_key=True, null=False, unique=True, db_index=True, default=uuid.uuid4())
    name = models.CharField(max_length=100, null=False,  db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")
    location = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} === {self.name} === {self.price}"

    class Meta:
        ordering = ["-created_at"]
        db_table = 'products'
        verbose_name_plural = 'products'

class Bookings(models.Model):
    class BookingType(models.TextChoices):
        HOTEL = "HOTEL", "Hotel"
        FLIGHT = "FLIGHT", "Flight"
        PACKAGE = "PACKAGE", "Package"


    class Status(models.TextChoices):
        PENDING ="PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
 
    booking_id = models.UUIDField(primary_key=True, null=False, max_length=20, unique=True, db_index=True, default=uuid.uuid4())
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    bookings_type = models.CharField(max_length=10, choices=BookingType.choices, editable=False, default=BookingType.HOTEL)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=200,choices=Status.choices, default=Status.PENDING)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Booking by {self.user.email} ==== {self.bookings_type}"

    class Meta:
        verbose_name = 'booking'
        db_table = "bookings"


class Reviews(models.Model):
    review_id = models.UUIDField(
        primary_key=True,
        db_index=True,
        null=False,
        unique=True,
        max_length=20,
        default=uuid.uuid4()
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    ratings = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, "Ratings can't be less than 1"),
            MaxValueValidator(5, "Ratings can't be greater than 5")
            ]

            )
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} === {self.product.name} === {self.ratings}"
    
    class Meta:
        ordering = ["-created_at"]
        db_table = "reviews"
        verbose_name = "Reviews"
