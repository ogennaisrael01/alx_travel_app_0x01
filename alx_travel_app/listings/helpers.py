from django.shortcuts import get_object_or_404
from  rest_framework.exceptions import ValidationError
from .models import Bookings
from uuid import UUID
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


def get_booking_by_id(booking_id: UUID) -> dict:
    if not isinstance(booking_id, UUID):
        raise ValidationError(detail=f"{booking_id} is an instance of a uuid class")
    try:
        with transaction.atomic():
            booking = get_object_or_404(Bookings, pk=booking_id)
    except Exception:
        logger.exception(f"Failed to get booking object with id {booking_id}", exc_info=True)
        raise

    return {
        "status": "success",
        "booking": booking
    }

