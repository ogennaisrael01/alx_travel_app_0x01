from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Bookings
from .serializers import BookingsOutSerializer, BookingSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.request import Request


@api_view(["POST"])
def register(request):
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


@api_view(["POST", 'GET'])
def booking_view(request: Request) -> Response:
    if request.method == 'GET':
        try:
            bookings = Bookings.objects.all()
        except Bookings.DoesNotExist:
            raise NotFound(detail={"success": False, "message": "bookings not found"})
        serializer = BookingsOut(bookings, many=True)
        return Response({"success": True, "bookings": serializer.data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        response = BookingsOut(serializer)
        return Response(response.data)

    else:
        return Response({"success": False, "message": "Method not allkowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
