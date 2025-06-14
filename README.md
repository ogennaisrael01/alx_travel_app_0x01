# ALX Travel App

A Django-based travel booking platform with REST API support for listings, bookings, users, and reviews.

## Features

- User registration and management
- Property listings with host assignment
- Booking system with status tracking
- User reviews for listings
- REST API with Swagger documentation

## Tech Stack

- Django & Django REST Framework
- MySQL database
- drf-yasg for API docs
- CORS support

## Setup

1. **Clone the repo**  
   `git clone <repo-url>`

2. **Install dependencies**  
   `pip install -r requirements.txt`

3. **Configure database**  
   Update DB settings in [`alx_travel_app/alx_travel_app/settings.py`](alx_travel_app/alx_travel_app/settings.py).

4. **Apply migrations**  
   `python manage.py migrate`

5. **Run the server**  
   `python manage.py runserver`

6. **Access API docs**  
   Visit [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

## Project Structure

- [`alx_travel_app/alx_travel_app/`](alx_travel_app/alx_travel_app/) – Project settings and URLs
- [`alx_travel_app/listings/`](alx_travel_app/listings/) – App models, views, serializers, and urls

## Educational purposes