from django.shortcuts import get_object_or_404
from  rest_framework.exceptions import ValidationError
from .models import Bookings, Payments
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

def get_payment_by_tx_ref(tx_ref: str, user) -> dict:
    try:
        with transaction.atomic():      
            payment = get_object_or_404(Payments, pmt_ref=tx_ref, user=user)
    except Exception:
        logger.exception(f"Failed to get payment object with tx_ref {tx_ref}", exc_info=True)
        raise
    return {
        "status": "success",
        "payment": payment
    }


