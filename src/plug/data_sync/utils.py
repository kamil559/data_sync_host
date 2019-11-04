from datetime import datetime
from django.conf import settings
from ntplib import NTPClient


def get_current_timestamp() -> float:
    client = NTPClient()
    response = client.request(settings.EUROPE_POOL_NTP_TIME)
    return response.orig_time


def get_datetime_from_timestamp(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp)
