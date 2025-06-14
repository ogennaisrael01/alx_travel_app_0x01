from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

# User model for hosts and guests
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    first_name = models.CharField(max_length=64)  
    last_name = models.CharField(max_length=64)   
    email = models.CharField(max_length=64, unique=True, null=False)  
    username = models.CharField(max_length=64, null=False) 
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"{self.username} ({self.email})"

# Listing model for properties
class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")    
    name = models.CharField(max_length=100, null=False)         
    description = models.TextField(null=False)                   
    location = models.CharField(max_length=100, null=False)      
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False)  
    created_at = models.DateTimeField(auto_now_add=True)         
    updated_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} in {self.location} (Host: {self.host.username})"

# Booking model for reservations
class Booking(models.Model):
    BOOKING_STATUS = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    ]

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")        
    start_date = models.DateTimeField(null=False)    
    end_date = models.DateTimeField(null=False)     
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False) 
    status = models.CharField(max_length=64, choices=BOOKING_STATUS, default="Pending") 
    date_created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Booking #{self.booking_id} | {self.listing.name} | "
    

# Review model for user feedback
class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")       
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  
    comment = models.TextField()                  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return (
            f"Reviewed By: {self.user.username} | Rating: {self.rating} | {self.comment[:30]}..."
            f"Property reviewed: {self.listing.name}"
        )