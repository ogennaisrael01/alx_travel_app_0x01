import environ 
from pathlib import Path
import os
import requests
from django.db import transaction
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
logger = logging.getLogger(__name__)

CHAPA_SECRET = env("CHAPA_SECRET_KEY")
CHAPA_INIT_URL = env("CHAPA_INIT_URL")

def payment_init(
        email: str,
        amount: float,
        first_name: str,
        last_name: str,
        pmt_ref: str,
        phone_number: str,

) -> dict: 

    if not any([email, amount, first_name, last_name, pmt_ref]):
        raise ValueError("All payment fields are required")
    if CHAPA_SECRET is None:
        raise ValueError("Chapa secret key is not set")
    if CHAPA_INIT_URL is None:
        raise ValueError("Initialization url is empty")
    
    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET}",
        "Content-Type": "application/json"
    }

    payment_payload = {
        "email": email,
        "first_name": first_name, 
        "last_name": last_name,
        "phone": phone_number,
        "tx_ref": pmt_ref,
        "amount": amount,
        "currency": ["USD", "ETB"],
        "callback_url": "",
        "return_url": "",
        "customoization": {
            "title": "Payments for travel app",
            "description": "payments"
        }

    }

    try:
        with transaction.atomic():
            response = requests.post(url=CHAPA_INIT_URL, json=payment_payload, headers=headers)
    except Exception:
        logger.exception("payment request failed", exc_info=True)
        raise

    return response.text







